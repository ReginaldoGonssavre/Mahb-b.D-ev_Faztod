#!/bin/bash
# AI Terms CLI - Baseado na imagem educativa da Mindstream (40 termos)
# Modo educacional e integrativo: ajuda a consultar rapidamente definições de IA.

echo "🧠 Bem-vindo ao AI Terms CLI"
echo "Use: ./ai-terms.sh [termo]"
echo "Exemplo: ./ai-terms.sh model"

declare -A TERMS

TERMS["bias"]="When an AI unfairly prefers one thing, often because of the data it was trained on."
TERMS["label"]="A tag or answer given to data so AI learns from it."
TERMS["model"]="The final program that can do tasks."
TERMS["training"]="The process where AI learns from data."
TERMS["chatbot"]="A computer program that talks using text or voice."
TERMS["dataset"]="A big collection of information that trains AI."
TERMS["algorithm"]="Step-by-step instructions for solving a task."
TERMS["token"]="Words or pieces of words AI uses to understand input."
TERMS["overfitting"]="When AI memorizes data and fails to generalize."
TERMS["ai_agent"]="Software that does jobs for you on its own."
TERMS["ai_ethics"]="Ensures AI systems are fair and ethical."
TERMS["explainability"]="How easily decisions of an AI can be explained."
TERMS["inference"]="When AI uses what it learned to answer questions."
TERMS["turing_test"]="A test to see if AI can imitate human responses."
TERMS["prompt"]="The input question given to AI."
TERMS["fine_tuning"]="Training AI on new, specific data to specialize."
TERMS["generative_ai"]="AI that creates new data like images, text, or sound."
TERMS["ai_automation"]="Using AI to make tasks automatic and intelligent."
TERMS["neural_network"]="Inspired by the brain, AI that learns from data layers."
TERMS["computer_vision"]="AI that understands and interprets images."
TERMS["transfer_learning"]="Using an AI trained on one task for another."
TERMS["guardrails"]="Rules to keep AI safe and aligned."
TERMS["open_source_ai"]="AI shared publicly so everyone can use and improve."
TERMS["deep_learning"]="AI with many layers that analyze complex data."
TERMS["reinforcement_learning"]="AI learns by trial and error and receiving rewards."
TERMS["hallucination"]="When AI makes up incorrect or false info."
TERMS["zero_shot_learning"]="AI does tasks it hasn't seen before using reasoning."
TERMS["speech_recognition"]="AI that converts spoken words to text."
TERMS["supervised_learning"]="AI learns from labeled data (right answers known)."
TERMS["model_context"]="Rules for how AI models communicate and run."
TERMS["machine_learning"]="A field of AI where computers learn from data."
TERMS["unsupervised_learning"]="AI finds patterns in data with no labels."
TERMS["llm"]="Large Language Model – AI trained on lots of text."
TERMS["asi"]="Artificial Superintelligence – smarter than any human."
TERMS["gpu"]="Specialized chips that run AI computations fast."
TERMS["nlp"]="Natural Language Processing – how AI understands human language."
TERMS["agi"]="Artificial General Intelligence – can do anything a human can."
TERMS["gpt"]="A transformer model that generates human-like text."
TERMS["api"]="Application Programming Interface – lets programs talk to each other."

if [ -z "$1" ]; then
  echo "❌ Nenhum termo foi passado."
  echo "Sugestão: ./ai-terms.sh neural_network"
  exit 1
fi

TERM_KEY="${1,,}" # converter para minúsculas

if [ "${TERMS[$TERM_KEY]+_}" ]; then
  echo "🔍 Definição de '$TERM_KEY':"
  echo "${TERMS[$TERM_KEY]}"
else
  echo "❓ Termo '$TERM_KEY' não encontrado no glossário."
  echo "Use: ./ai-terms.sh help"
fi
