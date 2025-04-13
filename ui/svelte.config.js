/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: () => {
    return {
      markup: ({ content }) => {
        return { code: content };
      }
    };
  },

  kit: {
    // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
    // If your environment is not supported, or you settled on a specific environment, switch out the adapter.
    // See https://kit.svelte.dev/docs/adapters for more information about adapters.
    adapter: {
      name: 'static',
      adapt: () => {
        // This is a placeholder for the adapter functionality
        // In a real project, this would be replaced by @sveltejs/adapter-static
        console.log('Using static adapter');
      }
    }
  }
};

module.exports = config;