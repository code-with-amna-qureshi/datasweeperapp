import streamlit as st
import pandas as pd
import io
from io import BytesIO
import os  # Importing os module to handle file paths

# Page configuration
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS to improve visibility and style success message
st.markdown(
    """
    <style>
    .stApp {
        background-color:rgb(58, 167, 191);  /* Dark background for the app */
        color: white;  /* White text color for visibility */
    }

    /* Custom styling for the success message */
    .stAlert.stSuccess {
        background-color: #FF6347;  /* Tomato background for success message */
        color: white;               /* White text color */
        font-size: 18px;            /* Optional: Increase font size */
        border-radius: 10px;        /* Optional: Add rounded corners */
    }

    /* Custom styling for other components */
    .stButton {
        margin: 10px;
    }

    .stCheckbox > div {
        color: white !important;
    }
    .stDataFrame {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description with gradient color
st.markdown(
    """
    <h1 style="background: black; color: white; text-align: center; padding: 20px; border-radius: 10px;">
        📀 Datasweeper Sterling Integrator By Amna Qureshi
    </h1>
    <p style="text-align: center; color:rgb(229, 229, 240);">Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3.</p>
    """,
    unsafe_allow_html=True
)

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Check if file type is CSV or Excel
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details 
        st.write("🔎Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

            # Column selection for cleaning
            st.subheader("Select Columns to keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # Data visualization
            st.subheader("Data Visualization")
            if st.checkbox(f"Show visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion Options
            st.subheader("Conversion Options🎲")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)  # Move cursor to the beginning of the buffer
                st.download_button(
                    label=f"Download converted {file.name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

# Display success message with customized color
st.success("All files processed successfully!⭐")
