# ============================================================
# WEEK 2 CAPSTONE - END-TO-END TESTS
# ============================================================
# OBJECTIVE:
# Test the real AfyaPlus AI application using:
# 1. Live RAG retrieval
# 2. BMI tool calling
# 3. Conversation memory
# ============================================================

# STEP 1: IMPORT LIBRARIES
from uuid import uuid4
from langchain_core.messages import HumanMessage

from src import main as app


# STEP 2: CREATE A HELPER TO ASK THE REAL AI
def ask_live(question, session_id, capsys):
    """Send a question through the real AfyaPlus application."""

    # Use streaming if available
    if hasattr(app, "stream_response"):
        app.stream_response(question, session_id)
        return capsys.readouterr().out

    # Otherwise use the regular response function
    answer = app.get_response(question, session_id)
    capsys.readouterr()
    return answer


# STEP 3: RETRIEVE CONVERSATION HISTORY
def get_messages(session_id):
    """Read messages stored in the agent's memory."""

    config = {"configurable": {"thread_id": session_id}}

    state = app.agent.get_state(config)

    return state.values["messages"]


# STEP 4: CHECK WHICH TOOLS WERE CALLED
def get_tool_calls(session_id):
    """Extract tool names used during the conversation."""

    messages = get_messages(session_id)

    return [
        call["name"]
        for message in messages
        for call in getattr(message, "tool_calls", [])
    ]


# ============================================================
# TEST 1: LIVE RAG RETRIEVAL
# ============================================================
def test_live_rag(capsys):

    session_id = str(uuid4())

    answer = ask_live(
        "Use the AfyaPlus knowledge search tool. "
        "Does diagnostic imaging require prior authorization?",
        session_id,
        capsys,
    )

    # Verify the policy answer
    assert "prior authorization" in answer.lower()

    # Confirm the real RAG tool was called
    assert "search_afyaplus_knowledge" in get_tool_calls(session_id)


# ============================================================
# TEST 2: LIVE BMI CALCULATION
# ============================================================
def test_live_bmi(capsys):

    session_id = str(uuid4())

    answer = ask_live(
        "Use the calculate_bmi tool to calculate BMI "
        "for an adult weighing 70 kg and measuring 170 cm.",
        session_id,
        capsys,
    )

    # Verify the BMI result
    assert "24.22" in answer

    # Confirm the calculation tool was called
    assert "calculate_bmi" in get_tool_calls(session_id)


# ============================================================
# TEST 3: CONVERSATION MEMORY
# ============================================================
def test_live_memory(capsys):

    session_id = str(uuid4())

    # Ask the first question
    ask_live("Does diagnostic imaging require prior authorization?", session_id, capsys)

    # Ask a follow-up in the same conversation
    answer = ask_live(
        "Which department handles questions about " "that authorization?",
        session_id,
        capsys,
    )

    # Retrieve conversation history
    messages = get_messages(session_id)

    user_messages = [
        message for message in messages if isinstance(message, HumanMessage)
    ]

    # Confirm both questions are stored
    assert len(user_messages) == 2

    # Confirm the answer identifies the correct department
    assert "insurance verification" in answer.lower()
