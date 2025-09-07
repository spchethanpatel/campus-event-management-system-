from sqlalchemy.orm import Session
from . import models, schemas

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(name=event.name, description=event.description, date=event.date)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def register_student(db: Session, student_id: int, event_id: int):
    registration = models.Registration(student_id=student_id, event_id=event_id)
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def mark_attendance(db: Session, student_id: int, event_id: int):
    attendance = models.Attendance(student_id=student_id, event_id=event_id)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance
