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

# 🔐 Use environment variable for security (SET THIS IN RENDER)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.0-pro")

# Daily limit
daily_count = 0
current_date = datetime.now().date()


# ✅ Home Route (Fixes 404)
@app.route("/")
def home():
    return render_template("index.html")


# ✅ Generate Diet Plan
@app.route("/generate", methods=["POST"])
def generate():
    global daily_count, current_date

    # Reset count if new day
    if datetime.now().date() != current_date:
        daily_count = 0
        current_date = datetime.now().date()

    # Limit 20 per day
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

    try:
        response = model.generate_content(prompt)
        plan_text = response.text
    except Exception as e:
        return jsonify({
            "limit": False,
            "plan": "Error generating plan. Please check API key."
        })

    daily_count += 1

    return jsonify({
        "limit": False,
        "plan": plan_text
    })


# ✅ Download PDF
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


# ✅ Required for local run (Render uses gunicorn)
if __name__ == "__main__":
    app.run(debug=True)
