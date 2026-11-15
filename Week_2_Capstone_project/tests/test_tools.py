# ============================================================
# WEEK 2 CAPSTONE - STEP 8: CALCULATION TOOL TESTS
# ============================================================
# OBJECTIVE:
# Verify accurate BMI calculations, input validation,
# and correct LangChain tool registration.
# ============================================================

# STEP 1: IMPORT LIBRARIES
import pytest

from src.tools import calculate_bmi, search_afyaplus_knowledge


# STEP 2: TEST BMI CALCULATIONS AND INVALID INPUTS
@pytest.mark.parametrize(
    "weight, height, expected",
    [
        (70, 170, "BMI: 24.22 (informational only)."),
        (60, 160, "BMI: 23.44 (informational only)."),
        (70, 0, "Error: Weight and height must be positive."),
        (-70, 170, "Error: Weight and height must be positive."),
        (0, 170, "Error: Weight and height must be positive."),
    ],
)
def test_bmi_calculation(weight, height, expected):

    # Execute the LangChain calculation tool
    result = calculate_bmi.invoke({"weight_kg": weight, "height_cm": height})

    # Confirm the calculation returns the expected result
    assert result == expected


# STEP 3: VERIFY BOTH TOOLS ARE REGISTERED
def test_tool_registration():

    assert calculate_bmi.name == "calculate_bmi"

    assert search_afyaplus_knowledge.name == "search_afyaplus_knowledge"

    # Confirm the BMI tool accepts the required parameters
    assert "weight_kg" in calculate_bmi.args
    assert "height_cm" in calculate_bmi.args
