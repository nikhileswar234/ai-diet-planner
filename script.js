document.addEventListener("DOMContentLoaded", function () {

    const button = document.querySelector("button");
    const resultDiv = document.getElementById("result");

    button.addEventListener("click", function () {

        const age = document.getElementById("age").value;
        const weight = document.getElementById("weight").value;
        const height = document.getElementById("height").value;
        const goal = document.getElementById("goal").value;
        const dietType = document.getElementById("dietType").value;
        const duration = document.getElementById("duration").value;

        if (!age || !weight || !height) {
            resultDiv.innerHTML = "⚠ Please fill all fields properly.";
            return;
        }

        resultDiv.innerHTML = "⏳ Generating your AI diet plan... Please wait (first request may take 30 sec)";

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
                dietType: dietType,
                duration: duration
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.plan) {
                resultDiv.innerHTML = `
                    <h2>Your Personalized Diet Plan 🥗</h2>
                    <pre style="white-space: pre-wrap; font-family: Arial;">
${data.plan}
                    </pre>
                `;
            } else if (data.error) {
                resultDiv.innerHTML = "❌ Error: " + data.error;
            } else {
                resultDiv.innerHTML = "⚠ Something went wrong.";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            resultDiv.innerHTML = "❌ Server not responding. Please try again.";
        });

    });

});
