from fastapi import FastAPI
from subprocess import Popen

app = FastAPI()

robot_script = "robot.py"

robots = []


@app.post("/start_robot")
def start_robot(start_int: int = 0):
    process = Popen(["python", robot_script, str(start_int)])
    robots.append(process)

    return {"message": "Started one more robot"}


@app.post("/stop_robot")
def stop_robot():
    if len(robots) == 0:
        return {"message": "There are no robots"}

    last_robot = robots[-1]
    last_robot.kill()
    robots.pop()

    return {"message": "Stopped last robot"}
