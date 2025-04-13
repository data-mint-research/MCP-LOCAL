<script>
  import Navigation from './Navigation.svelte';
</script>

<div class="app-container">
  <Navigation />
  
  <main class="main-content">
    <slot />
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #f8fafc;
    color: #334155;
  }
  
  :global(*) {
    box-sizing: border-box;
  }
  
  .app-container {
    display: flex;
    min-height: 100vh;
  }
  
  .main-content {
    flex: 1;
    margin-left: 250px; /* Match navigation width */
    min-height: 100vh;
    overflow-x: hidden;
  }
</style>