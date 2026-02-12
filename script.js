const backendURL = "https://ai-diet-planner-otbr.onrender.com/generate";

let useFeet = false;
let latestPlan = "";

// Dark mode
document.addEventListener("DOMContentLoaded", function () {

  const darkBtn = document.getElementById("darkToggle");
  darkBtn.addEventListener("click", function () {
    document.body.classList.toggle("dark");
  });

  const toggle = document.getElementById("unitToggle");

  toggle.addEventListener("change", function () {

    useFeet = toggle.checked;

    document.getElementById("heightCm").style.display =
      useFeet ? "none" : "block";

    document.getElementById("heightFeet").style.display =
      useFeet ? "block" : "none";

    document.getElementById("cmLabel").classList.toggle("active", !useFeet);
    document.getElementById("feetLabel").classList.toggle("active", useFeet);
  });

});

function calculateBMI(weight, heightCm) {
  const h = heightCm / 100;
  return (weight / (h * h)).toFixed(1);
}

function generatePlan() {

  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;

  let height;

  if (useFeet) {
    const feet = document.getElementById("heightFeet").value;
    height = feet * 30.48;
  } else {
    height = document.getElementById("heightCm").value;
  }

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

function downloadPlan() {
  const blob = new Blob([latestPlan], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "DietPlan.txt";
  link.click();
}
