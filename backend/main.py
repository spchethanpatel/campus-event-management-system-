from fastapi import FastAPI, Form, Depends
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve HTML pages
@app.get("/")
def index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/admin")
def admin():
    return FileResponse(os.path.join(frontend_path, "admin.html"))

@app.get("/reports")
def reports():
    return FileResponse(os.path.join(frontend_path, "reports.html"))

# API endpoints for form submissions
@app.post("/create-event")
def create_event(
    name: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db)
):
    event = schemas.EventCreate(name=name, description=description, date=date)
    crud.create_event(db, event)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/register")
def register(
    student_id: int = Form(...),
    event_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.register_student(db, student_id, event_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/attendance")
def attendance(
    student_id: int = Form(...),
    event_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.mark_attendance(db, student_id, event_id)
    return RedirectResponse(url="/", status_code=303)
