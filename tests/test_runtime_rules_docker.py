# 📄 Script: test_runtime_rules_docker.py
# 🔧 Zweck: Tests für die Runtime-Validierung von Policies gegen Regeln (Docker-Version)
# 🗂 Pfad: tests/test_runtime_rules_docker.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: pytest, yaml
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Skript testet die Funktionalität des runtime_rules-Moduls,
# HINWEIS (MCP): das für die Validierung von Policies gegen definierte Regeln zuständig ist.

import os
import sys
import pytest
import yaml
from typing import Dict, Any

# Import directly from the app directory
sys.path.append("/app")
from runtime_rules import check_policy_against_rules, get_rule_files, load_rule_file

def load_test_policy(policy_file: str) -> Dict[str, Any]:
    """Load a policy file for testing."""
    with open(policy_file, "r") as f:
        return yaml.safe_load(f)

def test_valid_policy():
    """Test that a valid policy passes validation."""
    # Load a known valid policy
    policy = load_test_policy("/app/config/policies/graph.policy.yaml")
    
    # Check policy against rules
    violations = check_policy_against_rules(policy)
    
    # A valid policy should have no violations
    assert len(violations) == 0, f"Expected no violations, but got: {violations}"

def test_empty_policy():
    """Test that an empty policy fails validation."""
    # Empty policy
    policy = {}
    
    # Check policy against rules
    violations = check_policy_against_rules(policy)
    
    # An empty policy should have violations
    assert len(violations) > 0, "Expected violations for empty policy, but got none"
    assert "Policy is empty or None" in violations

def test_invalid_policy():
    """Test that an invalid policy fails validation."""
    # Create an invalid policy with a component name that should definitely fail validation
    policy = {
        "component": "INVALID-COMPONENT-NAME!@#",  # Invalid characters
        "enabled": True
    }
    
    # Print out the rule files that are being loaded
    rule_files = get_rule_files()
    print(f"Rule files: {rule_files}")
    
    # Load and print naming rules
    for rule_file in rule_files:
        if "naming" in rule_file:
            naming_rules = load_rule_file(rule_file)
            print(f"Naming rules: {naming_rules}")
    
    # Check policy against rules
    violations = check_policy_against_rules(policy)
    print(f"Violations: {violations}")
    
    # This policy should have violations (component name doesn't match pattern)
    assert len(violations) > 0, "Expected violations for invalid policy, but got none"

def test_specific_rule_files():
    """Test checking against specific rule files."""
    # Load a policy
    policy = load_test_policy("/app/config/policies/graph.policy.yaml")
    
    # Check against only the structure rules
    rule_files = ["/app/config/rules/structure.rules.yaml"]
    violations = check_policy_against_rules(policy, rule_files)
    
    # Should validate against only the specified rule file
    assert isinstance(violations, list), "Expected a list of violations"