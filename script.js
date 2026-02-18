function login() {
  const name = document.getElementById("username").value;
  localStorage.setItem("user", name);
  document.getElementById("loginBox").style.display = "none";
}

window.onload = function() {

  // Hide login if user exists
  if (localStorage.getItem("user")) {
    document.getElementById("loginBox").style.display = "none";
  }

  // Restore dark mode safely
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }

};


function toggleHeightInputs() {
  const unit = document.getElementById("heightUnit").value;

  if (unit === "cm") {
    document.getElementById("cmInput").style.display = "block";
    document.getElementById("ftInput").style.display = "none";
  } else {
    document.getElementById("cmInput").style.display = "none";
    document.getElementById("ftInput").style.display = "flex";
  }
}

function calculateBMI(weight, heightCm) {
  const heightM = heightCm / 100;
  return (weight / (heightM * heightM)).toFixed(1);
}

function generate() {
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const goal = document.getElementById("goal").value;
  const food = document.getElementById("food").value;
  const duration = document.getElementById("duration").value;

  let height;
  const unit = document.getElementById("heightUnit").value;

  if (unit === "cm") {
    height = document.getElementById("heightCm").value;
  } else {
    const ft = document.getElementById("heightFt").value || 0;
    const inch = document.getElementById("heightIn").value || 0;
    height = (ft * 30.48) + (inch * 2.54);
  }

  const bmi = calculateBMI(weight, height);

  document.getElementById("result").innerText =
    "Your BMI: " + bmi + "\nGenerating plan...\n\n";

  fetch("https://ai-diet-planner-3zig.onrender.com/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      age,
      weight,
      height,
      goal,
      dietType: food,
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
      "Your BMI: " + bmi + "\n\n" + data.plan +
      "\n\nRemaining AI plans today: " + data.remaining;

    localStorage.setItem("lastWeight", weight);
  })
  .catch(() => {
    document.getElementById("result").innerText =
      "Unable to connect. Try again.";
  });
}

function downloadPDF() {
  const content = document.getElementById("result").innerText;

  if (!content) {
    alert("Generate a plan first!");
    return;
  }

  const blob = new Blob([content], { type: "application/pdf" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "AI_Diet_Plan.pdf";
  link.click();
}
functionfunction toggleDarkMode() {
  const isDark = document.body.classList.toggle("dark-mode");
  localStorage.setItem("theme", isDark ? "dark" : "light");
}








