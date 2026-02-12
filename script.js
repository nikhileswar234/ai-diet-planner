const backendURL = "https://ai-diet-planner-otbr.onrender.com/generate";
let currentUnit = "cm";
let latestPlan = "";

document.addEventListener("DOMContentLoaded", function () {

  const toggle = document.getElementById("darkToggle");

  toggle.addEventListener("click", function () {
    document.body.classList.toggle("dark");
  });

});

function setUnit(unit) {
  currentUnit = unit;
  const heightInput = document.getElementById("height");

  if (unit === "cm") {
    heightInput.placeholder = "Height (cm)";
  } else {
    heightInput.placeholder = "Height (feet)";
  }
}

function convertToCm(height) {
  if (currentUnit === "feet") {
    return height * 30.48;
  }
  return height;
}

function calculateBMI(weight, heightCm) {
  const h = heightCm / 100;
  return (weight / (h * h)).toFixed(1);
}

function generatePlan() {

  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  let height = document.getElementById("height").value;

  height = convertToCm(height);

  const goal = document.getElementById("goal").value;
  const dietType = document.getElementById("dietType").value;
  const duration = document.getElementById("duration").value;

  const bmi = calculateBMI(weight, height);

  document.getElementById("result").innerText =
    "Your BMI: " + bmi + "\nGenerating...\n";

  fetch(backendURL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ age, weight, height, goal, dietType, duration })
  })
  .then(res => res.json())
  .then(data => {

    if (data.limit) {
      document.getElementById("result").innerText = data.message;
      return;
    }

    latestPlan = data.plan;

    document.getElementById("result").innerText =
      "Your BMI: " + bmi + "\n\n" + data.plan;

    document.getElementById("downloadBtn").style.display = "block";
  })
  .catch(() => {
    document.getElementById("result").innerText =
      "❌ Unable to connect to server.";
  });
}

function downloadPDF() {

  const element = document.createElement("a");
  const file = new Blob([latestPlan], { type: "text/plain" });
  element.href = URL.createObjectURL(file);
  element.download = "DietPlan.txt";
  element.click();
}
