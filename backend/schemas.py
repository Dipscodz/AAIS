from pydantic import BaseModel
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class StudentData(BaseModel):
    attendance: float
    assignment_rate: float
    study_hours: float
    sleep_hours: float
    screen_time: float
    stress_level: float
    mood_score: float
    previous_gpa: float