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
    0.4 * (10 - sleep_hours) +
    0.4 * stress_level +
    0.2 * screen_time -
    0.2 * mood_score
)


burnout_score += np.random.normal(0, 2, n_samples)


burnout_prob = 1 / (1 + np.exp(-burnout_score / 5))


threshold = np.median(burnout_prob)

burnout_risk = (burnout_prob > threshold).astype(int)