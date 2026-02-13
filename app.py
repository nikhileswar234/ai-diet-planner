from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

app = Flask(__name__)
CORS(app)

# ✅ Use environment variable for security
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.0-pro")

daily_count = 0
current_date = datetime.now().date()


# ✅ HOME ROUTE (THIS FIXES 404)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    global daily_count, current_date

    if datetime.now().date() != current_date:
        daily_count = 0
        current_date = datetime.now().date()

    if daily_count >= 20:
        return jsonify({
            "limit": True,
            "message": "Sorry there is only 20 quote per day try again tomorrow"
        })

    data = request.json

    prompt = f"""
    Create a professional Indian diet plan.

    Age: {data['age']}
    Weight: {data['weight']} kg
    Height: {data['height']} cm
    Goal: {data['goal']}
    Diet Type: {data['dietType']}
    Duration: {data['duration']} days

    Give structured meal plan day-wise.
    """

    response = model.generate_content(prompt)

    daily_count += 1

    return jsonify({
        "limit": False,
        "plan": response.text
    })


@app.route("/download", methods=["POST"])
def download():
    content = request.json["content"]

    file_path = "diet
