from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# ✅ Load Gemini API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use working Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return "AI Diet Planner Backend Running ✅"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        age = data.get("age")
        weight = data.get("weight")
        height = data.get("height")
        goal = data.get("goal")
        food = data.get("food")
        duration = data.get("duration")

        if not age or not weight or not height:
            return jsonify({"error": "Missing required fields"}), 400

        prompt = f"""
        Create a detailed {duration}-day diet plan.

        User Details:
        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Food Preference: {food}

        Include:
        - Breakfast
        - Lunch
        - Dinner
        - Snacks
        - Estimated daily calories
        - Protein intake

        Make it clean and structured.
        """

        response = model.generate_content(prompt)

        return jsonify({
            "result": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
