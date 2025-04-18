const form = document.getElementById("expense-form");
const expenseList = document.getElementById("expense-list");
const summary = document.getElementById("summary");
const categorySummary = document.getElementById("category-summary");
const themeToggle = document.getElementById("themeToggle");
const chartCanvas = document.getElementById("expenseChart");
let chart;

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const amount = parseFloat(document.getElementById("amount").value);
  const category = document.getElementById("category").value;
  const description = document.getElementById("description").value;
  const date = new Date().toISOString().split("T")[0];

  const expense = { date, amount, category, description };

  const expenses = JSON.parse(localStorage.getItem("expenses")) || [];
  expenses.push(expense);
  localStorage.setItem("expenses", JSON.stringify(expenses));

  form.reset();
  loadExpenses();
});

function deleteExpense(index) {
  let expenses = JSON.parse(localStorage.getItem("expenses")) || [];
  expenses.splice(index, 1);
  localStorage.setItem("expenses", JSON.stringify(expenses));
  loadExpenses();
}

function loadExpenses() {
  const expenses = JSON.parse(localStorage.getItem("expenses")) || [];
  const thisMonth = new Date().toISOString().slice(0, 7);
  let total = 0;
  const categoryTotals = {};
  expenseList.innerHTML = "";
  categorySummary.innerHTML = "";

  expenses.forEach((exp, index) => {
    if (exp.date.startsWith(thisMonth)) {
      total += exp.amount;
      categoryTotals[exp.category] = (categoryTotals[exp.category] || 0) + exp.amount;
    }

    const li = document.createElement("li");
    li.innerHTML = `
      ${exp.date} - ₹${exp.amount} (${exp.category}) - ${exp.description}
      <button onclick="deleteExpense(${index})">❌</button>
    `;
    expenseList.appendChild(li);
  });

  summary.textContent = `Total This Month: ₹${total.toFixed(2)}`;

  for (let cat in categoryTotals) {
    const li = document.createElement("li");
    li.textContent = `${cat}: ₹${categoryTotals[cat].toFixed(2)}`;
    categorySummary.appendChild(li);
  }

  renderChart(categoryTotals);
}

function renderChart(data) {
  const labels = Object.keys(data);
  const values = Object.values(data);
  const colors = ["#800000", "#8B4513", "#008080", "#FF7F50", "#4682B4"];

  if (chart) chart.destroy();
  chart = new Chart(chartCanvas, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        label: "Expenses",
        data: values,
        backgroundColor: colors
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom"
        }
      }
    }
  });
}

// Theme toggle
themeToggle.addEventListener("change", () => {
  document.body.classList.toggle("dark");
});

loadExpenses();
