<script>
  import { onMount, onDestroy } from 'svelte';
  import { getStatus } from '$lib/api';
  
  let statusData = [];
  let loading = true;
  let error = null;
  let refreshInterval;
  
  // Fetch status data
  async function fetchStatusData() {
    try {
      loading = true;
      statusData = await getStatus();
      error = null;
    } catch (err) {
      error = `Failed to load status data: ${err.message}`;
      console.error(error);
    } finally {
      loading = false;
    }
  }
  
  // Set up polling for status updates (every 5 seconds)
  onMount(() => {
    fetchStatusData();
    refreshInterval = setInterval(fetchStatusData, 5000);
  });
  
  onDestroy(() => {
    if (refreshInterval) clearInterval(refreshInterval);
  });
</script>

<svelte:head>
  <title>MCP-LOCAL Dashboard</title>
</svelte:head>

<div class="dashboard">
  <h1>MCP-LOCAL Dashboard</h1>
  
  {#if loading && !statusData.length}
    <div class="loading">Loading status data...</div>
  {:else if error}
    <div class="error">
      <p>{error}</p>
      <button on:click={fetchStatusData}>Retry</button>
    </div>
  {:else}
    <div class="status-grid">
      {#each statusData as unit}
        <div class="status-card">
          <div class="card-header">
            <h3>{unit.name}</h3>
            <span class="status-badge {unit.health === 'healthy' ? 'healthy' : 'unhealthy'}">
              {unit.health}
            </span>
          </div>
          <div class="card-body">
            <p><strong>Port:</strong> {unit.port || 'N/A'}</p>
            <p><strong>Type:</strong> {unit.type || 'N/A'}</p>
            {#if unit.activity}
              <p><strong>Activity:</strong> {unit.activity}</p>
            {/if}
            <p><strong>Last Updated:</strong> {new Date(unit.timestamp).toLocaleString()}</p>
          </div>
        </div>
      {/each}
      
      {#if statusData.length === 0}
        <div class="no-data">No active units found</div>
      {/if}
    </div>
    
    <div class="controls">
      <button on:click={fetchStatusData}>Refresh</button>
    </div>
  {/if}
</div>

<style>
  .dashboard {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h1 {
    margin-bottom: 1.5rem;
    color: #333;
  }
  
  .loading, .error, .no-data {
    padding: 2rem;
    text-align: center;
    background: #f5f5f5;
    border-radius: 4px;
    margin: 1rem 0;
  }
  
  .error {
    background: #fff0f0;
    color: #d32f2f;
  }
  
  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .status-card {
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }
  
  .card-header {
    padding: 1rem;
    background: #f5f5f5;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .card-header h3 {
    margin: 0;
    font-size: 1.2rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .card-body p {
    margin: 0.5rem 0;
  }
  
  .status-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
  }
  
  .status-badge.healthy {
    background: #e8f5e9;
    color: #2e7d32;
  }
  
  .status-badge.unhealthy {
    background: #ffebee;
    color: #c62828;
  }
  
  .controls {
    margin-top: 1rem;
    display: flex;
    justify-content: flex-end;
  }
  
  button {
    background: #1976d2;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  button:hover {
    background: #1565c0;
  }
</style>