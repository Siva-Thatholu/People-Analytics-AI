from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import Employee
from .generator import generate_synthetic_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="People Analytics API")

@app.post("/api/generate")
def trigger_data_generation(num_records: int = 50000, db: Session = Depends(get_db)):
    return generate_synthetic_data(db, num_records)

@app.get("/api/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@app.get("/api/analytics/risk-summary")
def get_risk_summary(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    summary = {}
    for emp in employees:
        dept = emp.department
        if dept not in summary:
            summary[dept] = {"High": 0, "Medium": 0, "Low": 0, "Avg_Sentiment": 0.0, "Count": 0}
        
        summary[dept][emp.flight_risk] += 1
        summary[dept]["Avg_Sentiment"] += emp.sentiment_score
        summary[dept]["Count"] += 1

    for dept in summary:
        summary[dept]["Avg_Sentiment"] = round(summary[dept]["Avg_Sentiment"] / summary[dept]["Count"], 2)
        
    return summary
