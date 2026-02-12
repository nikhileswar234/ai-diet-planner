import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "AI Diet Planner Backend Running 🚀"

@app.route("/generate", methods=["POST"])
def generate():
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
        - Approx daily calories
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "plan": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run()
