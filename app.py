import math

import streamlit as st

# ---------- Settings ----------
CURRENCY = "SAR"  # the currency name shown after every amount

# Each box: (key, label, text used in its "Please enter ..." message)
FIELDS = [
    ("allowance", "Monthly allowance", "your monthly allowance"),
    ("food", "Food and drinks", "your food and drinks expenses"),
    ("transport", "Transportation", "your transportation expenses"),
    ("supplies", "University supplies", "your university supplies expenses"),
    ("other", "Other expenses", "your other expenses"),
]

st.set_page_config(page_title="Student Monthly Budget", layout="centered")

# ---------- Look and feel (CSS) ----------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden; height: 0;}
    [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none;}
    [data-testid="InputInstructions"] {display: none;}

    .stApp {background-color: #eef2f8;}
    .stApp, .stApp p, .stApp label, .stApp input, .stApp button, .stApp div {
        font-family: Arial, sans-serif;
    }

    /* The white card */
    .block-container {
        max-width: 460px;
        background-color: #ffffff;
        border-radius: 14px;
        padding: 28px !important;
        margin: 32px auto;
        box-shadow: 0 4px 18px rgba(31, 56, 100, 0.12);
    }
    @media (max-width: 520px) {
        .block-container {margin: 12px; max-width: calc(100% - 24px);}
    }
    .stMain {padding-top: 0;}

    .stApp p.title {font-size: 24px; font-weight: bold; color: #1f3864; margin: 0;}
    .stApp p.subtitle {font-size: 14px; color: #5a6785; margin: 4px 0 12px 0;}
    .stApp p.error {font-size: 14px; color: #c0272d; margin: -8px 0 8px 0;}

    /* Make both buttons full width */
    .st-key-calculate, .st-key-new_month,
    .st-key-calculate .stButton, .st-key-new_month .stButton {width: 100%;}

    /* Calculate button */
    .st-key-calculate button {
        width: 100%;
        background-color: #1f3864;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 12px;
    }
    .st-key-calculate button p {font-size: 18px; font-weight: bold;}
    .st-key-calculate button:hover, .st-key-calculate button:focus,
    .st-key-calculate button:active, .st-key-calculate button:focus:not(:active) {
        background-color: #2a4a80; color: #ffffff; border: none; box-shadow: none;
    }

    /* New Month button */
    .st-key-new_month button {
        width: 100%;
        background-color: #e3e9f5;
        color: #1f3864;
        border: none;
        border-radius: 10px;
        padding: 12px;
    }
    .st-key-new_month button p {font-size: 18px; font-weight: bold;}
    .st-key-new_month button:hover, .st-key-new_month button:focus,
    .st-key-new_month button:active, .st-key-new_month button:focus:not(:active) {
        background-color: #d3dcef; color: #1f3864; border: none; box-shadow: none;
    }

    /* Result box */
    .result {
        background-color: #f3f6fb;
        border: 2px solid #c5cee0;
        border-radius: 10px;
        padding: 18px;
        margin: 8px 0 12px 0;
    }
    .stApp .result p {font-size: 18px; margin: 4px 0; color: #1f3864;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Memory between clicks ----------
for key, label, message in FIELDS:
    if key not in st.session_state:
        st.session_state[key] = ""
if "errors" not in st.session_state:
    st.session_state["errors"] = {}
if "result" not in st.session_state:
    st.session_state["result"] = None


# ---------- Functions ----------
def check_inputs():  # reads all five boxes, returns the numbers and the error messages
    values = {}
    errors = {}
    for key, label, message in FIELDS:  # repeats the same checks for each of the five boxes
        text = st.session_state[key].strip()
        if text == "":  # the box is empty
            errors[key] = "Please enter " + message
            continue
        try:
            number = float(text)
        except ValueError:
            errors[key] = "Please enter a number only"
            continue
        if math.isnan(number) or math.isinf(number):
            errors[key] = "Please enter a number only"
        elif number < 0:
            errors[key] = "Invalid input. Enter a non-negative amount."
        else:
            values[key] = number
    return values, errors


def calculate(values):
    allowance = values["allowance"]
    total_expenses = values["food"] + values["transport"] + values["supplies"] + values["other"]
    amount_left = allowance - total_expenses

    if total_expenses > allowance:
        message = "You have exceeded your monthly budget."
        color = "#c0272d"
    elif total_expenses == allowance:
        message = "You used your entire monthly allowance."
        color = "#b26a00"
    else:
        message = "You have money remaining from your monthly allowance."
        color = "#1b7a3e"

    return {"total": total_expenses, "left": amount_left, "message": message, "color": color}


def on_calculate():
    values, errors = check_inputs()
    st.session_state["errors"] = errors
    if errors:
        st.session_state["result"] = None
    else:
        st.session_state["result"] = calculate(values)


def clear_all():
    for key, label, message in FIELDS:
        st.session_state[key] = ""
    st.session_state["errors"] = {}
    st.session_state["result"] = None


# ---------- Screen ----------
st.markdown('<p class="title">Student Monthly Budget</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Enter your allowance and expenses in SAR.</p>',
    unsafe_allow_html=True,
)

for key, label, message in FIELDS:
    st.text_input(label, key=key)
    if key in st.session_state["errors"]:
        st.markdown(
            '<p class="error">' + st.session_state["errors"][key] + "</p>",
            unsafe_allow_html=True,
        )

st.button("Calculate", key="calculate", on_click=on_calculate)

result = st.session_state["result"]
if result is not None:
    st.markdown(
        f"""
        <div class="result">
            <p>Total Expenses: {result['total']:,.2f} {CURRENCY}</p>
            <p>Amount Left: {result['left']:,.2f} {CURRENCY}</p>
            <p style="font-weight: bold; color: {result['color']};">{result['message']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.button("New Month", key="new_month", on_click=clear_all)
