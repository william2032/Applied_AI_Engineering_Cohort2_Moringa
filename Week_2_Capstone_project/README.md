# AfyaPlus Health — Enterprise-Grade RAG-Powered Agent System

## Moringa School | Applied AI Engineering — Week 2 Capstone

### 1. Project Overview

AfyaPlus Health is an AI-powered training assistant designed
to answer fictional healthcare insurance and clinical-routing
questions using verified local knowledge documents.

The system combines:

- LangChain for AI agent orchestration
- LlamaIndex for document retrieval
- OpenRouter for LLM and embedding access
- Python tools for validated BMI calculations
- Conversation memory for multi-turn interactions
- Privacy masking for personal contact information
- Controlled output de-masking



### 2. System Architecture

User Question
|
v
Privacy Masking (privacy.py)
|
v
LangChain AI Agent (agent.py)
|
+----> LlamaIndex RAG Pipeline
| |
| +--> Insurance Policies
| +--> Clinical Guidelines
|
+----> BMI Calculation Tool
|
+----> Conversation Memory
|
v
Controlled Output Layer (output_safety.py)
|
v
Final User Response

### 3. Project Structure

Week2_Capstone/
data/
knowledge_manuals/
insurance_policy.txt
clinical_guidelines.txt
src/
**init**.py
privacy.py
rag_pipeline.py
tools.py
agent.py
output_safety.py
main.py
tests/
**init**.py
test_privacy.py
test_rag.py
test_tools.py
test_end_to_end.py
.env.example
.gitignore
requirements.txt
README.md

### 4. Core Components

#### Privacy Masking

The privacy.py module uses regular expressions to identify
common Kenyan phone-number formats and email addresses.

Detected values are replaced with placeholders such as:

[PHONE_1]
[EMAIL_1]

The original values are kept in a separate mapping within
the application.

#### LlamaIndex RAG Pipeline

The rag_pipeline.py module:

1. Loads fictional AfyaPlus knowledge documents.
2. Splits them into smaller text chunks.
3. Converts chunks into embeddings.
4. Creates a searchable vector index.
5. Retrieves relevant evidence for user questions.

#### LangChain Agent and Tools

The agent uses the registered tools:

- search_afyaplus_knowledge
- calculate_bmi

The knowledge-search tool retrieves supporting policy
excerpts and source filenames.

The BMI tool performs a validated numerical calculation.

#### Conversation Memory

LangGraph's InMemorySaver maintains conversation state
using a unique thread_id for each session.

This allows the agent to understand follow-up questions.

Memory is temporary and does not persist between
application restarts.

#### Controlled Output Handling

The output_safety.py module supports selective restoration
of approved placeholders.

The integrated application currently defaults to
restoring no personal contact information.

### 5. RAG and Token Management

The retrieval pipeline uses:

- SentenceSplitter for text segmentation
- Chunk size: 256 tokens
- Chunk overlap: 30 tokens
- Similarity top-k: 2
- OpenRouter-compatible embeddings

These settings aim to balance retrieved context,
search relevance, and token usage.

The current vector index is constructed in memory.
Persistent vector storage is not yet implemented.

Retrieved source text is provided to the agent as
evidence. The agent is instructed to acknowledge
missing information rather than invent policy details.

### 6. Privacy and Compliance

The system includes these initial safeguards:

- Contact-information masking before model access
- No automatic restoration of masked details
- Input validation in calculation tools
- Instructions against unsupported diagnoses
- Escalation instructions for emergency concerns
- Separation of API keys from source code
- Fictional rather than real patient information

Limitations:

- Regex masking does not detect every form of PII.
- Retrieved documents are not inherently trustworthy.
- The current system does not prove compliance with
  Kenya's Data Protection Act, 2019.
- Production deployment would require additional
  authorization, access controls, auditing, and testing.

### 7. Installation

Prerequisites:

- Python 3.12
- A compatible Python virtual environment
- An OpenRouter API key

Install dependencies:

    python -m pip install -r requirements.txt

Copy .env.example to .env and configure:

    OPENROUTER_API_KEY=your_key_here
    MODEL_BASE_URL=https://openrouter.ai/api/v1

Never commit real API keys.

### 8. Running the Application

From the Week2_Capstone directory:

    python -m src.main

Example questions:

1. Does diagnostic imaging require prior authorization?
2. Which department handles that authorization?
3. Calculate BMI for 70 kg and 170 cm.

Type exit to close the application.

### 9. Automated Testing

Privacy tests:

    python -m pytest tests/test_privacy.py -v

RAG tests:

    python -m pytest tests/test_rag.py -v

Calculation tool tests:

    python -m pytest tests/test_tools.py -v

Live end-to-end tests:

    python -m pytest tests/test_end_to_end.py -v

Run all tests:

    python -m pytest tests/ -v

The end-to-end tests use the real OpenRouter API and
may incur usage charges.

### 10. Evaluation

Verified during development:

- Privacy masking: 9 initial tests passed
- RAG retrieval: live retrieval test passed
- LangChain RAG tool: successfully executed
- Live end-to-end tests: 3 passed

These results are development checks, not a formal
clinical safety or security certification.

### 11. Git Workflow

Required feature branch:

    feat-rag-agent-system

The completed capstone should be submitted through
a GitHub pull request into main, followed by review
and merge.

### 12. Future Improvements

- Persistent vector database
- Stronger PII detection and redaction
- Streaming-specific privacy validation
- Retrieval relevance and groundedness evaluation
- Request authorization and audit logging
- More comprehensive error handling
- Production-grade monitoring

### 13. Conclusion

AfyaPlus demonstrates how AI engineering components
can be combined into a document-grounded assistant
with tool calling, conversation memory, and initial
privacy safeguards.

The project is an educational prototype intended
to demonstrate Week 2 Applied AI Engineering skills.
