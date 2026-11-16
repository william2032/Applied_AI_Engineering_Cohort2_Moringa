# ============================================================
# WEEK 2 CAPSTONE - STEP 5C: LLAMAINDEX RAG PIPELINE
# ============================================================
# OBJECTIVE:
# Load AfyaPlus documents, split them into chunks,
# create embeddings, and retrieve relevant information.
# ============================================================

# STEP 1: IMPORT LIBRARIES
import os
from pathlib import Path
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

# STEP 2: CONFIGURE PROJECT PATHS
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge_manuals"

# Load environment settings
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT.parent.parent / ".env")

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("MODEL_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")


# STEP 3: CONFIGURE EMBEDDINGS
embed_model = OpenAILikeEmbedding(
    model_name="openai/text-embedding-3-small", api_key=api_key, api_base=base_url
)


# STEP 4: BUILD THE KNOWLEDGE INDEX
def build_knowledge_index():
    """Load documents and build a searchable vector index."""

    # Read the knowledge documents
    documents = SimpleDirectoryReader(
        input_dir=str(KNOWLEDGE_DIR), required_exts=[".txt"]
    ).load_data()

    if not documents:
        raise ValueError("No knowledge documents found.")

    # print(f"Loaded {len(documents)} documents.")

    # Split documents into smaller chunks
    splitter = SentenceSplitter(chunk_size=256, chunk_overlap=30)

    nodes = splitter.get_nodes_from_documents(documents)

    # print(f"Created {len(nodes)} text chunks.")

    # Generate embeddings and create the index
    index = VectorStoreIndex(nodes=nodes, embed_model=embed_model)

    # print("Vector index created successfully.")

    return index


# STEP 5: TEST DOCUMENT RETRIEVAL
if __name__ == "__main__":

    index = build_knowledge_index()

    # Retrieve the two most relevant chunks
    retriever = index.as_retriever(similarity_top_k=2)

    question = "Does diagnostic imaging require " "prior authorization?"

    results = retriever.retrieve(question)

    print("\n--- RETRIEVAL TEST ---")
    print("Question:", question)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}:")
        print("Source:", result.node.metadata.get("file_name"))
        print("Score:", result.score)
        print("Content:", result.node.get_content()[:500])
