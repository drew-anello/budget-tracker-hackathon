<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let data: any;
  let chart: Chart | null = null;
  let chartContainer: HTMLCanvasElement;

  onMount(() => {
    if (!data || !chartContainer) return;

    // Calculate total expenses by category
    const categories = new Map<string, number>();
    data.expenses.forEach((expense: any) => {
      const current = categories.get(expense.category) || 0;
      categories.set(expense.category, current + expense.amount);
    });

    // Sort categories by amount (descending)
    const sortedCategories = Array.from(categories.entries())
      .sort((a, b) => b[1] - a[1]);

    const ctx = chartContainer.getContext('2d');
    if (!ctx) return;

    // Destroy existing chart if it exists
    if (chart) {
      chart.destroy();
    }

    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sortedCategories.map(([category]) => category),
        datasets: [{
          label: 'Monthly Expenses',
          data: sortedCategories.map(([_, amount]) => amount),
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
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
              label: (context) => {
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
              callback: (value) => `$${value.toLocaleString()}`
            }
          },
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 45
            }
          }
        }
      }
    });

    return () => {
      if (chart) {
        chart.destroy();
      }
    };
  });
</script>

<div class="chart-container">
  <canvas bind:this={chartContainer}></canvas>
</div>

<style>
  .chart-container {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 300px;
    margin-top: 1rem;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style> 