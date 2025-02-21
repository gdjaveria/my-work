import streamlit as st
import pandas as pd
import os
from io import BytesIO

 # setup our app

st.set_page_config(page_title="Datasweeper sterling Integrator By Javeria ", layout='wide')
st.title("Data sweeper")
st.write("transform your file between csv and excel formats with built-in data cleaning and visualization tools")

uploaded_files = st.file_uploader("Choose a file (csv or excel)", type=['csv', 'xlsx'], accept_multiple_files=True)

 # If the user uploads a file

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df=pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Invalid file format. Please upload a csv or excel file")
            continue

        # Display the file info
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size/1024:.2f} KB")

        # Display the data
        st.write("Preview of the data:")
        st.dataframe(df.head())

        # Data Cleaning options
        st.subheader("Data Cleaning")
        if st.checkbox(f"Cleansing for {uploaded_file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from file : {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")

            with col2:
                if st.button(f"Fill Missing Values from {uploaded_file.name}"):
                   numeric_cols = df.select_dtypes(include=['numbers']).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing values have been filled successfully")

            # choose specific columns to keep convert to csv or excel
                   st.subheader("select Columns to convert to csv or excel")
                   columns= st.multiselect(f"Choose Columns for {uploaded_file.name}", df.columns, default=df.columns)
                   df = df[columns]

            # Create same visualiziation
            st.subheader("Data Visualization")
            if st.checkbox("Show Data Visualization for {uploaded_file.name}"):
              st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

              # Convert the file to csv or excel
              st.subheader("Conversion Options")
              conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ["csv", "excel"], key=uploaded_file.name)
              if st.button(f"Convert{uploaded_file.name}"):
                buffer = BytesIO()
                if conversion_type == "csv":
                    df.to_csv(buffer, index=False)
                    file_name = uploaded_file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "excel":
                    df.to_excel(buffer, index=False)
                    file_name = uploaded_file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    buffer.seek(0)

                # Download button
                st.download_button(
                    label=f"Click here to download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

                st.success("All done! Your file has been converted successfully!")
                
                     