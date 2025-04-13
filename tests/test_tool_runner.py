# 📄 Script: test_tool_runner.py
# 🔧 Zweck: Testfälle für die Tool-Executor-Komponente
# 🗂 Pfad: tests/test_tool_runner.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_tool_executor.tool_runner, unittest.mock
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität des Tool-Executor-Dienstes.
# HINWEIS (MCP): Er testet die Befehlsausführungsfunktionen, Eingabevalidierung und
# HINWEIS (MCP): Fehlerbehandlung des Dienstes. Diese Tests sind wichtig für die
# HINWEIS (MCP): Qualitätssicherung der Werkzeugausführung im MCP-System.

import unittest
from unittest.mock import patch, MagicMock
import pytest
import os
import sys
import time
import subprocess

from mcp_units.mcp_tool_executor.tool_runner import run_shell_command, start_server

class TestToolRunner:
    """Test class for the Tool Executor Service."""
    
    def test_run_shell_command_with_valid_command(self):
        """Test command execution with a valid command."""
        with patch('subprocess.check_output') as mock_check_output:
            mock_check_output.return_value = "Command output"
            result = run_shell_command("echo Hello")
            assert result == "Command output"
            mock_check_output.assert_called_once_with("echo Hello", shell=True, stderr=subprocess.STDOUT, text=True)
    
    def test_run_shell_command_with_empty_command(self):
        """Test command execution with an empty command."""
        # Test with empty string
        assert run_shell_command("") == "Kein Befehl eingegeben."
        # Test with whitespace only
        assert run_shell_command("   ") == "Kein Befehl eingegeben."
    
    def test_run_shell_command_with_error(self):
        """Test command execution with a command that raises an error."""
        with patch('subprocess.check_output') as mock_check_output:
            error = subprocess.CalledProcessError(1, "invalid_command")
            error.output = "Command not found"
            mock_check_output.side_effect = error
            
            result = run_shell_command("invalid_command")
            assert "Fehler:" in result
            assert "Command not found" in result
    
    @patch('mcp_units.mcp_tool_executor.tool_runner.logger')
    def test_run_shell_command_logging(self, mock_logger):
        """Test that command execution is properly logged."""
        with patch('subprocess.check_output') as mock_check_output:
            mock_check_output.return_value = "Command output"
            run_shell_command("echo Hello")
            # Verify logging is not implemented in the current version
            # This test can be expanded when logging is added to run_shell_command
    
    @patch('mcp_units.mcp_tool_executor.tool_runner.time.sleep')
    @patch('mcp_units.mcp_tool_executor.tool_runner.logger')
    def test_start_server_initialization(self, mock_logger, mock_sleep):
        """Test server initialization and logging."""
        # Configure mock to raise KeyboardInterrupt after first sleep to exit the loop
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # Call the function
        start_server()
        
        # Verify logging calls
        mock_logger.info.assert_any_call("Starting tool runner server...")
        mock_logger.info.assert_any_call(f"Process ID: {os.getpid()}")
        mock_logger.info.assert_any_call(f"Working directory: {os.getcwd()}")
        mock_logger.info.assert_any_call("Tool runner server is running...")
        mock_logger.info.assert_any_call("Tool runner server shutting down...")
        mock_logger.info.assert_any_call("Tool runner server stopped.")
    
    @patch('mcp_units.mcp_tool_executor.tool_runner.time.sleep')
    @patch('mcp_units.mcp_tool_executor.tool_runner.logger')
    def test_start_server_exception_handling(self, mock_logger, mock_sleep):
        """Test server exception handling."""
        # Configure mock to raise an Exception after first sleep
        mock_sleep.side_effect = Exception("Test exception")
        
        # Call the function
        start_server()
        
        # Verify error logging
        mock_logger.error.assert_called_once_with("Error in tool runner server: Test exception")
        mock_logger.info.assert_any_call("Tool runner server stopped.")
    
    def test_run_shell_command_with_complex_command(self):
        """Test command execution with a more complex command."""
        with patch('subprocess.check_output') as mock_check_output:
            mock_check_output.return_value = "file1.txt\nfile2.txt\nfile3.txt"
            result = run_shell_command("ls -la | grep .txt")
            assert "file1.txt" in result
            assert "file2.txt" in result
            assert "file3.txt" in result
            mock_check_output.assert_called_once_with("ls -la | grep .txt", shell=True, stderr=subprocess.STDOUT, text=True)
    
    def test_run_shell_command_with_long_output(self):
        """Test command execution with a command that produces long output."""
        with patch('subprocess.check_output') as mock_check_output:
            # Generate a long output string
            long_output = "\n".join([f"Line {i}" for i in range(1, 1001)])
            mock_check_output.return_value = long_output
            
            result = run_shell_command("cat large_file.txt")
            assert result == long_output.strip()
            mock_check_output.assert_called_once_with("cat large_file.txt", shell=True, stderr=subprocess.STDOUT, text=True)
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])
    pytest.main(["-v", "test_tool_runner.py"])