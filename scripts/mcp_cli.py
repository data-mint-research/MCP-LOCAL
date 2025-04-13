#!/usr/bin/env python3
# 📄 Script: mcp_cli.py
# 🔧 Zweck: Command-Line-Interface für MCP-Funktionen, insbesondere Regelprüfung
# 🗂 Pfad: scripts/mcp_cli.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: argparse, yaml, sys, os
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Skript implementiert ein CLI für MCP-Funktionen,
# HINWEIS (MCP): insbesondere für die Überprüfung von Policies gegen definierte Regeln.
# HINWEIS (MCP): Es verwendet die check_policy_against_rules()-Funktion aus runtime_rules.py.

import os
import sys
import argparse
import yaml
import logging
from typing import Dict, List, Any, Optional

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_units.mcp_agent_interaction_engine.runtime_rules import (
    check_policy_against_rules,
    load_rule_file,
    get_rule_files
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp_cli')

def setup_parser() -> argparse.ArgumentParser:
    """
    Set up the command-line argument parser.
    
    Returns:
        An ArgumentParser instance configured with all available commands and options
    """
    # Create the main parser
    parser = argparse.ArgumentParser(
        description='MCP Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a policy against all rules
  mcp rules check --policy config/policies/tool.policy.yaml
  
  # Check a policy against specific rule files
  mcp rules check --policy config/policies/tool.policy.yaml --rule-file config/rules/structure.rules.yaml
  
  # List available rule files
  mcp rules list
"""
    )
    
    # Create subparsers for different command groups
    subparsers = parser.add_subparsers(dest='command_group', help='Command group')
    
    # Create the 'rules' command group
    rules_parser = subparsers.add_parser('rules', help='Operations related to rules')
    rules_subparsers = rules_parser.add_subparsers(dest='command', help='Rules command')
    
    # Create the 'check' command under 'rules'
    check_parser = rules_subparsers.add_parser('check', help='Check a policy against rules')
    check_parser.add_argument(
        '--policy', 
        required=True,
        help='Path to the policy file to check'
    )
    check_parser.add_argument(
        '--rule-file', 
        action='append', 
        dest='rule_files',
        help='Path to a specific rule file to check against (can be specified multiple times)'
    )
    check_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Create the 'list' command under 'rules'
    list_parser = rules_subparsers.add_parser('list', help='List available rule files')
    list_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show rule file contents'
    )
    
    return parser

def load_policy_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML policy file.
    
    Args:
        file_path: Path to the policy file
        
    Returns:
        Dictionary containing the parsed policy content
        
    Raises:
        FileNotFoundError: If the policy file doesn't exist
        yaml.YAMLError: If the policy file contains invalid YAML
    """
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Policy file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing policy file {file_path}: {e}")
        raise

def handle_check_command(args: argparse.Namespace) -> int:
    """
    Handle the 'rules check' command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Load the policy file
        logger.debug(f"Loading policy file: {args.policy}")
        policy = load_policy_file(args.policy)
        
        # Check the policy against rules
        logger.debug(f"Checking policy against rules (rule files: {args.rule_files})")
        violations = check_policy_against_rules(policy, args.rule_files)
        
        # Print the results
        if violations:
            print(f"❌ Policy validation failed with {len(violations)} violation(s):")
            for i, violation in enumerate(violations, 1):
                print(f"  {i}. {violation}")
            return 1
        else:
            print("✅ Policy validation successful! No violations found.")
            return 0
            
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {str(e)}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return 1

def handle_list_command(args: argparse.Namespace) -> int:
    """
    Handle the 'rules list' command.
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Get all rule files
        rule_files = get_rule_files()
        
        if not rule_files:
            print("No rule files found.")
            return 0
        
        print(f"Found {len(rule_files)} rule file(s):")
        
        for i, file_path in enumerate(rule_files, 1):
            rule_type = os.path.basename(file_path).split('.')[0]
            print(f"  {i}. {file_path} (Type: {rule_type})")
            
            if args.verbose:
                try:
                    # Load and print rule content
                    rules = load_rule_file(file_path)
                    print(f"     Content: {rules}")
                except Exception as e:
                    print(f"     Error loading rule content: {str(e)}")
        
        return 0
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return 1

def main() -> int:
    """
    Main entry point for the MCP CLI.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = setup_parser()
    args = parser.parse_args()
    
    # Handle the case when no command is provided
    if not args.command_group:
        parser.print_help()
        return 1
    
    # Handle the 'rules' command group
    if args.command_group == 'rules':
        if not args.command:
            # If no subcommand is provided, print help for the rules command
            parser.parse_args(['rules', '--help'])
            return 1
        
        # Handle the 'check' command
        if args.command == 'check':
            return handle_check_command(args)
        
        # Handle the 'list' command
        elif args.command == 'list':
            return handle_list_command(args)
    
    # If we get here, the command wasn't recognized
    print(f"Unknown command: {args.command_group} {getattr(args, 'command', '')}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
