const cmBtn = document.getElementById("cmBtn");
const ftBtn = document.getElementById("ftBtn");
const heightCmInput = document.getElementById("heightCm");
const feetInputs = document.getElementById("feetInputs");

cmBtn.addEventListener("click", () => {
  cmBtn.classList.add("active");
  ftBtn.classList.remove("active");
  heightCmInput.style.display = "block";
  feetInputs.style.display = "none";
});

ftBtn.addEventListener("click", () => {
  ftBtn.classList.add("active");
  cmBtn.classList.remove("active");
  heightCmInput.style.display = "none";
  feetInputs.style.display = "block";
});

async function generatePlan() {

  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const goal = document.getElementById("goal").value;
  const diet = document.getElementById("dietType").value;
  const duration = document.getElementById("duration").value;
  const resultDiv = document.getElementById("result");
  const downloadBtn = document.getElementById("downloadBtn");

  let height;

  if (heightCmInput.style.display !== "none") {
    height = document.getElementById("heightCm").value;
  } else {
    const feet = document.getElementById("heightFeet").value;
    const inches = document.getElementById("heightInches").value;
    height = (feet * 30.48 + inches * 2.54).toFixed(1);
  }

  if (!age || !weight || !height) {
    alert("Please fill all fields.");
    return;
  }

  resultDiv.innerHTML = "Generating plan...";
  downloadBtn.style.display = "none";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        age,
        weight,
        height,
        goal,
        diet,
        duration
      })
    });

    const data = await response.json();

    if (data.error) {
      resultDiv.innerHTML = "Error: " + data.error;
      return;
    }

    resultDiv.innerHTML = data.plan.replace(/\n/g, "<br>");
    downloadBtn.style.display = "block";

  } catch (error) {
    resultDiv.innerHTML = "Something went wrong.";
  }
}

function downloadPDF() {
  const content = document.getElementById("result").innerText;
  const blob = new Blob([content], { type: "text/plain" });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "AI_Diet_Plan.txt";
  a.click();

  window.URL.revokeObjectURL(url);
}
