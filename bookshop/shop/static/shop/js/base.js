const data = JSON.parse(document.getElementById('data').textContent);
const ctx1 = document.getElementById('myChart1');

new Chart(ctx1, {
type: 'line',
data: {
  labels: data.labels,
  datasets: [{
    label: 'Кол-во заказов',
    data: data.order_counts,
    borderWidth: 1
  }]
},
options: {
  scales: {
    y: {
      beginAtZero: true
    }
  }
}
});

const ctx2 = document.getElementById('myChart2');

new Chart(ctx2, {
type: 'line',
data: {
  labels: data.labels,
  datasets: [{
    label: 'Сумма по заказам',
    data: data.total_amounts,
    borderWidth: 1
  }]
},
options: {
  scales: {
    y: {
      beginAtZero: true
    }
  }
}
});