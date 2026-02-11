from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# 🔐 Load Gemini API Key from Environment Variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use latest working model
model = genai.GenerativeModel("gemini-1.5-pro")


@app.route("/")
def home():
    return "AI Diet Planner Backend is Running 🚀"


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.get_json()

        age = data.get("age")
        weight = data.get("weight")
        height = data.get("height")
        goal = data.get("goal")
        diet_type = data.get("dietType")
        duration = data.get("duration")

        if not age or not weight or not height:
            return jsonify({"error": "Missing required fields"}), 400

        # 🧠 Prompt for Gemini
        prompt = f"""
        Create a detailed Indian diet plan for:

        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Food Preference: {diet_type}
        Duration: {duration} days

        Include:
        - Morning routine
        - Breakfast
        - Lunch
        - Evening snack
        - Dinner
        - Basic workout suggestion
        - Approximate calorie guidance

        Make it structured and easy to read.
        """

        response = model.generate_content(prompt)

        return jsonify({"plan": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

