# 📄 Script: test_rules.py
# 🔧 Zweck: Tests für die Validierung von Rules-Dateien und Policy-Regeln
# 🗂 Pfad: tests/test_rules.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: pytest, yaml, glob, re
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Skript testet die Format, Eindeutigkeit und Struktur aller .rules.yaml-Dateien
# HINWEIS (MCP): sowie die check_policy_against_rules()-Funktion mit Beispiel-Policies.

import os
import sys
import glob
import re
import pytest
import yaml
from typing import Dict, List, Any, Set

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_units.mcp_agent_interaction_engine.runtime_rules import (
    check_policy_against_rules,
    load_rule_file,
    get_rule_files,
    RULES_DIR
)

def test_rules_directory_exists():
    """Test that the rules directory exists."""
    assert os.path.isdir(RULES_DIR), f"Rules directory {RULES_DIR} does not exist"

def test_rules_files_exist():
    """Test that there are rules files in the rules directory."""
    rule_files = get_rule_files()
    assert len(rule_files) > 0, f"No rule files found in {RULES_DIR}"
    
    # Print the found rule files for debugging
    print(f"Found {len(rule_files)} rule files: {rule_files}")

def test_rules_files_naming_convention():
    """Test that all rules files follow the naming convention."""
    rule_files = get_rule_files()
    pattern = re.compile(r'^[a-z0-9_]+\.rules\.yaml$')
    
    for rule_file in rule_files:
        filename = os.path.basename(rule_file)
        assert pattern.match(filename), f"Rule file {filename} does not follow naming convention"

def test_rules_files_uniqueness():
    """Test that rule types are unique across all rule files."""
    rule_files = get_rule_files()
    rule_types = set()
    
    for rule_file in rule_files:
        rule_type = os.path.basename(rule_file).split('.')[0]
        assert rule_type not in rule_types, f"Duplicate rule type found: {rule_type}"
        rule_types.add(rule_type)

def test_rules_files_valid_yaml():
    """Test that all rules files contain valid YAML."""
    rule_files = get_rule_files()
    
    for rule_file in rule_files:
        try:
            rules = load_rule_file(rule_file)
            assert rules is not None, f"Rule file {rule_file} contains None"
            assert isinstance(rules, dict), f"Rule file {rule_file} does not contain a dictionary"
        except Exception as e:
            pytest.fail(f"Error loading rule file {rule_file}: {e}")

def test_rules_files_structure():
    """Test that all rules files have the expected structure."""
    rule_files = get_rule_files()
    
    for rule_file in rule_files:
        rule_type = os.path.basename(rule_file).split('.')[0]
        rules = load_rule_file(rule_file)
        
        # Check that the rule file contains its own type as a top-level key
        assert rule_type in rules, f"Rule file {rule_file} does not contain its type as a top-level key"
        
        # Check that the rule content is a dictionary
        assert isinstance(rules[rule_type], dict), f"Rule content for {rule_type} is not a dictionary"

def test_rules_files_metadata():
    """Test that all rules files have the required metadata."""
    rule_files = get_rule_files()
    required_metadata = [
        "# 📄 Datei:",
        "# 🔧 Zweck:",
        "# 👤 Autor:",
        "# 📅 Erstellt:",
        "# 📘 Gültigkeit:",
        "# 🧱 Version:"
    ]
    
    for rule_file in rule_files:
        with open(rule_file, "r") as f:
            content = f.read()
            
            for metadata in required_metadata:
                assert metadata in content, f"Rule file {rule_file} is missing required metadata: {metadata}"

def create_valid_policy() -> Dict[str, Any]:
    """Create a valid policy for testing."""
    return {
        "component": "graph_engine",
        "enabled": True,
        "log_each_step": True,
        "fallback_on_failure": False
    }

def create_invalid_policy_missing_fields() -> Dict[str, Any]:
    """Create an invalid policy with missing required fields."""
    return {
        "component": "graph_engine"
        # Missing required fields
    }

def create_invalid_policy_invalid_component() -> Dict[str, Any]:
    """Create an invalid policy with an invalid component name."""
    return {
        "component": "INVALID-COMPONENT-NAME!@#",  # Invalid characters
        "enabled": True,
        "log_each_step": True,
        "fallback_on_failure": False
    }

