"""
March Madness Bracket Runner — CSV In, Excel Out

Usage:
    python run_bracket.py                          # uses built-in team data
    python run_bracket.py my_kenpom_data.csv       # uses your KenPom CSV

Input CSV columns (paste from KenPom/Excel):
    team, seed, region, adj_off, adj_def, adj_tempo, barthag,
    sos, wins, efg_pct, turnover_pct, oreb_pct, ft_rate,
    opp_efg_pct, opp_turnover_pct, opp_oreb_pct, opp_ft_rate

Outputs (Excel-ready CSVs):
    output_power_rankings.csv   — All 64 teams ranked by model power rating
    output_all_matchups.csv     — Every possible matchup with win probabilities
    output_bracket.csv          — Round-by-round bracket picks with probabilities
"""

import sys
import os
import csv
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Allow importing from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from team_data import HISTORICAL_MATCHUPS, FIRST_FOUR
from team_names import normalize_team_name, find_close_matches
from model import (
    compute_matchup_features,
    compute_team_features,
    build_training_data,
    augment_training_data,
    SIMPLE_FEATURE_COLS,
)


def load_teams_from_csv(csv_path):
    """Load team data from a CSV file (paste from KenPom/Excel)."""
    teams = {}
    df = pd.read_csv(csv_path)

    # Normalize column names (strip whitespace, lowercase)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Map common KenPom column name variations
    col_aliases = {
        "team": ["team", "team_name", "name", "school"],
        "seed": ["seed", "tournament_seed"],
        "region": ["region"],
        "adj_off": ["adj_off", "adjoe", "adj_oe", "adjoff", "offensive_efficiency",
                     "adj_o", "adjo"],
        "adj_def": ["adj_def", "adjde", "adj_de", "adjdef", "defensive_efficiency",
                     "adj_d", "adjd"],
        "adj_tempo": ["adj_tempo", "adjtempo", "adj_t", "tempo", "adjt"],
        "barthag": ["barthag", "power_rating", "bart"],
        "sos": ["sos", "strength_of_schedule", "sос"],
        "wins": ["wins", "w"],
        "efg_pct": ["efg_pct", "efg%", "efg", "eff_fg_pct", "effective_fg_pct"],
        "turnover_pct": ["turnover_pct", "tor", "to%", "to_pct", "tov%", "tov_pct"],
        "oreb_pct": ["oreb_pct", "orb%", "orb_pct", "or%", "or_pct", "off_reb_pct"],
        "ft_rate": ["ft_rate", "ftr", "ft_rate", "free_throw_rate"],
        "opp_efg_pct": ["opp_efg_pct", "opp_efg%", "opp_efg", "def_efg_pct"],
        "opp_turnover_pct": ["opp_turnover_pct", "opp_tor", "opp_to%",
                              "opp_tov%", "def_tov_pct"],
        "opp_oreb_pct": ["opp_oreb_pct", "opp_orb%", "opp_or%", "def_orb_pct"],
        "opp_ft_rate": ["opp_ft_rate", "opp_ftr", "def_ft_rate"],
    }

    # Build column mapping
    col_map = {}
    for standard_name, aliases in col_aliases.items():
        for alias in aliases:
            if alias in df.columns:
                col_map[standard_name] = alias
                break

    # Check for required columns
    required = ["team", "seed", "region", "adj_off", "adj_def"]
    missing = [r for r in required if r not in col_map]
    if missing:
        print(f"ERROR: Missing required columns: {missing}")
        print(f"Found columns: {list(df.columns)}")
        print(f"\nSee kenpom_template.csv for the expected format.")
        sys.exit(1)

    # Provide defaults for optional columns
    defaults = {
        "adj_tempo": 68.0, "barthag": None, "sos": 5.0, "wins": 22,
        "efg_pct": 0.50, "turnover_pct": 17.0, "oreb_pct": 30.0,
        "ft_rate": 0.33, "opp_efg_pct": 0.49, "opp_turnover_pct": 18.0,
        "opp_oreb_pct": 27.0, "opp_ft_rate": 0.31,
    }

    normalized_count = 0
    unmatched = []

    for _, row in df.iterrows():
        raw_name = str(row[col_map["team"]]).strip()
        team_name = normalize_team_name(raw_name)
        if team_name != raw_name:
            normalized_count += 1

        team_stats = {}

        for standard_name in col_aliases:
            if standard_name == "team":
                continue
            if standard_name in col_map:
                val = row[col_map[standard_name]]
                # Handle percentage columns that might be 0-100 instead of 0-1
                if standard_name in ("efg_pct", "opp_efg_pct", "ft_rate", "opp_ft_rate"):
                    val = float(val)
                    if val > 1.0:
                        val = val / 100.0
                elif standard_name in ("barthag",):
                    val = float(val)
                    if val > 1.0:
                        val = val / 100.0
                else:
                    val = float(val) if standard_name != "region" else str(val).strip()
            elif standard_name in defaults:
                val = defaults[standard_name]
            else:
                val = 0

            team_stats[standard_name] = val

        # Auto-compute barthag if not provided
        if team_stats.get("barthag") is None:
            adj_em = float(team_stats["adj_off"]) - float(team_stats["adj_def"])
            # Approximate BARTHAG from efficiency margin using logistic function
            team_stats["barthag"] = round(1 / (1 + 10 ** (-adj_em / 10)), 4)

        # Ensure numeric types
        for key in team_stats:
            if key != "region":
                team_stats[key] = float(team_stats[key])
        team_stats["seed"] = int(team_stats["seed"])

        teams[team_name] = team_stats

    if normalized_count > 0:
        print(f"  Normalized {normalized_count} team name(s) to match bracket format.")

    # Check for bracket teams not found in CSV
    from team_data import TOURNAMENT_TEAMS
    bracket_teams = set(TOURNAMENT_TEAMS.keys())
    csv_teams = set(teams.keys())
    missing_from_csv = bracket_teams - csv_teams
    if missing_from_csv and len(teams) >= 30:
        # Only warn if this looks like a full bracket CSV
        print(f"\n  WARNING: {len(missing_from_csv)} bracket team(s) not found in CSV:")
        for m in sorted(missing_from_csv)[:10]:
            suggestions = find_close_matches(m, n=2)
            hint = ""
            if suggestions:
                hint = f" (did you mean: {', '.join(s[0] for s in suggestions)}?)"
            print(f"    - {m}{hint}")
        if len(missing_from_csv) > 10:
            print(f"    ... and {len(missing_from_csv) - 10} more")

    return teams


