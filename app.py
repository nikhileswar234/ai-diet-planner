import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "AI Diet Planner Backend Running"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    prompt = f"""
    Create a detailed diet plan.

    Age: {data['age']}
    Weight: {data['weight']} kg
    Height: {data['height']} cm
    Goal: {data['goal']}
    Diet Type: {data['dietType']}
    Duration: {data['duration']}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return jsonify({
        "plan": response.text,
        "remaining": 5
    })

if __name__ == "__main__":
    app.run()
