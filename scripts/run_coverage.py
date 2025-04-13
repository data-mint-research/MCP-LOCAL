#!/usr/bin/env python3
# 📄 Script: run_coverage.py
# 🔧 Zweck: Misst die Testabdeckung für das MCP-Projekt
# 🗂 Pfad: scripts/run_coverage.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: coverage, pytest
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Skript führt alle Tests im tests/-Verzeichnis aus und
# HINWEIS (MCP): generiert einen Testabdeckungsbericht mit Prozentmetriken.
# HINWEIS (MCP): Es identifiziert, welche Teile des Codes nicht durch Tests abgedeckt sind.
# HINWEIS (MCP): Teil der kontinuierlichen Compliance-Anforderungen.

import os
import sys
import subprocess
import argparse
from pathlib import Path

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run test coverage for MCP project')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--xml', action='store_true', help='Generate XML report for CI')
    parser.add_argument('--output', type=str, default='coverage_reports', 
                        help='Output directory for reports')
    return parser.parse_args()

def ensure_dependencies():
    """Ensure required packages are installed."""
    try:
        import coverage
        import pytest
    except ImportError:
        print("Installing required dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "coverage", "pytest"])
        print("Dependencies installed successfully.")

def run_coverage(args):
    """Run test coverage and generate reports."""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(project_root, args.output)
    os.makedirs(output_dir, exist_ok=True)
    
    # Change to project root directory
    os.chdir(project_root)
    
    print(f"Running test coverage from {project_root}...")
    
    # Run coverage
    coverage_cmd = [
        sys.executable, "-m", "coverage", "run", 
        "--source=mcp_units", 
        "-m", "pytest", "tests/"
    ]
    
    try:
        subprocess.run(coverage_cmd, check=True)
        print("Tests completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        return False
    
    # Generate coverage report
    print("Generating coverage report...")
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"])
    
    # Generate HTML report if requested
    if args.html:
        html_output = os.path.join(output_dir, "html")
        print(f"Generating HTML report in {html_output}...")
        subprocess.run([
            sys.executable, "-m", "coverage", "html", 
            f"--directory={html_output}"
        ])
        print(f"HTML report generated at {html_output}/index.html")
    
    # Generate XML report if requested (useful for CI)
    if args.xml:
        xml_output = os.path.join(output_dir, "coverage.xml")
        print(f"Generating XML report at {xml_output}...")
        subprocess.run([
            sys.executable, "-m", "coverage", "xml", 
            f"-o={xml_output}"
        ])
        print(f"XML report generated at {xml_output}")
    
    return True

def main():
    """Main function."""
    args = parse_arguments()
    ensure_dependencies()
    success = run_coverage(args)
    
    if success:
        print("\nCoverage analysis completed successfully.")
        print("\nTo view detailed reports:")
        if args.html:
            print(f"- HTML Report: Open {args.output}/html/index.html in your browser")
        if args.xml:
            print(f"- XML Report: {args.output}/coverage.xml (for CI integration)")
        print("\nAreas with low coverage should be prioritized for additional testing.")
    else:
        print("\nCoverage analysis failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()