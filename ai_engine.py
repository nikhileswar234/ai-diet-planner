import google.generativeai as genai
import json
import os

genai.configure(api_key=os.getenv("AIzaSyCnXNYMdi_mrRsit-OtRXuEJayI203mtcc"))

model = genai.GenerativeModel("gemini-1.0-pro")

def generate_week_plan(age, weight, height, goal, calories, food_type):
    prompt = f"""
You are an Indian nutrition expert.

Create a 7-day diet plan in JSON format.

User details:
Age: {age}
Weight: {weight} kg
Height: {height} cm
Goal: {goal}
Daily Calories: {calories}
Food Preference: {food_type}

Rules:
- Indian foods only
- No supplements
- Include Breakfast, Lunch, Snacks, Dinner
- Avoid repeating main dishes daily
- Simple, affordable home foods
- Output ONLY valid JSON
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    return json.loads(text)
