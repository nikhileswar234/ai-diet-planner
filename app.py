import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Daily quota tracker
daily_count = 0
current_day = datetime.utcnow().date()
MAX_DAILY_LIMIT = 20


@app.route("/")
def home():
    return "AI Diet Planner Backend Running 🚀"


@app.route("/generate", methods=["POST"])
def generate():
    global daily_count, current_day

    today = datetime.utcnow().date()

    if today != current_day:
        daily_count = 0
        current_day = today

    if daily_count >= MAX_DAILY_LIMIT:
        return jsonify({
            "limit": True,
            "message": "Sorry, there are only 20 AI plans allowed per day. Please try again tomorrow 🙏"
        })

    try:
        data = request.get_json()

        age = data.get("age")
        weight = data.get("weight")
        height = data.get("height")
        goal = data.get("goal")
        diet_type = data.get("dietType")
        duration = data.get("duration")

        prompt = f"""
        Create a professional {duration}-day Indian diet plan.

        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Diet Type: {diet_type}

        Include:
        - Breakfast
        - Lunch
        - Snacks
        - Dinner
        - Approximate daily calories
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        daily_count += 1

        return jsonify({
            "plan": response.text,
            "remaining": MAX_DAILY_LIMIT - daily_count
        })

    except Exception:
        return jsonify({
            "message": "AI is temporarily busy. Please try again later."
        }), 500


if __name__ == "__main__":
    app.run()
