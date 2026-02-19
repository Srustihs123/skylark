import pandas as pd

# ---------- LOADERS ----------

def load_pilots():
    return pd.read_csv("data/pilot_roster.csv")

def load_drones():
    return pd.read_csv("data/drone_fleet.csv")

def load_missions():
    return pd.read_csv("data/missions.csv")


# ---------- PILOT FILTER ----------

def filter_pilots_by_skill_and_availability(skill: str):
    df = load_pilots()

    # Only available pilots
    df = df[df["status"] == "Available"]

    # Skill match (case-insensitive)
    df = df[df["skills"].str.contains(skill, case=False, na=False)]

    return df


# ---------- MISSION HELPERS ----------

def get_mission_by_id(project_id: str):
    df = load_missions()
    mission = df[df["project_id"] == project_id]

    if mission.empty:
        return None

    return mission.iloc[0]


# ---------- CORE MATCHING LOGIC ----------

def match_pilots_for_mission(project_id: str):
    mission = get_mission_by_id(project_id)

    # 🚫 IMPORTANT: return EMPTY DATAFRAME, not list
    if mission is None:
        return pd.DataFrame()

    required_skill = mission["required_skills"]

    # ✅ Budget guard (safe int conversion)
    mission_budget = int(mission["mission_budget_inr"])

    df = load_pilots()

    # Only available pilots
    df = df[df["status"] == "Available"]

    # Skill match
    df = df[df["skills"].str.contains(required_skill, case=False, na=False)]

    # ✅ Budget filter
    df = df[df["daily_rate_inr"] <= mission_budget]

    return df
