# MCP-LOCAL Control Panel

A cross-platform desktop application built with Tauri and SvelteKit for managing and interacting with the MCP-LOCAL system.

## Features

- **Dashboard**: Overview of all active MCP units
- **Prompt Engine**: Interface for sending prompts to the inference engine
- **Logs**: View system logs for different units
- **Rules & Policies**: Manage and check system rules and policies
- **System State**: View the state of different memory areas

## Prerequisites

- [Node.js](https://nodejs.org/) (v16 or later)
- [pnpm](https://pnpm.io/) (v7 or later)
- [Rust](https://www.rust-lang.org/) (v1.60 or later)
- [Tauri CLI](https://tauri.app/v1/guides/getting-started/prerequisites)

## Development

### Frontend Only

To run the SvelteKit frontend in development mode:

```bash
cd ui
pnpm install
pnpm dev
```

This will start the development server at http://localhost:5173.

### Full Application (Tauri)

To run the full Tauri application in development mode:

```bash
cd ui
pnpm install
cargo tauri dev
```

This will build and launch the desktop application with hot-reloading enabled.

## Building

To build the application for production:

```bash
cd ui
pnpm install
cargo tauri build
```

This will create platform-specific binaries in the `ui/src-tauri/target/release` directory.

## Architecture

- **Frontend**: SvelteKit
- **Backend**: Tauri with Rust
- **API Communication**: REST API calls to MCP-Gateway (localhost:9000)

## Project Structure

```
/ui/
  ├── src/                  # SvelteKit source code
  │   ├── routes/           # SvelteKit routes/pages
  │   ├── lib/              # Shared components and utilities
  │   │   ├── api.ts        # API client for MCP-Gateway
  │   │   └── components/   # Reusable UI components
  ├── src-tauri/            # Tauri/Rust backend code
  │   ├── src/              # Rust source code
  │   ├── Cargo.toml        # Rust dependencies
  │   └── icons/            # Application icons
  ├── static/               # Static assets
  ├── package.json          # Node.js dependencies
  └── tauri.conf.json       # Tauri configuration
```

## Notes

- The application communicates with a local MCP-Gateway running on `localhost:9000`
- No data is persisted locally - all data is loaded from the API
- The application is designed to be cross-platform (Windows, macOS, Linux)