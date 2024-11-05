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


const data1 = JSON.parse(document.getElementById('data1').textContent);
const ctx3 = document.getElementById('myChart3');

new Chart(ctx3, {
type: 'line',
data: {
  labels: data1.labels,
  datasets: [{
    label: 'Рейтинг книг',
    data: data1.total_rate/data1.rate_counts,
    data: new Array(data1.total_rate.length).fill(0).map((_,i)=>Math.round(data1.total_rate[i]/(data1.rate_counts[i]||1))),
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