# 📄 Script: test_integration_mcp.py
# 🔧 Zweck: Integrationstests für MCP-Komponenten
# 🗂 Pfad: tests/test_integration_mcp.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: pytest, unittest.mock
# 🧪 Testbar: ✅
# HINWEIS (MCP): Diese Testdatei implementiert Integrationstests zwischen verschiedenen MCP-Einheiten.
# HINWEIS (MCP): Sie überprüft die korrekte Interaktion und Datenflüsse zwischen den Komponenten
# HINWEIS (MCP): und stellt sicher, dass die Einheiten als Gesamtsystem funktionieren.
# HINWEIS (MCP): Die Tests simulieren reale Verarbeitungsketten und prüfen die Fehlerbehandlung.

import unittest
from unittest.mock import patch, MagicMock, call
import pytest
import os
import sys
import json

# Import the MCP units
from mcp_units.mcp_agent_interaction_engine.graph_executor import invoke_graph
from mcp_units.mcp_host_llm_infer.llm_service import generate_text
from mcp_units.mcp_host_memory_store.memory_handler import write_memory, read_memory, persist_memory
from mcp_units.mcp_tool_executor.tool_runner import run_shell_command

class TestGraphExecutorWithLLM:
    """Integration tests for Dialog Flow and LLM Inference interaction."""
    
    @patch('mcp_units.mcp_agent_interaction_engine.graph.build_graph')
    def test_invoke_graph_calls_build_graph(self, mock_build_graph):
        """Test that invoke_graph correctly calls build_graph."""
        # Arrange
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {"output": "Mocked response"}
        mock_build_graph.return_value = mock_graph
        user_input = "Hallo, wie geht es dir?"
        
        # Act
        response = invoke_graph(user_input)
        
        # Assert
        mock_build_graph.assert_called_once()
        mock_graph.invoke.assert_called_once()
        assert response["output"] == "Mocked response"
    
    @patch('mcp_units.mcp_host_llm_infer.llm_service.generate_text')
    def test_graph_executor_with_llm_integration(self, mock_generate_text):
        """Test integration between graph executor and LLM service."""
        # Arrange
        mock_generate_text.return_value = "Ich bin ein Sprachmodell und kann dir helfen."
        
        # Mock the graph to use the LLM service
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {
            "output": mock_generate_text.return_value,
            "nodes_visited": ["llm_node"]
        }
        
        # Act
        with patch('mcp_units.mcp_agent_interaction_engine.graph.build_graph',
                  return_value=mock_graph):
            response = invoke_graph("Was kannst du als Sprachmodell?")
        
        # Assert
        assert response["output"] == "Ich bin ein Sprachmodell und kann dir helfen."
    
    def test_graph_executor_error_handling_with_llm(self):
        """Test error handling in the integration between graph executor and LLM."""
        # Arrange
        mock_graph = MagicMock()
        mock_graph.invoke.return_value = {
            "output": "Entschuldigung, der Dienst ist momentan nicht verfügbar.",
            "error": "LLM service unavailable"
        }
        
        # Act & Assert
        with patch('mcp_units.mcp_agent_interaction_engine.graph.build_graph',
                  return_value=mock_graph):
            response = invoke_graph("Komplexe Anfrage")
            assert "nicht verfügbar" in response["output"]


class TestToolExecutorWithMemoryStore:
    """Integration tests for Tool Executor and Memory Store interaction."""
    
    @patch('mcp_units.mcp_host_memory_store.memory_handler.persist_memory')
    def test_command_result_stored_in_memory(self, mock_persist_memory):
        """Test that command execution results are stored in memory."""
        # Arrange
        with patch('mcp_units.mcp_tool_executor.tool_runner.run_shell_command', 
                  return_value="Command output"):
            with patch('mcp_units.mcp_host_memory_store.memory_handler.write_memory') as mock_write_memory:
                
                # Act
                # Simulate a workflow where a command is executed and its result stored
                command = "echo Hello World"
                command_result = run_shell_command(command)
                write_memory("last_command_result", command_result)
                
                # Assert
                mock_write_memory.assert_called_once_with("last_command_result", "Command output")
                mock_persist_memory.assert_called_once()
    
    @patch('mcp_units.mcp_host_memory_store.memory_handler.read_memory')
    def test_tool_executor_uses_stored_command(self, mock_read_memory):
        """Test that tool executor uses commands stored in memory."""
        # Arrange
        mock_read_memory.return_value = "echo Hello from memory"
        
        with patch('mcp_units.mcp_tool_executor.tool_runner.run_shell_command') as mock_run_command:
            mock_run_command.return_value = "Hello from memory"
            
            # Act
            # Simulate retrieving a stored command from memory and executing it
            stored_command = read_memory("saved_command")
            result = run_shell_command(stored_command)
            
            # Assert
            mock_read_memory.assert_called_once_with("saved_command")
            mock_run_command.assert_called_once_with("echo Hello from memory")
            assert result == "Hello from memory"
    
    def test_error_handling_between_tool_and_memory(self):
        """Test error handling in the integration between tool executor and memory store."""
        # Arrange
        with patch('mcp_units.mcp_host_memory_store.memory_handler.write_memory', 
                  side_effect=Exception("Memory write error")):
            with patch('mcp_units.mcp_tool_executor.tool_runner.run_shell_command', 
                      return_value="Command executed successfully"):
                
                # Act & Assert
                # In a real integration, there would be error handling code
                # Here we're testing that errors in one component don't crash the other
                try:
                    # Execute command
                    result = run_shell_command("echo test")
                    assert result == "Command executed successfully"
                    
                    # Try to store result (this will fail)
                    write_memory("last_result", result)
                    pytest.fail("Should have raised an exception")
                except Exception as e:
                    assert str(e) == "Memory write error"


class TestCompleteProcessingChain:
    """Integration tests for a complete processing chain involving multiple MCP units."""
    
    def test_end_to_end_processing_chain(self):
        """Test a complete processing chain from user input to command execution and storage."""
        # Arrange
        user_query = "Führe den Befehl 'echo Hello MCP' aus"
        
        # Mock all the components in the chain
        with patch('mcp_units.mcp_agent_interaction_engine.graph.build_graph') as mock_build_graph:
            mock_graph = MagicMock()
            mock_graph.invoke.return_value = {"output": "Ich führe den Befehl aus"}
            mock_build_graph.return_value = mock_graph
            with patch('mcp_units.mcp_tool_executor.tool_runner.run_shell_command', 
                      return_value="Hello MCP"):
                with patch('mcp_units.mcp_host_memory_store.memory_handler.write_memory') as mock_write_memory:
                    with patch('mcp_units.mcp_host_memory_store.memory_handler.persist_memory') as mock_persist:
                        
                        # Act - Simulate the complete chain
                        # 1. Handle user input
                        dialog_response = invoke_graph(user_query)["output"]
                        
                        # 2. Extract and execute command (in a real system, this would be parsed from the input)
                        command = "echo Hello MCP"
                        command_result = run_shell_command(command)
                        
                        # 3. Store the result in memory
                        write_memory("last_command", command)
                        write_memory("last_result", command_result)
                        
                        # Assert
                        assert dialog_response == "Ich führe den Befehl aus"
                        assert command_result == "Hello MCP"
                        
                        # Verify memory interactions
                        assert mock_write_memory.call_count == 2
                        mock_write_memory.assert_has_calls([
                            call("last_command", "echo Hello MCP"),
                            call("last_result", "Hello MCP")
                        ])
                        assert mock_persist.call_count == 2


# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])