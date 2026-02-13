from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
CORS(app)

# 🔐 SET YOUR GEMINI KEY HERE
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.0-pro")

# Daily limit storage
daily_count = 0
current_date = datetime.now().date()


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

    file_path = "diet_report.pdf"
    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>AI Diet Plan Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(content.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
