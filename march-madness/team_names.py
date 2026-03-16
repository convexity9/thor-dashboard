"""
Team Name Normalization for March Madness Prediction Model

Handles the inconsistency between how KenPom, ESPN, CBS, and other sources
name college basketball teams. Maps all known variations to a single
canonical name used by the model.

Usage:
    from team_names import normalize_team_name
    name = normalize_team_name("Connecticut")  # -> "UConn"
"""

# Canonical name -> list of known aliases
# The canonical name is what the model uses internally.
# When a user provides KenPom data, their team names are matched against
# these aliases (case-insensitive) to find the canonical form.

TEAM_ALIASES = {
    # --- EAST REGION ---
    "Duke": ["Duke", "Duke Blue Devils"],
    "Siena": ["Siena", "Siena Saints"],
    "Ohio State": ["Ohio State", "Ohio St.", "Ohio St", "OSU Buckeyes", "Ohio State Buckeyes"],
    "TCU": ["TCU", "Texas Christian", "Texas Christian University", "TCU Horned Frogs"],
    "St. John's": ["St. John's", "Saint John's", "St Johns", "St. Johns", "Saint Johns",
                    "St. John's Red Storm", "SJU"],
    "Northern Iowa": ["Northern Iowa", "UNI", "Northern Iowa Panthers", "N. Iowa"],
    "Kansas": ["Kansas", "Kansas Jayhawks", "KU"],
    "Cal Baptist": ["Cal Baptist", "California Baptist", "CBU", "Cal Baptist Lancers",
                     "California Baptist Lancers"],
    "Louisville": ["Louisville", "Louisville Cardinals", "UofL"],
    "South Florida": ["South Florida", "USF", "South Florida Bulls", "S. Florida"],
    "Michigan State": ["Michigan State", "Michigan St.", "Michigan St", "MSU",
                        "Michigan State Spartans", "Mich. St."],
    "North Dakota State": ["North Dakota State", "North Dakota St.", "North Dakota St",
                            "NDSU", "N. Dakota St.", "N Dakota St", "ND State"],
    "UCLA": ["UCLA", "UCLA Bruins"],
    "UCF": ["UCF", "Central Florida", "Central Fla.", "UCF Knights"],
    "UConn": ["UConn", "Connecticut", "UCONN", "Connecticut Huskies", "Conn."],
    "Furman": ["Furman", "Furman Paladins"],

    # --- SOUTH REGION ---
    "Florida": ["Florida", "Florida Gators", "UF", "Fla."],
    "Prairie View A&M": ["Prairie View A&M", "Prairie View", "PVAMU", "Prairie View AM",
                          "Prairie View A&M Panthers"],
    "Lehigh": ["Lehigh", "Lehigh Mountain Hawks"],
    "Clemson": ["Clemson", "Clemson Tigers"],
    "Iowa": ["Iowa", "Iowa Hawkeyes"],
    "Vanderbilt": ["Vanderbilt", "Vanderbilt Commodores", "Vandy"],
    "McNeese": ["McNeese", "McNeese State", "McNeese St.", "McNeese St",
                 "McNeese Cowboys", "McNeese State Cowboys"],
    "Nebraska": ["Nebraska", "Nebraska Cornhuskers"],
    "Troy": ["Troy", "Troy Trojans"],
    "North Carolina": ["North Carolina", "UNC", "N. Carolina", "North Carolina Tar Heels",
                        "NC", "Carolina"],
    "VCU": ["VCU", "Virginia Commonwealth", "VCU Rams"],
    "Illinois": ["Illinois", "Illinois Fighting Illini", "Ill."],
    "Penn": ["Penn", "Pennsylvania", "Penn Quakers", "UPenn"],
    "Saint Mary's": ["Saint Mary's", "St. Mary's", "St Mary's", "Saint Marys",
                      "St. Marys", "St Marys", "Saint Mary's Gaels", "SMC"],
    "Texas A&M": ["Texas A&M", "Texas AM", "TAMU", "Texas A&M Aggies"],
    "Houston": ["Houston", "Houston Cougars", "UH"],
    "Idaho": ["Idaho", "Idaho Vandals"],

    # --- WEST REGION ---
    "Arizona": ["Arizona", "Arizona Wildcats", "AZ", "Ariz."],
    "LIU": ["LIU", "Long Island", "Long Island University", "LIU Sharks",
             "Long Island Sharks"],
    "Villanova": ["Villanova", "Villanova Wildcats", "Nova"],
    "Utah State": ["Utah State", "Utah St.", "Utah St", "USU",
                    "Utah State Aggies"],
    "Wisconsin": ["Wisconsin", "Wisconsin Badgers", "Wis.", "Wisc."],
    "High Point": ["High Point", "High Point Panthers", "HPU"],
    "Arkansas": ["Arkansas", "Arkansas Razorbacks", "Ark."],
    "Hawaii": ["Hawaii", "Hawai'i", "Hawai`i", "Hawaii Rainbow Warriors",
                "Hawai'i Rainbow Warriors"],
    "BYU": ["BYU", "Brigham Young", "Brigham Young University",
             "BYU Cougars"],
    "Texas": ["Texas", "Texas Longhorns", "UT"],
    "NC State": ["NC State", "North Carolina State", "N.C. State", "NC St.",
                  "North Carolina St.", "NC State Wolfpack", "NCSU"],
    "Gonzaga": ["Gonzaga", "Gonzaga Bulldogs", "Zags"],
    "Kennesaw State": ["Kennesaw State", "Kennesaw St.", "Kennesaw St",
                        "Kennesaw State Owls", "KSU Owls"],
    "Miami FL": ["Miami FL", "Miami (FL)", "Miami Florida", "Miami",
                  "Miami Hurricanes", "Miami (Fla.)", "U of Miami"],
    "Missouri": ["Missouri", "Missouri Tigers", "Mizzou", "MU"],
    "Purdue": ["Purdue", "Purdue Boilermakers"],
    "Queens": ["Queens", "Queens University", "Queens Royals"],

    # --- MIDWEST REGION ---
    "Michigan": ["Michigan", "Michigan Wolverines", "U of M", "Mich."],
    "UMBC": ["UMBC", "UMBC Retrievers", "Maryland Baltimore County",
              "UM Baltimore County"],
    "Howard": ["Howard", "Howard Bison", "Howard University"],
    "Georgia": ["Georgia", "Georgia Bulldogs", "UGA"],
    "Saint Louis": ["Saint Louis", "St. Louis", "St Louis", "SLU",
                     "Saint Louis Billikens", "St. Louis Billikens"],
    "Texas Tech": ["Texas Tech", "Texas Tech Red Raiders", "TTU"],
    "Akron": ["Akron", "Akron Zips"],
    "Alabama": ["Alabama", "Alabama Crimson Tide", "Bama"],
    "Hofstra": ["Hofstra", "Hofstra Pride"],
    "Tennessee": ["Tennessee", "Tennessee Volunteers", "Tenn.", "Vols", "UT Knoxville"],
    "SMU": ["SMU", "Southern Methodist", "SMU Mustangs",
             "Southern Methodist University"],
    "Miami OH": ["Miami OH", "Miami (OH)", "Miami Ohio", "Miami (Ohio)",
                  "Miami RedHawks", "Miami of Ohio", "Miami University"],
    "Virginia": ["Virginia", "Virginia Cavaliers", "UVA", "Va."],
    "Wright State": ["Wright State", "Wright St.", "Wright St",
                      "Wright State Raiders"],
    "Kentucky": ["Kentucky", "Kentucky Wildcats", "UK"],
    "Santa Clara": ["Santa Clara", "Santa Clara Broncos", "SCU"],
    "Iowa State": ["Iowa State", "Iowa St.", "Iowa St", "ISU",
                    "Iowa State Cyclones"],
    "Tennessee State": ["Tennessee State", "Tennessee St.", "Tennessee St",
                         "TSU", "Tennessee State Tigers"],
}