def train_model():
    """Train the logistic regression model on historical data."""
    X, y = build_training_data()
    X_aug, y_aug = augment_training_data(X, y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_aug)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_scaled, y_aug)
    return model, scaler


def get_matchup_prob(model, scaler, teams, team_a, team_b):
    """Get win probability for team_a vs team_b."""
    features = compute_matchup_features(teams[team_a], teams[team_b])
    simple = [
        features["seed_diff"],
        features["adj_em_diff"],
        features["barthag_diff"],
        features["sos_diff"],
        features["tempo_diff"],
        features["efg_diff"],
    ]
    X = scaler.transform([simple])
    return model.predict_proba(X)[0][1]


def generate_power_rankings(model, scaler, teams):
    """Rank all teams by average win probability vs the field."""
    team_names = list(teams.keys())
    rankings = []

    for team in team_names:
        probs = []
        for opponent in team_names:
            if team == opponent:
                continue
            prob = get_matchup_prob(model, scaler, teams, team, opponent)
            probs.append(prob)
        avg_prob = np.mean(probs)
        adj_em = teams[team]["adj_off"] - teams[team]["adj_def"]
        rankings.append({
            "Rank": 0,
            "Team": team,
            "Power Rating": round(avg_prob, 4),
            "Seed": int(teams[team]["seed"]),
            "Region": teams[team]["region"],
            "AdjEM": round(adj_em, 1),
            "BARTHAG": teams[team]["barthag"],
            "AdjO": teams[team]["adj_off"],
            "AdjD": teams[team]["adj_def"],
            "Wins": int(teams[team]["wins"]),
        })

    rankings.sort(key=lambda x: x["Power Rating"], reverse=True)
    for i, r in enumerate(rankings):
        r["Rank"] = i + 1

    return rankings


