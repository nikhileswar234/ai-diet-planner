import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==============================
# Configure Gemini API
# ==============================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.0-pro")

# ==============================
# ROOT ROUTE (Fixes 404)
# ==============================
@app.route("/")
def home():
    return "AI Diet Planner Backend is Running 🚀"

# ==============================
# Generate Diet Plan Route
# ==============================
@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.json

        weight = data.get("weight")
        height = data.get("height")
        age = data.get("age")
        goal = data.get("goal")
        diet_type = data.get("dietType")
        duration = data.get("duration")

        prompt = f"""
        Create a detailed Indian {diet_type} diet plan.

        User Details:
        - Weight: {weight} kg
        - Height: {height} cm
        - Age: {age}
        - Goal: {goal}
        - Duration: {duration}

        Include:
        - Breakfast
        - Lunch
        - Evening Snacks
        - Dinner
        - Approx calories
        - Protein rich options
        - Weekly variation
        """

        response = model.generate_content(prompt)

        return jsonify({
            "plan": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# Run App (for local testing)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
