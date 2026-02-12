function toggleDark() {
  document.body.classList.toggle("dark");
}

// Toggle height inputs
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

function generate() {
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const unit = document.getElementById("heightUnit").value;
  const goal = document.getElementById("goal").value;
  const food = document.getElementById("food").value;
  const duration = document.getElementById("duration").value;

  let height;

  if (unit === "cm") {
    height = document.getElementById("heightCm").value;
  } else {
    const feet = document.getElementById("heightFt").value || 0;
    const inches = document.getElementById("heightIn").value || 0;

    // Convert to cm
    height = (feet * 30.48) + (inches * 2.54);
  }

  document.getElementById("result").innerText = "Generating plan... ⏳";

  fetch("https://ai-diet-planner-otbr.onrender.com/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
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
    if (data.plan) {
      document.getElementById("result").innerText = data.plan;
    } else {
      document.getElementById("result").innerText = "❌ Error generating plan.";
    }
  })
  .catch(error => {
    document.getElementById("result").innerText =
      "❌ Unable to connect to server. Try again.";
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
