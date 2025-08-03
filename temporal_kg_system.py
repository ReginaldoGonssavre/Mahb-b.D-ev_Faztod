import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Literal
import numpy as np
from dataclasses import dataclass
from enum import Enum, auto
import re
import os

# External libraries
import networkx as nx
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, SimpleImputer
from rapidfuzz import process, fuzz

# OpenAI (assuming client setup)
# from openai import OpenAI # Uncomment if using OpenAI Python client directly
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Configuration ---
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL_FOR_AGENTS = "gpt-4o" # Or "gpt-4-turbo", "gemini-pro", etc.

# --- 1. Temporal Agent Pipeline Components ---

class StatementType(Enum):
    FACT = auto()
    OPINION = auto()
    PREDICTION = auto()

class TemporalNature(Enum):
    STATIC = auto()
    DYNAMIC = auto()
    ATEMPORAL = auto()

@dataclass
class Triplet:
    subject: str
    predicate: str
    obj: str
    valid_at: Optional[datetime] = None
    invalid_at: Optional[datetime] = None
    statement_type: StatementType = StatementType.FACT
    temporal_nature: TemporalNature = TemporalNature.ATEMPORAL
    source_text: str = ""
    confidence: float = 1.0
    metadata: Dict[str, Any] = None

class SemanticChunker:
    """
    Realiza o chunking semântico de texto e gera embeddings.
    Para um sistema real, isso envolveria um modelo de embedding da OpenAI.
    """
    def __init__(self, embedding_model: str = OPENAI_EMBEDDING_MODEL):
        self.embedding_model = embedding_model
        # self.openai_client = client # Initialize OpenAI client here if needed

    def chunk_and_embed(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
        """
        Divide o texto em chunks e gera embeddings para cada um.
        (Simulação para demonstração; em produção, usaria um modelo real)
        """
        chunks = []
        # Simple chunking for demonstration
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                # In a real scenario, call OpenAI API for embedding:
                # response = self.openai_client.embeddings.create(input=[chunk], model=self.embedding_model)
                # embedding = response.data[0].embedding
                embedding = np.random.rand(1536).tolist() # Placeholder embedding
                chunks.append({"text": chunk, "embedding": embedding})
        return chunks

class TripletExtractor:
    """
    Extrai triplets (sujeito-predicado-objeto) e metadados temporais de texto.
    Em um sistema real, isso usaria um LLM para extração estruturada.
    """
    def __init__(self, llm_model: str = LLM_MODEL_FOR_AGENTS):
        self.llm_model = llm_model
        # self.openai_client = client # Initialize OpenAI client here if needed

    def extract(self, text: str) -> List[Triplet]:
        """
        Extrai triplets com validade temporal e classificação.
        (Simulação para demonstração; em produção, usaria um LLM)
        """
        triplets = []
        # Placeholder for LLM-based extraction
        # Example: "AMD launched Ryzen in 2017. NVIDIA's CEO was Jensen Huang in 2020."
        if "AMD launched Ryzen in 2017" in text:
            triplets.append(Triplet(
                subject="AMD",
                predicate="launched",
                obj="Ryzen",
                valid_at=datetime(2017, 1, 1),
                statement_type=StatementType.FACT,
                temporal_nature=TemporalNature.DYNAMIC,
                source_text=text
            ))
        if "NVIDIA's CEO was Jensen Huang in 2020" in text:
            triplets.append(Triplet(
                subject="NVIDIA's CEO",
                predicate="was",
                obj="Jensen Huang",
                valid_at=datetime(2020, 1, 1),
                statement_type=StatementType.FACT,
                temporal_nature=TemporalNature.STATIC, # Static for that specific time
                source_text=text
            ))
        if "AMD's R&D priority shifted to AI in 2018" in text:
             triplets.append(Triplet(
                subject="AMD's R&D priority",
                predicate="shifted to",
                obj="AI",
                valid_at=datetime(2018, 1, 1),
                statement_type=StatementType.FACT,
                temporal_nature=TemporalNature.DYNAMIC,
                source_text=text
            ))
        if "NVIDIA focused on GPUs for gaming until 2019" in text:
            triplets.append(Triplet(
                subject="NVIDIA",
                predicate="focused on",
                obj="GPUs for gaming",
                valid_at=datetime(2016, 1, 1), # Assuming this was true from 2016
                invalid_at=datetime(2019, 12, 31),
                statement_type=StatementType.FACT,
                temporal_nature=TemporalNature.DYNAMIC,
                source_text=text
            ))
        return triplets

class StatementClassifier:
    """
    Classifica declarações em FACT/OPINION/PREDICTION e STATIC/DYNAMIC/ATEMPORAL.
    """
    def __init__(self, llm_model: str = LLM_MODEL_FOR_AGENTS):
        self.llm_model = llm_model
        # self.openai_client = client # Initialize OpenAI client here if needed

    def classify(self, statement: str) -> Tuple[StatementType, TemporalNature]:
        """
        Classifica uma declaração.
        (Simulação; em produção, usaria um LLM para análise semântica)
        """
        # Placeholder for LLM-based classification
        if "will" in statement or "expect" in statement:
            stmt_type = StatementType.PREDICTION
        elif "believe" in statement or "think" in statement:
            stmt_type = StatementType.OPINION
        else:
            stmt_type = StatementType.FACT

        if any(kw in statement.lower() for kw in ["changed", "shifted", "evolved"]):
            temporal_nature = TemporalNature.DYNAMIC
        elif any(kw in statement.lower() for kw in ["always", "never", "constant"]):
            temporal_nature = TemporalNature.ATEMPORAL
        else:
            temporal_nature = TemporalNature.STATIC # Default for a single point in time
        return stmt_type, temporal_nature

# --- 2. Critical Components ---

class EntityResolver:
    """
    Resolve entidades usando fuzzy matching para padronização.
    """
    def __init__(self, known_entities: List[str]):
        self.known_entities = known_entities

    def resolve(self, entity_name: str) -> str:
        """
        Resolve um nome de entidade para uma entidade conhecida usando fuzzy matching.
        """
        if not self.known_entities:
            return entity_name # No entities to resolve against

        # Use rapidfuzz to find the best match
        best_match = process.extractOne(entity_name, self.known_entities, scorer=fuzz.ratio)
        if best_match and best_match[1] > 80:  # Threshold for a good match
            return best_match[0]
        return entity_name # Return original if no good match

class InvalidationAgent:
    """
    Agente com LLM para detectar e gerenciar conflitos temporais em declarações.
    """
    def __init__(self, llm_model: str = LLM_MODEL_FOR_AGENTS):
        self.llm_model = llm_model
        # self.openai_client = client # Initialize OpenAI client here if needed

    def detect_and_invalidate(self, new_triplet: Triplet, existing_triplets: List[Triplet]) -> List[Triplet]:
        """
        Detecta conflitos temporais e invalida triplets antigos se necessário.
        (Simulação; em produção, usaria um LLM para raciocínio complexo)
        """
        updated_triplets = existing_triplets[:]
        for existing_t in existing_triplets:
            # Exemplo simplificado de detecção de conflito:
            # Se o mesmo sujeito e predicado têm objetos diferentes em períodos sobrepostos.
            if (
                new_triplet.subject == existing_t.subject and
                new_triplet.predicate == existing_t.predicate and
                new_triplet.obj != existing_t.obj
            ):

                # Verifica sobreposição temporal
                overlap = False
                if new_triplet.valid_at and existing_t.valid_at:
                    # Se ambos têm valid_at, verifica se o novo começa antes do antigo terminar
                    # ou se o antigo começa antes do novo terminar
                    if (
                        new_triplet.valid_at <= (existing_t.invalid_at or datetime.max) and
                        (new_triplet.invalid_at or datetime.max) >= existing_t.valid_at
                    ):
                        overlap = True
                elif new_triplet.valid_at and not existing_t.valid_at:
                    # Se o novo tem valid_at e o antigo não (assumindo validade contínua)
                    overlap = True # Simplificação: qualquer novo dado pode invalidar um antigo sem data de fim

                if overlap:
                    # LLM call to confirm invalidation and determine invalid_at for old triplet
                    # prompt = f"A nova afirmação '{new_triplet.subject} {new_triplet.predicate} {new_triplet.obj} (válido a partir de {new_triplet.valid_at})' conflita com a afirmação existente '{existing_t.subject} {existing_t.predicate} {existing_t.obj} (válido de {existing_t.valid_at} até {existing_t.invalid_at})'? Se sim, qual a data de invalidação para a afirmação antiga?"
                    # response = self.openai_client.chat.completions.create(...)
                    # decision = response.choices[0].message.content

                    # Simulação da decisão do LLM
                    print(f"Conflito potencial detectado: Nova '{new_triplet.subject} {new_triplet.predicate} {new_triplet.obj}' vs. Existente '{existing_t.subject} {existing_t.predicate} {existing_t.obj}'.")
                    print(f"Decisão temporal (simulada): Invalidar a afirmação existente a partir da data de validade da nova.")

                    # Invalida o triplet existente
                    existing_t.invalid_at = new_triplet.valid_at - timedelta(microseconds=1) if new_triplet.valid_at else datetime.now()
                    print(f"  -> Afirmação existente invalidada até: {existing_t.invalid_at}")

        return updated_triplets

# --- Temporal Knowledge Graph ---

class TemporalKnowledgeGraph:
    """
    Representa o grafo de conhecimento temporal usando NetworkX.
    """
    def __init__(self):
        self.graph = nx.MultiDiGraph() # MultiDiGraph para permitir múltiplas arestas entre nós (diferentes predicados/tempos)
        self.triplets: List[Triplet] = []
        self.entity_resolver = EntityResolver(known_entities=[]) # Inicializa vazio, será populado

    def add_triplet(self, triplet: Triplet):
        """Adiciona um triplet ao grafo e à lista de triplets."""
        # Resolve entidades antes de adicionar
        triplet.subject = self.entity_resolver.resolve(triplet.subject)
        triplet.obj = self.entity_resolver.resolve(triplet.obj)

        # Adiciona/atualiza entidades conhecidas para resolução futura
        if triplet.subject not in self.entity_resolver.known_entities:
            self.entity_resolver.known_entities.append(triplet.subject)
        if triplet.obj not in self.entity_resolver.known_entities:
            self.entity_resolver.known_entities.append(triplet.obj)

        # Adiciona nós se não existirem
        if not self.graph.has_node(triplet.subject):
            self.graph.add_node(triplet.subject, type="entity")
        if not self.graph.has_node(triplet.obj):
            self.graph.add_node(triplet.obj, type="entity")

        # Adiciona a aresta com atributos temporais e de declaração
        edge_attributes = {
            "predicate": triplet.predicate,
            "valid_at": triplet.valid_at,
            "invalid_at": triplet.invalid_at,
            "statement_type": triplet.statement_type.name,
            "temporal_nature": triplet.temporal_nature.name,
            "source_text": triplet.source_text,
            "confidence": triplet.confidence,
            "metadata": triplet.metadata
        }
        self.graph.add_edge(triplet.subject, triplet.obj, key=triplet.predicate, **edge_attributes)
        self.triplets.append(triplet)

    def get_triplets_at_time(self, query_time: datetime) -> List[Triplet]:
        """Retorna triplets válidos em um determinado ponto no tempo."""
        valid_triplets = []
        for triplet in self.triplets:
            is_valid_at = (triplet.valid_at is None or triplet.valid_at <= query_time)
            is_invalid_at = (triplet.invalid_at is None or triplet.invalid_at >= query_time)
            if is_valid_at and is_invalid_at:
                valid_triplets.append(triplet)
        return valid_triplets

    def get_triplets_in_range(self, start_time: datetime, end_time: datetime) -> List[Triplet]:
        """Retorna triplets válidos em algum momento dentro de um intervalo de tempo."""
        relevant_triplets = []
        for triplet in self.triplets:
            # Triplet is relevant if its validity period overlaps with the query range
            triplet_start = triplet.valid_at if triplet.valid_at else datetime.min
            triplet_end = triplet.invalid_at if triplet.invalid_at else datetime.max

            if max(triplet_start, start_time) <= min(triplet_end, end_time):
                relevant_triplets.append(triplet)
        return relevant_triplets

# --- Temporal Agent Pipeline Orchestrator ---

class TemporalAgentPipeline:
    """
    Orquestra o pipeline do agente temporal.
    """
    def __init__(self, known_entities: List[str] = None):
        self.chunker = SemanticChunker()
        self.extractor = TripletExtractor()
        self.classifier = StatementClassifier()
        self.entity_resolver = EntityResolver(known_entities if known_entities is not None else [])
        self.invalidation_agent = InvalidationAgent()
        self.knowledge_graph = TemporalKnowledgeGraph()
        self.knowledge_graph.entity_resolver = self.entity_resolver # Link resolver to graph

    def process_document(self, document_text: str):
        """Processa um documento completo através do pipeline."""
        print(f"Processando documento: {document_text[:100]}...")
        chunks = self.chunker.chunk_and_embed(document_text)
        for chunk_data in chunks:
            text_chunk = chunk_data["text"]
            extracted_triplets = self.extractor.extract(text_chunk)
            for triplet in extracted_triplets:
                # Classificação da declaração
                stmt_type, temporal_nature = self.classifier.classify(triplet.source_text)
                triplet.statement_type = stmt_type
                triplet.temporal_nature = temporal_nature

                # Resolução de entidades
                triplet.subject = self.entity_resolver.resolve(triplet.subject)
                triplet.obj = self.entity_resolver.resolve(triplet.obj)

                # Detecção de conflitos e invalidação
                # Passa uma cópia para o agente de invalidação para evitar modificação durante iteração
                self.knowledge_graph.triplets = self.invalidation_agent.detect_and_invalidate(
                    triplet, self.knowledge_graph.triplets
                )

                # Adiciona o triplet (potencialmente atualizado) ao grafo
                self.knowledge_graph.add_triplet(triplet)
        print("Documento processado e grafo atualizado.")

# --- 3. Multi-Step Retrieval ---

class RetrievalTools:
    """
    Ferramentas para recuperação de informações multi-passos.
    """
    def __init__(self, knowledge_graph: TemporalKnowledgeGraph, llm_model: str = LLM_MODEL_FOR_AGENTS):
        self.kg = knowledge_graph
        self.llm_model = llm_model
        # self.openai_client = client # Initialize OpenAI client here if needed

    def factual_qa(self, query: str, query_time: Optional[datetime] = None, time_range: Optional[Tuple[datetime, datetime]] = None) -> str:
        """
        Responde a perguntas factuais com base no grafo de conhecimento temporal.
        Pode especificar um ponto no tempo ou um intervalo.
        """
        if query_time:
            relevant_triplets = self.kg.get_triplets_at_time(query_time)
            time_context = f"no ponto no tempo {query_time.strftime('%Y-%m-%d')}"
        elif time_range:
            relevant_triplets = self.kg.get_triplets_in_range(time_range[0], time_range[1])
            time_context = f"no intervalo de {time_range[0].strftime('%Y-%m-%d')} a {time_range[1].strftime('%Y-%m-%d')}"
        else:
            relevant_triplets = self.kg.triplets # All triplets
            time_context = "em todo o histórico"

        if not relevant_triplets:
            return f"Não encontrei informações relevantes para '{query}' {time_context}."

        # Simulação de LLM para sintetizar a resposta
        context_for_llm = "\n".join([
            f"- {t.subject} {t.predicate} {t.obj} (Válido de {t.valid_at.strftime('%Y-%m-%d') if t.valid_at else 'sem início'} até {t.invalid_at.strftime('%Y-%m-%d') if t.invalid_at else 'sem fim'})"
            for t in relevant_triplets
        ])
        # In a real scenario, send context_for_llm and query to LLM
        # prompt = f"Com base nas seguintes informações temporais:\n{context_for_llm}\n\nResponda à pergunta: '{query}' {time_context}."
        # response = self.openai_client.chat.completions.create(...)
        # answer = response.choices[0].message.content
        answer = f"Com base nas informações disponíveis {time_context}, encontrei os seguintes fatos relevantes para '{query}':\n{context_for_llm}\n\n(Esta é uma resposta simulada do LLM.)"
        return answer

    def trend_analysis(self, entity: str, predicate: str, start_time: datetime, end_time: datetime) -> str:
        """
        Compara tendências para uma entidade e predicado ao longo do tempo.
        """
        relevant_triplets = self.kg.get_triplets_in_range(start_time, end_time)
        entity_history = [
            t for t in relevant_triplets
            if self.kg.entity_resolver.resolve(t.subject) == self.kg.entity_resolver.resolve(entity) and t.predicate == predicate
        ]

        if not entity_history:
            return f"Não encontrei dados de tendência para '{entity}' e predicado '{predicate}' entre {start_time.year}-{end_time.year}."

        # Sort by valid_at to show temporal progression
        entity_history.sort(key=lambda t: t.valid_at if t.valid_at else datetime.min)

        trend_summary = f"Análise de tendência para '{entity}' e '{predicate}' de {start_time.year} a {end_time.year}:\n"
        for t in entity_history:
            valid_str = t.valid_at.strftime('%Y-%m-%d') if t.valid_at else 'sem início'
            invalid_str = t.invalid_at.strftime('%Y-%m-%d') if t.invalid_at else 'sem fim'
            trend_summary += f"- Em {valid_str} (até {invalid_str}): {t.subject} {t.predicate} {t.obj} (Tipo: {t.statement_type.name}, Natureza: {t.temporal_nature.name})\n"

        # LLM call to synthesize trend
        # prompt = f"Analise a seguinte história temporal para '{entity}' e '{predicate}':\n{trend_summary}\n\nDescreva a tendência ou divergência observada."
        # response = self.openai_client.chat.completions.create(...)
        # analysis = response.choices[0].message.content
        analysis = f"{trend_summary}\n\n(Esta é uma análise de tendência simulada do LLM, baseada nos dados acima.)"
        return analysis

# --- Main Pipeline Example ---

def run_temporal_agent_system():
    """
    Demonstra o pipeline completo do sistema de agente temporal.
    """
    print("--- Inicializando Sistema de Agente Temporal ---")

    # 1. Configuração do pré-processador (scikit-learn)
    # Exemplo de dados para o pré-processador (não diretamente usado no pipeline de KG, mas para demonstração)
    # Imagine que estes são dados tabulares associados a documentos ou entidades.
    example_data_schema = {
        'revenue': 'numerical',
        'year': 'numerical',
        'industry': 'categorical',
        'country': 'categorical'
    }
    # Para um uso real, você passaria um DataFrame para o fit/transform
    # from pandas import DataFrame
    # df = DataFrame(...)

    # Pré-processamento com SimpleImputer para dados faltantes
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, ['revenue', 'year']),
            ('cat', categorical_transformer, ['industry', 'country'])
        ])

    print("\n--- Pré-processador scikit-learn configurado ---")
    print("Exemplo de uso: preprocessor.fit_transform(df)")

    # 2. Inicialização do pipeline do agente temporal
    # Entidades conhecidas iniciais para o resolvedor de entidades
    initial_known_entities = ["AMD", "NVIDIA", "Intel", "Lisa Su", "Jensen Huang", "GPU", "CPU", "AI"]
    temporal_agent_pipeline = TemporalAgentPipeline(known_entities=initial_known_entities)

    # 3. Processamento de documentos de exemplo
    document1 = "AMD launched Ryzen in 2017, which significantly impacted the CPU market. Lisa Su became CEO of AMD in 2014. NVIDIA's CEO was Jensen Huang in 2020, and they focused heavily on GPUs for gaming until 2019."
    document2 = "In 2018, AMD's R&D priority shifted towards AI and high-performance computing, moving beyond just CPUs. NVIDIA also started to heavily invest in AI research from 2017 onwards, diverging from their primary gaming GPU focus."
    document3 = "By 2020, both AMD and NVIDIA were competing fiercely in the AI chip market. Jensen Huang stated in 2021 that NVIDIA's future is in accelerated computing for AI."

    print("\n--- Processando Documentos ---")
    temporal_agent_pipeline.process_document(document1)
    temporal_agent_pipeline.process_document(document2)
    temporal_agent_pipeline.process_document(document3)

    print("\n--- Grafo de Conhecimento Temporal Final ---")
    for i, triplet in enumerate(temporal_agent_pipeline.knowledge_graph.triplets):
        valid_at_str = triplet.valid_at.strftime('%Y-%m-%d') if triplet.valid_at else 'N/A'
        invalid_at_str = triplet.invalid_at.strftime('%Y-%m-%d') if triplet.invalid_at else 'N/A'
        print(f"Triplet {i+1}: {triplet.subject} - {triplet.predicate} - {triplet.obj}")
        print(f"  Válido de: {valid_at_str}, Inválido em: {invalid_at_str}")
        print(f"  Tipo: {triplet.statement_type.name}, Natureza: {triplet.temporal_nature.name}")
        print(f"  Fonte: \"{triplet.source_text[:50]}...\"")
        print(f"  Confiança: {triplet.confidence}\n")

    # 4. Demonstração de Multi-Step Retrieval
    retrieval_tools = RetrievalTools(temporal_agent_pipeline.knowledge_graph)

    print("\n--- Demonstração de Recuperação Multi-Passos ---")

    # Exemplo de pergunta: 'Como as prioridades de R&D da AMD e NVIDIA divergiram de 2016-2020?'
    print("\nPergunta: Como as prioridades de R&D da AMD e NVIDIA divergiram de 2016-2020?")

    # Análise de tendência para AMD
    amd_trend = retrieval_tools.trend_analysis(
        entity="AMD",
        predicate="R&D priority shifted towards", # Predicado ajustado para o que foi extraído
        start_time=datetime(2016, 1, 1),
        end_time=datetime(2020, 12, 31)
    )
    print("\nAnálise de Tendência AMD:")
    print(amd_trend)

    # Análise de tendência para NVIDIA
    nvidia_trend = retrieval_tools.trend_analysis(
        entity="NVIDIA",
        predicate="invested in", # Predicado ajustado
        start_time=datetime(2016, 1, 1),
        end_time=datetime(2020, 12, 31)
    )
    print("\nAnálise de Tendência NVIDIA:")
    print(nvidia_trend)

    # LLM para sintetizar a divergência (simulação)
    print("\nSíntese da Divergência (Simulada por LLM):")
    print("Com base nas análises acima, a AMD mudou seu foco de P&D para IA e HPC a partir de 2018, enquanto a NVIDIA já estava investindo pesadamente em IA desde 2017, divergindo de seu foco principal em GPUs para jogos. Ambas as empresas convergiram para o mercado de chips de IA em 2020.")

    # Exemplo de QA factual em um ponto no tempo
    print("\nQA Factual: Quem era o CEO da NVIDIA em 2020?")
    qa_result = retrieval_tools.factual_qa(
        query="Quem era o CEO da NVIDIA?",
        query_time=datetime(2020, 6, 1)
    )
    print(qa_result)

    # Exemplo de QA factual em um intervalo
    print("\nQA Factual: O que a NVIDIA focou entre 2016 e 2019?")
    qa_result_range = retrieval_tools.factual_qa(
        query="O que a NVIDIA focou?",
        time_range=(datetime(2016, 1, 1), datetime(2019, 12, 31))
    )
    print(qa_result_range)

    print("\n--- Demonstração Concluída ---")

if __name__ == "__main__":
    # Para rodar este script, você precisará instalar as bibliotecas:
    # pip install numpy scikit-learn networkx rapidfuzz
    # Se for usar OpenAI, também: pip install openai
    # E definir a variável de ambiente OPENAI_API_KEY
    run_temporal_agent_system()
