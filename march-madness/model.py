"""
March Madness Prediction Model
Tests multiple regression approaches and validates accuracy.

Methodology:
1. Compute differential features between matchup teams
2. Train logistic regression, ridge classifier, and random forest
3. Cross-validate and compare models
4. Select best model and produce team power rankings + bracket predictions

Key Features (differentials between teams):
- Adjusted Efficiency Margin (adj_off - adj_def)
- BARTHAG power rating
- Strength of Schedule
- Seed difference
- Effective Field Goal % difference
- Tempo difference
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, log_loss, brier_score_loss
from itertools import combinations
import json
import sys

from team_data import TOURNAMENT_TEAMS, HISTORICAL_MATCHUPS


def compute_team_features(team_stats):
    """Compute derived features for a single team."""
    return {
        "adj_em": team_stats["adj_off"] - team_stats["adj_def"],
        "barthag": team_stats["barthag"],
        "seed": team_stats["seed"],
        "sos": team_stats["sos"],
        "adj_tempo": team_stats["adj_tempo"],
        "efg_pct": team_stats["efg_pct"],
        "turnover_pct": team_stats["turnover_pct"],
        "oreb_pct": team_stats["oreb_pct"],
        "ft_rate": team_stats["ft_rate"],
        "opp_efg_pct": team_stats["opp_efg_pct"],
        "opp_turnover_pct": team_stats["opp_turnover_pct"],
        "wins": team_stats["wins"],
        # Four Factors composite
        "four_factors_off": (
            team_stats["efg_pct"] * 0.4
            + (1 - team_stats["turnover_pct"] / 100) * 0.25
            + team_stats["oreb_pct"] / 100 * 0.20
            + team_stats["ft_rate"] * 0.15
        ),
        "four_factors_def": (
            (1 - team_stats["opp_efg_pct"]) * 0.4
            + team_stats["opp_turnover_pct"] / 100 * 0.25
            + (1 - team_stats["opp_oreb_pct"] / 100) * 0.20
            + (1 - team_stats["opp_ft_rate"]) * 0.15
        ),
    }


def compute_matchup_features(team_a_stats, team_b_stats):
    """Compute differential features for a matchup (team_a perspective)."""
    a = compute_team_features(team_a_stats)
    b = compute_team_features(team_b_stats)

    return {
        "seed_diff": a["seed"] - b["seed"],
        "adj_em_diff": a["adj_em"] - b["adj_em"],
        "barthag_diff": a["barthag"] - b["barthag"],
        "sos_diff": a["sos"] - b["sos"],
        "tempo_diff": a["adj_tempo"] - b["adj_tempo"],
        "efg_diff": a["efg_pct"] - b["efg_pct"],
        "turnover_diff": a["turnover_pct"] - b["turnover_pct"],  # lower is better for team
        "oreb_diff": a["oreb_pct"] - b["oreb_pct"],
        "ft_rate_diff": a["ft_rate"] - b["ft_rate"],
        "opp_efg_diff": a["opp_efg_pct"] - b["opp_efg_pct"],  # lower is better
        "wins_diff": a["wins"] - b["wins"],
        "four_factors_off_diff": a["four_factors_off"] - b["four_factors_off"],
        "four_factors_def_diff": a["four_factors_def"] - b["four_factors_def"],
    }


FEATURE_COLS = [
    "seed_diff", "adj_em_diff", "barthag_diff", "sos_diff",
    "tempo_diff", "efg_diff", "turnover_diff", "oreb_diff",
    "ft_rate_diff", "opp_efg_diff", "wins_diff",
    "four_factors_off_diff", "four_factors_def_diff",
]

# Simplified feature set matching historical data format
SIMPLE_FEATURE_COLS = [
    "seed_diff", "adj_eff_diff", "barthag_diff", "sos_diff",
    "tempo_diff", "efg_diff",
]


def build_training_data():
    """Build training dataset from historical matchup patterns."""
    X = []
    y = []
    for matchup_features, outcome in HISTORICAL_MATCHUPS:
        X.append([matchup_features[col] for col in SIMPLE_FEATURE_COLS])
        y.append(outcome)
    return np.array(X), np.array(y)


def augment_training_data(X, y):
    """
    Augment by flipping perspective (if A beats B, B loses to A).
    This doubles the dataset and ensures symmetry.
    """
    X_aug = np.vstack([X, -X])
    y_aug = np.concatenate([y, 1 - y])
    return X_aug, y_aug


def generate_full_matchup_data():
    """
    Generate all possible tournament matchup features from current team data.
    Used for prediction after model is trained.
    """
    teams = list(TOURNAMENT_TEAMS.keys())
    matchup_data = []

    for i, team_a in enumerate(teams):
        for j, team_b in enumerate(teams):
            if i >= j:
                continue
            features = compute_matchup_features(
                TOURNAMENT_TEAMS[team_a],
                TOURNAMENT_TEAMS[team_b],
            )
            # Map to simple feature format for prediction
            simple_features = {
                "seed_diff": features["seed_diff"],
                "adj_eff_diff": features["adj_em_diff"],
                "barthag_diff": features["barthag_diff"],
                "sos_diff": features["sos_diff"],
                "tempo_diff": features["tempo_diff"],
                "efg_diff": features["efg_diff"],
            }
            matchup_data.append({
                "team_a": team_a,
                "team_b": team_b,
                "features": simple_features,
            })

    return matchup_data


def train_and_evaluate_models():
    """Train multiple models and compare with cross-validation."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)

    models = {
        "Logistic Regression": LogisticRegression(
            C=1.0, max_iter=1000, random_state=42
        ),
        "Logistic Regression (L1)": LogisticRegression(
            C=0.5, l1_ratio=1.0, solver="saga", max_iter=1000, random_state=42
        ),
        "Ridge Classifier": RidgeClassifier(alpha=1.0, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
        ),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("=" * 70)
    print("MODEL COMPARISON - Cross-Validated Performance")
    print("=" * 70)
    print(f"{'Model':<30} {'Accuracy':>10} {'Std Dev':>10}")
    print("-" * 70)

    results = {}
    for name, model in models.items():
        scores = cross_val_score(model, X_scaled, y_aug, cv=cv, scoring="accuracy")
        results[name] = {"mean": scores.mean(), "std": scores.std()}
        print(f"{name:<30} {scores.mean():>10.4f} {scores.std():>10.4f}")

    # Also evaluate log loss for probabilistic models
    print("\n" + "=" * 70)
    print("PROBABILISTIC EVALUATION (Log Loss - lower is better)")
    print("=" * 70)

    prob_models = {
        "Logistic Regression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "Logistic Regression (L1)": LogisticRegression(
            C=0.5, l1_ratio=1.0, solver="saga", max_iter=1000, random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
        ),
    }

    print(f"{'Model':<30} {'Log Loss':>10} {'Brier Score':>12}")
    print("-" * 70)

    for name, model in prob_models.items():
        log_losses = cross_val_score(
            model, X_scaled, y_aug, cv=cv, scoring="neg_log_loss"
        )
        brier_scores = cross_val_score(
            model, X_scaled, y_aug, cv=cv, scoring="neg_brier_score"
        )
        results[name]["log_loss"] = -log_losses.mean()
        results[name]["brier"] = -brier_scores.mean()
        print(f"{name:<30} {-log_losses.mean():>10.4f} {-brier_scores.mean():>12.4f}")

    return results, scaler, X_aug, y_aug


