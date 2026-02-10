from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import generate_week_plan

app = Flask(__name__)
CORS(app)

def calculate_calories(weight, height, age, goal):
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    calories = bmr * 1.55  # moderate activity

    if goal == "loss":
        calories -= 500
    elif goal == "gain":
        calories += 300
    elif goal == "muscle":
        calories += 400

    return int(calories)

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.json

    age = data["age"]
    weight = data["weight"]
    height = data["height"]
    goal = data["goal"]
    food = data["food"]
    duration = data["duration"]

    calories = calculate_calories(weight, height, age, goal)

    week_plan = generate_week_plan(age, weight, height, goal, calories, food)

    if duration == "30":
        plan = {f"Week {i}": week_plan for i in range(1, 5)}

    else:  # 3 months
        plan = {
            "Month 1": {f"Week {i}": week_plan for i in range(1, 5)},
            "Month 2": {f"Week {i}": week_plan for i in range(1, 5)},
            "Month 3": {f"Week {i}": week_plan for i in range(1, 5)}
        }

    return jsonify({
        "calories": calories,
        "plan": plan
    })

if __name__ == "__main__":
    app.run(debug=True)