def generate_all_matchups(model, scaler, teams):
    """Generate win probabilities for every possible matchup."""
    team_names = sorted(teams.keys())
    matchups = []

    for i, team_a in enumerate(team_names):
        for j, team_b in enumerate(team_names):
            if i >= j:
                continue
            prob_a = get_matchup_prob(model, scaler, teams, team_a, team_b)
            seed_a = int(teams[team_a]["seed"])
            seed_b = int(teams[team_b]["seed"])
            favored = team_a if prob_a > 0.5 else team_b
            matchups.append({
                "Team A": team_a,
                "Seed A": seed_a,
                "Team B": team_b,
                "Seed B": seed_b,
                "Team A Win%": round(prob_a * 100, 1),
                "Team B Win%": round((1 - prob_a) * 100, 1),
                "Favored": favored,
                "Upset?": "Yes" if (prob_a > 0.5 and seed_a > seed_b) or
                                    (prob_a < 0.5 and seed_b > seed_a) else "",
            })

    return matchups


def resolve_first_four(model, scaler, teams):
    """Simulate First Four games and return results + updated region rosters."""
    results = []
    # Determine which First Four matchups exist in our team data
    for ff in FIRST_FOUR:
        if ff["team_a"] in teams and ff["team_b"] in teams:
            team_a, team_b = ff["team_a"], ff["team_b"]
            prob_a = get_matchup_prob(model, scaler, teams, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            loser = team_b if prob_a > 0.5 else team_a
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            results.append({
                "Round": "First Four",
                "Region": ff["region"],
                "Team A": team_a,
                "Seed A": ff["seed"],
                "Team B": team_b,
                "Seed B": ff["seed"],
                "Winner": winner,
                "Winner Seed": ff["seed"],
                "Win Probability": round(win_pct * 100, 1),
                "Upset": "",
            })
            # Remove the loser from the teams dict for bracket purposes
            # (don't mutate original — caller should handle)
            yield loser, results[-1]


def simulate_bracket(model, scaler, teams):
    """Simulate the full 68-team bracket with First Four, returning round-by-round results."""
    results = []

    # 1) Resolve First Four games
    bracket_teams = dict(teams)  # copy so we don't mutate
    first_four_losers = []
    for loser, ff_result in resolve_first_four(model, scaler, bracket_teams):
        results.append(ff_result)
        first_four_losers.append(loser)

    # Remove First Four losers
    for loser in first_four_losers:
        if loser in bracket_teams:
            del bracket_teams[loser]

    # 2) Build region rosters (should be 16 per region now)
    regions = {}
    for team, stats in bracket_teams.items():
        region = stats["region"]
        if region not in regions:
            regions[region] = []
        regions[region].append((int(stats["seed"]), team))

    for region in regions:
        regions[region].sort(key=lambda x: (x[0], x[1]))

    # Standard bracket: seeds 1-16, positions mapped by seed
    # 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
    seed_matchups = [(1,16), (8,9), (5,12), (4,13), (6,11), (3,14), (7,10), (2,15)]

    final_four = []
    for region_name in ["South", "West", "East", "Midwest"]:
        if region_name not in regions:
            continue
        region_teams = regions[region_name]

        # Build seed->team lookup
        seed_to_team = {}
        for seed, team in region_teams:
            seed_to_team[seed] = team  # last one wins if duplicates remain

        # Round of 64
        round_winners = []
        for seed_a, seed_b in seed_matchups:
            if seed_a not in seed_to_team or seed_b not in seed_to_team:
                continue
            team_a = seed_to_team[seed_a]
            team_b = seed_to_team[seed_b]
            prob_a = get_matchup_prob(model, scaler, bracket_teams, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            results.append({
                "Round": "Round of 64",
                "Region": region_name,
                "Team A": team_a,
                "Seed A": seed_a,
                "Team B": team_b,
                "Seed B": seed_b,
                "Winner": winner,
                "Winner Seed": winner_seed,
                "Win Probability": round(win_pct * 100, 1),
                "Upset": "Yes" if winner_seed > 8 else "",
            })
            round_winners.append((winner_seed, winner))

        # Round of 32
        sweet16 = []
        for i in range(0, len(round_winners), 2):
            seed_a, team_a = round_winners[i]
            seed_b, team_b = round_winners[i + 1]
            prob_a = get_matchup_prob(model, scaler, bracket_teams, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            results.append({
                "Round": "Round of 32",
                "Region": region_name,
                "Team A": team_a, "Seed A": seed_a,
                "Team B": team_b, "Seed B": seed_b,
                "Winner": winner, "Winner Seed": winner_seed,
                "Win Probability": round(win_pct * 100, 1), "Upset": "",
            })
            sweet16.append((winner_seed, winner))

        # Sweet 16
        elite8 = []
        for i in range(0, len(sweet16), 2):
            seed_a, team_a = sweet16[i]
            seed_b, team_b = sweet16[i + 1]
            prob_a = get_matchup_prob(model, scaler, bracket_teams, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            results.append({
                "Round": "Sweet 16",
                "Region": region_name,
                "Team A": team_a, "Seed A": seed_a,
                "Team B": team_b, "Seed B": seed_b,
                "Winner": winner, "Winner Seed": winner_seed,
                "Win Probability": round(win_pct * 100, 1), "Upset": "",
            })
            elite8.append((winner_seed, winner))

        # Elite 8
        if len(elite8) >= 2:
            seed_a, team_a = elite8[0]
            seed_b, team_b = elite8[1]
            prob_a = get_matchup_prob(model, scaler, bracket_teams, team_a, team_b)
            winner = team_a if prob_a > 0.5 else team_b
            winner_seed = seed_a if prob_a > 0.5 else seed_b
            win_pct = prob_a if prob_a > 0.5 else 1 - prob_a
            results.append({
                "Round": "Elite 8",
                "Region": region_name,
                "Team A": team_a, "Seed A": seed_a,
                "Team B": team_b, "Seed B": seed_b,
                "Winner": winner, "Winner Seed": winner_seed,
                "Win Probability": round(win_pct * 100, 1), "Upset": "",
            })
            final_four.append((winner_seed, winner, region_name))

    # Final Four
    if len(final_four) >= 4:
        # Semi 1: South vs West
        s1a, s1b = final_four[0], final_four[1]
        prob = get_matchup_prob(model, scaler, bracket_teams, s1a[1], s1b[1])
        w1 = s1a if prob > 0.5 else s1b
        wp1 = prob if prob > 0.5 else 1 - prob
        results.append({
            "Round": "Final Four", "Region": f"{s1a[2]} vs {s1b[2]}",
            "Team A": s1a[1], "Seed A": s1a[0],
            "Team B": s1b[1], "Seed B": s1b[0],
            "Winner": w1[1], "Winner Seed": w1[0],
            "Win Probability": round(wp1 * 100, 1), "Upset": "",
        })

        # Semi 2: East vs Midwest
        s2a, s2b = final_four[2], final_four[3]
        prob = get_matchup_prob(model, scaler, bracket_teams, s2a[1], s2b[1])
        w2 = s2a if prob > 0.5 else s2b
        wp2 = prob if prob > 0.5 else 1 - prob
        results.append({
            "Round": "Final Four", "Region": f"{s2a[2]} vs {s2b[2]}",
            "Team A": s2a[1], "Seed A": s2a[0],
            "Team B": s2b[1], "Seed B": s2b[0],
            "Winner": w2[1], "Winner Seed": w2[0],
            "Win Probability": round(wp2 * 100, 1), "Upset": "",
        })

        # Championship
        prob = get_matchup_prob(model, scaler, bracket_teams, w1[1], w2[1])
        champ = w1 if prob > 0.5 else w2
        wp_champ = prob if prob > 0.5 else 1 - prob
        results.append({
            "Round": "Championship", "Region": "National",
            "Team A": w1[1], "Seed A": w1[0],
            "Team B": w2[1], "Seed B": w2[0],
            "Winner": champ[1], "Winner Seed": champ[0],
            "Win Probability": round(wp_champ * 100, 1), "Upset": "",
        })

    return results


def main():
    # Determine data source
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        print(f"Loading teams from: {csv_path}")
        teams = load_teams_from_csv(csv_path)
    else:
        print("No CSV provided — using built-in team data.")
        print("Usage: python run_bracket.py your_kenpom_data.csv")
        from team_data import TOURNAMENT_TEAMS
        teams = TOURNAMENT_TEAMS

    print(f"Loaded {len(teams)} teams")

    # Train model
    print("Training model...")
    model, scaler = train_model()

    # Generate outputs
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Power Rankings
    print("Generating power rankings...")
    rankings = generate_power_rankings(model, scaler, teams)
    rankings_path = os.path.join(output_dir, "output_power_rankings.csv")
    pd.DataFrame(rankings).to_csv(rankings_path, index=False)
    print(f"  -> {rankings_path}")

    # Print top 20
    print(f"\n{'Rank':<6} {'Team':<20} {'Rating':>8} {'Seed':>6} {'Region':<10} {'AdjEM':>7}")
    print("-" * 60)
    for r in rankings[:20]:
        print(f"{r['Rank']:<6} {r['Team']:<20} {r['Power Rating']:>8.4f} "
              f"{r['Seed']:>6} {r['Region']:<10} {r['AdjEM']:>7.1f}")
    if len(rankings) > 20:
        print(f"  ... and {len(rankings) - 20} more (see output_power_rankings.csv)")

    # 2. All Matchups
    print("\nGenerating all matchup probabilities...")
    matchups = generate_all_matchups(model, scaler, teams)
    matchups_path = os.path.join(output_dir, "output_all_matchups.csv")
    pd.DataFrame(matchups).to_csv(matchups_path, index=False)
    print(f"  -> {matchups_path} ({len(matchups)} matchups)")

    # 3. Bracket Simulation
    print("\nSimulating bracket...")
    bracket = simulate_bracket(model, scaler, teams)
    bracket_path = os.path.join(output_dir, "output_bracket.csv")
    pd.DataFrame(bracket).to_csv(bracket_path, index=False)
    print(f"  -> {bracket_path}")

    # Print bracket summary
    print(f"\n{'=' * 65}")
    print("BRACKET RESULTS")
    print(f"{'=' * 65}")
    current_round = ""
    for game in bracket:
        if game["Round"] != current_round:
            current_round = game["Round"]
            print(f"\n  {current_round}:")
        region = f" [{game['Region']}]" if game["Region"] != "National" else ""
        print(f"    ({game['Seed A']}) {game['Team A']:<18} vs "
              f"({game['Seed B']}) {game['Team B']:<18} -> "
              f"{game['Winner']} ({game['Win Probability']}%){region}")

    # Champion
    if bracket:
        champ = bracket[-1]
        print(f"\n  CHAMPION: ({champ['Winner Seed']}) {champ['Winner']} "
              f"({champ['Win Probability']}%)")

    print(f"\n{'=' * 65}")
    print("OUTPUT FILES (open in Excel):")
    print(f"  1. {rankings_path}")
    print(f"  2. {matchups_path}")
    print(f"  3. {bracket_path}")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
