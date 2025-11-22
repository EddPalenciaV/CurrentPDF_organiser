import sys
import os
import re
import shutil
from datetime import datetime

# # Directory when working with system
# locate_path = os.path.dirname(os.path.realpath(__file__))
# directory = os.path.join(locate_path)

# Define the directory where the PDF files are located
path = os.path.abspath(".")
directory = os.path.join(path)

# Pattern that identifies a structural drawing
struct_Pattern = r'-S-'

# Get the current date from the system
current_date = datetime.now()
# Format the date as a string in the order: last two digits of the year, two digits month, and two digits day
current_Date = current_date.strftime("%y%m%d")

# Create civil folder with date
folder_Struct = current_Date + " STRUCTURE"

# VERIFY IF INSIDE MCVEIGH CONSULTANTS
def is_McVeigh(d):
    mcV = "M:\Synergy\Projects"
    if mcV in d:
        print("This program is being executed in McVeigh Consultants system")
    else:
        print("\nThis program has stopped because this is not a McVeigh Consultants system. \n\nDo not promote piracy!")
        input()
        sys.exit()

###################################################################### STRUCTURAL ######################################################################################
# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR ALPHABETICAL VALUE INSIDE THE BRACKETS --------------------------------
def organise_S_alphabetical():
    # Function to extract the alphabetic value within square brackets
    def extract_alpha_value(filename):
        match = re.search(r'\[([a-zA-Z])\]', filename)
        if match:
            return match.group(1).lower()  # Convert letter to lowercase for uniform comparison
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[[a-zA-Z]\]', '', filename)

    # Ensure the _SS directory exists
    ss_directory = os.path.join(directory, "_SS", folder_Struct)
    os.makedirs(ss_directory, exist_ok=True)

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(struct_Pattern, filename)):
            value = extract_alpha_value(filename)
            if value:
                base_name = get_base_name(filename)
                if base_name not in files_dict:
                    files_dict[base_name] = []
                files_dict[base_name].append((filename, value))

    # Compare files and move according to the conditions
    for base_name, files in files_dict.items():
        if len(files) > 1:
            files.sort(key=lambda x: x[1])  # Sort by the extracted alphabetic value
            for i in range(len(files) - 1):
                file_to_move = files[i][0]
                shutil.move(os.path.join(directory, file_to_move), ss_directory)
                print(f"Moved {file_to_move} to {ss_directory}")

# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR NUMERICAL VALUE INSIDE THE BRACKETS -----------------------------------
def organise_S_numerical():
    # Function to extract the numeric value within square brackets
    def extract_digit_value(filename):
        match = re.search(r'\[(\d+)\]', filename)
        if match:
            return int(match.group(1))
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[\d+\]', '', filename) 

    # Ensure the _SS directory exists
    ss_directory = os.path.join(directory, "_SS", folder_Struct)
    os.makedirs(ss_directory, exist_ok=True)

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(struct_Pattern, filename)):
            value = extract_digit_value(filename)
            if value is not None:
                base_name = get_base_name(filename)
                if base_name not in files_dict:
                    files_dict[base_name] = []
                files_dict[base_name].append((filename, value))

    # Compare files and move according to the conditions
    for base_name, files in files_dict.items():
        if len(files) > 1:
            files.sort(key=lambda x: x[1])  # Sort by the extracted numeric value
            for i in range(len(files) - 1):
                file_to_move = files[i][0]
                shutil.move(os.path.join(directory, file_to_move), ss_directory)
                print(f"Moved {file_to_move} to {ss_directory}")

# THIS FUNCTION GROUPS, COMPARES AND ORGANISES .PDF FILES BY THEIR NUMERICAL AND ALPHABETICAL VALUE INSIDE THE BRACKETS ---------------------------
def compare_S_NumAlpha():
    # Define a pattern to match the file names
    pattern = re.compile(r"(.*\[)(.*)(\].*.pdf)")

    # Initialize a dictionary to store the file names
    files = {}

    # Ensure the _SS directory exists
    ss_directory = os.path.join(directory, "_SS", folder_Struct)
    os.makedirs(ss_directory, exist_ok=True)

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        # If the file is a PDF and the file name matches the pattern
        if filename.endswith(".pdf") and bool(re.search(struct_Pattern, filename)) and pattern.match(filename):
            # Extract the parts of the file name
            prefix, value, suffix = pattern.match(filename).groups()
            # Add the value to the list for this prefix and suffix
            files.setdefault((prefix, suffix), []).append(value)

    # Iterate over the file name combinations in the dictionary
    for (prefix, suffix), values in files.items():
        # If there are exactly two files with this prefix and suffix
        if len(values) == 2:
            # Sort the values so that the numeric one comes first
            values.sort(key=str.isdigit, reverse=True)
            # If the first value is numeric and the second is alphabetic
            if values[0].isdigit() and values[1].isalpha():
                # Move the file with the alphabetic value to the "_SS" folder
                old_path = os.path.join(directory, f"{prefix}{values[1]}{suffix}")
                new_path = os.path.join(ss_directory, f"{prefix}{values[1]}{suffix}")
                shutil.move(old_path, new_path)
                print(f"Moved {prefix}{values[1]}{suffix} to {ss_directory}")

if __name__ == "__main__":

    #---VERIFY IF EXECUTABLE IS FROZEN
    if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    is_McVeigh(directory)
    organise_S_alphabetical()
    organise_S_numerical()
    compare_S_NumAlpha()
    
    # Inform user
    print("\n\nOlder versions of Structural drawings have been moved to _SS folder")

    # Print Author
    print("\nCreated by Soft. Dev. Edd Palencia Vanegas \nDate: 02/08/2024 \nVersion: 3.7.2 \n\n Made for McVeigh Consultants")
    input()