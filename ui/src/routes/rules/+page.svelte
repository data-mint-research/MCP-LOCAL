<script>
  import { onMount } from 'svelte';
  import { getRules, checkPolicy } from '$lib/api';
  
  let rulesData = null;
  let selectedPolicy = '';
  let policyCheckResult = null;
  let loading = {
    rules: false,
    check: false
  };
  let error = {
    rules: null,
    check: null
  };
  
  // Fetch rules overview
  async function fetchRules() {
    try {
      loading.rules = true;
      error.rules = null;
      rulesData = await getRules();
    } catch (err) {
      error.rules = `Failed to load rules: ${err.message}`;
      console.error(error.rules);
    } finally {
      loading.rules = false;
    }
  }
  
  // Check policy against rules
  async function handlePolicyCheck() {
    if (!selectedPolicy) return;
    
    try {
      loading.check = true;
      error.check = null;
      policyCheckResult = await checkPolicy(selectedPolicy);
    } catch (err) {
      error.check = `Failed to check policy: ${err.message}`;
      console.error(error.check);
      policyCheckResult = null;
    } finally {
      loading.check = false;
    }
  }
  
  onMount(() => {
    fetchRules();
  });
</script>

<svelte:head>
  <title>MCP-LOCAL Rules & Policies</title>
</svelte:head>

<div class="rules-view">
  <h1>Rules & Policies</h1>
  
  <div class="rules-container">
    <h2>System Rules</h2>
    
    {#if loading.rules}
      <div class="loading">Loading rules data...</div>
    {:else if error.rules}
      <div class="error-message">
        <p>{error.rules}</p>
        <button on:click={fetchRules}>Retry</button>
      </div>
    {:else if rulesData}
      <div class="rules-overview">
        <div class="rules-card">
          <h3>Active Rules</h3>
          <div class="rules-count">{rulesData.active_rules?.length || 0}</div>
          
          {#if rulesData.active_rules?.length > 0}
            <div class="rules-list">
              {#each rulesData.active_rules as rule}
                <div class="rule-item">
                  <div class="rule-name">{rule.name || 'Unnamed Rule'}</div>
                  <div class="rule-description">{rule.description || 'No description'}</div>
                  {#if rule.tags?.length > 0}
                    <div class="rule-tags">
                      {#each rule.tags as tag}
                        <span class="tag">{tag}</span>
                      {/each}
                    </div>
                  {/if}
                </div>
              {/each}
            </div>
          {/if}
        </div>
        
        <div class="rules-card">
          <h3>Policy Files</h3>
          {#if rulesData.policy_files?.length > 0}
            <div class="policy-files">
              {#each rulesData.policy_files as policy}
                <div class="policy-item">
                  <label>
                    <input 
                      type="radio" 
                      name="policy" 
                      value={policy} 
                      bind:group={selectedPolicy}
                    />
                    {policy}
                  </label>
                </div>
              {/each}
            </div>
            
            <button 
              on:click={handlePolicyCheck} 
              disabled={loading.check || !selectedPolicy}
              class="check-button"
            >
              {loading.check ? 'Checking...' : 'Check Selected Policy'}
            </button>
          {:else}
            <p>No policy files available</p>
          {/if}
        </div>
      </div>
      
      {#if error.check}
        <div class="error-message">
          {error.check}
        </div>
      {/if}
      
      {#if policyCheckResult}
        <div class="policy-check-result">
          <h3>Policy Check Results</h3>
          
          <div class="result-summary">
            <div class="result-status {policyCheckResult.valid ? 'valid' : 'invalid'}">
              {policyCheckResult.valid ? 'VALID' : 'INVALID'}
            </div>
            
            {#if policyCheckResult.message}
              <div class="result-message">{policyCheckResult.message}</div>
            {/if}
          </div>
          
          {#if policyCheckResult.violations?.length > 0}
            <div class="violations">
              <h4>Violations ({policyCheckResult.violations.length})</h4>
              
              <div class="violations-list">
                {#each policyCheckResult.violations as violation}
                  <div class="violation-item">
                    <div class="violation-rule">{violation.rule || 'Unknown Rule'}</div>
                    <div class="violation-details">{violation.details || 'No details provided'}</div>
                    {#if violation.severity}
                      <div class="violation-severity {violation.severity.toLowerCase()}">
                        {violation.severity}
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      {/if}
    {:else}
      <div class="no-data">No rules data available</div>
    {/if}
  </div>
</div>

<style>
  .rules-view {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  h1, h2, h3, h4 {
    color: #333;
    margin-bottom: 1rem;
  }
  
  h2 {
    margin-top: 1.5rem;
  }
  
  .loading, .no-data {
    padding: 2rem;
    text-align: center;
    background: #f5f5f5;
    border-radius: 4px;
    margin: 1rem 0;
  }
  
  .error-message {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin: 1rem 0;
  }
  
  .rules-overview {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  @media (max-width: 768px) {
    .rules-overview {
      grid-template-columns: 1fr;
    }
  }
  
  .rules-card {
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
  }
  
  .rules-count {
    font-size: 2rem;
    font-weight: bold;
    color: #1976d2;
    margin-bottom: 1rem;
  }
  
  .rules-list, .policy-files {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .rule-item {
    padding: 0.75rem;
    background: #f5f5f5;
    border-radius: 4px;
    border-left: 4px solid #1976d2;
  }
  
  .rule-name {
    font-weight: bold;
    margin-bottom: 0.25rem;
  }
  
  .rule-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.5rem;
  }
  
  .rule-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
  }
  
  .tag {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
  }
  
  .policy-item {
    padding: 0.5rem;
    border-bottom: 1px solid #eee;
  }
  
  .policy-item:last-child {
    border-bottom: none;
  }
  
  .policy-item label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
  }
  
  .check-button {
    margin-top: 1rem;
    width: 100%;
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
  
  .policy-check-result {
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-top: 1.5rem;
  }
  
  .result-summary {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  .result-status {
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-transform: uppercase;
  }
  
  .result-status.valid {
    background: #e8f5e9;
    color: #2e7d32;
  }
  
  .result-status.invalid {
    background: #ffebee;
    color: #c62828;
  }
  
  .result-message {
    flex: 1;
  }
  
  .violations {
    margin-top: 1.5rem;
  }
  
  .violations-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .violation-item {
    padding: 0.75rem;
    background: #fff8e1;
    border-radius: 4px;
    border-left: 4px solid #ff9800;
    position: relative;
  }
  
  .violation-rule {
    font-weight: bold;
    margin-bottom: 0.25rem;
  }
  
  .violation-details {
    font-size: 0.9rem;
  }
  
  .violation-severity {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    text-transform: uppercase;
  }
  
  .violation-severity.high {
    background: #ffebee;
    color: #c62828;
  }
  
  .violation-severity.medium {
    background: #fff8e1;
    color: #f57c00;
  }
  
  .violation-severity.low {
    background: #e8f5e9;
    color: #2e7d32;
  }
</style>