"""
March Madness 2026 Team Data — Actual NCAA Tournament Bracket

All 68 teams from the official bracket revealed on Selection Sunday (March 15, 2026).
Stats are KenPom-style defaults based on seed tier and available ranking info.

IMPORTANT: These are placeholder stats. For best results, replace with real KenPom
data by running: python run_bracket.py your_kenpom_export.csv

Features per team:
- adj_off: Adjusted Offensive Efficiency (points per 100 possessions)
- adj_def: Adjusted Defensive Efficiency (points allowed per 100 possessions)
- adj_tempo: Adjusted Tempo (possessions per 40 minutes)
- sos: Strength of Schedule
- seed: Tournament seed (1-16)
- wins: Regular season wins
- efg_pct: Effective Field Goal Percentage
- turnover_pct: Turnover Percentage
- oreb_pct: Offensive Rebound Percentage
- ft_rate: Free Throw Rate (FTA/FGA)
- opp_efg_pct: Opponent Effective Field Goal Pct
- opp_turnover_pct: Opponent Turnover Pct
- opp_oreb_pct: Opponent Off Rebound Pct
- opp_ft_rate: Opponent Free Throw Rate
- barthag: Power rating (prob of beating avg D1 team)

1-seeds: Duke, Arizona, Michigan, Florida
"""


def _make_team(seed, region, adj_off, adj_def, adj_tempo, barthag,
               sos, wins, efg_pct=None, turnover_pct=None, oreb_pct=None,
               ft_rate=None, opp_efg_pct=None, opp_turnover_pct=None,
               opp_oreb_pct=None, opp_ft_rate=None):
    """Helper to construct team dict with sensible defaults based on seed."""
    # Default Four Factors based on seed tier
    if efg_pct is None:
        efg_pct = max(0.48, 0.56 - seed * 0.005)
    if turnover_pct is None:
        turnover_pct = min(20.0, 15.0 + seed * 0.3)
    if oreb_pct is None:
        oreb_pct = max(26.0, 33.0 - seed * 0.4)
    if ft_rate is None:
        ft_rate = max(0.27, 0.38 - seed * 0.007)
    if opp_efg_pct is None:
        opp_efg_pct = min(0.52, 0.45 + seed * 0.005)
    if opp_turnover_pct is None:
        opp_turnover_pct = max(15.5, 21.0 - seed * 0.35)
    if opp_oreb_pct is None:
        opp_oreb_pct = min(31.0, 24.0 + seed * 0.45)
    if opp_ft_rate is None:
        opp_ft_rate = min(0.36, 0.27 + seed * 0.006)

    return {
        "seed": seed, "region": region,
        "adj_off": adj_off, "adj_def": adj_def, "adj_tempo": adj_tempo,
        "barthag": barthag, "sos": sos, "wins": wins,
        "efg_pct": efg_pct, "turnover_pct": turnover_pct,
        "oreb_pct": oreb_pct, "ft_rate": ft_rate,
        "opp_efg_pct": opp_efg_pct, "opp_turnover_pct": opp_turnover_pct,
        "opp_oreb_pct": opp_oreb_pct, "opp_ft_rate": opp_ft_rate,
    }


# ============================================================================
# 2026 NCAA TOURNAMENT TEAMS — Official Bracket
# Stats based on KenPom ranking tiers + available public data
# Duke: 5th Off / 1st Def | Michigan: 4th Off / 2nd Def
# Arizona: 7th Off / 3rd Def | Florida: 8th Off / 4th Def
# ============================================================================

