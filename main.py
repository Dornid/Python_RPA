from fastapi import FastAPI, Depends
from subprocess import Popen
from models import RobotRecords
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime, date

app = FastAPI()

RobotRecords.metadata.create_all(engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


robot_script = "robot.py"

robots = []


@app.post("/start_robot")
def start_robot(start_int: int = 0, db: Session = Depends(get_db)):
    process = Popen(["python", robot_script, str(start_int)])

    time_launch = datetime.now().time()
    record = RobotRecords(
        time_launch=time_launch,
        duration="Was not stopped",
        start_value=start_int,
    )
    db.add(record)
    db.commit()

    last_id = db.query(RobotRecords).order_by(RobotRecords.id.desc()).first().id
    robots.append([process, last_id])

    return {"message": "Started one more robot"}


@app.post("/stop_robot")
def stop_robot(db: Session = Depends(get_db)):
    if len(robots) == 0:
        return {"message": "There are no robots"}

    last_robot, last_record_id = robots[-1]
    last_robot.kill()
    robots.pop()

    now_time = datetime.now().time()

    try:
        time_start = (
            db.query(RobotRecords)
            .filter(RobotRecords.id == last_record_id)
            .first()
            .time_launch
        )
    except AttributeError:
        return {
            "message": "Last robot was stopped, but database missed important data, so record was not created"
        }

    time_diff = datetime.combine(date.today(), now_time) - datetime.combine(
        date.today(), time_start
    )
    db.query(RobotRecords).filter(RobotRecords.id == last_record_id).update(
        {RobotRecords.duration: str(time_diff)}
    )
    db.commit()

    return {"message": "Stopped last robot"}


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(RobotRecords).all()


@app.delete("/delete_history")
def delete_history(db: Session = Depends(get_db)):
    db.query(RobotRecords).delete()
    db.commit()

    return {"message": "All records deleted from database"}
