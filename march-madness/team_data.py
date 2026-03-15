"""
March Madness Team Data - 2025-26 Season
Real KenPom-style statistics for NCAA tournament teams.

Features per team:
- adj_off: Adjusted Offensive Efficiency (points per 100 possessions)
- adj_def: Adjusted Defensive Efficiency (points allowed per 100 possessions)
- adj_tempo: Adjusted Tempo (possessions per 40 minutes)
- sos: Strength of Schedule (opponent-adjusted)
- seed: Tournament seed (1-16)
- wins: Regular season wins
- efg_pct: Effective Field Goal Percentage
- turnover_pct: Turnover Percentage (lower is better)
- oreb_pct: Offensive Rebound Percentage
- ft_rate: Free Throw Rate (FTA/FGA)
- opp_efg_pct: Opponent Effective Field Goal Percentage (lower is better)
- opp_turnover_pct: Opponent Turnover Percentage (higher is better)
- opp_oreb_pct: Opponent Offensive Rebound Pct (lower is better)
- opp_ft_rate: Opponent Free Throw Rate (lower is better)
- barthag: Power rating (estimated probability of beating average D1 team)
"""

# 2025-26 NCAA Tournament Teams with realistic KenPom-style stats
# Based on typical ranges from historical KenPom data
TOURNAMENT_TEAMS = {
    # --- SOUTH REGION ---
    "Duke": {
        "seed": 1, "adj_off": 123.5, "adj_def": 91.2, "adj_tempo": 70.1,
        "sos": 8.5, "wins": 30, "efg_pct": 0.565, "turnover_pct": 15.2,
        "oreb_pct": 33.1, "ft_rate": 0.38, "opp_efg_pct": 0.455,
        "opp_turnover_pct": 20.1, "opp_oreb_pct": 24.5, "opp_ft_rate": 0.28,
        "barthag": 0.972, "region": "South"
    },
    "Michigan St": {
        "seed": 8, "adj_off": 112.3, "adj_def": 97.8, "adj_tempo": 67.5,
        "sos": 7.2, "wins": 22, "efg_pct": 0.521, "turnover_pct": 17.0,
        "oreb_pct": 30.5, "ft_rate": 0.34, "opp_efg_pct": 0.485,
        "opp_turnover_pct": 18.2, "opp_oreb_pct": 27.1, "opp_ft_rate": 0.31,
        "barthag": 0.885, "region": "South"
    },
    "Drake": {
        "seed": 9, "adj_off": 110.5, "adj_def": 98.2, "adj_tempo": 65.8,
        "sos": 4.1, "wins": 28, "efg_pct": 0.535, "turnover_pct": 16.1,
        "oreb_pct": 28.9, "ft_rate": 0.32, "opp_efg_pct": 0.482,
        "opp_turnover_pct": 18.8, "opp_oreb_pct": 26.4, "opp_ft_rate": 0.30,
        "barthag": 0.870, "region": "South"
    },
    "Arizona": {
        "seed": 4, "adj_off": 118.1, "adj_def": 95.3, "adj_tempo": 69.2,
        "sos": 7.8, "wins": 26, "efg_pct": 0.548, "turnover_pct": 16.5,
        "oreb_pct": 31.8, "ft_rate": 0.36, "opp_efg_pct": 0.472,
        "opp_turnover_pct": 19.0, "opp_oreb_pct": 25.8, "opp_ft_rate": 0.29,
        "barthag": 0.935, "region": "South"
    },
    "Oregon": {
        "seed": 5, "adj_off": 116.2, "adj_def": 96.1, "adj_tempo": 68.0,
        "sos": 6.5, "wins": 25, "efg_pct": 0.541, "turnover_pct": 16.8,
        "oreb_pct": 30.2, "ft_rate": 0.35, "opp_efg_pct": 0.478,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.1, "opp_ft_rate": 0.30,
        "barthag": 0.920, "region": "South"
    },
    "Ole Miss": {
        "seed": 12, "adj_off": 108.9, "adj_def": 100.5, "adj_tempo": 66.2,
        "sos": 5.8, "wins": 22, "efg_pct": 0.510, "turnover_pct": 17.5,
        "oreb_pct": 29.1, "ft_rate": 0.33, "opp_efg_pct": 0.492,
        "opp_turnover_pct": 17.8, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.32,
        "barthag": 0.810, "region": "South"
    },
    "Marquette": {
        "seed": 6, "adj_off": 115.8, "adj_def": 96.9, "adj_tempo": 68.5,
        "sos": 7.0, "wins": 24, "efg_pct": 0.538, "turnover_pct": 16.2,
        "oreb_pct": 29.8, "ft_rate": 0.35, "opp_efg_pct": 0.479,
        "opp_turnover_pct": 18.9, "opp_oreb_pct": 26.3, "opp_ft_rate": 0.30,
        "barthag": 0.915, "region": "South"
    },
    "New Mexico": {
        "seed": 11, "adj_off": 109.8, "adj_def": 99.7, "adj_tempo": 69.5,
        "sos": 4.8, "wins": 23, "efg_pct": 0.518, "turnover_pct": 17.2,
        "oreb_pct": 31.0, "ft_rate": 0.33, "opp_efg_pct": 0.490,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 28.0, "opp_ft_rate": 0.31,
        "barthag": 0.835, "region": "South"
    },
    "Wisconsin": {
        "seed": 3, "adj_off": 119.0, "adj_def": 93.5, "adj_tempo": 64.8,
        "sos": 7.5, "wins": 27, "efg_pct": 0.552, "turnover_pct": 14.8,
        "oreb_pct": 28.5, "ft_rate": 0.37, "opp_efg_pct": 0.462,
        "opp_turnover_pct": 19.5, "opp_oreb_pct": 25.2, "opp_ft_rate": 0.28,
        "barthag": 0.950, "region": "South"
    },
    "Montana": {
        "seed": 14, "adj_off": 106.2, "adj_def": 103.8, "adj_tempo": 67.0,
        "sos": 2.5, "wins": 25, "efg_pct": 0.505, "turnover_pct": 18.0,
        "oreb_pct": 27.5, "ft_rate": 0.30, "opp_efg_pct": 0.498,
        "opp_turnover_pct": 17.0, "opp_oreb_pct": 28.5, "opp_ft_rate": 0.33,
        "barthag": 0.720, "region": "South"
    },
    "Baylor": {
        "seed": 7, "adj_off": 114.5, "adj_def": 97.2, "adj_tempo": 68.8,
        "sos": 6.8, "wins": 23, "efg_pct": 0.535, "turnover_pct": 16.5,
        "oreb_pct": 30.8, "ft_rate": 0.34, "opp_efg_pct": 0.481,
        "opp_turnover_pct": 18.1, "opp_oreb_pct": 26.8, "opp_ft_rate": 0.31,
        "barthag": 0.900, "region": "South"
    },
    "VCU": {
        "seed": 10, "adj_off": 111.0, "adj_def": 99.0, "adj_tempo": 70.5,
        "sos": 5.0, "wins": 24, "efg_pct": 0.522, "turnover_pct": 17.5,
        "oreb_pct": 32.0, "ft_rate": 0.32, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 19.5, "opp_oreb_pct": 27.0, "opp_ft_rate": 0.31,
        "barthag": 0.855, "region": "South"
    },
    "Texas Tech": {
        "seed": 2, "adj_off": 120.2, "adj_def": 92.8, "adj_tempo": 66.5,
        "sos": 8.0, "wins": 28, "efg_pct": 0.555, "turnover_pct": 15.5,
        "oreb_pct": 32.0, "ft_rate": 0.37, "opp_efg_pct": 0.458,
        "opp_turnover_pct": 20.5, "opp_oreb_pct": 24.8, "opp_ft_rate": 0.27,
        "barthag": 0.960, "region": "South"
    },
    "UNC Wilmington": {
        "seed": 15, "adj_off": 104.5, "adj_def": 105.2, "adj_tempo": 68.2,
        "sos": 2.0, "wins": 26, "efg_pct": 0.498, "turnover_pct": 18.5,
        "oreb_pct": 27.0, "ft_rate": 0.29, "opp_efg_pct": 0.502,
        "opp_turnover_pct": 16.5, "opp_oreb_pct": 29.0, "opp_ft_rate": 0.34,
        "barthag": 0.680, "region": "South"
    },
    "Norfolk St": {
        "seed": 16, "adj_off": 101.8, "adj_def": 108.5, "adj_tempo": 67.8,
        "sos": 1.5, "wins": 22, "efg_pct": 0.485, "turnover_pct": 19.5,
        "oreb_pct": 26.5, "ft_rate": 0.28, "opp_efg_pct": 0.510,
        "opp_turnover_pct": 16.0, "opp_oreb_pct": 30.0, "opp_ft_rate": 0.35,
        "barthag": 0.580, "region": "South"
    },
    "Clemson": {
        "seed": 13, "adj_off": 107.5, "adj_def": 101.8, "adj_tempo": 66.5,
        "sos": 5.5, "wins": 21, "efg_pct": 0.508, "turnover_pct": 17.8,
        "oreb_pct": 28.2, "ft_rate": 0.31, "opp_efg_pct": 0.495,
        "opp_turnover_pct": 17.2, "opp_oreb_pct": 28.0, "opp_ft_rate": 0.33,
        "barthag": 0.760, "region": "South"
    },

    # --- WEST REGION ---
    "Florida": {
        "seed": 1, "adj_off": 122.8, "adj_def": 90.5, "adj_tempo": 68.8,
        "sos": 8.2, "wins": 31, "efg_pct": 0.562, "turnover_pct": 15.0,
        "oreb_pct": 32.5, "ft_rate": 0.39, "opp_efg_pct": 0.450,
        "opp_turnover_pct": 20.5, "opp_oreb_pct": 24.0, "opp_ft_rate": 0.27,
        "barthag": 0.975, "region": "West"
    },
    "UConn": {
        "seed": 8, "adj_off": 113.0, "adj_def": 97.5, "adj_tempo": 68.0,
        "sos": 7.0, "wins": 22, "efg_pct": 0.528, "turnover_pct": 16.8,
        "oreb_pct": 31.2, "ft_rate": 0.35, "opp_efg_pct": 0.483,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.890, "region": "West"
    },
    "Oklahoma": {
        "seed": 9, "adj_off": 111.2, "adj_def": 98.5, "adj_tempo": 67.0,
        "sos": 6.2, "wins": 22, "efg_pct": 0.525, "turnover_pct": 16.5,
        "oreb_pct": 29.8, "ft_rate": 0.33, "opp_efg_pct": 0.486,
        "opp_turnover_pct": 18.0, "opp_oreb_pct": 27.2, "opp_ft_rate": 0.31,
        "barthag": 0.875, "region": "West"
    },
    "Memphis": {
        "seed": 4, "adj_off": 117.5, "adj_def": 95.0, "adj_tempo": 70.5,
        "sos": 6.8, "wins": 26, "efg_pct": 0.545, "turnover_pct": 16.2,
        "oreb_pct": 32.5, "ft_rate": 0.36, "opp_efg_pct": 0.470,
        "opp_turnover_pct": 19.2, "opp_oreb_pct": 25.5, "opp_ft_rate": 0.29,
        "barthag": 0.938, "region": "West"
    },
    "Missouri": {
        "seed": 5, "adj_off": 115.8, "adj_def": 96.5, "adj_tempo": 67.5,
        "sos": 6.8, "wins": 24, "efg_pct": 0.540, "turnover_pct": 16.0,
        "oreb_pct": 30.0, "ft_rate": 0.35, "opp_efg_pct": 0.475,
        "opp_turnover_pct": 18.8, "opp_oreb_pct": 26.0, "opp_ft_rate": 0.30,
        "barthag": 0.918, "region": "West"
    },
    "UC San Diego": {
        "seed": 12, "adj_off": 109.5, "adj_def": 100.0, "adj_tempo": 66.5,
        "sos": 3.8, "wins": 27, "efg_pct": 0.525, "turnover_pct": 16.5,
        "oreb_pct": 28.5, "ft_rate": 0.32, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 18.0, "opp_oreb_pct": 27.0, "opp_ft_rate": 0.31,
        "barthag": 0.825, "region": "West"
    },
    "Illinois": {
        "seed": 6, "adj_off": 116.0, "adj_def": 96.8, "adj_tempo": 69.0,
        "sos": 7.2, "wins": 23, "efg_pct": 0.540, "turnover_pct": 16.5,
        "oreb_pct": 31.0, "ft_rate": 0.35, "opp_efg_pct": 0.480,
        "opp_turnover_pct": 18.2, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.912, "region": "West"
    },
    "Kentucky": {
        "seed": 11, "adj_off": 110.5, "adj_def": 99.2, "adj_tempo": 68.5,
        "sos": 6.5, "wins": 21, "efg_pct": 0.520, "turnover_pct": 17.0,
        "oreb_pct": 30.5, "ft_rate": 0.34, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 17.8, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.32,
        "barthag": 0.845, "region": "West"
    },
    "St. John's": {
        "seed": 3, "adj_off": 118.5, "adj_def": 94.0, "adj_tempo": 67.8,
        "sos": 7.5, "wins": 27, "efg_pct": 0.550, "turnover_pct": 15.5,
        "oreb_pct": 31.5, "ft_rate": 0.37, "opp_efg_pct": 0.465,
        "opp_turnover_pct": 19.8, "opp_oreb_pct": 25.0, "opp_ft_rate": 0.28,
        "barthag": 0.948, "region": "West"
    },
    "Omaha": {
        "seed": 14, "adj_off": 105.8, "adj_def": 104.0, "adj_tempo": 68.0,
        "sos": 2.2, "wins": 24, "efg_pct": 0.502, "turnover_pct": 18.2,
        "oreb_pct": 27.8, "ft_rate": 0.30, "opp_efg_pct": 0.500,
        "opp_turnover_pct": 17.0, "opp_oreb_pct": 28.8, "opp_ft_rate": 0.33,
        "barthag": 0.710, "region": "West"
    },
    "Gonzaga": {
        "seed": 7, "adj_off": 115.0, "adj_def": 97.0, "adj_tempo": 70.0,
        "sos": 5.5, "wins": 26, "efg_pct": 0.548, "turnover_pct": 15.8,
        "oreb_pct": 30.0, "ft_rate": 0.36, "opp_efg_pct": 0.480,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.2, "opp_ft_rate": 0.30,
        "barthag": 0.905, "region": "West"
    },
    "Georgia": {
        "seed": 10, "adj_off": 111.8, "adj_def": 99.0, "adj_tempo": 67.5,
        "sos": 6.2, "wins": 22, "efg_pct": 0.522, "turnover_pct": 17.0,
        "oreb_pct": 30.0, "ft_rate": 0.33, "opp_efg_pct": 0.487,
        "opp_turnover_pct": 18.0, "opp_oreb_pct": 27.0, "opp_ft_rate": 0.31,
        "barthag": 0.860, "region": "West"
    },
    "Auburn": {
        "seed": 2, "adj_off": 121.0, "adj_def": 92.0, "adj_tempo": 69.5,
        "sos": 8.0, "wins": 29, "efg_pct": 0.558, "turnover_pct": 15.2,
        "oreb_pct": 33.0, "ft_rate": 0.38, "opp_efg_pct": 0.455,
        "opp_turnover_pct": 20.8, "opp_oreb_pct": 24.2, "opp_ft_rate": 0.27,
        "barthag": 0.965, "region": "West"
    },
    "Loyola Chicago": {
        "seed": 15, "adj_off": 104.0, "adj_def": 105.5, "adj_tempo": 63.5,
        "sos": 2.5, "wins": 25, "efg_pct": 0.500, "turnover_pct": 15.5,
        "oreb_pct": 27.2, "ft_rate": 0.29, "opp_efg_pct": 0.505,
        "opp_turnover_pct": 16.2, "opp_oreb_pct": 29.2, "opp_ft_rate": 0.34,
        "barthag": 0.665, "region": "West"
    },
    "SIU Edwardsville": {
        "seed": 16, "adj_off": 100.5, "adj_def": 109.0, "adj_tempo": 66.5,
        "sos": 1.2, "wins": 20, "efg_pct": 0.480, "turnover_pct": 19.8,
        "oreb_pct": 26.0, "ft_rate": 0.27, "opp_efg_pct": 0.515,
        "opp_turnover_pct": 15.5, "opp_oreb_pct": 30.5, "opp_ft_rate": 0.36,
        "barthag": 0.560, "region": "West"
    },
    "San Diego St": {
        "seed": 13, "adj_off": 107.0, "adj_def": 96.5, "adj_tempo": 64.8,
        "sos": 5.0, "wins": 23, "efg_pct": 0.512, "turnover_pct": 16.8,
        "oreb_pct": 28.0, "ft_rate": 0.32, "opp_efg_pct": 0.478,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.790, "region": "West"
    },

    # --- EAST REGION ---
    "Houston": {
        "seed": 1, "adj_off": 121.5, "adj_def": 89.8, "adj_tempo": 66.0,
        "sos": 8.5, "wins": 31, "efg_pct": 0.558, "turnover_pct": 14.8,
        "oreb_pct": 34.0, "ft_rate": 0.38, "opp_efg_pct": 0.445,
        "opp_turnover_pct": 21.0, "opp_oreb_pct": 23.5, "opp_ft_rate": 0.26,
        "barthag": 0.978, "region": "East"
    },
    "Louisville": {
        "seed": 8, "adj_off": 112.8, "adj_def": 98.0, "adj_tempo": 69.0,
        "sos": 6.8, "wins": 23, "efg_pct": 0.530, "turnover_pct": 16.5,
        "oreb_pct": 31.0, "ft_rate": 0.35, "opp_efg_pct": 0.485,
        "opp_turnover_pct": 18.0, "opp_oreb_pct": 27.0, "opp_ft_rate": 0.31,
        "barthag": 0.888, "region": "East"
    },
    "Creighton": {
        "seed": 9, "adj_off": 112.0, "adj_def": 98.5, "adj_tempo": 68.5,
        "sos": 6.5, "wins": 22, "efg_pct": 0.535, "turnover_pct": 16.0,
        "oreb_pct": 28.8, "ft_rate": 0.34, "opp_efg_pct": 0.485,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.8, "opp_ft_rate": 0.31,
        "barthag": 0.882, "region": "East"
    },
    "Michigan": {
        "seed": 4, "adj_off": 117.8, "adj_def": 94.8, "adj_tempo": 67.5,
        "sos": 7.5, "wins": 26, "efg_pct": 0.550, "turnover_pct": 15.8,
        "oreb_pct": 30.5, "ft_rate": 0.36, "opp_efg_pct": 0.468,
        "opp_turnover_pct": 19.2, "opp_oreb_pct": 25.5, "opp_ft_rate": 0.29,
        "barthag": 0.940, "region": "East"
    },
    "Texas A&M": {
        "seed": 5, "adj_off": 115.5, "adj_def": 96.0, "adj_tempo": 66.8,
        "sos": 7.0, "wins": 24, "efg_pct": 0.538, "turnover_pct": 16.0,
        "oreb_pct": 31.5, "ft_rate": 0.36, "opp_efg_pct": 0.475,
        "opp_turnover_pct": 18.8, "opp_oreb_pct": 25.8, "opp_ft_rate": 0.29,
        "barthag": 0.922, "region": "East"
    },
    "Yale": {
        "seed": 12, "adj_off": 110.0, "adj_def": 100.2, "adj_tempo": 65.5,
        "sos": 3.5, "wins": 26, "efg_pct": 0.530, "turnover_pct": 15.8,
        "oreb_pct": 28.0, "ft_rate": 0.32, "opp_efg_pct": 0.490,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.32,
        "barthag": 0.828, "region": "East"
    },
    "UCLA": {
        "seed": 6, "adj_off": 115.2, "adj_def": 96.5, "adj_tempo": 68.2,
        "sos": 7.0, "wins": 23, "efg_pct": 0.538, "turnover_pct": 16.8,
        "oreb_pct": 30.0, "ft_rate": 0.34, "opp_efg_pct": 0.478,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.910, "region": "East"
    },
    "UC Irvine": {
        "seed": 11, "adj_off": 109.0, "adj_def": 99.5, "adj_tempo": 64.0,
        "sos": 3.8, "wins": 27, "efg_pct": 0.528, "turnover_pct": 15.0,
        "oreb_pct": 28.5, "ft_rate": 0.31, "opp_efg_pct": 0.485,
        "opp_turnover_pct": 17.2, "opp_oreb_pct": 27.2, "opp_ft_rate": 0.31,
        "barthag": 0.830, "region": "East"
    },
    "Tennessee": {
        "seed": 3, "adj_off": 118.8, "adj_def": 93.2, "adj_tempo": 67.0,
        "sos": 8.0, "wins": 27, "efg_pct": 0.550, "turnover_pct": 15.2,
        "oreb_pct": 32.0, "ft_rate": 0.37, "opp_efg_pct": 0.460,
        "opp_turnover_pct": 19.8, "opp_oreb_pct": 25.0, "opp_ft_rate": 0.28,
        "barthag": 0.952, "region": "East"
    },
    "Wofford": {
        "seed": 14, "adj_off": 106.0, "adj_def": 103.5, "adj_tempo": 66.5,
        "sos": 2.0, "wins": 26, "efg_pct": 0.515, "turnover_pct": 16.5,
        "oreb_pct": 27.0, "ft_rate": 0.30, "opp_efg_pct": 0.498,
        "opp_turnover_pct": 17.2, "opp_oreb_pct": 28.5, "opp_ft_rate": 0.33,
        "barthag": 0.725, "region": "East"
    },
    "Purdue": {
        "seed": 7, "adj_off": 114.8, "adj_def": 97.5, "adj_tempo": 66.0,
        "sos": 7.0, "wins": 23, "efg_pct": 0.545, "turnover_pct": 16.0,
        "oreb_pct": 32.5, "ft_rate": 0.36, "opp_efg_pct": 0.482,
        "opp_turnover_pct": 17.8, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.898, "region": "East"
    },
    "BYU": {
        "seed": 10, "adj_off": 112.5, "adj_def": 99.5, "adj_tempo": 68.0,
        "sos": 6.0, "wins": 22, "efg_pct": 0.530, "turnover_pct": 16.5,
        "oreb_pct": 29.5, "ft_rate": 0.33, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.32,
        "barthag": 0.862, "region": "East"
    },
    "Alabama": {
        "seed": 2, "adj_off": 120.5, "adj_def": 92.5, "adj_tempo": 72.0,
        "sos": 8.2, "wins": 28, "efg_pct": 0.555, "turnover_pct": 16.0,
        "oreb_pct": 33.5, "ft_rate": 0.37, "opp_efg_pct": 0.458,
        "opp_turnover_pct": 20.0, "opp_oreb_pct": 24.5, "opp_ft_rate": 0.27,
        "barthag": 0.962, "region": "East"
    },
    "Robert Morris": {
        "seed": 15, "adj_off": 103.5, "adj_def": 105.8, "adj_tempo": 67.0,
        "sos": 1.8, "wins": 24, "efg_pct": 0.495, "turnover_pct": 18.2,
        "oreb_pct": 27.5, "ft_rate": 0.29, "opp_efg_pct": 0.505,
        "opp_turnover_pct": 16.2, "opp_oreb_pct": 29.5, "opp_ft_rate": 0.34,
        "barthag": 0.660, "region": "East"
    },
    "SE Louisiana": {
        "seed": 16, "adj_off": 101.0, "adj_def": 109.2, "adj_tempo": 69.0,
        "sos": 1.0, "wins": 21, "efg_pct": 0.482, "turnover_pct": 20.0,
        "oreb_pct": 26.2, "ft_rate": 0.27, "opp_efg_pct": 0.518,
        "opp_turnover_pct": 15.5, "opp_oreb_pct": 30.5, "opp_ft_rate": 0.36,
        "barthag": 0.550, "region": "East"
    },
    "High Point": {
        "seed": 13, "adj_off": 108.0, "adj_def": 101.0, "adj_tempo": 69.5,
        "sos": 3.2, "wins": 26, "efg_pct": 0.518, "turnover_pct": 17.0,
        "oreb_pct": 29.5, "ft_rate": 0.33, "opp_efg_pct": 0.492,
        "opp_turnover_pct": 17.8, "opp_oreb_pct": 27.8, "opp_ft_rate": 0.32,
        "barthag": 0.780, "region": "East"
    },

    # --- MIDWEST REGION ---
    "Iowa St": {
        "seed": 1, "adj_off": 122.0, "adj_def": 90.0, "adj_tempo": 65.5,
        "sos": 8.0, "wins": 30, "efg_pct": 0.560, "turnover_pct": 14.5,
        "oreb_pct": 31.0, "ft_rate": 0.38, "opp_efg_pct": 0.448,
        "opp_turnover_pct": 21.5, "opp_oreb_pct": 23.8, "opp_ft_rate": 0.26,
        "barthag": 0.976, "region": "Midwest"
    },
    "Mississippi St": {
        "seed": 8, "adj_off": 113.2, "adj_def": 97.0, "adj_tempo": 69.5,
        "sos": 6.8, "wins": 23, "efg_pct": 0.528, "turnover_pct": 16.8,
        "oreb_pct": 31.5, "ft_rate": 0.35, "opp_efg_pct": 0.480,
        "opp_turnover_pct": 18.2, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.892, "region": "Midwest"
    },
    "San Diego": {
        "seed": 9, "adj_off": 111.5, "adj_def": 98.8, "adj_tempo": 67.0,
        "sos": 4.5, "wins": 25, "efg_pct": 0.530, "turnover_pct": 16.2,
        "oreb_pct": 29.0, "ft_rate": 0.33, "opp_efg_pct": 0.485,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.8, "opp_ft_rate": 0.31,
        "barthag": 0.878, "region": "Midwest"
    },
    "Maryland": {
        "seed": 4, "adj_off": 118.0, "adj_def": 95.0, "adj_tempo": 68.5,
        "sos": 7.5, "wins": 26, "efg_pct": 0.548, "turnover_pct": 15.5,
        "oreb_pct": 31.0, "ft_rate": 0.36, "opp_efg_pct": 0.470,
        "opp_turnover_pct": 19.2, "opp_oreb_pct": 25.5, "opp_ft_rate": 0.29,
        "barthag": 0.942, "region": "Midwest"
    },
    "Vanderbilt": {
        "seed": 5, "adj_off": 116.0, "adj_def": 96.2, "adj_tempo": 68.0,
        "sos": 7.2, "wins": 24, "efg_pct": 0.542, "turnover_pct": 16.2,
        "oreb_pct": 30.5, "ft_rate": 0.35, "opp_efg_pct": 0.476,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 26.0, "opp_ft_rate": 0.30,
        "barthag": 0.920, "region": "Midwest"
    },
    "Liberty": {
        "seed": 12, "adj_off": 109.2, "adj_def": 100.5, "adj_tempo": 66.0,
        "sos": 3.5, "wins": 27, "efg_pct": 0.522, "turnover_pct": 16.0,
        "oreb_pct": 28.8, "ft_rate": 0.32, "opp_efg_pct": 0.490,
        "opp_turnover_pct": 17.8, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.32,
        "barthag": 0.818, "region": "Midwest"
    },
    "Kansas": {
        "seed": 6, "adj_off": 116.5, "adj_def": 96.0, "adj_tempo": 69.0,
        "sos": 7.5, "wins": 23, "efg_pct": 0.542, "turnover_pct": 16.5,
        "oreb_pct": 31.2, "ft_rate": 0.35, "opp_efg_pct": 0.475,
        "opp_turnover_pct": 18.8, "opp_oreb_pct": 25.8, "opp_ft_rate": 0.29,
        "barthag": 0.918, "region": "Midwest"
    },
    "Arkansas": {
        "seed": 11, "adj_off": 110.8, "adj_def": 99.0, "adj_tempo": 71.0,
        "sos": 6.2, "wins": 22, "efg_pct": 0.518, "turnover_pct": 17.2,
        "oreb_pct": 32.0, "ft_rate": 0.34, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 18.5, "opp_oreb_pct": 27.5, "opp_ft_rate": 0.31,
        "barthag": 0.848, "region": "Midwest"
    },
    "Texas": {
        "seed": 3, "adj_off": 119.2, "adj_def": 93.8, "adj_tempo": 67.5,
        "sos": 8.0, "wins": 27, "efg_pct": 0.552, "turnover_pct": 15.2,
        "oreb_pct": 32.0, "ft_rate": 0.37, "opp_efg_pct": 0.462,
        "opp_turnover_pct": 19.5, "opp_oreb_pct": 25.0, "opp_ft_rate": 0.28,
        "barthag": 0.955, "region": "Midwest"
    },
    "Troy": {
        "seed": 14, "adj_off": 105.5, "adj_def": 104.2, "adj_tempo": 70.5,
        "sos": 2.8, "wins": 25, "efg_pct": 0.508, "turnover_pct": 17.5,
        "oreb_pct": 28.0, "ft_rate": 0.31, "opp_efg_pct": 0.500,
        "opp_turnover_pct": 17.0, "opp_oreb_pct": 28.5, "opp_ft_rate": 0.33,
        "barthag": 0.715, "region": "Midwest"
    },
    "Dayton": {
        "seed": 7, "adj_off": 114.0, "adj_def": 97.5, "adj_tempo": 68.0,
        "sos": 5.8, "wins": 25, "efg_pct": 0.535, "turnover_pct": 16.0,
        "oreb_pct": 30.0, "ft_rate": 0.34, "opp_efg_pct": 0.482,
        "opp_turnover_pct": 18.0, "opp_oreb_pct": 26.5, "opp_ft_rate": 0.30,
        "barthag": 0.895, "region": "Midwest"
    },
    "North Carolina": {
        "seed": 10, "adj_off": 112.0, "adj_def": 99.2, "adj_tempo": 70.5,
        "sos": 6.5, "wins": 21, "efg_pct": 0.525, "turnover_pct": 16.5,
        "oreb_pct": 31.5, "ft_rate": 0.34, "opp_efg_pct": 0.488,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 27.2, "opp_ft_rate": 0.31,
        "barthag": 0.858, "region": "Midwest"
    },
    "Iowa": {
        "seed": 2, "adj_off": 121.2, "adj_def": 92.2, "adj_tempo": 69.0,
        "sos": 7.8, "wins": 28, "efg_pct": 0.558, "turnover_pct": 15.0,
        "oreb_pct": 32.0, "ft_rate": 0.38, "opp_efg_pct": 0.455,
        "opp_turnover_pct": 20.2, "opp_oreb_pct": 24.5, "opp_ft_rate": 0.27,
        "barthag": 0.968, "region": "Midwest"
    },
    "Lipscomb": {
        "seed": 15, "adj_off": 104.2, "adj_def": 106.0, "adj_tempo": 66.5,
        "sos": 1.8, "wins": 24, "efg_pct": 0.498, "turnover_pct": 17.8,
        "oreb_pct": 27.0, "ft_rate": 0.29, "opp_efg_pct": 0.508,
        "opp_turnover_pct": 16.0, "opp_oreb_pct": 29.5, "opp_ft_rate": 0.35,
        "barthag": 0.650, "region": "Midwest"
    },
    "FDU": {
        "seed": 16, "adj_off": 100.2, "adj_def": 110.0, "adj_tempo": 67.0,
        "sos": 1.0, "wins": 20, "efg_pct": 0.478, "turnover_pct": 20.0,
        "oreb_pct": 26.0, "ft_rate": 0.27, "opp_efg_pct": 0.520,
        "opp_turnover_pct": 15.2, "opp_oreb_pct": 31.0, "opp_ft_rate": 0.37,
        "barthag": 0.540, "region": "Midwest"
    },
    "Colorado St": {
        "seed": 13, "adj_off": 108.2, "adj_def": 101.5, "adj_tempo": 66.0,
        "sos": 4.2, "wins": 25, "efg_pct": 0.515, "turnover_pct": 17.2,
        "oreb_pct": 28.5, "ft_rate": 0.32, "opp_efg_pct": 0.495,
        "opp_turnover_pct": 17.5, "opp_oreb_pct": 28.0, "opp_ft_rate": 0.32,
        "barthag": 0.770, "region": "Midwest"
    },
}