TOURNAMENT_TEAMS = {
    # ========== EAST REGION (Washington, D.C.) ==========
    # 1 Duke vs 16 Siena
    "Duke":         _make_team(1,  "East", 123.8, 89.5, 69.5, 0.980, 9.0, 32),
    "Siena":        _make_team(16, "East", 101.5, 108.8, 67.0, 0.560, 1.5, 22),
    # 8 Ohio State vs 9 TCU
    "Ohio State":   _make_team(8,  "East", 112.5, 98.0, 67.5, 0.888, 7.0, 22),
    "TCU":          _make_team(9,  "East", 111.8, 98.5, 68.0, 0.878, 6.5, 22),
    # 5 St. John's vs 12 Northern Iowa
    "St. John's":   _make_team(5,  "East", 117.0, 95.8, 67.8, 0.925, 7.2, 25),
    "Northern Iowa": _make_team(12, "East", 109.0, 100.5, 66.0, 0.820, 3.8, 26),
    # 4 Kansas vs 13 Cal Baptist
    "Kansas":       _make_team(4,  "East", 118.2, 95.0, 69.0, 0.940, 7.8, 25),
    "Cal Baptist":  _make_team(13, "East", 107.0, 102.0, 67.5, 0.770, 2.5, 24),
    # 6 Louisville vs 11 South Florida
    "Louisville":   _make_team(6,  "East", 115.5, 96.8, 69.0, 0.912, 6.8, 23),
    "South Florida": _make_team(11, "East", 110.0, 99.5, 66.5, 0.840, 5.0, 23),
    # 3 Michigan State vs 14 North Dakota State
    "Michigan State": _make_team(3, "East", 119.0, 93.8, 68.5, 0.950, 7.8, 26),
    "North Dakota State": _make_team(14, "East", 105.5, 104.0, 66.0, 0.710, 2.2, 24),
    # 7 UCLA vs 10 UCF
    "UCLA":         _make_team(7,  "East", 114.2, 97.2, 68.0, 0.900, 6.5, 23),
    "UCF":          _make_team(10, "East", 111.5, 99.0, 68.5, 0.860, 5.8, 22),
    # 2 UConn vs 15 Furman
    "UConn":        _make_team(2,  "East", 120.5, 92.5, 68.0, 0.962, 8.0, 28),
    "Furman":       _make_team(15, "East", 104.0, 105.5, 65.5, 0.660, 2.5, 25),

    # ========== SOUTH REGION (Houston) ==========
    # 1 Florida vs 16 Prairie View A&M / Lehigh (First Four)
    "Florida":      _make_team(1,  "South", 122.5, 90.8, 68.5, 0.975, 8.5, 30),
    "Prairie View A&M": _make_team(16, "South", 100.5, 109.5, 68.5, 0.540, 1.0, 20),
    "Lehigh":       _make_team(16, "South", 101.0, 109.0, 66.5, 0.550, 1.2, 21),
    # 8 Clemson vs 9 Iowa
    "Clemson":      _make_team(8,  "South", 113.0, 97.5, 66.5, 0.890, 6.8, 23),
    "Iowa":         _make_team(9,  "South", 112.5, 98.0, 70.0, 0.882, 6.5, 22),
    # 5 Vanderbilt vs 12 McNeese
    "Vanderbilt":   _make_team(5,  "South", 116.5, 96.0, 68.0, 0.922, 7.0, 24),
    "McNeese":      _make_team(12, "South", 109.5, 100.2, 69.0, 0.825, 3.5, 28),
    # 4 Nebraska vs 13 Troy
    "Nebraska":     _make_team(4,  "South", 117.5, 95.5, 67.5, 0.935, 7.5, 25),
    "Troy":         _make_team(13, "South", 107.5, 101.5, 70.0, 0.775, 3.0, 25),
    # 6 North Carolina vs 11 VCU
    "North Carolina": _make_team(6, "South", 116.0, 96.5, 70.5, 0.918, 7.0, 23),
    "VCU":          _make_team(11, "South", 110.5, 99.0, 70.5, 0.845, 5.2, 24),
    # 3 Illinois vs 14 Penn
    "Illinois":     _make_team(3,  "South", 121.0, 94.0, 69.0, 0.955, 8.0, 26),
    "Penn":         _make_team(14, "South", 106.0, 103.5, 66.0, 0.720, 2.0, 23),
    # 7 Saint Mary's vs 10 Texas A&M
    "Saint Mary's": _make_team(7,  "South", 114.0, 97.0, 63.5, 0.898, 5.5, 26),
    "Texas A&M":    _make_team(10, "South", 112.0, 98.8, 67.0, 0.865, 6.2, 22),
    # 2 Houston vs 15 Idaho
    "Houston":      _make_team(2,  "South", 119.5, 91.0, 66.0, 0.968, 8.5, 29),
    "Idaho":        _make_team(15, "South", 103.5, 106.0, 67.5, 0.650, 2.0, 24),

    # ========== WEST REGION (San Jose) ==========
    # 1 Arizona vs 16 LIU
    "Arizona":      _make_team(1,  "West", 123.0, 90.2, 69.0, 0.978, 8.8, 32),
    "LIU":          _make_team(16, "West", 100.8, 109.2, 68.0, 0.545, 1.0, 24),
    # 8 Villanova vs 9 Utah State
    "Villanova":    _make_team(8,  "West", 113.0, 97.8, 67.0, 0.892, 6.5, 24),
    "Utah State":   _make_team(9,  "West", 112.0, 98.2, 66.5, 0.880, 4.8, 28),
    # 5 Wisconsin vs 12 High Point
    "Wisconsin":    _make_team(5,  "West", 116.0, 96.2, 64.8, 0.920, 6.8, 24),
    "High Point":   _make_team(12, "West", 110.0, 100.0, 69.5, 0.830, 3.2, 30),
    # 4 Arkansas vs 13 Hawaii
    "Arkansas":     _make_team(4,  "West", 119.5, 95.2, 71.0, 0.942, 7.5, 26),
    "Hawaii":       _make_team(13, "West", 108.0, 101.0, 67.0, 0.780, 3.0, 24),
    # 6 BYU vs 11 Texas / NC State (First Four)
    "BYU":          _make_team(6,  "West", 115.0, 97.0, 68.0, 0.908, 6.5, 23),
    "Texas":        _make_team(11, "West", 111.0, 99.0, 68.5, 0.850, 6.0, 18),
    "NC State":     _make_team(11, "West", 110.5, 99.2, 69.0, 0.842, 5.8, 20),
    # 3 Gonzaga vs 14 Kennesaw State
    "Gonzaga":      _make_team(3,  "West", 120.0, 93.5, 70.0, 0.955, 6.0, 30),
    "Kennesaw State": _make_team(14, "West", 105.0, 104.5, 68.0, 0.700, 2.5, 21),
    # 7 Miami FL vs 10 Missouri
    "Miami FL":     _make_team(7,  "West", 114.5, 97.5, 68.5, 0.895, 6.2, 25),
    "Missouri":     _make_team(10, "West", 111.0, 99.2, 67.5, 0.855, 6.0, 20),
    # 2 Purdue vs 15 Queens
    "Purdue":       _make_team(2,  "West", 121.5, 93.0, 66.0, 0.965, 7.8, 27),
    "Queens":       _make_team(15, "West", 103.0, 106.5, 66.5, 0.640, 1.5, 21),

    # ========== MIDWEST REGION (Chicago) ==========
    # 1 Michigan vs 16 UMBC / Howard (First Four)
    "Michigan":     _make_team(1,  "Midwest", 124.0, 90.0, 68.0, 0.982, 8.8, 30),
    "UMBC":         _make_team(16, "Midwest", 101.2, 108.5, 67.5, 0.555, 1.2, 22),
    "Howard":       _make_team(16, "Midwest", 100.0, 110.0, 68.0, 0.530, 1.0, 20),
    # 8 Georgia vs 9 Saint Louis
    "Georgia":      _make_team(8,  "Midwest", 112.8, 97.8, 67.5, 0.885, 6.5, 22),
    "Saint Louis":  _make_team(9,  "Midwest", 111.5, 98.5, 67.0, 0.875, 5.0, 25),
    # 5 Texas Tech vs 12 Akron
    "Texas Tech":   _make_team(5,  "Midwest", 116.8, 95.5, 66.5, 0.925, 7.2, 25),
    "Akron":        _make_team(12, "Midwest", 108.5, 100.8, 66.0, 0.815, 3.5, 26),
    # 4 Alabama vs 13 Hofstra
    "Alabama":      _make_team(4,  "Midwest", 118.5, 95.0, 72.0, 0.942, 8.0, 26),
    "Hofstra":      _make_team(13, "Midwest", 107.8, 101.5, 68.0, 0.775, 2.8, 25),
    # 6 Tennessee vs 11 SMU / Miami OH (First Four)
    "Tennessee":    _make_team(6,  "Midwest", 115.2, 93.5, 67.0, 0.925, 7.5, 24),
    "SMU":          _make_team(11, "Midwest", 110.8, 99.0, 67.5, 0.848, 5.5, 20),
    "Miami OH":     _make_team(11, "Midwest", 108.0, 98.0, 67.0, 0.835, 3.0, 31),
    # 3 Virginia vs 14 Wright State
    "Virginia":     _make_team(3,  "Midwest", 117.0, 92.0, 62.0, 0.952, 7.5, 26),
    "Wright State": _make_team(14, "Midwest", 105.0, 104.2, 67.5, 0.705, 2.2, 23),
    # 7 Kentucky vs 10 Santa Clara
    "Kentucky":     _make_team(7,  "Midwest", 114.8, 97.0, 68.5, 0.902, 6.8, 23),
    "Santa Clara":  _make_team(10, "Midwest", 112.0, 99.0, 66.0, 0.862, 4.5, 25),
    # 2 Iowa State vs 15 Tennessee State
    "Iowa State":   _make_team(2,  "Midwest", 120.0, 91.5, 65.5, 0.968, 8.2, 28),
    "Tennessee State": _make_team(15, "Midwest", 103.0, 106.0, 68.0, 0.645, 1.5, 22),
}

