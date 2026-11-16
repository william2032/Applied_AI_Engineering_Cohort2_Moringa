# ============================================================
# WEEK 2 CAPSTONE - STEP 5D: RAG RETRIEVAL TEST
# ============================================================
# OBJECTIVE:
# Verify that LlamaIndex retrieves the actual policy
# needed to answer a diagnostic-imaging question.
# ============================================================

# STEP 1: IMPORT THE RAG PIPELINE
from src.rag_pipeline import build_knowledge_index


# STEP 2: TEST POLICY RETRIEVAL
def test_diagnostic_policy_retrieval():

    # Build the knowledge index
    index = build_knowledge_index()

    # Retrieve the two most relevant chunks
    retriever = index.as_retriever(similarity_top_k=2)

    question = "Does diagnostic imaging require prior authorization?"

    results = retriever.retrieve(question)

    # STEP 3: DISPLAY THE RETRIEVED EVIDENCE
    print("\n--- RAG RETRIEVAL TEST ---")
    print("Question:", question)

    for number, result in enumerate(results, start=1):
        print(f"\nResult {number}")
        print("Source:", result.node.metadata.get("file_name"))
        print("Score:", result.score)
        print("Full content:", result.node.get_content())

    # STEP 4: CHECK FOR THE REQUIRED POLICY
    required_fact = "diagnostic imaging requires prior authorization"

    found = any(
        required_fact in result.node.get_content().lower() for result in results
    )

    assert found, (
        "The retriever did not return the required "
        "diagnostic-imaging policy in its top 2 results."
    )

    print("\nPASS: Required diagnostic policy was retrieved.")
