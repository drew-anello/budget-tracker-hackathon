<script lang="ts">
  import { onMount } from 'svelte';
  import BudgetChart from './BudgetChart.svelte';

  let analysis: string = '';
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
      // Extract the text from the analysis response
      analysis = data.analysis[0].text;
    } catch (e) {
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
        <h2>Budget Optimization Suggestions</h2>
        <div class="analysis-content">
          {@html analysis}
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
    margin-bottom: 1rem;
  }

  .analysis-content {
    background: white;
    padding: 1.5rem;
    border-radius: 4px;
    color: #333;
    line-height: 1.6;
  }

  .analysis-content h1,
  .analysis-content h2,
  .analysis-content h3 {
    color: #333;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }

  .analysis-content ul,
  .analysis-content ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
  }

  .analysis-content li {
    margin-bottom: 0.5rem;
  }

  .error {
    color: #ff3e00;
    margin-top: 0.5rem;
  }
</style> 