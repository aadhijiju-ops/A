import streamlit as st
import pandas as pd
import io

# Set the page title
st.set_page_config(page_title="Excel Merger Bot", page_icon="🤖")

st.title("Excel Merger Bot 🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! Upload your Excel files below, and I'll merge them into one single file for you."
        }
    ]

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Upload files
uploaded_files = st.file_uploader(
    "Upload Excel files here",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

# Process uploaded files
if uploaded_files:

    with st.chat_message("user"):
        st.markdown(f"I have uploaded **{len(uploaded_files)}** file(s).")

    with st.chat_message("assistant"):

        if len(uploaded_files) < 2:
            st.warning("Please upload at least 2 Excel files to merge.")

        else:
            st.markdown("Processing and merging your files...")

            try:
                # Read all Excel files
                dataframes = [pd.read_excel(file) for file in uploaded_files]

                # Merge them
                merged_df = pd.concat(dataframes, ignore_index=True)

                # Save merged dataframe to memory
                output = io.BytesIO()

                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    merged_df.to_excel(
                        writer,
                        index=False,
                        sheet_name="Merged Data"
                    )

                output.seek(0)

                st.success("✅ Success! Your files have been merged.")

                # Download button
                st.download_button(
                    label="📥 Download Merged Excel",
                    data=output,
                    file_name="merged_output.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            except Exception as e:
                st.error(f"An error occurred while merging the files:\n\n{e}")
