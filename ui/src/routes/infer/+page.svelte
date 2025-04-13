<script>
  import { sendPrompt } from '$lib/api';
  
  let prompt = '';
  let messages = [];
  let loading = false;
  let error = null;
  
  // Send prompt to inference engine
  async function handleSubmit() {
    if (!prompt.trim()) return;
    
    const userMessage = {
      role: 'user',
      content: prompt,
      timestamp: new Date().toISOString()
    };
    
    // Add user message to chat
    messages = [...messages, userMessage];
    
    // Clear input
    const currentPrompt = prompt;
    prompt = '';
    
    try {
      loading = true;
      error = null;
      
      // Send prompt to API
      const response = await sendPrompt(currentPrompt);
      
      // Add system response to chat
      messages = [...messages, {
        role: 'system',
        content: response.result || response.message || 'No response received',
        timestamp: new Date().toISOString()
      }];
    } catch (err) {
      error = `Failed to process prompt: ${err.message}`;
      console.error(error);
    } finally {
      loading = false;
    }
  }
  
  // Clear chat history
  function clearChat() {
    messages = [];
    error = null;
  }
</script>

<svelte:head>
  <title>MCP-LOCAL Prompt Engine</title>
</svelte:head>

<div class="prompt-engine">
  <h1>Prompt Engine</h1>
  
  <div class="chat-container">
    {#if messages.length === 0}
      <div class="empty-chat">
        <p>Enter a prompt below to start a conversation with the inference engine.</p>
      </div>
    {:else}
      <div class="messages">
        {#each messages as message}
          <div class="message {message.role}">
            <div class="message-content">
              {message.content}
            </div>
            <div class="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        {/each}
        
        {#if loading}
          <div class="message system loading">
            <div class="loading-indicator">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        {/if}
      </div>
    {/if}
    
    {#if error}
      <div class="error-message">
        {error}
      </div>
    {/if}
  </div>
  
  <form on:submit|preventDefault={handleSubmit} class="prompt-form">
    <div class="input-container">
      <textarea
        bind:value={prompt}
        placeholder="Enter your prompt here..."
        rows="3"
        disabled={loading}
      ></textarea>
    </div>
    
    <div class="controls">
      <button type="button" on:click={clearChat} disabled={loading || messages.length === 0}>
        Clear Chat
      </button>
      <button type="submit" disabled={loading || !prompt.trim()}>
        {loading ? 'Processing...' : 'Send'}
      </button>
    </div>
  </form>
</div>

<style>
  .prompt-engine {
    padding: 1rem;
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    height: calc(100vh - 2rem);
  }
  
  h1 {
    margin-bottom: 1rem;
    color: #333;
  }
  
  .chat-container {
    flex: 1;
    background: #f5f5f5;
    border-radius: 4px;
    padding: 1rem;
    overflow-y: auto;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
  }
  
  .empty-chat {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    text-align: center;
    padding: 2rem;
  }
  
  .messages {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    position: relative;
  }
  
  .message.user {
    align-self: flex-end;
    background: #1976d2;
    color: white;
  }
  
  .message.system {
    align-self: flex-start;
    background: white;
    color: #333;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }
  
  .message-timestamp {
    font-size: 0.7rem;
    opacity: 0.7;
    margin-top: 0.25rem;
    text-align: right;
  }
  
  .loading-indicator {
    display: flex;
    justify-content: center;
    gap: 0.25rem;
  }
  
  .loading-indicator span {
    animation: pulse 1.4s infinite;
    animation-fill-mode: both;
  }
  
  .loading-indicator span:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  .loading-indicator span:nth-child(3) {
    animation-delay: 0.4s;
  }
  
  @keyframes pulse {
    0%, 80%, 100% {
      opacity: 0.4;
    }
    40% {
      opacity: 1;
    }
  }
  
  .error-message {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin: 1rem 0;
  }
  
  .prompt-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .input-container {
    position: relative;
  }
  
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: none;
    font-family: inherit;
    font-size: 1rem;
  }
  
  .controls {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
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
  
  button[type="button"] {
    background: #f5f5f5;
    color: #333;
  }
  
  button:hover:not(:disabled) {
    background: #1565c0;
  }
  
  button[type="button"]:hover:not(:disabled) {
    background: #e0e0e0;
  }
  
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>