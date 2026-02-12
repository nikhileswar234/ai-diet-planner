import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# ==============================
# Configure Gemini (NEW SDK)
# ==============================
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ==============================
# Home Route
# ==============================
@app.route("/")
def home():
    return "AI Diet Planner Backend Running 🚀"

# ==============================
# Generate Route
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

        prompt = f"""
        Create a {duration}-day professional diet plan.

        User:
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
        - Approximate daily calories
        - Protein suggestions if muscle gain

        Format clearly day-wise.
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        return jsonify({
            "plan": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
