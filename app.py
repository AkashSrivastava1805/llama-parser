import streamlit as st
import nest_asyncio
import tempfile
import os

# Apply nest_asyncio at the very top
nest_asyncio.apply()

# --- Page Config ---
st.set_page_config(page_title="LlamaParse Converter", layout="wide")

# --- Error Handling for Imports ---
try:
    from llama_parse import LlamaParse
except Exception as e:
    st.error(f"Failed to load LlamaParse: {e}")
    st.info("Try running: pip install llama-parse pydantic==1.10.13")

# --- UI Layout ---
st.title("📄 LlamaParse pdf summarizer app")
st.markdown("---")

col_input, col_output = st.columns([1, 1], gap="medium")

with col_input:
    st.subheader("1. Setup & Upload")
    api_key = st.text_input("LlamaCloud API Key", type="password")
    uploaded_file = st.file_uploader("Choose a PDF or Docx", type=["pdf", "docx"])
    
    instructions = st.text_area(
        "Custom Instructions (Optional)", 
        placeholder="e.g. 'Summarize this in bullet points' or 'Focus on the financial tables'"
    )

    if st.button("🚀 Convert Document"):
        if not api_key:
            st.error("Please enter your API Key!")
        elif not uploaded_file:
            st.warning("Please upload a file!")
        else:
            try:
                with st.spinner("Processing document... this may take a moment."):
                    # Save to temp file
                    suffix = f".{uploaded_file.name.split('.')[-1]}"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name

                    # Initialize and Run Parser
                    parser = LlamaParse(
                        api_key=api_key,
                        result_type="markdown",
                        parsing_instruction=instructions if instructions else None
                    )

                    # Extract text
                    documents = parser.load_data(tmp_path)
                    parsed_text = "\n\n".join([doc.text for doc in documents])
                    
                    # Store in Session State
                    st.session_state['result'] = parsed_text
                    st.session_state['original_name'] = uploaded_file.name
                    
                    # Cleanup
                    os.remove(tmp_path)
                    st.success("Successfully converted!")
            except Exception as e:
                st.error(f"Error: {e}")

with col_output:
    st.subheader("2. Preview & Download")
    
    if 'result' in st.session_state:
        # Display the result in a scrollable container
        st.markdown("**Converted Content:**")
        with st.container(border=True):
            st.markdown(st.session_state['result'])
        
        # Download button
        st.download_button(
            label="📥 Download Markdown (.md)",
            data=st.session_state['result'],
            file_name=f"converted_{st.session_state['original_name']}.md",
            mime="text/markdown"
        )
    else:
        st.info("The converted document will appear here.")
        # Placeholder image/graphic
        st.image("https://via.placeholder.com/600x300?text=Result+Preview+Area", use_container_width=True)

st.markdown("---")
st.caption("Using LlamaParse API v1")
