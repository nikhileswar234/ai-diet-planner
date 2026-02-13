import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        age = data.get("age")
        weight = data.get("weight")
        height = data.get("height")
        goal = data.get("goal")
        diet = data.get("diet")
        duration = data.get("duration")

        prompt = f"""
        Create a {duration}-day Indian diet plan.

        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Diet Type: {diet}

        Include:
        - Breakfast
        - Lunch
        - Snacks
        - Dinner

        Format clearly day-wise.
        """

        response = model.generate_content(prompt)

        return jsonify({"plan": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
