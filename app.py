import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# --- Custom CSS ---
st.markdown(
    """
    <stle>
        .stApp {
            background-color: #0f0f0f;
            color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
        }
        .css-1d391kg { color: white; }
        h1, h2, h3, h4 {
            color: #61dafb;
        }
    </stle>
    """,
    unsafe_allow_html=True
)

# --- Title & Description ---
st.title("🧹 Datasweeper by Sharmeen Ibrahim")
st.markdown("Transform your files between **CSV** and **Excel** format with built-in data cleaning tools.")

# --- File Uploader ---
uploaded_files = st.file_uploader(
    "📁 Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # --- File Reading ---
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading {file.name}: {e}")
            continue

        # --- File Preview ---
        st.subheader(f"📄 Preview: {file.name}")
        st.dataframe(df.head(), use_container_width=True)

        # --- Data Cleaning ---
        st.subheader("🧼 Data Cleaning Options")
        if st.checkbox(f"Enable cleaning for: {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🧩 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled!")

        # --- Column Selector ---
        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}:", df.columns, default=df.columns)
        df = df[columns]

        # --- Data Visualization ---
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

        # --- Conversion ---
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert and Download - {file.name}"):
            buffer = BytesIO()
            file_base = os.path.splitext(file.name)[0]

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
                download_name = f"{file_base}_cleaned.csv"
            else:
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                download_name = f"{file_base}_cleaned.xlsx"

            buffer.seek(0)
            st.download_button(
                label=f"📥 Download {download_name}",
                data=buffer,
                file_name=download_name,
                mime=mime_type
            )

    st.success("✅ All files processed successfully!")
