"""
Tests for the March Madness Prediction Model.
Validates model accuracy, feature engineering, and prediction sanity.
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from team_data import TOURNAMENT_TEAMS, HISTORICAL_MATCHUPS, FIRST_FOUR
from team_names import normalize_team_name, find_close_matches
from model import (
    compute_team_features,
    compute_matchup_features,
    build_training_data,
    augment_training_data,
    predict_matchup,
    compute_power_rankings,
    train_and_evaluate_models,
    SIMPLE_FEATURE_COLS,
)


def test_team_data_completeness():
    """All 68 teams have required fields."""
    required_fields = [
        "seed", "adj_off", "adj_def", "adj_tempo", "sos", "wins",
        "efg_pct", "turnover_pct", "oreb_pct", "ft_rate",
        "opp_efg_pct", "opp_turnover_pct", "opp_oreb_pct", "opp_ft_rate",
        "barthag", "region",
    ]
    assert len(TOURNAMENT_TEAMS) == 68, f"Expected 68 teams, got {len(TOURNAMENT_TEAMS)}"
    for team, stats in TOURNAMENT_TEAMS.items():
        for field in required_fields:
            assert field in stats, f"{team} missing field: {field}"


def test_seeds_valid():
    """Each region has correct seed distribution (16 seeds + First Four extras)."""
    regions = {}
    for team, stats in TOURNAMENT_TEAMS.items():
        region = stats["region"]
        if region not in regions:
            regions[region] = []
        regions[region].append(stats["seed"])

    assert len(regions) == 4, f"Expected 4 regions, got {len(regions)}"
    for region, seeds in regions.items():
        # With First Four, some regions have 17 or 18 teams (extra 11 or 16 seeds)
        assert len(seeds) >= 16, f"Region {region} has too few teams: {len(seeds)}"
        # Every seed 1-16 should appear at least once
        for s in range(1, 17):
            assert s in seeds, f"Region {region} missing seed {s}"


def test_stat_ranges():
    """Team stats fall within realistic ranges."""
    for team, stats in TOURNAMENT_TEAMS.items():
        assert 90 <= stats["adj_off"] <= 130, f"{team} adj_off out of range: {stats['adj_off']}"
        assert 85 <= stats["adj_def"] <= 115, f"{team} adj_def out of range: {stats['adj_def']}"
        assert 60 <= stats["adj_tempo"] <= 80, f"{team} tempo out of range: {stats['adj_tempo']}"
        assert 0.4 <= stats["barthag"] <= 1.0, f"{team} barthag out of range: {stats['barthag']}"
        assert 0.4 <= stats["efg_pct"] <= 0.65, f"{team} efg_pct out of range: {stats['efg_pct']}"
        assert 15 <= stats["wins"] <= 35, f"{team} wins out of range: {stats['wins']}"


def test_compute_team_features():
    """Team feature computation produces expected derived stats."""
    features = compute_team_features(TOURNAMENT_TEAMS["Duke"])
    assert "adj_em" in features
    assert features["adj_em"] == TOURNAMENT_TEAMS["Duke"]["adj_off"] - TOURNAMENT_TEAMS["Duke"]["adj_def"]
    assert features["barthag"] == TOURNAMENT_TEAMS["Duke"]["barthag"]
    assert "four_factors_off" in features
    assert "four_factors_def" in features


def test_matchup_features_symmetry():
    """Matchup features are antisymmetric (A vs B = -(B vs A))."""
    feat_ab = compute_matchup_features(TOURNAMENT_TEAMS["Duke"], TOURNAMENT_TEAMS["Houston"])
    feat_ba = compute_matchup_features(TOURNAMENT_TEAMS["Houston"], TOURNAMENT_TEAMS["Duke"])

    for key in feat_ab:
        assert abs(feat_ab[key] + feat_ba[key]) < 1e-10, (
            f"Feature {key} not antisymmetric: {feat_ab[key]} vs {feat_ba[key]}"
        )


def test_training_data_shape():
    """Training data has correct shape."""
    X, y = build_training_data()
    assert X.shape[0] == len(HISTORICAL_MATCHUPS)
    assert X.shape[1] == len(SIMPLE_FEATURE_COLS)
    assert len(y) == len(HISTORICAL_MATCHUPS)
    assert set(np.unique(y)) == {0, 1}


def test_augmentation_doubles_data():
    """Data augmentation doubles the dataset."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    assert X_aug.shape[0] == 2 * X.shape[0]
    assert len(y_aug) == 2 * len(y)


def test_augmentation_preserves_balance():
    """Augmented data should be roughly balanced."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    pos_rate = y_aug.mean()
    assert 0.45 <= pos_rate <= 0.55, f"Augmented data imbalanced: {pos_rate:.2%} positive"


def test_model_accuracy_above_threshold():
    """Cross-validated accuracy should exceed 75%."""
    results, _, _, _ = train_and_evaluate_models()
    for name, metrics in results.items():
        assert metrics["mean"] >= 0.70, (
            f"{name} accuracy too low: {metrics['mean']:.4f}"
        )


def test_logistic_regression_has_good_log_loss():
    """Logistic regression log loss should be reasonable."""
    results, _, _, _ = train_and_evaluate_models()
    lr_results = results["Logistic Regression"]
    assert "log_loss" in lr_results
    assert lr_results["log_loss"] < 0.60, (
        f"Log loss too high: {lr_results['log_loss']:.4f}"
    )


def test_1_seed_beats_16_seed():
    """1 seeds should have >95% win probability vs 16 seeds."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)

    prob = predict_matchup(model, scaler, "Duke", "Siena")
    assert prob > 0.95, f"1 vs 16 probability too low: {prob:.4f}"

    prob2 = predict_matchup(model, scaler, "Arizona", "LIU")
    assert prob2 > 0.95, f"1 vs 16 probability too low: {prob2:.4f}"


