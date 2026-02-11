import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# ==============================
# Configure Gemini API
# ==============================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Try safest stable model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


# ==============================
# Home Route (Health Check)
# ==============================
@app.route("/")
def home():
    return "AI Diet Planner Backend is Running 🚀"


# ==============================
# Generate Diet Plan Route
# ==============================
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

        if not age or not weight or not height:
            return jsonify({"error": "Missing required fields"}), 400

        # Create smart prompt
        prompt = f"""
        Create a professional {duration}-day diet plan.

        User Details:
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
        - Approximate calories per day
        - Protein-rich suggestions if muscle gain
        - Healthy balanced Indian-friendly foods

        Format clearly day-wise.
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
# Run App
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
