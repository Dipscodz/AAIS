import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 3000

attendance = np.random.uniform(60, 100, n_samples)
assignment_rate = np.random.uniform(50, 100, n_samples)
study_hours = np.random.uniform(1, 10, n_samples)
sleep_hours = np.random.uniform(4, 9, n_samples)
screen_time = np.random.uniform(1, 10, n_samples)
stress_level = np.random.uniform(1, 10, n_samples)
mood_score = np.random.uniform(1, 10, n_samples)
previous_gpa = np.random.uniform(5, 10, n_samples)

burnout_score = (
    0.5 * stress_level
    - 0.4 * sleep_hours
    + 0.3 * screen_time
    - 0.3 * mood_score
)

burnout_score += np.random.normal(0, 3, n_samples)


sorted_indices = np.argsort(burnout_score)
burnout_risk = np.zeros(n_samples)
burnout_risk[sorted_indices[n_samples//2:]] = 1

data = pd.DataFrame({
    "attendance": attendance,
    "assignment_rate": assignment_rate,
    "study_hours": study_hours,
    "sleep_hours": sleep_hours,
    "screen_time": screen_time,
    "stress_level": stress_level,
    "mood_score": mood_score,
    "previous_gpa": previous_gpa,
    "burnout_risk": burnout_risk.astype(int)
})

print(data["burnout_risk"].value_counts())

data.to_csv("student_burnout_data.csv", index=False)
print("Dataset generated successfully")