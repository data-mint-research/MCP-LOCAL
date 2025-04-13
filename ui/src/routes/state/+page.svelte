<script>
  import { onMount } from 'svelte';
  import { getState } from '$lib/api';
  
  // Available memory areas
  const memoryAreas = [
    { id: 'memory', name: 'Memory' },
    { id: 'policy', name: 'Policy' },
    { id: 'context', name: 'Context' },
    { id: 'status', name: 'Status' }
  ];
  
  let selectedArea = memoryAreas[0].id;
  let stateData = null;
  let loading = false;
  let error = null;
  
  // Fetch state data for selected area
  async function fetchStateData() {
    if (!selectedArea) return;
    
    try {
      loading = true;
      error = null;
      stateData = await getState(selectedArea);
    } catch (err) {
      error = `Failed to load state data: ${err.message}`;
      console.error(error);
      stateData = null;
    } finally {
      loading = false;
    }
  }
  
  // Handle area selection change
  function handleAreaChange() {
    fetchStateData();
  }
  
  // Format JSON data for display
  function formatJson(data) {
    return JSON.stringify(data, null, 2);
  }
  
  onMount(() => {
    fetchStateData();
  });
</script>

<svelte:head>
  <title>MCP-LOCAL System State</title>
</svelte:head>

<div class="state-view">
  <h1>System State</h1>
  
  <div class="controls">
    <div class="area-selector">
      <label for="area-select">Select Memory Area:</label>
      <select 
        id="area-select" 
        bind:value={selectedArea} 
        on:change={handleAreaChange}
        disabled={loading}
      >
        {#each memoryAreas as area}
          <option value={area.id}>{area.name}</option>
        {/each}
      </select>
    </div>
    
    <button on:click={fetchStateData} disabled={loading || !selectedArea}>
      {loading ? 'Loading...' : 'Refresh'}
    </button>
  </div>
  
  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}
  
  <div class="state-container">
    {#if loading}
      <div class="loading">Loading state data...</div>
    {:else if !stateData}
      <div class="empty-state">
        No state data available for {selectedArea}
      </div>
    {:else}
      <div class="state-content">
        <div class="state-header">
          <h3>{getSelectedAreaName(selectedArea)}</h3>
          <div class="state-meta">
            {#if stateData.timestamp}
              <span class="timestamp">Last updated: {new Date(stateData.timestamp).toLocaleString()}</span>
            {/if}
          </div>
        </div>
        
        <div class="json-viewer">
          <pre>{formatJson(stateData)}</pre>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .state-view {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 2rem);
  }
  
  h1 {
    margin-bottom: 1rem;
    color: #333;
  }
  
  .controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    align-items: center;
  }
  
  .area-selector {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  select {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ddd;
    min-width: 200px;
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
  
  button:hover:not(:disabled) {
    background: #1565c0;
  }
  
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .error-message {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
  }
  
  .state-container {
    flex: 1;
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  
  .loading, .empty-state {
    padding: 2rem;
    text-align: center;
    color: #666;
    background: #f5f5f5;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .state-content {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .state-header {
    padding: 1rem;
    background: #f5f5f5;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .state-header h3 {
    margin: 0;
    color: #333;
  }
  
  .state-meta {
    font-size: 0.8rem;
    color: #666;
  }
  
  .json-viewer {
    flex: 1;
    overflow: auto;
    padding: 1rem;
    background: #fafafa;
  }
  
  pre {
    margin: 0;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #333;
    white-space: pre-wrap;
    word-break: break-word;
  }
</style>

<script context="module">
  // Helper function to get the display name for a memory area
  function getSelectedAreaName(areaId) {
    const areaMap = {
      'memory': 'Memory Store',
      'policy': 'Policy Configuration',
      'context': 'Context Data',
      'status': 'System Status'
    };
    
    return areaMap[areaId] || areaId;
  }
</script>