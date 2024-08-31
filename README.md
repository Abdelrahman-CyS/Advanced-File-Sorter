# Advanced File Sorter

## Overview

The **Advanced File Sorter** is a Python-based graphical application designed to organize files in a specified directory into categorized subfolders. This tool helps users to manage their files efficiently by sorting them based on various criteria such as file type, size, modification date, and more. It is built using `customtkinter` for the GUI, providing a modern and user-friendly interface.

## Features

- **Organize by File Type**: Sort files into categories like images, videos, documents, etc.
- **Organize by Date**: Sort files based on their modification date (by year or year and month).
- **Organize by Size**: Classify files into small, medium, or large categories.
- **Organize by File Extension**: Sort files by their specific file extensions.
- **Customizable Options**: Choose to rename or skip files if a conflict occurs in the destination directory.
- **Real-Time Progress Updates**: See how many files have been processed and how many are left.
- **Thread-Safe UI**: The application remains responsive while sorting files in the background.

## Installation

To run the Advanced File Sorter, you need Python installed on your machine. Follow these steps to set up the environment:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Abdelrahman-CyS/advanced-file-sorter.git
   cd advanced-file-sorter
   ```

2. **Install Required Python Libraries:**
   Install the dependencies using `pip`:
   ```bash
   pip install customtkinter
   ```

   Ensure `tkinter` is installed (it is usually included with Python installations).

## Usage

1. **Run the Application:**
   Execute the script using Python:
   ```bash
   python advanced_file_sorter.py
   ```

2. **Select Directories:**
   - Use the "Browse" buttons to select the source directory (where your files are located) and the destination directory (where sorted files will be saved).

3. **Choose Sorting Options:**
   - Select from available sorting options:
     - Organize by Date
     - Organize by Size
     - Organize by File Extension
     - Organize by Year and Month

4. **Start Sorting:**
   - Click the "Start Sorting" button to begin the process. The progress bar and status label will update in real-time, showing the sorting progress and how many files are left.

5. **Completion:**
   - A message will be displayed once all files have been sorted. Check the destination directory to see your organized files.

## Screenshots

![image](https://github.com/user-attachments/assets/48b3ef67-a673-4e46-a3dd-9fda99c5778b)

*Main UI of the Advanced File Sorter application.*

## Contact

For any inquiries, please contact [abdelrahman.cys@gmail.com](abdelrahman.cys@gmail.com).

## Acknowledgments

- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for providing a modern look and feel to the application.
- Python community for the extensive libraries and resources.