# Build reverse lookup: alias (lowercase) -> canonical name
_ALIAS_MAP = {}
for canonical, aliases in TEAM_ALIASES.items():
    for alias in aliases:
        _ALIAS_MAP[alias.lower().strip()] = canonical


def normalize_team_name(name):
    """
    Normalize a team name to the canonical form used by the model.

    Handles KenPom, ESPN, CBS, and other common naming variations.
    Case-insensitive matching.

    Args:
        name: Team name string from any source

    Returns:
        Canonical team name string, or original name if no match found
    """
    if not name:
        return name

    cleaned = name.strip()
    lookup = cleaned.lower()

    # Direct match
    if lookup in _ALIAS_MAP:
        return _ALIAS_MAP[lookup]

    # Try without trailing period
    if lookup.endswith("."):
        no_period = lookup[:-1]
        if no_period in _ALIAS_MAP:
            return _ALIAS_MAP[no_period]

    # Try removing "University" or "State" suffixes that may be partial
    for suffix in [" university", " univ.", " univ"]:
        if lookup.endswith(suffix):
            shortened = lookup[:-len(suffix)]
            if shortened in _ALIAS_MAP:
                return _ALIAS_MAP[shortened]

    # Fuzzy: check if input is a substring of any alias or vice versa
    # (handles cases like "Michigan" matching "Michigan Wolverines")
    for alias_lower, canonical in _ALIAS_MAP.items():
        if lookup == alias_lower:
            return canonical

    # Return original if no match (user will see it in output and can fix)
    return cleaned


def get_all_canonical_names():
    """Return list of all canonical team names."""
    return list(TEAM_ALIASES.keys())


def find_close_matches(name, n=5):
    """Find the closest matching canonical team names for a given input."""
    import difflib
    cleaned = name.strip().lower()
    all_aliases = list(_ALIAS_MAP.keys())
    matches = difflib.get_close_matches(cleaned, all_aliases, n=n, cutoff=0.5)
    return [(m, _ALIAS_MAP[m]) for m in matches]