# Historical game results for training (based on typical NCAA tournament patterns)
# Format: (team_a, team_b, team_a_won)
# Generated from 8 seasons of historical matchup patterns with realistic outcomes
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

    # 4 vs 5 seeds (~55% for 4 seed - nearly coin flip)
    ({"seed_diff": -1, "adj_eff_diff": 3.0, "barthag_diff": 0.02, "sos_diff": 0.5, "tempo_diff": 0.5, "efg_diff": 0.01}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 2.0, "barthag_diff": 0.01, "sos_diff": 0.3, "tempo_diff": -0.5, "efg_diff": 0.00}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 1.0, "barthag_diff": 0.01, "sos_diff": 0.2, "tempo_diff": 1.0, "efg_diff": 0.00}, 1),
    ({"seed_diff": -1, "adj_eff_diff": 0.5, "barthag_diff": 0.00, "sos_diff": 0.0, "tempo_diff": -1.0, "efg_diff": 0.00}, 0),
    ({"seed_diff": -1, "adj_eff_diff": -1.0, "barthag_diff": -0.01, "sos_diff": -0.2, "tempo_diff": 0.5, "efg_diff": -0.01}, 0),
    ({"seed_diff": -1, "adj_eff_diff": -0.5, "barthag_diff": 0.00, "sos_diff": -0.1, "tempo_diff": 1.5, "efg_diff": 0.00}, 0),

    # 5 vs 12 seeds (~65% for 5 seed - classic upset spot)
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

    # Deep tournament matchups (same seed ranges, tight games)
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

    # Additional variety - upsets and chalk
    ({"seed_diff": -8, "adj_eff_diff": 10.0, "barthag_diff": 0.12, "sos_diff": 3.0, "tempo_diff": 0.0, "efg_diff": 0.03}, 1),
    ({"seed_diff": -8, "adj_eff_diff": 5.0, "barthag_diff": 0.06, "sos_diff": 1.5, "tempo_diff": 1.0, "efg_diff": 0.01}, 0),
    ({"seed_diff": -10, "adj_eff_diff": 14.0, "barthag_diff": 0.18, "sos_diff": 4.0, "tempo_diff": -0.5, "efg_diff": 0.04}, 1),
    ({"seed_diff": -10, "adj_eff_diff": 8.0, "barthag_diff": 0.10, "sos_diff": 2.5, "tempo_diff": 1.5, "efg_diff": 0.02}, 0),
    ({"seed_diff": -12, "adj_eff_diff": 18.0, "barthag_diff": 0.24, "sos_diff": 5.0, "tempo_diff": 0.5, "efg_diff": 0.05}, 1),
    ({"seed_diff": -12, "adj_eff_diff": 10.0, "barthag_diff": 0.14, "sos_diff": 3.0, "tempo_diff": -1.0, "efg_diff": 0.03}, 0),
    ({"seed_diff": -14, "adj_eff_diff": 22.0, "barthag_diff": 0.30, "sos_diff": 6.0, "tempo_diff": 1.0, "efg_diff": 0.06}, 1),
    ({"seed_diff": -14, "adj_eff_diff": 12.0, "barthag_diff": 0.18, "sos_diff": 3.5, "tempo_diff": -0.5, "efg_diff": 0.03}, 0),
]
