function generate() {

    const age = document.getElementById("age").value;
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;
    const goal = document.getElementById("goal").value;
    const food = document.getElementById("food").value;
    const duration = document.getElementById("duration").value;

    const resultDiv = document.getElementById("result");

    if (!age || !weight || !height) {
        resultDiv.innerHTML = "⚠ Please fill all details.";
        return;
    }

    resultDiv.innerHTML = "⏳ Generating your AI diet plan... (Please wait 20-40 seconds if server is sleeping)";

    fetch("https://ai-diet-planner-zw7x.onrender.com/generate-plan", {
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
    })
    .then(response => response.json())
    .then(data => {
        if (data.plan) {
            resultDiv.innerHTML = `
                <h2>Your Personalized Diet Plan 🥗</h2>
                <pre style="white-space: pre-wrap;">${data.plan}</pre>
            `;
        } else if (data.error) {
            resultDiv.innerHTML = "❌ Error: " + data.error;
        } else {
            resultDiv.innerHTML = "⚠ Something went wrong.";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        resultDiv.innerHTML = "❌ Server error. Please try again.";
    });
}
