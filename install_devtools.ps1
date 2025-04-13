Write-Host "╔═════════════════════════════════════════════╗"
Write-Host "║ MCP-LOCAL PowerShell Devtool Installer      ║"
Write-Host "╚═════════════════════════════════════════════╝`n"

function Is-Installed($command) {
    return (Get-Command $command -ErrorAction SilentlyContinue) -ne $null
}

# 1. pnpm via npm fallback
if (-not (Is-Installed "pnpm")) {
    Write-Host "🔧 Installing pnpm via npm ..."
    if (Is-Installed "npm") {
        npm install -g pnpm
        if (Is-Installed "pnpm") {
            Write-Host "✅ pnpm installiert: $(pnpm --version)"
        } else {
            Write-Host "❌ pnpm konnte nicht installiert werden."
        }
    } else {
        Write-Host "❌ npm nicht gefunden. Bitte installiere Node.js zuerst:"
        Write-Host "   🔗 https://nodejs.org/"
    }
} else {
    Write-Host "✅ pnpm bereits vorhanden: $(pnpm --version)"
}

# 2. Rust/Cargo via Browser
if (-not (Is-Installed "cargo")) {
    Write-Host "🔧 Rust (cargo) nicht gefunden. Öffne Windows-Installer im Browser ..."
    Start-Process "https://win.rustup.rs"
    Write-Host "⚠️ Bitte Installer ausführen und danach PowerShell neu starten."
    exit
} else {
    Write-Host "✅ cargo bereits vorhanden: $(cargo --version)"
}

# 3. Tauri CLI
if (-not (Is-Installed "tauri")) {
    Write-Host "🔧 Installing Tauri CLI ..."
    cargo install tauri-cli
    if (Is-Installed "tauri") {
        Write-Host "✅ tauri installiert: $(tauri --version)"
    } else {
        Write-Host "❌ tauri konnte nicht installiert werden. Prüfe cargo-Installation."
    }
} else {
    Write-Host "✅ tauri bereits vorhanden: $(tauri --version)"
}

Write-Host "`n🎉 Alle Devtools sind installiert oder bereits vorhanden."
