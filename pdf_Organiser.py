# Program Summary - Made by Edd Palencia-Vanegas
# 1. Checks if system has python and if there are errors.
# 2. Checks if the program is running in destination address
# 3. Looks for civil, architectural and structural PDF drawings
#   3.1 Looks for alphabetical revisions, keeps the biggest value and moves smaller ones to _SS
#   3.2 Looks for numerical revisions, keeps the biggest value and moves smaller ones to _SS
#   3.3 Compares alphabetical and numerical revisions, and keeps the numerical only
# 4. Prints report of files moved to _SS
# 5. Ends by requesting random input.

import sys
import os
import re
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import time
from datetime import datetime

# # Directory when working with system
# locate_path = os.path.dirname(os.path.realpath(__file__))
# directory = os.path.join(locate_path)

def is_currentDirectory():
    # Define the directory where the PDF files are located
    path = os.path.abspath(".")
    directory = os.path.join(path)
    return directory

# Pattern that identifies a civil drawing
civil_Pattern = r'-C-'
# Pattern that identifies a architectural drawing
arch_Pattern = r'-A-'
# Pattern that identifies a structural drawing
struct_Pattern = r'-S-'

def set_SS_directory(department):
    # Get the current date from the system
    get_date = datetime.now()
    # Format the date as a string in the order: last two digits of the year, two digits month, and two digits day
    set_Date = get_date.strftime("%y%m%d")

    # Ensure the _SS directory exists
    ss_directory = os.path.join(directory, "_SS")
    os.makedirs(ss_directory, exist_ok=True)

    return ss_directory

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores files there
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# LOAD SCREEN
def show_splash_screen():
    # Create the root window for the splash screen
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
    
    # Load the image for the splash screen
    image_path = resource_path("DdevedD 460x540.png")
    splash_image = Image.open(image_path)  # Replace with your image file
    splash_photo = ImageTk.PhotoImage(splash_image)

    # Set up the canvas to display the image
    canvas = tk.Canvas(splash_root, width=splash_image.width, height=splash_image.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=splash_photo)

    # Center the splash screen on the screen
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x_pos = (screen_width // 2) - (splash_image.width // 2)
    y_pos = (screen_height // 2) - (splash_image.height // 2)
    splash_root.geometry(f"{splash_image.width}x{splash_image.height}+{x_pos}+{y_pos}")

    # Show the splash screen for 2 seconds
    splash_root.after(2000, splash_root.destroy)  # Destroy the splash screen after 2 seconds
    splash_root.mainloop()

# VERIFY IF CORRECT DESTINATION
def is_Destination(d):
    destCompany = "M:\Synergy\Projects"    
    if destCompany in d:
        print("This program is being executed in correct company system")
    else:
        print("\nThis program has stopped because this is not a valid system. \n\nDo not promote piracy!")
        input()
        sys.exit()

################################################################################## CIVIL ############################################################################
# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR ALPHABETICAL VALUE INSIDE THE BRACKETS ------------------------------
def organise_C_alphabetical():    
    # Function to extract the alphabetic value within square brackets
    def extract_alpha_value(filename):
        match = re.search(r'\[([a-zA-Z])\]', filename)
        if match:
            return match.group(1).lower()  # Convert letter to lowercase for uniform comparison
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[[a-zA-Z]\]', '', filename)

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(civil_Pattern, filename)):
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

# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR NUMERICAL VALUE INSIDE THE BRACKETS ---------------------------------------------
def organise_C_numerical():
    # Function to extract the numeric value within square brackets
    def extract_digit_value(filename):
        match = re.search(r'\[(\d+)\]', filename)
        if match:
            return int(match.group(1))
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[\d+\]', '', filename)     

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(civil_Pattern, filename)):
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

# THIS FUNCTION GROUPS, COMPARES AND ORGANISES .PDF FILES BY THEIR NUMERICAL AND ALPHABETICAL VALUE INSIDE THE BRACKETS ---------------------------------------
def compare_C_NumAlpha():
    # Define a pattern to match the file names
    pattern = re.compile(r"(.*\[)(.*)(\].*.pdf)")

    # Initialize a dictionary to store the file names
    files = {}

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        # If the file is a PDF and the file name matches the pattern
        if filename.endswith(".pdf") and bool(re.search(civil_Pattern, filename)) and pattern.match(filename):
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

###################################################################### ARCHITECTURAL #########################################################################
# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR ALPHABETICAL VALUE INSIDE THE BRACKETS -------------------------------
def organise_A_alphabetical():
    # Function to extract the alphabetic value within square brackets
    def extract_alpha_value(filename):
        match = re.search(r'\[([a-zA-Z])\]', filename)
        if match:
            return match.group(1).lower()  # Convert letter to lowercase for uniform comparison
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[[a-zA-Z]\]', '', filename)

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(arch_Pattern, filename)):
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

# THIS FUNCTION GROUPS AND ORGANISES .PDF FILES BY THEIR NUMERICAL VALUE INSIDE THE BRACKETS ---------------------------------
def organise_A_numerical():
    # Function to extract the numeric value within square brackets
    def extract_digit_value(filename):
        match = re.search(r'\[(\d+)\]', filename)
        if match:
            return int(match.group(1))
        return None

    # Function to get the base name without the value in square brackets
    def get_base_name(filename):
        return re.sub(r'\[\d+\]', '', filename) 

    # Dictionary to store files by their base name
    files_dict = {}

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf") and bool(re.search(arch_Pattern, filename)):
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

# THIS FUNCTION GROUPS, COMPARES AND ORGANISES .PDF FILES BY THEIR NUMERICAL AND ALPHABETICAL VALUE INSIDE THE BRACKETS --------------------------
def compare_A_NumAlpha():
    # Define a pattern to match the file names
    pattern = re.compile(r"(.*\[)(.*)(\].*.pdf)")

    # Initialize a dictionary to store the file names
    files = {}

    # Iterate over the files in the directory
    for filename in os.listdir(directory):
        # If the file is a PDF and the file name matches the pattern
        if filename.endswith(".pdf") and bool(re.search(arch_Pattern, filename)) and pattern.match(filename):
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
    
    #show_splash_screen()
    
    #is_Destination(directory)
    
    directory = is_currentDirectory()

    #temp
    ss_directory = set_SS_directory()

    ss_Civil_directory = set_SS_directory("civil")
    ss_Arch_directory = set_SS_directory("architectural")
    ss_Struct_directory = set_SS_directory("structural")

    organise_C_alphabetical()
    organise_C_numerical()
    compare_C_NumAlpha()

    organise_A_alphabetical()
    organise_A_numerical()
    compare_A_NumAlpha()

    organise_S_alphabetical()
    organise_S_numerical()
    compare_S_NumAlpha()
    
    # Inform user
    print("Older versions of drawings have been moved to _SS folder")

    # Print Author
    print("Created by Soft. Dev. Edd Palencia Vanegas \nDate: 02/08/2024 \nVersion: 4.0 \n\n Made for McVeigh Consultants")
    input()