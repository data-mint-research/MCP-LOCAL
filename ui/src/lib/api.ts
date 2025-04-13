/**
 * API client for MCP-Gateway
 * Provides methods to interact with the MCP-LOCAL REST API endpoints
 */

const API_BASE_URL = 'http://localhost:9000';

/**
 * Fetch wrapper with error handling for MCP-Gateway API calls
 */
async function fetchWithErrorHandling(endpoint: string, options: RequestInit = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * Get system status information
 * @returns Status information for all active units
 */
export async function getStatus() {
  return fetchWithErrorHandling('/mcp/status');
}

/**
 * Send a prompt to the inference engine
 * @param prompt The user prompt to process
 * @returns The inference result
 */
export async function sendPrompt(prompt: string) {
  return fetchWithErrorHandling('/mcp/infer', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  });
}

/**
 * Get logs for a specific unit
 * @param unit The unit name to get logs for
 * @returns The last 100 log lines for the specified unit
 */
export async function getLogs(unit: string) {
  return fetchWithErrorHandling(`/mcp/logs?unit=${encodeURIComponent(unit)}`);
}

/**
 * Get rules overview
 * @returns Information about system rules
 */
export async function getRules() {
  return fetchWithErrorHandling('/mcp/rules');
}

/**
 * Check a policy against the rules
 * @param policyFile The policy file to check
 * @returns The policy check result
 */
export async function checkPolicy(policyFile: string) {
  return fetchWithErrorHandling('/mcp/rules/check', {
    method: 'POST',
    body: JSON.stringify({ policy: policyFile }),
  });
}

/**
 * Get system state for a specific memory area
 * @param area The memory area to retrieve (memory, policy, etc.)
 * @returns The state data for the specified area
 */
export async function getState(area: string) {
  return fetchWithErrorHandling(`/mcp/state/${encodeURIComponent(area)}`);
}