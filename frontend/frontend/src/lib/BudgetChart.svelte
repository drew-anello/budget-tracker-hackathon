<script lang="ts">
  import { onMount } from 'svelte';
  import Papa from 'papaparse';
  import { Chart, registerables } from 'chart.js';

  let chartCanvas: HTMLCanvasElement;
  let chart: Chart | null = null;
  let chartType: 'pie' | 'bar' = 'pie';

  // Register all Chart.js components
  Chart.register(...registerables);

  const sampleData = `category,amount
Housing,1200
Food,600
Transportation,300
Utilities,200
Entertainment,150
Healthcare,250
Shopping,400
Education,350
Personal Care,100
Savings,500`;

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

  function createChart(data: { labels: string[], values: number[] }) {
    if (chart) {
      chart.destroy();
    }

    const isPie = chartType === 'pie';
    
    chart = new Chart(chartCanvas, {
      type: chartType,
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Spending',
          data: data.values,
          backgroundColor: isPie ? colors : 'rgba(54, 162, 235, 0.5)',
          borderColor: isPie ? colors.map(color => color.replace('0.5', '1')) : 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right' as const,
            display: isPie
          },
          title: {
            display: true,
            text: 'Budget Analysis'
          }
        }
      }
    });
  }

  function processData(data: string) {
    Papa.parse(data, {
      header: true,
      complete: (results) => {
        console.log('Parsed CSV data:', results);
        const categories = new Map<string, number>();

        results.data.forEach((row: any) => {
          if (row.category && row.amount) {
            const currentAmount = categories.get(row.category) || 0;
            categories.set(row.category, currentAmount + Number(row.amount));
          }
        });

        console.log('Processed categories:', categories);
        
        createChart({
          labels: Array.from(categories.keys()),
          values: Array.from(categories.values())
        });
      },
      error: (error) => {
        console.error('Error parsing CSV:', error);
      }
    });
  }

  function handleFileUpload(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const data = e.target?.result as string;
      processData(data);
    };
    reader.readAsText(file);
  }

  function toggleChartType() {
    chartType = chartType === 'pie' ? 'bar' : 'pie';
    if (chart) {
      const currentData = {
        labels: chart.data.labels as string[],
        values: chart.data.datasets[0].data as number[]
      };
      createChart(currentData);
    }
  }

  onMount(() => {
    console.log('BudgetChart component mounted');
    // Load sample data automatically
    processData(sampleData);
  });
</script>

<div class="budget-container">
  <div class="upload-section">
    <h2>Budget Analysis</h2>
    <p>Sample budget data is displayed below. You can also upload your own CSV file:</p>
    <div class="controls">
      <input
        type="file"
        accept=".csv"
        on:change={handleFileUpload}
      />
      <button on:click={toggleChartType}>
        Switch to {chartType === 'pie' ? 'Bar' : 'Pie'} Chart
      </button>
    </div>
  </div>

  <div class="chart-section">
    <canvas bind:this={chartCanvas}></canvas>
  </div>
</div>

<style>
  .budget-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  .upload-section {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .chart-section {
    min-height: 400px;
    padding: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .controls {
    display: flex;
    gap: 1rem;
    align-items: center;
    margin-top: 1rem;
  }

  input[type="file"] {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    flex: 1;
  }

  button {
    padding: 0.5rem 1rem;
    background-color: #646cff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #535bf2;
  }

  canvas {
    width: 100% !important;
    height: 400px !important;
  }
</style> 