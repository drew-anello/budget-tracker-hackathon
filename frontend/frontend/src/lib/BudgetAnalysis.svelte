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
    essential_expenses: Array<{
      category: string;
      amount: string;
      percentage: string;
    }>;
    non_essential_expenses: Array<{
      category: string;
      amount: string;
      percentage: string;
    }>;
    recommendations: Array<{
      category: string;
      suggestions: string[];
    }>;
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
      // The analysis is already parsed JSON
      analysis = data.analysis;
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
        <h2>Budget Analysis</h2>
        
        <div class="overview-section">
          <h3>Overview</h3>
          <div class="metrics-grid">
            <div class="metric">
              <span class="label">Monthly Income</span>
              <span class="value">{analysis.overview.monthly_income}</span>
            </div>
            <div class="metric">
              <span class="label">Total Expenses</span>
              <span class="value">{analysis.overview.total_expenses}</span>
            </div>
            <div class="metric">
              <span class="label">Monthly Surplus</span>
              <span class="value">{analysis.overview.monthly_surplus}</span>
            </div>
            <div class="metric">
              <span class="label">Surplus Percentage</span>
              <span class="value">{analysis.overview.surplus_percentage}</span>
            </div>
          </div>
        </div>

        <div class="expenses-section">
          <div class="expense-type">
            <h3>Essential Expenses</h3>
            <ul>
              {#each analysis.essential_expenses as expense}
                <li>
                  <span class="category">{expense.category}</span>
                  <span class="amount">{expense.amount}</span>
                  <span class="percentage">{expense.percentage}</span>
                </li>
              {/each}
            </ul>
          </div>

          <div class="expense-type">
            <h3>Non-Essential Expenses</h3>
            <ul>
              {#each analysis.non_essential_expenses as expense}
                <li>
                  <span class="category">{expense.category}</span>
                  <span class="amount">{expense.amount}</span>
                  <span class="percentage">{expense.percentage}</span>
                </li>
              {/each}
            </ul>
          </div>
        </div>

        <div class="recommendations-section">
          <h3>Recommendations</h3>
          {#each analysis.recommendations as category}
            <div class="recommendation-category">
              <h4>{category.category}</h4>
              <ul>
                {#each category.suggestions as suggestion}
                  <li>{suggestion}</li>
                {/each}
              </ul>
            </div>
          {/each}
        </div>

        <div class="summary-section">
          <h3>Summary</h3>
          <p>{analysis.summary}</p>
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

  .analysis-section h3 {
    color: #333;
    margin: 1.5rem 0 1rem;
    font-size: 1.2rem;
  }

  .analysis-section h4 {
    color: #333;
    margin: 1rem 0 0.5rem;
    font-size: 1.1rem;
  }

  .metrics-grid {
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

  .expenses-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

  .expense-type ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .expense-type li {
    background: white;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .expense-type .category {
    font-weight: 500;
  }

  .expense-type .amount {
    color: #333;
    font-weight: bold;
  }

  .expense-type .percentage {
    color: #666;
    font-size: 0.9rem;
  }

  .recommendations-section {
    background: white;
    padding: 1.5rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
  }

  .recommendation-category {
    margin-bottom: 1rem;
  }

  .recommendation-category ul {
    list-style-type: disc;
    margin-left: 1.5rem;
    color: #333;
  }

  .recommendation-category li {
    margin-bottom: 0.5rem;
  }

  .summary-section {
    background: white;
    padding: 1.5rem;
    border-radius: 4px;
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