<script lang="ts">
  import { onMount } from 'svelte';
  import BudgetChart from './BudgetChart.svelte';

  interface AnalysisData {
    overview: {
      monthly_income: string;
      total_expenses: string;
      monthly_surplus: string;
      surplus_percentage: string;
    };
    summary: string;
  }

  let analysis: AnalysisData | null = null;
  let testData: any = null;
  let loading: boolean = false;
  let error: string = '';

  async function loadData() {
    loading = true;
    error = '';
    
    try {
      // Get the test data
      const testDataResponse = await fetch('http://localhost:8000/test-data');
      if (!testDataResponse.ok) {
        throw new Error('Failed to get test data');
      }
      testData = await testDataResponse.json();

      // Get the analysis
      const analysisResponse = await fetch('http://localhost:8000/test-analyze');
      if (!analysisResponse.ok) {
        throw new Error('Failed to get analysis');
      }

      const data = await analysisResponse.json();
      console.log('Analysis response:', data); // Debug log
      
      if (data.analysis) {
        analysis = data.analysis;
      } else {
        console.error('Unexpected response structure:', data);
        error = 'Unexpected response format';
      }
    } catch (e) {
      console.error('Error loading data:', e);
      error = e instanceof Error ? e.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadData();
  });
</script>

<div class="budget-analysis">
  {#if loading}
    <p>Loading budget analysis...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <div class="chart-section">
      <h2>Budget Breakdown</h2>
      {#if testData}
        <BudgetChart data={testData} />
      {/if}
    </div>

    {#if analysis}
      <div class="analysis-section">
        <h2>Budget Analysis</h2>
        
        <div class="metrics-section">
          <div class="metric">
            <span class="label">Monthly Income</span>
            <span class="value">{analysis.overview?.income || analysis.overview?.monthly_income || '$0'}</span>
          </div>
          <div class="metric">
            <span class="label">Total Expenses</span>
            <span class="value">{analysis.overview.total_expenses || 'N/A'}</span>
          </div>
        </div>

        <div class="summary-section">
          <h3>Summary</h3>
          <p>{analysis.summary || 'No summary available'}</p>
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .budget-analysis {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 1rem;
  }

  .chart-section {
    width: 100%;
    height: 400px;
    background: #f5f5f5;
    padding: 1.5rem;
    border-radius: 8px;
  }

  .chart-section h2 {
    color: #333;
    margin-bottom: 1rem;
    text-align: left;
  }

  .analysis-section {
    background: #f5f5f5;
    padding: 1.5rem;
    border-radius: 8px;
    text-align: left;
  }

  .analysis-section h2 {
    color: #333;
    margin-bottom: 1.5rem;
  }

  .metrics-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .metric {
    background: white;
    padding: 1rem;
    border-radius: 4px;
    text-align: center;
  }

  .metric .label {
    display: block;
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }

  .metric .value {
    display: block;
    color: #333;
    font-size: 1.2rem;
    font-weight: bold;
  }

  .summary-section {
    background: white;
    padding: 1.5rem;
    border-radius: 4px;
  }

  .summary-section h3 {
    color: #333;
    margin-bottom: 1rem;
  }

  .summary-section p {
    color: #333;
    line-height: 1.6;
  }

  .error {
    color: #ff3e00;
    margin-top: 0.5rem;
  }
</style> 