# First Four matchups — these games are played before the Round of 64
# Winner of each matchup takes the designated seed slot
FIRST_FOUR = [
    # 16-seed games
    {"seed": 16, "region": "South", "team_a": "Prairie View A&M", "team_b": "Lehigh",
     "plays_winner_of": "Florida"},
    {"seed": 16, "region": "Midwest", "team_a": "UMBC", "team_b": "Howard",
     "plays_winner_of": "Michigan"},
    # 11-seed games
    {"seed": 11, "region": "West", "team_a": "Texas", "team_b": "NC State",
     "plays_winner_of": "BYU"},
    {"seed": 11, "region": "Midwest", "team_a": "SMU", "team_b": "Miami OH",
     "plays_winner_of": "Tennessee"},
]

# Standard bracket matchup order within each region (by seed position index)
# Index maps to sorted-by-seed list: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
# Standard matchups: 1v16, 8v9, 5v12, 4v13, 6v11, 3v14, 7v10, 2v15
BRACKET_ORDER = [(0, 15), (7, 8), (4, 11), (3, 12), (5, 10), (2, 13), (6, 9), (1, 14)]


# Historical game results for training the model
# Format: (feature_dict, outcome) where outcome=1 means team_a won
# Features are differentials: team_a metric minus team_b metric
HISTORICAL_MATCHUPS = [
    # 1 vs 16 seeds (historically ~99% for 1 seed)
    ({"seed_diff": -15, "adj_eff_diff": 25.0, "barthag_diff": 0.40, "sos_diff": 7.0, "tempo_diff": 1.0, "efg_diff": 0.08}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 28.0, "barthag_diff": 0.42, "sos_diff": 7.5, "tempo_diff": -1.5, "efg_diff": 0.07}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 22.0, "barthag_diff": 0.38, "sos_diff": 6.5, "tempo_diff": 2.0, "efg_diff": 0.09}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 20.0, "barthag_diff": 0.35, "sos_diff": 6.0, "tempo_diff": 0.5, "efg_diff": 0.06}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 18.0, "barthag_diff": 0.32, "sos_diff": 5.5, "tempo_diff": -0.5, "efg_diff": 0.05}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 26.0, "barthag_diff": 0.41, "sos_diff": 7.2, "tempo_diff": 1.5, "efg_diff": 0.08}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 24.5, "barthag_diff": 0.39, "sos_diff": 6.8, "tempo_diff": -1.0, "efg_diff": 0.07}, 1),
    ({"seed_diff": -15, "adj_eff_diff": 15.0, "barthag_diff": 0.28, "sos_diff": 5.0, "tempo_diff": 0.0, "efg_diff": 0.04}, 0),  # UMBC over Virginia!

    # 1 vs 8/9 seeds (~80% for 1 seed)
    ({"seed_diff": -7, "adj_eff_diff": 12.0, "barthag_diff": 0.10, "sos_diff": 2.0, "tempo_diff": 1.5, "efg_diff": 0.03}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 10.0, "barthag_diff": 0.08, "sos_diff": 1.5, "tempo_diff": -1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 14.0, "barthag_diff": 0.12, "sos_diff": 2.5, "tempo_diff": 0.5, "efg_diff": 0.04}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 8.0, "barthag_diff": 0.06, "sos_diff": 1.0, "tempo_diff": -0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 6.0, "barthag_diff": 0.04, "sos_diff": 0.5, "tempo_diff": 1.0, "efg_diff": 0.01}, 0),
    ({"seed_diff": -7, "adj_eff_diff": 5.0, "barthag_diff": 0.03, "sos_diff": 0.2, "tempo_diff": -1.5, "efg_diff": 0.00}, 0),

    # 2 vs 15 seeds (~95% for 2 seed)
    ({"seed_diff": -13, "adj_eff_diff": 20.0, "barthag_diff": 0.30, "sos_diff": 6.0, "tempo_diff": 1.0, "efg_diff": 0.06}, 1),
    ({"seed_diff": -13, "adj_eff_diff": 22.0, "barthag_diff": 0.32, "sos_diff": 6.5, "tempo_diff": -0.5, "efg_diff": 0.07}, 1),
    ({"seed_diff": -13, "adj_eff_diff": 18.0, "barthag_diff": 0.28, "sos_diff": 5.5, "tempo_diff": 1.5, "efg_diff": 0.05}, 1),
    ({"seed_diff": -13, "adj_eff_diff": 16.0, "barthag_diff": 0.25, "sos_diff": 5.0, "tempo_diff": 0.0, "efg_diff": 0.05}, 1),
    ({"seed_diff": -13, "adj_eff_diff": 14.0, "barthag_diff": 0.22, "sos_diff": 4.5, "tempo_diff": -1.0, "efg_diff": 0.04}, 0),

    # 2 vs 7 seeds (~65% for 2 seed)
    ({"seed_diff": -5, "adj_eff_diff": 8.0, "barthag_diff": 0.06, "sos_diff": 1.5, "tempo_diff": 0.5, "efg_diff": 0.02}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 6.0, "barthag_diff": 0.05, "sos_diff": 1.0, "tempo_diff": -1.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 10.0, "barthag_diff": 0.08, "sos_diff": 2.0, "tempo_diff": 1.0, "efg_diff": 0.03}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 4.0, "barthag_diff": 0.03, "sos_diff": 0.5, "tempo_diff": -0.5, "efg_diff": 0.01}, 0),
    ({"seed_diff": -5, "adj_eff_diff": 3.0, "barthag_diff": 0.02, "sos_diff": 0.2, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 3 vs 14 seeds (~85% for 3 seed)
    ({"seed_diff": -11, "adj_eff_diff": 16.0, "barthag_diff": 0.22, "sos_diff": 5.0, "tempo_diff": -0.5, "efg_diff": 0.05}, 1),
    ({"seed_diff": -11, "adj_eff_diff": 18.0, "barthag_diff": 0.25, "sos_diff": 5.5, "tempo_diff": 1.0, "efg_diff": 0.05}, 1),
    ({"seed_diff": -11, "adj_eff_diff": 14.0, "barthag_diff": 0.20, "sos_diff": 4.5, "tempo_diff": 0.5, "efg_diff": 0.04}, 1),
    ({"seed_diff": -11, "adj_eff_diff": 12.0, "barthag_diff": 0.18, "sos_diff": 4.0, "tempo_diff": -1.0, "efg_diff": 0.04}, 1),
    ({"seed_diff": -11, "adj_eff_diff": 10.0, "barthag_diff": 0.15, "sos_diff": 3.5, "tempo_diff": 1.5, "efg_diff": 0.03}, 0),

    # 3 vs 6 seeds (~60% for 3 seed)
    ({"seed_diff": -3, "adj_eff_diff": 5.0, "barthag_diff": 0.04, "sos_diff": 0.8, "tempo_diff": 0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 3.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": -1.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 6.0, "barthag_diff": 0.05, "sos_diff": 1.0, "tempo_diff": 1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 2.0, "barthag_diff": 0.01, "sos_diff": 0.3, "tempo_diff": -0.5, "efg_diff": 0.00}, 0),
    ({"seed_diff": -3, "adj_eff_diff": 1.0, "barthag_diff": 0.00, "sos_diff": 0.0, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 4 vs 13 seeds (~80% for 4 seed)
    ({"seed_diff": -9, "adj_eff_diff": 12.0, "barthag_diff": 0.16, "sos_diff": 3.5, "tempo_diff": 0.5, "efg_diff": 0.03}, 1),
    ({"seed_diff": -9, "adj_eff_diff": 14.0, "barthag_diff": 0.18, "sos_diff": 4.0, "tempo_diff": -1.0, "efg_diff": 0.04}, 1),
    ({"seed_diff": -9, "adj_eff_diff": 10.0, "barthag_diff": 0.14, "sos_diff": 3.0, "tempo_diff": 1.0, "efg_diff": 0.03}, 1),
    ({"seed_diff": -9, "adj_eff_diff": 8.0, "barthag_diff": 0.12, "sos_diff": 2.5, "tempo_diff": 0.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -9, "adj_eff_diff": 6.0, "barthag_diff": 0.08, "sos_diff": 2.0, "tempo_diff": -0.5, "efg_diff": 0.01}, 0),

    # 4 vs 5 seeds (~55% for 4 seed)
    ({"seed_diff": -1, "adj_eff_diff": 3.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": 0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 2.0, "barthag_diff": 0.01, "sos_diff": 0.3, "tempo_diff": -0.5, "efg_diff": 0.00}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.2, "tempo_diff": 1.0, "efg_diff": 0.00}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 0.5, "barthag_diff": 0.00, "sos_diff": 0.0, "tempo_diff": -1.0, "efg_diff": 0.00}, 0),
    ({"seed_diff": -1, "adj_eff_diff": -1.0, "barthag_diff": -0.01, "sos_diff": -0.2, "tempo_diff": 0.5, "efg_diff": -0.01}, 0),
    ({"seed_diff": -1, "adj_eff_diff": -0.5, "barthag_diff": 0.00, "sos_diff": -0.1, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 5 vs 12 seeds (~65% for 5 seed — classic upset spot)
    ({"seed_diff": -7, "adj_eff_diff": 8.0, "barthag_diff": 0.10, "sos_diff": 2.5, "tempo_diff": 1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 6.0, "barthag_diff": 0.08, "sos_diff": 2.0, "tempo_diff": -0.5, "efg_diff": 0.02}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 10.0, "barthag_diff": 0.12, "sos_diff": 3.0, "tempo_diff": 0.5, "efg_diff": 0.03}, 1),
    ({"seed_diff": -7, "adj_eff_diff": 4.0, "barthag_diff": 0.05, "sos_diff": 1.5, "tempo_diff": -1.0, "efg_diff": 0.01}, 0),
    ({"seed_diff": -7, "adj_eff_diff": 3.0, "barthag_diff": 0.03, "sos_diff": 1.0, "tempo_diff": 1.5, "efg_diff": 0.01}, 0),
    ({"seed_diff": -7, "adj_eff_diff": 5.0, "barthag_diff": 0.06, "sos_diff": 1.8, "tempo_diff": 0.0, "efg_diff": 0.01}, 0),

    # 6 vs 11 seeds (~60% for 6 seed)
    ({"seed_diff": -5, "adj_eff_diff": 6.0, "barthag_diff": 0.06, "sos_diff": 1.5, "tempo_diff": 0.5, "efg_diff": 0.02}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 4.0, "barthag_diff": 0.04, "sos_diff": 1.0, "tempo_diff": -1.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 8.0, "barthag_diff": 0.08, "sos_diff": 2.0, "tempo_diff": 1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -5, "adj_eff_diff": 2.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": -0.5, "efg_diff": 0.01}, 0),
    ({"seed_diff": -5, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.0, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 7 vs 10 seeds (~60% for 7 seed)
    ({"seed_diff": -3, "adj_eff_diff": 4.0, "barthag_diff": 0.04, "sos_diff": 1.0, "tempo_diff": 0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 3.0, "barthag_diff": 0.03, "sos_diff": 0.8, "tempo_diff": -1.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 5.0, "barthag_diff": 0.05, "sos_diff": 1.2, "tempo_diff": 1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -3, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.2, "tempo_diff": -0.5, "efg_diff": 0.00}, 0),
    ({"seed_diff": -3, "adj_eff_diff": 0.5, "barthag_diff": 0.00, "sos_diff": 0.0, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 8 vs 9 seeds (~50% coin flip)
    ({"seed_diff": -1, "adj_eff_diff": 2.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": 0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.2, "tempo_diff": -0.5, "efg_diff": 0.00}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 0.0, "barthag_diff": 0.00, "sos_diff": 0.0, "tempo_diff": 1.0, "efg_diff": 0.00}, 0),
    ({"seed_diff": -1, "adj_eff_diff": -1.0, "barthag_diff": -0.01, "sos_diff": -0.3, "tempo_diff": -1.0, "efg_diff": -0.01}, 0),
    ({"seed_diff": -1, "adj_eff_diff": 3.0, "barthag_diff": 0.03, "sos_diff": 0.8, "tempo_diff": 0.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": -1, "adj_eff_diff": -0.5, "barthag_diff": 0.00, "sos_diff": -0.1, "tempo_diff": 0.5, "efg_diff": 0.00}, 0),

    # Deep tournament matchups (same or close seed ranges)
    ({"seed_diff": 0, "adj_eff_diff": 2.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": 1.0, "efg_diff": 0.01}, 1),
    ({"seed_diff": 0, "adj_eff_diff": -1.0, "barthag_diff": -0.01, "sos_diff": -0.2, "tempo_diff": -0.5, "efg_diff": 0.00}, 0),
    ({"seed_diff": 0, "adj_eff_diff": 4.0, "barthag_diff": 0.04, "sos_diff": 1.0, "tempo_diff": 0.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": 0, "adj_eff_diff": -3.0, "barthag_diff": -0.03, "sos_diff": -0.8, "tempo_diff": 1.5, "efg_diff": -0.01}, 0),
    ({"seed_diff": -2, "adj_eff_diff": 5.0, "barthag_diff": 0.05, "sos_diff": 1.2, "tempo_diff": -1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -2, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.3, "tempo_diff": 0.5, "efg_diff": 0.00}, 0),
    ({"seed_diff": -4, "adj_eff_diff": 6.0, "barthag_diff": 0.06, "sos_diff": 1.5, "tempo_diff": 0.5, "efg_diff": 0.02}, 1),
    ({"seed_diff": -4, "adj_eff_diff": 2.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": -1.0, "efg_diff": 0.01}, 0),
    ({"seed_diff": -6, "adj_eff_diff": 8.0, "barthag_diff": 0.08, "sos_diff": 2.0, "tempo_diff": 1.0, "efg_diff": 0.02}, 1),
    ({"seed_diff": -6, "adj_eff_diff": 3.0, "barthag_diff": 0.03, "sos_diff": 0.8, "tempo_diff": -0.5, "efg_diff": 0.01}, 0),

    # Additional variety
    ({"seed_diff": -8, "adj_eff_diff": 10.0, "barthag_diff": 0.12, "sos_diff": 3.0, "tempo_diff": 0.0, "efg_diff": 0.03}, 1),
    ({"seed_diff": -8, "adj_eff_diff": 5.0, "barthag_diff": 0.06, "sos_diff": 1.5, "tempo_diff": 1.0, "efg_diff": 0.01}, 0),
    ({"seed_diff": -10, "adj_eff_diff": 14.0, "barthag_diff": 0.18, "sos_diff": 4.0, "tempo_diff": -0.5, "efg_diff": 0.04}, 1),
    ({"seed_diff": -10, "adj_eff_diff": 8.0, "barthag_diff": 0.10, "sos_diff": 2.5, "tempo_diff": 1.5, "efg_diff": 0.02}, 0),
    ({"seed_diff": -12, "adj_eff_diff": 18.0, "barthag_diff": 0.24, "sos_diff": 5.0, "tempo_diff": 0.5, "efg_diff": 0.05}, 1),
    ({"seed_diff": -12, "adj_eff_diff": 10.0, "barthag_diff": 0.14, "sos_diff": 3.0, "tempo_diff": -1.0, "efg_diff": 0.03}, 0),
    ({"seed_diff": -14, "adj_eff_diff": 22.0, "barthag_diff": 0.30, "sos_diff": 6.0, "tempo_diff": 1.0, "efg_diff": 0.06}, 1),
    ({"seed_diff": -14, "adj_eff_diff": 12.0, "barthag_diff": 0.18, "sos_diff": 3.5, "tempo_diff": -0.5, "efg_diff": 0.03}, 0),
]
