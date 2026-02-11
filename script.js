// Main generate function
async function generate() {
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value;
  const height = document.getElementById("height").value;
  const goal = document.getElementById("goal").value;
  const food = document.getElementById("food").value;
  const duration = document.getElementById("duration").value;
  const resultDiv = document.getElementById("result");

  // Validate input
  if (!age || !weight || !height) {
    resultDiv.innerHTML = "⚠️ Please fill all required fields.";
    return;
  }

  resultDiv.innerHTML = "⏳ Calculating... Please wait.";

  // ===== BMI Calculation =====
  const heightMeters = height / 100;
  const bmi = (weight / (heightMeters * heightMeters)).toFixed(1);

  // ===== BMR Calculation (Mifflin-St Jeor) =====
  const bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5;

  let targetCalories;
  if (goal === "loss") targetCalories = bmr - 400;
  if (goal === "gain") targetCalories = bmr + 400;
  if (goal === "muscle") targetCalories = bmr + 300;
  if (!targetCalories) targetCalories = bmr;

  // Show user stats first
  resultDiv.innerHTML = `
    <div class="stat-box">
      <strong>Your Stats:</strong><br>
      BMI: ${bmi} kg/m²<br>
      Daily Target Calories: ${Math.round(targetCalories)} kcal
    </div>
    <p>⏳ Generating AI diet plan from server... please wait.</p>
  `;

  try {
    const response = await fetch("https://ai-diet-planner-zw7x.onrender.com/generate", {

      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        age: age,
        weight: weight,
        height: height,
        goal: goal,
        dietType: food,
        duration: duration
      })
    });

    const data = await response.json();

    if (data.plan || data.result) {
      // Some variants of backend return data.plan or data.result
      const planText = data.plan || data.result || "";
      resultDiv.innerHTML += `<pre style="white-space: pre-wrap; margin-top:10px;">${planText}</pre>`;
    } else if (data.error) {
      resultDiv.innerHTML = "❌ Server error: " + data.error;
    } else {
      resultDiv.innerHTML = "⚠ Unexpected response from server";
    }

  } catch (error) {
    console.error("Error fetching plan:", error);
    resultDiv.innerHTML = "❌ Unable to connect to server. Try again.";
  }
}

// ===== Dark Mode Toggle =====
function toggleDark() {
  document.body.classList.toggle("dark");
}

// ===== Simple PDF Download =====
function downloadPDF() {
  const content = document.getElementById("result").innerText;
  if (!content) {
    alert("Nothing to download yet!");
    return;
  }
  const blob = new Blob([content], { type: "text/plain" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "Diet_Plan.txt";
  link.click();
}

