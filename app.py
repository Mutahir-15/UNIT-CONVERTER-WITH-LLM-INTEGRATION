# Unit Converter app using Streamlit and LLM Integration
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pint import UnitRegistry

# Setting Environment Variable
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Unit Registry
ureg = UnitRegistry()
Q_ = ureg.Quantity

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# Streamlit code starts here: 
st.set_page_config(page_title="Unit Converter", page_icon="📐", layout="wide")
st.title("📐 Smart Unit Converter - Gemini 2.0 Flash 🧠")

# Custom CSS for styling
st.markdown("""
<style>
div[data-baseweb="select"] {margin: 5px 0;}
.st-emotion-cache-1qg05tj {border-radius: 10px; padding: 20px;}
.gradient-text {background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Unit categories and options
UNIT_CATEGORIES = {
    "Length": ["meter", "kilometer", "centimeter", "millimeter", 
               "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "milligram", "metric ton",
              "pound", "ounce"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Area": ["square meter", "square kilometer", "square mile",
            "square yard", "square foot", "square inch"],
    "Volume": ["liter", "milliliter", "gallon", "quart", "pint"],
    "Speed": ["miles per hour", "kilometers per hour", "meters per second"]
}

# Traditional Converter Section
st.markdown('<p class="gradient-text">Traditional Converter</p>', unsafe_allow_html=True)

# Category selector at top
category = st.selectbox("Select Category", list(UNIT_CATEGORIES.keys()), key='cat_select')

# Conversion row with aligned elements
conv_col1, conv_col2, conv_col3, conv_col4 = st.columns([3, 1, 3, 2])

with conv_col1:
    from_unit = st.selectbox("From", UNIT_CATEGORIES[category], key='from_select')

with conv_col2:
    st.markdown("<br>", unsafe_allow_html=True)  
    swap = st.button("🔄 Swap", key='swap_btn')

with conv_col3:
    to_unit = st.selectbox("To", UNIT_CATEGORIES[category], key='to_select')

with conv_col4:
    value = st.number_input("Enter Value", 
                          min_value=0.0, 
                          value=1.0,
                          key='value_input')

# Handle swap
if swap:
    from_unit, to_unit = to_unit, from_unit
    st.rerun()

# Perform conversion (keep this part the same)
try:
    quantity = Q_(value, from_unit)
    result = quantity.to(to_unit).magnitude
    st.success(f"✅ {value} {from_unit} = {result:.4f} {to_unit}")
except:
    st.error("⚠️ Conversion not supported between selected units")

# AI Converter Section
st.markdown("---")
st.markdown('<p class="gradient-text">AI-Powered Converter (Gemini 2.0 Flash)</p>', unsafe_allow_html=True)
user_input = st.text_input("Ask natural language conversion (e.g., 'Convert 5 feet 2 inches to meters'):")

if st.button("✨ Convert with AI"):
    if not user_input.strip():
        st.warning("Please enter a conversion query")
        st.stop()
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        with st.spinner("🧠 Processing your request with Gemini..."):
            response = model.generate_content(
                f"""Convert this unit with detailed explanation: {user_input}
                Use this format:
                **Conversion Result**
                [value] [from unit] = [converted value] [to unit]
                **Explanation**
                [brief explanation in simple terms]"""
            )
            
        if response.text:
            with st.expander("🔍 See Detailed Conversion", expanded=True):
                st.markdown(response.text)
        else:
            st.error("No response from Gemini API")
            
    except Exception as e:
        st.error(f"Error in conversion: {str(e)}")

# Conversion History
st.markdown("---")
st.subheader("📜 Conversion History")

if 'history' not in st.session_state:
    st.session_state.history = []

# Add to history
history_entry = f"{value} {from_unit} → {result:.2f} {to_unit}" if 'result' in locals() else ""
if history_entry:
    st.session_state.history = [history_entry] + st.session_state.history[:4]

# Display history
for entry in st.session_state.history:
    st.markdown(f"- {entry}")

# Sidebar Section
st.sidebar.markdown("## 📚 Supported Units")
for category, units in UNIT_CATEGORIES.items():
    with st.sidebar.expander(f"🗃️ {category}"):
        # Changed from comma-separated to bullet points
        st.markdown("\n".join([f"- {unit}" for unit in units]))

st.sidebar.markdown("## ℹ️ About")
st.sidebar.info("""
This smart converter combines:
- Traditional unit conversion
- AI-powered natural language processing
- Real-time conversion history
- Multi-category support
""")