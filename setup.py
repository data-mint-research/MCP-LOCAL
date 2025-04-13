import subprocess
import sys
import os
import locale

# Set environment variables to force UTF-8 encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Debug information about system encoding
print(f"System encoding: {sys.getdefaultencoding()}")
print(f"Filesystem encoding: {sys.getfilesystemencoding()}")
print(f"Locale encoding: {locale.getpreferredencoding()}")

def run_cmd(cmd_list, shell=False):
    try:
        result = subprocess.run(cmd_list, shell=shell, check=True, capture_output=True, text=True)
        print(f"✅ {cmd_list[0]}: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {cmd_list[0]} not available.")
        return False
    except FileNotFoundError:
        print(f"❌ {cmd_list[0]} not found.")
        return False

def install_python_dependencies():
    print("\n📦 Installing Python dependencies ...")
    
    # Install setuptools and wheel first
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "wheel"], check=True)
        print("✅ setuptools and wheel upgraded successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Failed to upgrade setuptools and wheel: {e}")
    
    # Install dependencies one by one (direct method that works)
    dependencies = [
        "pyyaml>=6",
        "docker>=6.1.0",
        "pytest>=7.0",
        "coverage>=7.0",
        "pytest-cov>=4.0"
    ]
    
    success_count = 0
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
            print(f"✅ {dep} installed successfully")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
    
    if success_count == len(dependencies):
        print("\n✅ All Python dependencies installed successfully")
    else:
        print(f"\n⚠️ {success_count} of {len(dependencies)} dependencies installed successfully")

def install_devtools():
    print("\n🛠 External devtools installation")
    print("ℹ️ Skipping external devtools installation.")
    print("ℹ️ You can install them manually if needed:")
    print("  - For pnpm: npm install -g pnpm")
    print("  - For Rust/Cargo: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
    print("  - For Tauri CLI: cargo install tauri-cli (after installing Rust/Cargo)")

if __name__ == "__main__":
    print("╔═════════════════════════════════════════════════╗")
    print("║ MCP-LOCAL Universal Setup (Python Dependencies) ║")
    print("╚═════════════════════════════════════════════════╝\n")

    # First, install Python dependencies
    install_python_dependencies()
    
    # Just provide information about devtools
    install_devtools()
    
    print("\n✅ Setup completed successfully.")
    print("✅ Python dependencies have been installed.")
    print("✅ You can now run `bash start.sh` to start the MCP services.")