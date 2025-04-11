<script lang="ts">
  import BudgetChart from './lib/BudgetChart.svelte';
</script>

<main>
  <h1>Budget Analysis Tool</h1>
  <BudgetChart />
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 1200px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 2.5em;
    font-weight: 100;
    margin-bottom: 2rem;
  }
</style>
