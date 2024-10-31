import pandas as pd
import os
import streamlit as st
import datetime
st.title("GP Files Server")

# Specify the existing folder where files will be saved
existing_folder = "C:/Users/admin/OneDrive/BOT Files/ML_GP_Files"  # Replace with the actual folder name

# Check if the folder exists and create it if it doesn't
if not os.path.exists(existing_folder):
    os.makedirs(existing_folder)
    st.warning(f"Folder '{existing_folder}' did not exist and was created.")
elif not os.path.isdir(existing_folder):
    st.error(f"'{existing_folder}' exists but is not a directory. Please specify a valid directory.")
    st.stop()  # Stop execution if the path is not a directory


# Upload VRR File
vrr_file = st.file_uploader("Upload VRR File", type=["xlsx"], key="vrr_uploader")  # Added key
pdr_file = st.file_uploader("Upload PDR File", type=["xlsx"], key="pdr_uploader") # Added key
files_upload_button = st.button("Upload Files", key="files_upload") # Upload button for Files

if files_upload_button and vrr_file: # Process only when button is clicked and file is uploaded
    try:
        df_vrr = pd.read_excel(vrr_file)
        # st.subheader("VRR Data:")
        # st.dataframe(df_vrr)

        vrr_filepath = os.path.join(existing_folder, vrr_file.name)
        with open(vrr_filepath, "wb") as f:
            f.write(vrr_file.getbuffer())
        st.success(f"VRR file saved to: {vrr_filepath}")

        # Add your VRR processing logic here

    except Exception as e:
        st.error(f"Error processing VRR file: {e}")


# Upload PDR File (similar logic to VRR)


if files_upload_button and pdr_file: # Process only when button is clicked and file is uploaded
    try:
        df_pdr = pd.read_excel(pdr_file)
        # st.subheader("PDR Data:")
        # st.dataframe(df_pdr)

        pdr_filepath = os.path.join(existing_folder, pdr_file.name)
        with open(pdr_filepath, "wb") as f:
            f.write(pdr_file.getbuffer())
        st.success(f"PDR file saved to: {pdr_filepath}")

        # Add your PDR processing logic here

    except Exception as e:
        st.error(f"Error processing PDR file: {e}")



if not vrr_file and not pdr_file:
    st.info("Upload VRR and/or PDR files to begin processing.")



# Function to get file details
def get_file_details(folder):
    file_data = []
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        file_size = os.path.getsize(file_path) / 1024  # File size in KB
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        
        file_data.append({
            "File Name": file_name,
            "Size (KB)": f"{file_size:.2f}",
            "Creation Date": creation_time
        })
    return pd.DataFrame(file_data)

# Show files in folder
st.subheader("Files in Folder:")
df_files = get_file_details(existing_folder)

if not df_files.empty:
    # Sort DataFrame by Creation Date in descending order
    df_files = df_files.sort_values(by="Creation Date", ascending=False)
    st.table(df_files)
else:
    st.info("No files found in the folder.")
