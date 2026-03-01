from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Dict, List

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_weak_factors(user_data: Dict) -> List[str]:
    """
    Rule-based pre-analysis before sending to LLM.
    This improves quality and reduces generic responses.
    """
    weak_factors = []

    if user_data["attendance"] < 75:
        weak_factors.append("Low Attendance")

    if user_data["assignment_rate"] < 70:
        weak_factors.append("Poor Assignment Completion")

    if user_data["study_hours"] < 3:
        weak_factors.append("Insufficient Study Hours")

    if user_data["sleep_hours"] < 6:
        weak_factors.append("Sleep Deprivation")

    if user_data["stress_level"] > 7:
        weak_factors.append("High Stress Levels")

    if user_data["mood_score"] < 5:
        weak_factors.append("Low Emotional Wellbeing")

    if user_data["previous_gpa"] < 6:
        weak_factors.append("Low Academic Performance")

    return weak_factors


def generate_burnout_advice(
    user_data: Dict,
    risk_level: str,
    risk_score: float
) -> str:
    """
    Generates structured, personalized academic strategy
    using OpenAI with fallback protection.
    """

    weak_factors = detect_weak_factors(user_data)

    prompt = f"""
You are AAIS (Autonomous Academic Intelligence System).

Your job is to analyze student academic and psychological signals
and generate a structured improvement strategy.

Student Data:
- Attendance: {user_data['attendance']}%
- Assignment Completion Rate: {user_data['assignment_rate']}%
- Study Hours Per Day: {user_data['study_hours']}
- Sleep Hours Per Day: {user_data['sleep_hours']}
- Screen Time Per Day: {user_data['screen_time']}
- Stress Level (1-10): {user_data['stress_level']}
- Mood Score (1-10): {user_data['mood_score']}
- Previous GPA: {user_data['previous_gpa']}

Predicted Risk Level: {risk_level}
Risk Score: {risk_score}%

Identified Weak Factors:
{weak_factors}

Instructions:
1. Identify the primary academic risk.
2. Identify psychological contributors.
3. Provide a structured 4-part improvement plan:
   - Academic Strategy
   - Mental Health Strategy
   - Lifestyle Adjustments
   - Short-Term Action Plan (7 days)
4. Keep response under 300 words.
5. Be professional, motivating, and precise.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an academic performance optimization AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
       
        return generate_fallback_advice(risk_level, weak_factors)


def generate_fallback_advice(risk_level: str, weak_factors: List[str]) -> str:
    """
    Safe fallback advice if API fails or quota exceeded.
    """

    base_message = f"Risk Level: {risk_level}\n\n"

    if risk_level == "High":
        base_message += (
            "You are currently at high academic risk. "
            "Immediate intervention is recommended.\n\n"
        )
    elif risk_level == "Medium":
        base_message += (
            "Your academic indicators show moderate risk. "
            "Preventive action is advised.\n\n"
        )
    else:
        base_message += (
            "Your academic performance is stable. "
            "Maintain consistency and monitor stress levels.\n\n"
        )

    if weak_factors:
        base_message += "Areas to Improve:\n"
        for factor in weak_factors:
            base_message += f"- {factor}\n"

    base_message += (
        "\nSuggested Actions:\n"
        "- Maintain structured study schedule\n"
        "- Improve sleep quality (7–8 hours)\n"
        "- Reduce unnecessary screen time\n"
        "- Practice weekly self-evaluation\n"
    )

    return base_message