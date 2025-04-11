<script lang="ts">
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';

  export let data: {
    income: number;
    expenses: Array<{
      category: string;
      subcategory: string;
      amount: number;
      frequency: string;
      essential: boolean;
    }>;
  };

  let chartCanvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  // Register all Chart.js components
  Chart.register(...registerables);

  const colors = [
    'rgba(255, 99, 132, 0.5)',
    'rgba(54, 162, 235, 0.5)',
    'rgba(255, 206, 86, 0.5)',
    'rgba(75, 192, 192, 0.5)',
    'rgba(153, 102, 255, 0.5)',
    'rgba(255, 159, 64, 0.5)',
    'rgba(199, 199, 199, 0.5)',
    'rgba(83, 102, 255, 0.5)',
    'rgba(40, 159, 64, 0.5)',
    'rgba(210, 199, 199, 0.5)'
  ];

  function createChart() {
    if (!chartCanvas) return;
    
    if (chart) {
      chart.destroy();
    }

    // Group expenses by category
    const categories = new Map<string, number>();
    data.expenses.forEach(expense => {
      const current = categories.get(expense.category) || 0;
      categories.set(expense.category, current + expense.amount);
    });

    const labels = Array.from(categories.keys());
    const values = Array.from(categories.values());

    const ctx = chartCanvas.getContext('2d');
    if (!ctx) return;

    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Monthly Expenses by Category',
          data: values,
          backgroundColor: colors.slice(0, labels.length),
          borderColor: colors.slice(0, labels.length).map(color => color.replace('0.5', '1')),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.raw as number;
                return `$${value.toLocaleString()}`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toLocaleString();
              }
            }
          }
        }
      }
    });
  }

  $: if (data && chartCanvas) {
    createChart();
  }

  onMount(() => {
    if (data && chartCanvas) {
      createChart();
    }
  });
</script>

<div class="chart-container">
  <canvas bind:this={chartCanvas}></canvas>
</div>

<style>
  .chart-container {
    position: relative;
    height: 100%;
    width: 100%;
  }
</style> 