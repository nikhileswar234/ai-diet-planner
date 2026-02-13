const backendURL = " https://ai-diet-planner-3zig.onrender.com";

let useFeet = false;
let latestPlan = "";

document.getElementById("cmBtn").onclick = function() {
  useFeet = false;
  document.getElementById("heightCm").style.display = "block";
  document.getElementById("feetInputs").style.display = "none";
  this.classList.add("active");
  document.getElementById("ftBtn").classList.remove("active");
};

document.getElementById("ftBtn").onclick = function() {
  useFeet = true;
  document.getElementById("heightCm").style.display = "none";
  document.getElementById("feetInputs").style.display = "block";
  this.classList.add("active");
  document.getElementById("cmBtn").classList.remove("active");
};

function generatePlan() {

  const age = age.value;
  const weight = weight.value;

  let height;

  if (useFeet) {
    const feet = document.getElementById("heightFeet").value;
    const inches = document.getElementById("heightInches").value;
    height = (feet * 30.48) + (inches * 2.54);
  } else {
    height = document.getElementById("heightCm").value;
  }

  const goal = goal.value;
  const dietType = dietType.value;
  const duration = duration.value;

  fetch(`${backendURL}/generate`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({age, weight, height, goal, dietType, duration})
  })
  .then(res => res.json())
  .then(data => {

    if (data.limit) {
      result.innerText = data.message;
      return;
    }

    latestPlan = data.plan;
    result.innerText = data.plan;
    downloadBtn.style.display = "block";
  });
}

function downloadPDF() {

  fetch(`${backendURL}/download`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({content: latestPlan})
  })
  .then(res => res.blob())
  .then(blob => {
    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "DietPlan.pdf";
    link.click();
  });
}

