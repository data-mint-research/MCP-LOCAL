#!/usr/bin/env python3
"""
MCP Registry Updater

This script automatically updates the MCP registry (config/mcp_register.yaml)
by scanning the mcp_units directory and registering all found MCP units.
It preserves the special markdown format of the registry file.
"""

import os
import yaml
import sys
import re
import traceback
from pathlib import Path

# Constants
MCP_UNITS_DIR = "mcp_units"
REGISTRY_FILE = "config/mcp_register.yaml"

# Markdown template for the registry file
REGISTRY_TEMPLATE = """---

### 📄 `MCP-LOCAL/config/mcp_register.yaml`

```yaml
{yaml_content}
```
"""

def get_unit_type(dir_name):
    """
    Determine the unit type based on the directory name.
    
    Args:
        dir_name: The directory name (e.g., mcp_agent_interaction_engine)
        
    Returns:
        The unit type (e.g., mcp_agent)
    """
    # Extract the type from the directory name (e.g., mcp_agent from mcp_agent_interaction_engine)
    match = re.match(r'(mcp_[a-z]+)_', dir_name)
    if match:
        return match.group(1)
    return "mcp_unknown"  # Fallback

def get_unit_id(dir_name):
    """
    Determine the unit ID based on the directory name.
    
    Args:
        dir_name: The directory name (e.g., mcp_agent_interaction_engine)
        
    Returns:
        The unit ID (e.g., interaction_engine)
    """
    # Extract the ID from the directory name (e.g., interaction_engine from mcp_agent_interaction_engine)
    match = re.match(r'mcp_[a-z]+_(.+)', dir_name)
    if match:
        return match.group(1)
    return dir_name.replace("mcp_", "")  # Fallback

def find_main_file(unit_dir):
    """
    Find the main Python file in the unit directory.
    
    Args:
        unit_dir: The unit directory path
        
    Returns:
        The path to the main Python file
    """
    # List all Python files in the directory
    py_files = list(Path(unit_dir).glob("*.py"))
    
    if not py_files:
        return None
    
    # If there's only one Python file, use that
    if len(py_files) == 1:
        return py_files[0]
    
    # Otherwise, look for common main file names
    for name in ["main.py", "app.py", "service.py", "handler.py", "runner.py", "flow.py"]:
        for file in py_files:
            if file.name == name:
                return file
    
    # If no common name is found, just use the first Python file
    return py_files[0]

def scan_mcp_units():
    """
    Scan the mcp_units directory and return information about all found units.
    
    Returns:
        A list of dictionaries with unit information
    """
    units = []
    
    # Get all subdirectories in the mcp_units directory
    for item in os.listdir(MCP_UNITS_DIR):
        unit_dir = os.path.join(MCP_UNITS_DIR, item)
        
        # Skip if not a directory or doesn't start with "mcp_"
        if not os.path.isdir(unit_dir) or not item.startswith("mcp_"):
            continue
        
        # Find the main Python file
        main_file = find_main_file(unit_dir)
        if not main_file:
            continue
        
        # Get unit type and ID
        unit_type = get_unit_type(item)
        unit_id = get_unit_id(item)
        
        # Add unit to the list
        units.append({
            "id": unit_id,
            "type": unit_type,
            "path": str(main_file)
        })
    
    return units

def update_registry():
    """
    Update the MCP registry file with information about all found units.
    """
    print("DEBUG: Starting update_registry()")
    
    # Scan for MCP units
    print("DEBUG: Scanning MCP units...")
    units = scan_mcp_units()
    print(f"DEBUG: Found {len(units)} MCP units:")
    for unit in units:
        print(f"DEBUG:   - {unit['id']} ({unit['type']}): {unit['path']}")
    
    # List all files in mcp_units directory
    print("\nDEBUG: Listing all files in mcp_units directory:")
    for root, dirs, files in os.walk(MCP_UNITS_DIR):
        for file in files:
            print(f"DEBUG:   - {os.path.join(root, file)}")
    
    # Create registry data
    print("\nDEBUG: Creating registry data...")
    registry_data = {
        "units": units
    }
    
    # Convert registry data to YAML
    print("DEBUG: Converting registry data to YAML...")
    yaml_content = yaml.dump(registry_data, default_flow_style=False, sort_keys=False)
    print(f"DEBUG: YAML content:\n{yaml_content}")
    
    # Format the registry file with markdown
    print("DEBUG: Formatting registry file with markdown...")
    registry_content = REGISTRY_TEMPLATE.format(yaml_content=yaml_content)
    print(f"DEBUG: Registry content:\n{registry_content}")
    
    # Write to registry file
    print(f"DEBUG: Writing to registry file: {REGISTRY_FILE}")
    try:
        with open(REGISTRY_FILE, "w") as f:
            f.write(registry_content)
        print(f"DEBUG: Successfully wrote to registry file")
    except Exception as e:
        print(f"DEBUG: Error writing to registry file: {e}")
    
    print(f"✅ Updated MCP registry with {len(units)} units")
    print(f"Registry file: {REGISTRY_FILE}")

if __name__ == "__main__":
    # Set up debug log file
    debug_log_file = os.path.join(os.path.dirname(__file__), "update_registry_debug.log")
    with open(debug_log_file, "w") as log_file:
        # Redirect stdout to the log file
        original_stdout = sys.stdout
        sys.stdout = log_file
        
        try:
            print(f"DEBUG LOG: {debug_log_file}")
            print(f"Starting script at: {os.getcwd()}")
            print(f"MCP_UNITS_DIR: {MCP_UNITS_DIR}")
            print(f"REGISTRY_FILE: {REGISTRY_FILE}")
            
            # Update the registry
            update_registry()
            
            # Print the content of the registry file
            print("\nContent of the updated registry file:")
            try:
                with open(REGISTRY_FILE, "r") as f:
                    print(f.read())
            except Exception as e:
                print(f"Error reading registry file: {e}")
                print(traceback.format_exc())
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(traceback.format_exc())
        finally:
            # Restore stdout
            sys.stdout = original_stdout
    
    print(f"Debug log written to: {debug_log_file}")