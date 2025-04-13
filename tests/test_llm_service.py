# 📄 Script: test_llm_service.py
# 🔧 Zweck: Testfälle für die LLM-Inferenz-Komponente
# 🗂 Pfad: tests/test_llm_service.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: mcp_units.mcp_host_llm_infer.llm_service, unittest.mock
# 🧪 Testbar: ✅
# HINWEIS (MCP): Dieser Test überprüft die Funktionalität des LLM-Inferenzdienstes.
# HINWEIS (MCP): Er testet die Textgenerierungsfunktionen, Eingabevalidierung und
# HINWEIS (MCP): Fehlerbehandlung des Dienstes. Diese Tests sind wichtig für die
# HINWEIS (MCP): Qualitätssicherung der Sprachmodell-Interaktionen im MCP-System.

import unittest
from unittest.mock import patch, MagicMock
import pytest
import os
import sys
import time

from mcp_units.mcp_host_llm_infer.llm_service import generate_text, start_server

class TestLLMService:
    """Test class for the LLM Inference Service."""
    
    def test_generate_text_with_valid_prompt(self):
        """Test text generation with a valid prompt."""
        prompt = "Wie ist das Wetter heute?"
        result = generate_text(prompt)
        assert isinstance(result, str)
        assert prompt in result
        assert result.startswith("[MOCK-LLM]")
    
    def test_generate_text_with_empty_prompt(self):
        """Test text generation with an empty prompt."""
        # Test with empty string
        assert generate_text("") == "Kein Prompt angegeben."
        # Test with whitespace only
        assert generate_text("   ") == "Kein Prompt angegeben."
    
    def test_generate_text_with_help_keyword(self):
        """Test text generation with 'hilfe' in the prompt."""
        prompt = "Ich brauche hilfe bei meiner Aufgabe."
        result = generate_text(prompt)
        assert "Ich bin ein Platzhalter für ein Sprachmodell" in result
        assert "Was brauchst du?" in result
    
    def test_generate_text_case_insensitivity(self):
        """Test that the 'hilfe' keyword detection is case-insensitive."""
        prompt = "Ich brauche HILFE bei meiner Aufgabe."
        result = generate_text(prompt)
        assert "Ich bin ein Platzhalter für ein Sprachmodell" in result
    
    @patch('mcp_units.mcp_host_llm_infer.llm_service.logger')
    def test_generate_text_logging(self, mock_logger):
        """Test that text generation logs the prompt."""
        prompt = "Ein Test-Prompt für Logging."
        generate_text(prompt)
        mock_logger.info.assert_called_with(f"Generating text for prompt: {prompt[:50]}...")
    
    @patch('mcp_units.mcp_host_llm_infer.llm_service.time.sleep')
    @patch('mcp_units.mcp_host_llm_infer.llm_service.logger')
    def test_start_server_initialization(self, mock_logger, mock_sleep):
        """Test server initialization and logging."""
        # Configure mock to raise KeyboardInterrupt after first sleep to exit the loop
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # Call the function
        start_server()
        
        # Verify logging calls
        mock_logger.info.assert_any_call("Starting LLM inference server...")
        mock_logger.info.assert_any_call(f"Process ID: {os.getpid()}")
        mock_logger.info.assert_any_call(f"Working directory: {os.getcwd()}")
        mock_logger.info.assert_any_call("LLM inference server is running...")
        mock_logger.info.assert_any_call("LLM inference server shutting down...")
        mock_logger.info.assert_any_call("LLM inference server stopped.")
    
    @patch('mcp_units.mcp_host_llm_infer.llm_service.time.sleep')
    @patch('mcp_units.mcp_host_llm_infer.llm_service.logger')
    def test_start_server_exception_handling(self, mock_logger, mock_sleep):
        """Test server exception handling."""
        # Configure mock to raise an Exception after first sleep
        mock_sleep.side_effect = Exception("Test exception")
        
        # Call the function
        start_server()
        
        # Verify error logging
        mock_logger.error.assert_called_once_with("Error in LLM inference server: Test exception")
        mock_logger.info.assert_any_call("LLM inference server stopped.")

    def test_generate_text_with_long_prompt(self):
        """Test text generation with a very long prompt."""
        long_prompt = "A" * 1000  # A 1000-character prompt
        result = generate_text(long_prompt)
        assert isinstance(result, str)
        assert "[MOCK-LLM]" in result
        # Verify the prompt is included in the response (though it might be truncated in logs)
        assert "Du hast gefragt: 'A" in result
# HINWEIS (MCP): Verwendet absolute Pfade, um von jedem Verzeichnis aus ausführbar zu sein
if __name__ == "__main__":
    pytest.main(["-v", __file__])
    pytest.main(["-v", "test_llm_service.py"])