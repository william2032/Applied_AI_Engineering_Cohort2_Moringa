# ============================================================
# WEEK 2 CAPSTONE - STEP 11: AFYAPLUS MAIN APPLICATION
# ============================================================
# OBJECTIVE:
# Integrate privacy masking, the LangChain agent,
# RAG retrieval, calculation tools, conversation memory,
# and safe output handling.
# ============================================================

# STEP 1: IMPORT LIBRARIES
from uuid import uuid4
import logging
from src.privacy import mask_pii
from src.agent import agent
from src.output_safety import demask_approved_output

logging.disable(logging.INFO)  # Suppress verbose logs for clarity


# STEP 2: CREATE THE RESPONSE FUNCTION
def get_response(question: str, session_id: str) -> str:
    """Process a user's question through the AfyaPlus system."""

    # Mask sensitive information before model access
    masked_question, replacements = mask_pii(question)

    # Configure conversation memory
    config = {"configurable": {"thread_id": session_id}}

    # STEP 3: SEND MASKED QUESTION TO THE AI AGENT
    result = agent.invoke(
        {"messages": [{"role": "user", "content": masked_question}]}, config=config
    )

    # Extract the agent's final response
    response = str(result["messages"][-1].content)

    # STEP 4: APPLY OUTPUT SAFETY
    # No personal information is approved for restoration.
    safe_response = demask_approved_output(
        response=response, replacements=replacements, approved_placeholders=set()
    )

    return safe_response


# STEP 5: CREATE THE INTERACTIVE APPLICATION
def main():

    print("\n===================================")
    print("   AFYAPLUS HEALTH AI ASSISTANT")
    print("===================================")
    print("Training system.")
    print("Do not enter real patient information.")
    print("Type 'exit' to end the conversation.")

    # Create a unique conversation ID
    session_id = str(uuid4())

    # Continue until the user exits
    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("AfyaPlus: Session ended.")
            break

        if not question:
            print("Please enter a question.")
            continue

        # Process the question through the AI system
        try:
            answer = get_response(question, session_id)
            print("\nAfyaPlus:", answer)

        except Exception as error:
            # Avoid printing sensitive request data in error logs
            print(
                f"\nRequest failed: {type(error).__name__}. "
                "Check your configuration and connection."
            )


# STEP 6: RUN THE APPLICATION
if __name__ == "__main__":
    main()