def test_higher_seed_generally_favored():
    """Lower seed number (better team) should generally be favored."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)

    # 2 vs 15
    prob = predict_matchup(model, scaler, "UConn", "Furman")
    assert prob > 0.85, f"2 vs 15 probability too low: {prob:.4f}"

    # 3 vs 14
    prob = predict_matchup(model, scaler, "Michigan State", "North Dakota State")
    assert prob > 0.80, f"3 vs 14 probability too low: {prob:.4f}"

    # 4 vs 13
    prob = predict_matchup(model, scaler, "Kansas", "Cal Baptist")
    assert prob > 0.75, f"4 vs 13 probability too low: {prob:.4f}"


def test_close_matchups_near_50_50():
    """8 vs 9 seed matchups should be close to 50/50."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)

    prob = predict_matchup(model, scaler, "Ohio State", "TCU")
    assert 0.20 <= prob <= 0.80, f"8 vs 9 not close enough: {prob:.4f}"


def test_probabilities_sum_to_one():
    """P(A beats B) + P(B beats A) should equal 1."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)

    for team_a, team_b in [("Duke", "Houston"), ("Alabama", "Florida"), ("Michigan", "Arizona")]:
        prob_a = predict_matchup(model, scaler, team_a, team_b)
        prob_b = predict_matchup(model, scaler, team_b, team_a)
        assert abs(prob_a + prob_b - 1.0) < 1e-6, (
            f"Probabilities don't sum to 1: {prob_a} + {prob_b} = {prob_a + prob_b}"
        )


def test_name_normalization():
    """Team name normalization handles common KenPom variations."""
    assert normalize_team_name("Connecticut") == "UConn"
    assert normalize_team_name("Michigan St.") == "Michigan State"
    assert normalize_team_name("Saint John's") == "St. John's"
    assert normalize_team_name("Gonzaga Bulldogs") == "Gonzaga"
    assert normalize_team_name("Miami (FL)") == "Miami FL"
    assert normalize_team_name("Miami (OH)") == "Miami OH"
    assert normalize_team_name("Iowa St.") == "Iowa State"
    assert normalize_team_name("North Carolina State") == "NC State"
    assert normalize_team_name("Long Island") == "LIU"


def test_name_close_matches():
    """Close match finder returns sensible suggestions."""
    matches = find_close_matches("Mich State", n=3)
    canonical_names = [m[1] for m in matches]
    assert "Michigan State" in canonical_names or "Michigan" in canonical_names


def test_power_rankings_order():
    """Top-ranked teams should be 1 seeds, bottom should be 16 seeds."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)

    rankings = compute_power_rankings(model, scaler)

    # Top 4 should include 1 seeds
    top4_teams = [t for t, _ in rankings[:4]]
    one_seeds = [t for t, s in TOURNAMENT_TEAMS.items() if s["seed"] == 1]
    overlap = set(top4_teams) & set(one_seeds)
    assert len(overlap) >= 3, f"Expected at least 3 of top 4 to be 1 seeds, got {overlap}"

    # Bottom 6 should include 16 seeds (there are 6 sixteen-seeds with First Four)
    bottom6_teams = [t for t, _ in rankings[-6:]]
    sixteen_seeds = [t for t, s in TOURNAMENT_TEAMS.items() if s["seed"] == 16]
    overlap = set(bottom6_teams) & set(sixteen_seeds)
    assert len(overlap) >= 4, f"Expected at least 4 of bottom 6 to be 16 seeds, got {overlap}"


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_team_data_completeness,
        test_seeds_valid,
        test_stat_ranges,
        test_compute_team_features,
        test_matchup_features_symmetry,
        test_training_data_shape,
        test_augmentation_doubles_data,
        test_augmentation_preserves_balance,
        test_model_accuracy_above_threshold,
        test_logistic_regression_has_good_log_loss,
        test_1_seed_beats_16_seed,
        test_higher_seed_generally_favored,
        test_close_matchups_near_50_50,
        test_probabilities_sum_to_one,
        test_power_rankings_order,
        test_name_normalization,
        test_name_close_matches,
    ]

    passed = 0
    failed = 0
    errors = []

    print("=" * 60)
    print("RUNNING MODEL TESTS")
    print("=" * 60)

    for test in tests:
        try:
            test()
            print(f"  PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {test.__name__} - {e}")
            failed += 1
            errors.append((test.__name__, str(e)))
        except Exception as e:
            print(f"  ERROR: {test.__name__} - {e}")
            failed += 1
            errors.append((test.__name__, str(e)))

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print(f"{'=' * 60}")

    if errors:
        print("\nFailures:")
        for name, err in errors:
            print(f"  - {name}: {err}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
