# ============================================================
# WEEK 2 CAPSTONE - STEP 6: LANGCHAIN RAG TOOL
# ============================================================
# OBJECTIVE:
# Allow LangChain to search our LlamaIndex knowledge base.
# ============================================================

# STEP 1: IMPORT LIBRARIES
from functools import lru_cache
from langchain_core.tools import tool
import math


from src.rag_pipeline import build_knowledge_index


# STEP 2: CREATE A CACHED RETRIEVER
@lru_cache(maxsize=1)
def get_retriever():
    """Build the knowledge index once per program run."""

    index = build_knowledge_index()

    return index.as_retriever(similarity_top_k=2)


# STEP 3: CREATE THE LANGCHAIN TOOL
@tool
def search_afyaplus_knowledge(question: str) -> str:
    """
    Search AfyaPlus internal insurance policies
    and clinical routing guidelines.

    Use this tool for questions about insurance coverage,
    prior authorization, emergency routing, medication
    inquiries, and privacy policies.

    Returns supporting document excerpts, not verification
    of an individual patient's insurance eligibility.
    """

    if not question.strip():
        return "Error: Please provide a question."

    # Search the LlamaIndex knowledge base
    results = get_retriever().retrieve(question)

    if not results:
        return "No relevant internal documents were retrieved."

    # STEP 4: RETURN EVIDENCE WITH SOURCES
    evidence = []

    for result in results:
        source = result.node.metadata.get("file_name", "Unknown")

        content = result.node.get_content()

        evidence.append(f"Source: {source}\n" f"Evidence:\n{content}")

    return "\n\n".join(evidence)


# ============================================================
# WEEK 2 CAPSTONE - STEP 7: BMI CALCULATION TOOL
# ============================================================
# OBJECTIVE:
# Calculate BMI safely using validated numerical inputs.
# ============================================================


@tool
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """
    Calculate Body Mass Index (BMI) using weight in
    kilograms and height in centimetres.

    Use for educational BMI calculations only.
    Do not use this result as a medical diagnosis.
    """

    try:
        # STEP 1: CONVERT INPUTS TO NUMBERS
        weight = float(weight_kg)
        height = float(height_cm)

        # STEP 2: VALIDATE INPUTS
        if not math.isfinite(weight) or not math.isfinite(height):
            return "Error: Inputs must be finite numbers."

        if weight <= 0 or height <= 0:
            return "Error: Weight and height must be positive."

        # STEP 3: CONVERT HEIGHT TO METRES
        height_m = height / 100

        # STEP 4: CALCULATE BMI
        bmi = weight / (height_m**2)

        return f"BMI: {bmi:.2f} (informational only)."

    # STEP 5: HANDLE ERRORS
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return "Error: Invalid numerical input."


# STEP 5: TEST THE TOOL
if __name__ == "__main__":

    question = "Does diagnostic imaging require " "prior authorization?"

    response = search_afyaplus_knowledge.invoke({"question": question})

    print("\n--- LANGCHAIN RAG TOOL TEST ---")
    print(response)