def select_best_model(results):
    """Select the best model based on accuracy and log loss."""
    # Prefer models with both high accuracy and low log loss
    best_name = None
    best_score = -float("inf")

    for name, metrics in results.items():
        # Combined score: accuracy - 0.5 * log_loss (if available)
        score = metrics["mean"]
        if "log_loss" in metrics:
            score -= 0.3 * metrics["log_loss"]
        if score > best_score:
            best_score = score
            best_name = name

    return best_name


def compute_power_rankings(model, scaler):
    """
    Compute power rankings by simulating every possible matchup
    and computing average win probability.
    """
    teams = list(TOURNAMENT_TEAMS.keys())
    n = len(teams)
    win_probs = {team: [] for team in teams}

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            features = compute_matchup_features(
                TOURNAMENT_TEAMS[teams[i]],
                TOURNAMENT_TEAMS[teams[j]],
            )
            simple = [
                features["seed_diff"],
                features["adj_em_diff"],
                features["barthag_diff"],
                features["sos_diff"],
                features["tempo_diff"],
                features["efg_diff"],
            ]
            X = scaler.transform([simple])
            prob = model.predict_proba(X)[0][1]
            win_probs[teams[i]].append(prob)

    # Average win probability = power ranking
    rankings = {}
    for team in teams:
        rankings[team] = np.mean(win_probs[team])

    # Sort by power ranking
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    return sorted_rankings