def create_invalid_policy_invalid_values() -> Dict[str, Any]:
    """Create an invalid policy with invalid values."""
    return {
        "component": "graph_engine",
        "enabled": "not_a_boolean",  # Should be a boolean
        "log_each_step": True,
        "fallback_on_failure": False
    }

def test_check_policy_against_rules_valid():
    """Test that a valid policy passes validation."""
    policy = create_valid_policy()
    violations = check_policy_against_rules(policy)
    
    assert isinstance(violations, list), "Expected a list of violations"
    assert len(violations) == 0, f"Expected no violations for valid policy, but got: {violations}"

def test_check_policy_against_rules_empty():
    """Test that an empty policy fails validation."""
    policy = {}
    violations = check_policy_against_rules(policy)
    
    assert isinstance(violations, list), "Expected a list of violations"
    assert len(violations) > 0, "Expected violations for empty policy, but got none"
    assert "Policy is empty or None" in violations, "Expected 'Policy is empty or None' violation"

def test_check_policy_against_rules_none():
    """Test that a None policy fails validation."""
    policy = None
    violations = check_policy_against_rules(policy)
    
    assert isinstance(violations, list), "Expected a list of violations"
    assert len(violations) > 0, "Expected violations for None policy, but got none"
    assert "Policy is empty or None" in violations, "Expected 'Policy is empty or None' violation"

def test_check_policy_against_rules_invalid_component():
    """Test that a policy with an invalid component name fails validation."""
    policy = create_invalid_policy_invalid_component()
    violations = check_policy_against_rules(policy)
    
    assert isinstance(violations, list), "Expected a list of violations"
    assert len(violations) > 0, "Expected violations for invalid component name, but got none"
    
    # Check for specific violation message about component name
    component_violation = False
    for violation in violations:
        if "Component name" in violation and "invalid" in violation.lower():
            component_violation = True
            break
    
    assert component_violation, "Expected violation about invalid component name"

def test_check_policy_against_rules_specific_rule_file():
    """Test checking a policy against a specific rule file."""
    policy = create_valid_policy()
    rule_files = ["config/rules/structure.rules.yaml"]
    violations = check_policy_against_rules(policy, rule_files)
    
    assert isinstance(violations, list), "Expected a list of violations"
    # We don't assert on the specific violations since we're only testing against structure rules

def test_check_policy_against_rules_multiple_rule_files():
    """Test checking a policy against multiple specific rule files."""
    policy = create_valid_policy()
    rule_files = [
        "config/rules/structure.rules.yaml",
        "config/rules/naming.rules.yaml"
    ]
    violations = check_policy_against_rules(policy, rule_files)
    
    assert isinstance(violations, list), "Expected a list of violations"
    # We don't assert on the specific violations since we're testing against multiple rule files

def test_check_policy_against_rules_nonexistent_rule_file():
    """Test checking a policy against a nonexistent rule file."""
    policy = create_valid_policy()
    rule_files = ["config/rules/nonexistent.rules.yaml"]
    
    # This should not raise an exception, but return an empty list of violations
    # since no rules were found to check against
    violations = check_policy_against_rules(policy, rule_files)
    
    assert isinstance(violations, list), "Expected a list of violations"
    assert len(violations) == 0, "Expected no violations when no rule files are found"

def test_load_rule_file_nonexistent():
    """Test that loading a nonexistent rule file raises an exception."""
    with pytest.raises(FileNotFoundError):
        load_rule_file("config/rules/nonexistent.rules.yaml")

def test_get_rule_files_specific():
    """Test getting specific rule files."""
    rule_files = ["config/rules/structure.rules.yaml", "config/rules/naming.rules.yaml"]
    result = get_rule_files(rule_files)
    
    assert result == rule_files, "Expected the same list of rule files"

def test_get_rule_files_all():
    """Test getting all rule files."""
    result = get_rule_files()
    
    assert isinstance(result, list), "Expected a list of rule files"
    assert len(result) > 0, "Expected at least one rule file"
    
    # Check that all files have the .rules.yaml extension
    for file in result:
        assert file.endswith(".rules.yaml"), f"Expected file with .rules.yaml extension, got {file}"

if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__])