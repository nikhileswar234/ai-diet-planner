from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Auto-select model
def get_available_model():
    models = genai.list_models()
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            return m.name
    return None

model_name = get_available_model()

if model_name:
    model = genai.GenerativeModel(model_name)
else:
    model = None


@app.route("/")
def home():
    return "AI Diet Planner Backend Running 🚀"


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        if not model:
            return jsonify({"error": "No supported Gemini model found for this API key"}), 500

        data = request.get_json()

        age = data.get("age")
        weight = data.get("weight")
        height = data.get("height")
        goal = data.get("goal")
        diet_type = data.get("dietType")
        duration = data.get("duration")

        prompt = f"""
        Create a structured Indian diet plan.

        Age: {age}
        Weight: {weight} kg
        Height: {height} cm
        Goal: {goal}
        Food Type: {diet_type}
        Duration: {duration} days

        Include:
        - Breakfast
        - Lunch
        - Snacks
        - Dinner
        - Workout suggestion
        - Calories guidance

        Make it clean and formatted.
        """

        response = model.generate_content(prompt)

        return jsonify({"plan": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
