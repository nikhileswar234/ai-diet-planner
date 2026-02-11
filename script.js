function generate() {
  const data = {
    age: +age.value,
    weight: +weight.value,
    height: +height.value,
    goal: goal.value,
    food: food.value,
    duration: duration.value
  };

  fetch("https://ai-diet-planner-zw7x.onrender.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(data => {
    let html = `<h3>Daily Calories: ${data.calories}</h3>`;

    for (let section in data.plan) {
      html += `<h2>${section}</h2>`;
      for (let week in data.plan[section]) {
        html += `<div class="week"><h4>${week}</h4>`;
        const days = data.plan[section][week];
        for (let day in days) {
          html += `<b>${day}</b><br>`;
          for (let meal in days[day]) {
            html += `${meal}: ${days[day][meal]}<br>`;
          }
          html += "<hr>";
        }
        html += "</div>";
      }
    }

    result.innerHTML = html;
  });
}


