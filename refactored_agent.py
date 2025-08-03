from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import numpy as np
from collections import deque
import random
import os
from src.cognition.rag_module import RAGModule
from src.cognition.gemini_integration import GeminiClient
from supabase_manager import SupabaseManager
from src.cognition.agent_tools import AgentTool, AVAILABLE_TOOLS
from input_data import InputData # New import
from src.cognition.memory_manager import MemoryManager

# 1. Conceitos de "Hands-On Machine Learning" (Scikit-Learn/Keras/TensorFlow)
class MLComponent:
    def __init__(self):
        self.model = self._build_model()

    def _build_model(self):
        """Simulação de modelo ML usando conceitos do livro"""
        return {
            'layers': ['input', 'dense_128', 'output'],
            'optimizer': 'adam',
            'metrics': ['accuracy']
        }

    def predict(self, input_data):
        """Processamento estilo scikit-learn"""
        return {'prediction': random.random(), 'confidence': np.random.rand()}

# 2. Princípios de "AI: A Modern Approach" (Russell & Norvig)
class IntelligentAgent(ABC):
    def __init__(self, agent_id: str, supabase_manager: Optional[SupabaseManager] = None, tools: Optional[Dict[str, AgentTool]] = None):
        self.agent_id = agent_id
        self.supabase_manager = supabase_manager
        self.memory_manager = MemoryManager(self.agent_id, supabase_manager) # Initialize MemoryManager
        self.tools = tools if tools is not None else {}

        # Initialize RAGModule
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
        pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "my-index") # Default index name

        if not pinecone_api_key or not pinecone_environment:
            print("WARNING: Pinecone API key or environment not set. RAG module will not be fully functional.")
            self.rag_module = None
        else:
            self.rag_module = RAGModule(pinecone_api_key, pinecone_environment, pinecone_index_name)

        # Initialize GeminiClient
        try:
            self.gemini_client = GeminiClient()
        except ValueError as e:
            print(f"WARNING: Gemini API key not set. Gemini integration will not be functional: {e}")
            self.gemini_client = None

        # Load state from DB if manager is provided
        if self.supabase_manager:
            self.load_state_from_db()

    def load_state_from_db(self):
        if self.supabase_manager:
            self.memory_manager.load_from_db()

    def save_state_to_db(self):
        if self.supabase_manager:
            self.memory_manager.save_to_db()

    @abstractmethod
    def perceive(self, environment: InputData):
        # Example of how RAG module could be used:
        if self.rag_module and environment.text:
            # Assuming 'environment' contains a query string
            query = environment.text # Or extract a specific query from environment
            results = self.rag_module.query_vectors(query)
            print(f"RAG search results for '{query}': {results}")
        pass

    @abstractmethod
    def act(self, intention: str, rag_context: str = "") -> str:
        # This method will be implemented in concrete agent classes to handle tool use.
        pass

    def bdi_loop(self):
        """Belief-Desire-Intention loop do livro"""
        while True:
            belief = self.perceive()
            desire = self._update_desires()
            intention = self._form_intention()
            self.act(intention)

# 3. Técnicas de "Deep Learning" (Goodfellow)
class NeuralAgentComponent:
    def __init__(self):
        self.nn_layers = self._init_layers()

    def _init_layers(self):
        """Arquitetura neural baseada no livro"""
        return [
            {'type': 'embedding', 'size': 256},
            {'type': 'transformer', 'heads': 8},
        ]
