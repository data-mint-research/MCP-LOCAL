<script>
  import { page } from '$app/stores';
  
  // Navigation items
  const navItems = [
    { path: '/', label: 'Dashboard', icon: 'dashboard' },
    { path: '/infer', label: 'Prompt Engine', icon: 'chat' },
    { path: '/logs', label: 'Logs', icon: 'list' },
    { path: '/rules', label: 'Rules & Policies', icon: 'shield' },
    { path: '/state', label: 'System State', icon: 'memory' }
  ];
</script>

<nav class="navigation">
  <div class="nav-header">
    <div class="logo">MCP-LOCAL</div>
    <div class="subtitle">Control Panel</div>
  </div>
  
  <ul class="nav-items">
    {#each navItems as item}
      <li class="nav-item {$page.url.pathname === item.path ? 'active' : ''}">
        <a href={item.path}>
          <span class="icon material-icons">{item.icon}</span>
          <span class="label">{item.label}</span>
        </a>
      </li>
    {/each}
  </ul>
  
  <div class="nav-footer">
    <div class="version">v1.0.0</div>
  </div>
</nav>

<style>
  .navigation {
    background: #1e293b;
    color: #e2e8f0;
    width: 250px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0;
    top: 0;
  }
  
  .nav-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .logo {
    font-size: 1.5rem;
    font-weight: bold;
    letter-spacing: 1px;
  }
  
  .subtitle {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.25rem;
  }
  
  .nav-items {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
  }
  
  .nav-item {
    margin: 0.25rem 0;
  }
  
  .nav-item a {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    color: inherit;
    text-decoration: none;
    transition: background-color 0.2s;
  }
  
  .nav-item a:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  .nav-item.active a {
    background: rgba(255, 255, 255, 0.15);
    border-left: 3px solid #3b82f6;
  }
  
  .icon {
    margin-right: 0.75rem;
    font-size: 1.25rem;
  }
  
  .nav-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 0.8rem;
    opacity: 0.7;
    text-align: center;
  }
</style>