import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "Backend Running 🚀"

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
        Create a {duration}-day diet plan.
        Age: {age}
        Weight: {weight}
        Height: {height}
        Goal: {goal}
        Diet Type: {diet_type}
        """

        response = model.generate_content(prompt)

        return jsonify({"plan": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
