from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# 🔐 Load API key from Render Environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Automatically select available Gemini model
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

        if not age or not weight or not height:
            return jsonify({"error": "Missing required
