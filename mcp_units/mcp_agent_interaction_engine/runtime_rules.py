# 📄 Script: runtime_rules.py
# 🔧 Zweck: Runtime-Validierung von Policies gegen Regeln
# 🗂 Pfad: mcp_units/mcp_agent_interaction_engine/runtime_rules.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: os, yaml, glob, logging
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieses Modul implementiert die Runtime-Validierung von Policies gegen definierte Regeln.
# HINWEIS (MCP): Es lädt alle .rules.yaml-Dateien aus dem config/rules/-Verzeichnis und vergleicht
# HINWEIS (MCP): die übergebene Policy gegen diese Regeln, um Verstöße zu identifizieren.

import os
import yaml
import glob
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logger = logging.getLogger('mcp_logger')

# Constants
RULES_DIR = "config/rules"

def load_rule_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML rule file.
    
    Args:
        file_path: Path to the rule file
        
    Returns:
        Dictionary containing the parsed rule content
        
    Raises:
        FileNotFoundError: If the rule file doesn't exist
        yaml.YAMLError: If the rule file contains invalid YAML
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Rule file not found: {file_path}")
        return []
    except yaml.YAMLError as e:
        logger.error(f"Error parsing rule file {file_path}: {e}")
        raise

def get_rule_files(rule_files: Optional[List[str]] = None) -> List[str]:
    """
    Get a list of rule files to check against.
    
    Args:
        rule_files: Optional list of specific rule files to use
        
    Returns:
        List of paths to rule files
    """
    if rule_files:
        return rule_files
    
    # Find all .rules.yaml files in the rules directory
    pattern = os.path.join(RULES_DIR, "*.rules.yaml")
    return glob.glob(pattern)

def check_policy_against_rules(policy: Dict[str, Any], rule_files: Optional[List[str]] = None) -> List[str]:
    """
    Check if a policy complies with all defined rules.
    
    This function loads all .rules.yaml files from config/rules/ (or uses the provided list)
    and compares the provided policy against these rules to identify violations.
    
    Args:
        policy: The policy dictionary to validate
        rule_files: Optional list of specific rule files to check against
        
    Returns:
        List of rule violations (empty list if no violations)
    """
    if not policy:
        return ["Policy is empty or None"]
    
    violations = []
    files = get_rule_files(rule_files)
    
    if not files:
        logger.warning("No rule files found to check against")
        return []
    
    try:
        # Process each rule file
        for rule_file in files:
            logger.debug(f"Checking policy against rule file: {rule_file}")
            rules = load_rule_file(rule_file)
            
            # Extract the rule type from the filename (e.g., "structure" from "structure.rules.yaml")
            rule_type = os.path.basename(rule_file).split('.')[0]
            
            # Skip if rules is None or empty
            if not rules:
                continue
            
            # For naming rules, always check component name pattern regardless of component
            if rule_type == "naming" and "component" in policy:
                naming_rules = rules.get("naming", {})
                
                # Check if component name follows a valid pattern
                # For this implementation, we'll consider valid component names to be:
                # - Must contain only lowercase letters, numbers, and underscores
                # - Must not start with a number
                import re
                valid_component_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
                if not valid_component_pattern.match(policy["component"]):
                    violations.append(f"Component name '{policy['component']}' is invalid. Must contain only lowercase letters, numbers, and underscores, and must not start with a number.")
                
                # Also check against any specific component pattern in the rules if it exists
                if "component_pattern" in naming_rules:
                    pattern = re.compile(naming_rules["component_pattern"].get("regex", ""))
                    if not pattern.match(policy["component"]):
                        violations.append(f"Component name '{policy['component']}' does not match required pattern")
                
            # Check if this rule applies to the policy's component
            if "component" in policy and rule_type in rules:
                # Structure rules
                if rule_type == "structure":
                    structure_rules = rules.get("structure", {})
                    
                    # Check for required fields in policy
                    if "required_fields" in structure_rules:
                        for field in structure_rules["required_fields"]:
                            if field not in policy:
                                violations.append(f"Missing required field: {field}")
                
                # Naming rules - already checked at the top level
                elif rule_type == "naming":
                    pass  # Naming rules are now checked for all components at the top level
                
                # Capabilities rules
                elif rule_type == "capabilities":
                    capabilities_rules = rules.get("capabilities", {})
                    
                    # Check if policy uses capabilities that are defined in the rules
                    if "capabilities" in policy:
                        for capability in policy["capabilities"]:
                            found = False
                            for component, allowed_capabilities in capabilities_rules.items():
                                if capability in allowed_capabilities:
                                    found = True
                                    break
                            
                            if not found:
                                violations.append(f"Undefined capability used: {capability}")
                
                # Agents rules
                elif rule_type == "agents":
                    agents_rules = rules.get("agents", {})
                    
                    # Check if agent configuration is valid
                    if policy["component"] in agents_rules:
                        agent_rules = agents_rules[policy["component"]]
                        
                        # Check required agent fields
                        if "required_fields" in agent_rules:
                            for field in agent_rules["required_fields"]:
                                if field not in policy:
                                    violations.append(f"Missing required field for agent {policy['component']}: {field}")
                
                # Permissions rules
                elif rule_type == "permissions":
                    # Check if component has necessary permissions
                    # Skip permission check if the component is not in the rules and there's no default
                    # This is to allow components that don't need specific permissions
                    if policy["component"] not in rules and "default" in rules:
                        # Use default permissions if available
                        permissions = rules.get("default", {})
                        if permissions.get("access") == "restricted":
                            violations.append(f"Component {policy['component']} has restricted access by default")
                
                # Logging rules
                elif rule_type == "logging":
                    logging_rules = rules.get("logging", {})
                    
                    # Check log level if specified
                    if "log_level" in policy and "allowed_levels" in logging_rules:
                        if policy["log_level"] not in logging_rules["allowed_levels"]:
                            violations.append(
                                f"Invalid log level: {policy['log_level']}. "
                                f"Allowed levels: {logging_rules['allowed_levels']}"
                            )
                
                # Generic component-specific rules
                component_rules = rules.get(rule_type, {}).get(policy["component"], {})
                
                # Check for required fields specific to this component
                if "required_fields" in component_rules:
                    for field in component_rules["required_fields"]:
                        if field not in policy:
                            violations.append(f"Missing required field for {policy['component']}: {field}")
                
                # Check for allowed values
                for field, field_rules in component_rules.items():
                    if isinstance(field_rules, dict) and field in policy and "allowed_values" in field_rules:
                        if policy[field] not in field_rules["allowed_values"]:
                            violations.append(
                                f"Invalid value for {field}: {policy[field]}. "
                                f"Allowed values: {field_rules['allowed_values']}"
                            )
    
    except Exception as e:
        logger.error(f"Error checking policy against rules: {e}")
        violations.append(f"Error during rule validation: {str(e)}")
    
    return violations