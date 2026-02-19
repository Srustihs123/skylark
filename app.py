from fastapi import FastAPI
from agent import (
    load_pilots,
    filter_pilots_by_skill_and_availability,
    match_pilots_for_mission
)

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Agent is running"}

@app.get("/pilots")
def get_pilots():
    pilots_df = load_pilots()
    return pilots_df.to_dict(orient="records")

@app.get("/pilots/search")
def search_pilots(skill: str):
    df = filter_pilots_by_skill_and_availability(skill)
    return df.to_dict(orient="records")

@app.get("/missions/{project_id}/pilots")
def get_pilots_for_mission(project_id: str):
    df = match_pilots_for_mission(project_id)
    return df.to_dict(orient="records")