def predict_matchup(model, scaler, team_a, team_b):
    """Predict win probability for team_a vs team_b."""
    features = compute_matchup_features(
        TOURNAMENT_TEAMS[team_a],
        TOURNAMENT_TEAMS[team_b],
    )
    simple = [
        features["seed_diff"],
        features["adj_em_diff"],
        features["barthag_diff"],
        features["sos_diff"],
        features["tempo_diff"],
        features["efg_diff"],
    ]
    X = scaler.transform([simple])
    prob = model.predict_proba(X)[0][1]
    return prob


def simulate_bracket(model, scaler):
    """Simulate the full 64-team bracket using model predictions."""
    regions = {}
    for team, stats in TOURNAMENT_TEAMS.items():
        region = stats["region"]
        if region not in regions:
            regions[region] = []
        regions[region].append((stats["seed"], team))

    # Sort each region by seed
    for region in regions:
        regions[region].sort(key=lambda x: x[0])

    # Standard bracket matchup order: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
    bracket_order = [(0, 15), (7, 8), (4, 11), (3, 12), (5, 10), (2, 13), (6, 9), (1, 14)]

    print("\n" + "=" * 70)
    print("FULL BRACKET SIMULATION")
    print("=" * 70)

    final_four = []

    for region_name in ["South", "West", "East", "Midwest"]:
        teams = regions[region_name]
        print(f"\n{'─' * 35}")
        print(f"  {region_name.upper()} REGION")
        print(f"{'─' * 35}")

        # Round of 64
        round_winners = []
        print(f"\n  Round of 64:")
        for idx_a, idx_b in bracket_order:
            seed_a, team_a = teams[idx_a]
            seed_b, team_b = teams[idx_b]
            prob_a = predict_matchup(model, scaler, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            marker = " *UPSET*" if winner_seed > 8 else ""
            print(f"    ({seed_a}) {team_a:<18} vs ({seed_b}) {team_b:<18} "
                  f"-> ({winner_seed}) {winner} ({win_pct:.1%}){marker}")
            round_winners.append((winner_seed, winner))

        # Round of 32
        print(f"\n  Round of 32:")
        sweet16 = []
        for i in range(0, len(round_winners), 2):
            seed_a, team_a = round_winners[i]
            seed_b, team_b = round_winners[i + 1]
            prob_a = predict_matchup(model, scaler, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            print(f"    ({seed_a}) {team_a:<18} vs ({seed_b}) {team_b:<18} "
                  f"-> ({winner_seed}) {winner} ({win_pct:.1%})")
            sweet16.append((winner_seed, winner))

        # Sweet 16
        print(f"\n  Sweet 16:")
        elite8 = []
        for i in range(0, len(sweet16), 2):
            seed_a, team_a = sweet16[i]
            seed_b, team_b = sweet16[i + 1]
            prob_a = predict_matchup(model, scaler, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            print(f"    ({seed_a}) {team_a:<18} vs ({seed_b}) {team_b:<18} "
                  f"-> ({winner_seed}) {winner} ({win_pct:.1%})")
            elite8.append((winner_seed, winner))

        # Elite 8
        print(f"\n  Elite 8 (Regional Final):")
        seed_a, team_a = elite8[0]
        seed_b, team_b = elite8[1]
        prob_a = predict_matchup(model, scaler, team_a, team_b)
        winner = team_a if prob_a > 0.5 else team_b
        winner_seed = seed_a if prob_a > 0.5 else seed_b
        win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
        print(f"    ({seed_a}) {team_a:<18} vs ({seed_b}) {team_b:<18} "
              f"-> ({winner_seed}) {winner} ({win_pct:.1%})")
        final_four.append((winner_seed, winner, region_name))
        print(f"\n  {region_name} Champion: ({winner_seed}) {winner}")

    # Final Four
    print(f"\n{'=' * 70}")
    print("FINAL FOUR")
    print("=" * 70)

    semi1_a = final_four[0]  # South
    semi1_b = final_four[1]  # West
    semi2_a = final_four[2]  # East
    semi2_b = final_four[3]  # Midwest

    print(f"\n  Semifinal 1: ({semi1_a[0]}) {semi1_a[1]} ({semi1_a[2]}) vs "
          f"({semi1_b[0]}) {semi1_b[1]} ({semi1_b[2]})")
    prob_1 = predict_matchup(model, scaler, semi1_a[1], semi1_b[1])
    finalist1 = semi1_a if prob_1 > 0.5 else semi1_b
    win_pct1 = prob_1 if prob_1 > 0.5 else 1 - prob_1
    print(f"    -> ({finalist1[0]}) {finalist1[1]} ({win_pct1:.1%})")

    print(f"\n  Semifinal 2: ({semi2_a[0]}) {semi2_a[1]} ({semi2_a[2]}) vs "
          f"({semi2_b[0]}) {semi2_b[1]} ({semi2_b[2]})")
    prob_2 = predict_matchup(model, scaler, semi2_a[1], semi2_b[1])
    finalist2 = semi2_a if prob_2 > 0.5 else semi2_b
    win_pct2 = prob_2 if prob_2 > 0.5 else 1 - prob_2
    print(f"    -> ({finalist2[0]}) {finalist2[1]} ({win_pct2:.1%})")

    # Championship
    print(f"\n{'=' * 70}")
    print("NATIONAL CHAMPIONSHIP")
    print("=" * 70)
    prob_champ = predict_matchup(model, scaler, finalist1[1], finalist2[1])
    champion = finalist1 if prob_champ > 0.5 else finalist2
    win_pct_champ = prob_champ if prob_champ > 0.5 else 1 - prob_champ
    print(f"\n  ({finalist1[0]}) {finalist1[1]} vs ({finalist2[0]}) {finalist2[1]}")
    print(f"  -> CHAMPION: ({champion[0]}) {champion[1]} ({win_pct_champ:.1%})")

    return champion


def analyze_feature_importance(model, feature_names):
    """Analyze which features matter most to the model."""
    print("\n" + "=" * 70)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 70)

    if hasattr(model, "coef_"):
        # Logistic regression coefficients
        coefs = model.coef_[0]
        importance = list(zip(feature_names, np.abs(coefs), coefs))
        importance.sort(key=lambda x: x[1], reverse=True)
        print(f"\n{'Feature':<20} {'|Coefficient|':>15} {'Direction':>12}")
        print("-" * 50)
        for feat, abs_coef, coef in importance:
            direction = "+" if coef > 0 else "-"
            print(f"{feat:<20} {abs_coef:>15.4f} {direction:>12}")
    elif hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        importance = list(zip(feature_names, importances))
        importance.sort(key=lambda x: x[1], reverse=True)
        print(f"\n{'Feature':<20} {'Importance':>15}")
        print("-" * 40)
        for feat, imp in importance:
            print(f"{feat:<20} {imp:>15.4f}")


def export_results(rankings, champion):
    """Export results to JSON for potential use in the dashboard."""
    output = {
        "model": "Logistic Regression (March Madness Predictor)",
        "features": SIMPLE_FEATURE_COLS,
        "power_rankings": [
            {
                "rank": i + 1,
                "team": team,
                "power_rating": round(float(rating), 4),
                "seed": TOURNAMENT_TEAMS[team]["seed"],
                "region": TOURNAMENT_TEAMS[team]["region"],
                "adj_em": round(
                    TOURNAMENT_TEAMS[team]["adj_off"] - TOURNAMENT_TEAMS[team]["adj_def"], 1
                ),
                "barthag": TOURNAMENT_TEAMS[team]["barthag"],
            }
            for i, (team, rating) in enumerate(rankings)
        ],
        "predicted_champion": {
            "team": champion[1],
            "seed": champion[0],
        },
    }

    with open("march_madness_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults exported to march_madness_results.json")


def main():
    print("=" * 70)
    print("  MARCH MADNESS PREDICTION MODEL")
    print("  Logistic Regression with KenPom-Style Features")
    print("=" * 70)
    print(f"\nTeams loaded: {len(TOURNAMENT_TEAMS)}")
    print(f"Training examples: {len(HISTORICAL_MATCHUPS)} (x2 with augmentation)")
    print(f"Features: {SIMPLE_FEATURE_COLS}")

    # Step 1: Train and evaluate models
    results, scaler, X_train, y_train = train_and_evaluate_models()

    # Step 2: Select best model
    best_model_name = select_best_model(results)
    print(f"\n>>> BEST MODEL: {best_model_name} <<<")
    print(f"    Accuracy: {results[best_model_name]['mean']:.4f}")
    if "log_loss" in results[best_model_name]:
        print(f"    Log Loss: {results[best_model_name]['log_loss']:.4f}")

    # Step 3: Train final model on full data
    best_models = {
        "Logistic Regression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "Logistic Regression (L1)": LogisticRegression(
            C=0.5, l1_ratio=1.0, solver="saga", max_iter=1000, random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=5, random_state=42
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
        ),
    }

    # Use logistic regression as primary (most consistent per research)
    final_model = best_models.get(
        best_model_name,
        LogisticRegression(C=1.0, max_iter=1000, random_state=42),
    )
    X_scaled = scaler.transform(X_train)
    final_model.fit(X_scaled, y_train)

    # Step 4: Feature importance
    analyze_feature_importance(final_model, SIMPLE_FEATURE_COLS)

    # Step 5: Power rankings
    print("\n" + "=" * 70)
    print("POWER RANKINGS (Average Win Probability vs All Teams)")
    print("=" * 70)
    rankings = compute_power_rankings(final_model, scaler)
    print(f"\n{'Rank':<6} {'Team':<20} {'Power Rating':>14} {'Seed':>6} {'Region':<10} {'AdjEM':>8}")
    print("-" * 70)
    for i, (team, rating) in enumerate(rankings):
        stats = TOURNAMENT_TEAMS[team]
        adj_em = stats["adj_off"] - stats["adj_def"]
        print(f"{i+1:<6} {team:<20} {rating:>14.4f} {stats['seed']:>6} "
              f"{stats['region']:<10} {adj_em:>8.1f}")

    # Step 6: Simulate bracket
    champion = simulate_bracket(final_model, scaler)

    # Step 7: Export
    export_results(rankings, champion)

    # Step 8: Validation - sanity check some known matchup patterns
    print("\n" + "=" * 70)
    print("VALIDATION: Sample Matchup Probabilities")
    print("=" * 70)
    test_matchups = [
        ("Houston", "SE Louisiana"),   # 1 vs 16
        ("Duke", "Norfolk St"),        # 1 vs 16
        ("Alabama", "Robert Morris"),  # 2 vs 15
        ("Houston", "Alabama"),        # 1 vs 2 (close)
        ("Duke", "Florida"),           # 1 vs 1
        ("Oregon", "Ole Miss"),        # 5 vs 12 (upset prone)
        ("Michigan St", "Drake"),      # 8 vs 9 (coin flip)
    ]
    print(f"\n{'Matchup':<40} {'Team A Win%':>12} {'Favored':>12}")
    print("-" * 70)
    for team_a, team_b in test_matchups:
        prob = predict_matchup(final_model, scaler, team_a, team_b)
        seed_a = TOURNAMENT_TEAMS[team_a]["seed"]
        seed_b = TOURNAMENT_TEAMS[team_b]["seed"]
        favored = team_a if prob > 0.5 else team_b
        label = f"({seed_a}) {team_a} vs ({seed_b}) {team_b}"
        print(f"{label:<40} {prob:>12.1%} {favored:>12}")

    return final_model, scaler, rankings


if __name__ == "__main__":
    model, scaler, rankings = main()
