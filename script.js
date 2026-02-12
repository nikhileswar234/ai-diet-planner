const backendURL = "https://ai-diet-planner-otbr.onrender.com/generate";

function calculateBMI(weight, heightCm) {
  const heightM = heightCm / 100;
  const bmi = weight / (heightM * heightM);
  return bmi.toFixed(1);
}

function login() {
  const name = document.getElementById("username").value;
  localStorage.setItem("user", name);
  document.getElementById("loginBox").style.display = "none";
}

window.onload = function() {
  if (localStorage.getItem("user")) {
    document.getElementById("loginBox").style.display = "none";
  }

  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark");
  }
};

document.getElementById("darkToggle").addEventListener("click", function() {
  document.body.classList.toggle("dark");

  const isDark = document.body.classList.contains("dark");
  localStorage.setItem("darkMode", isDark);
});

function generatePlan() {
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const height = document.getElementById("height").value;
  const goal = document.getElementById("goal").value;
  const dietType = document.getElementById("dietType").value;
  const duration = document.getElementById("duration").value;

  const bmi = calculateBMI(weight, height);

  document.getElementById("result").innerText =
    "Your BMI: " + bmi + "\nGenerating plan...\n\n";

  fetch(backendURL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      age,
      weight,
      height,
      goal,
      dietType,
      duration
    })
  })
  .then(res => res.json())
  .then(data => {

    if (data.limit) {
      document.getElementById("result").innerText = data.message;
      return;
    }

    document.getElementById("result").innerText =
      "Your BMI: " + bmi + "\n\n" + data.plan;

    if (data.remaining !== undefined) {
      document.getElementById("result").innerText +=
        "\n\nRemaining AI plans today: " + data.remaining;
    }
  })
  .catch(() => {
    document.getElementById("result").innerText =
      "❌ Unable to connect to server. Try again.";
  });
}
