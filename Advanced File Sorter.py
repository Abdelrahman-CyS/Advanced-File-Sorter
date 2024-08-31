import os
import shutil
import logging
from datetime import datetime
import tkinter as tk  # Import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading

# Initialize logging with enhanced configuration
logging.basicConfig(filename='file_sorting_log.txt', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# File type extensions
extensions = {
    "images": [".jpg", ".png", ".jpeg", ".gif"],
    "videos": [".mp4", ".mkv"],
    "musics": [".mp3", ".wav"],
    "zip": [".zip", ".tgz", ".rar", ".tar"],
    "documents": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".xls"],
    "setup": [".msi", ".exe"],
    "programs": [".py", ".c", ".cpp", ".php", ".C", ".CPP"],
    "design": [".xd", ".psd"],
    "others": []  # Catch-all for unlisted extensions
}

def create_directory(path):
    """Create directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def move_file(file_path, destination_dir, category, overwrite_option):
    """Move file to the appropriate directory based on category."""
    try:
        base_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_dir, category, base_name)
        create_directory(os.path.join(destination_dir, category))

        # Handle overwriting
        if os.path.exists(destination_path):
            if overwrite_option == 'rename':
                base, extension = os.path.splitext(destination_path)
                counter = 1
                new_destination = f"{base}_{counter}{extension}"
                while os.path.exists(new_destination):
                    counter += 1
                    new_destination = f"{base}_{counter}{extension}"
                destination_path = new_destination
            elif overwrite_option == 'skip':
                return  # Skip file

        shutil.move(file_path, destination_path)

    except Exception as e:
        logging.error(f"Failed to move file {file_path} to {destination_dir}: {e}", exc_info=True)

def get_date_subfolder(file_path, organize_by_month):
    """Get subfolder name based on file's modification date."""
    timestamp = os.path.getmtime(file_path)
    date = datetime.fromtimestamp(timestamp)
    if organize_by_month:
        return date.strftime('%Y-%m')
    else:
        return date.strftime('%Y')

def get_size_category(file_path):
    """Categorize file by size."""
    size = os.path.getsize(file_path)
    if size < 1024 * 1024:  # Less than 1MB
        return "Small Files"
    elif size < 1024 * 1024 * 1024:  # Less than 1GB
        return "Medium Files"
    else:
        return "Large Files"

def sort_files(source_dir, destination_dir, overwrite_option, organize_by_date, organize_by_size, organize_by_extension, organize_by_month, update_progress, update_status):
    """Sort files from source to destination directory."""
    try:
        total_files = sum([len(files) for r, d, files in os.walk(source_dir)])
        processed_files = 0

        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                category = next((cat for cat, exts in extensions.items() if file_ext in exts), "others")

                # Determine the target directory
                target_dir = destination_dir
                if organize_by_extension:
                    category = file_ext.lstrip('.').upper()
                    target_dir = os.path.join(destination_dir, category)
                elif organize_by_date:
                    date_folder = get_date_subfolder(file_path, organize_by_month)
                    target_dir = os.path.join(destination_dir, category, date_folder)
                elif organize_by_size:
                    size_folder = get_size_category(file_path)
                    target_dir = os.path.join(destination_dir, category, size_folder)
                else:
                    target_dir = os.path.join(destination_dir, category)

                # Move file to the determined target directory
                move_file(file_path, target_dir, category, overwrite_option)

                processed_files += 1
                files_left = total_files - processed_files
                progress = int((processed_files / total_files) * 100)
                update_progress(progress)
                update_status(f"Processed {processed_files}/{total_files} files, {files_left} files left")

        update_status("File sorting completed.")
    
    except Exception as e:
        logging.error(f"An error occurred during sorting: {e}", exc_info=True)
        update_status("An error occurred during sorting. Check logs for details.")

class ModernFileSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced File Sorter")
        self.geometry("800x650")

        # Set up grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        # Title with gradient text
        self.title_label = ctk.CTkLabel(self.main_frame, text="Advanced File Sorter", font=("Roboto", 32, "bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        # Create tabs
        self.tabview = ctk.CTkTabview(self.main_frame, width=750, height=450)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Create "Sort" tab
        self.sort_tab = self.tabview.add("Sort Files")
        self.sort_tab.grid_columnconfigure(0, weight=1)

        # Create "Settings" tab
        self.settings_tab = self.tabview.add("Settings")
        self.settings_tab.grid_columnconfigure(0, weight=1)

        # Source and Destination selection in Sort tab
        self.create_directory_selection(self.sort_tab)

        # Options in Sort tab
        self.create_options(self.sort_tab)

        # Progress frame in Sort tab
        self.create_progress_frame(self.sort_tab)

        # Start button in Sort tab
        self.start_button = ctk.CTkButton(self.sort_tab, text="Start Sorting",
                                          command=self.start_sorting, height=40,
                                          fg_color="#4CAF50", hover_color="#45a049")
        self.start_button.grid(row=4, column=0, pady=20)

        # Settings in Settings tab
        self.create_settings(self.settings_tab)

        # Footer
        self.footer = ctk.CTkLabel(self.main_frame, text="© 2024 Advanced File Sorter", font=("Roboto", 12))
        self.footer.grid(row=2, column=0, pady=10)

        self.source_dir = None
        self.destination_dir = None
        self.organize_by_date = False
        self.organize_by_size = False
        self.organize_by_extension = False
        self.organize_by_month = False

    def create_directory_selection(self, parent):
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        dir_frame.grid_columnconfigure(1, weight=1)

        # Source directory
        ctk.CTkLabel(dir_frame, text="Source:").grid(row=0, column=0, padx=10, pady=5)
        self.source_entry = ctk.CTkEntry(dir_frame, width=300)
        self.source_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(dir_frame, text="Browse", command=self.select_source_directory,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=0, column=2, padx=10, pady=5)

        # Destination directory
        ctk.CTkLabel(dir_frame, text="Destination:").grid(row=1, column=0, padx=10, pady=5)
        self.destination_entry = ctk.CTkEntry(dir_frame, width=300)
        self.destination_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(dir_frame, text="Browse", command=self.select_destination_directory,
                      fg_color="#3498db", hover_color="#2980b9").grid(row=1, column=2, padx=10, pady=5)

    def create_options(self, parent):
        options_frame = ctk.CTkFrame(parent)
        options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure((0, 1), weight=1)

        # Organize options
        self.date_option = ctk.CTkCheckBox(options_frame, text="Organize by Date", command=self.toggle_date_organize)
        self.date_option.grid(row=0, column=0, padx=10, pady=5)

        self.size_option = ctk.CTkCheckBox(options_frame, text="Organize by Size", command=self.toggle_size_organize)
        self.size_option.grid(row=0, column=1, padx=10, pady=5)

        self.extension_option = ctk.CTkCheckBox(options_frame, text="Organize by Extension", command=self.toggle_extension_organize)
        self.extension_option.grid(row=1, column=0, padx=10, pady=5)

        self.month_option = ctk.CTkCheckBox(options_frame, text="Organize by Year and Month", command=self.toggle_month_organize)
        self.month_option.grid(row=1, column=1, padx=10, pady=5)

        # Overwrite options
        ctk.CTkLabel(options_frame, text="Overwrite Options:").grid(row=2, column=0, padx=10, pady=5)
        self.overwrite_option = ctk.CTkComboBox(options_frame, values=["rename", "skip"])
        self.overwrite_option.set("rename")
        self.overwrite_option.grid(row=2, column=1, padx=10, pady=5)

    def create_progress_frame(self, parent):
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=500)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(progress_frame, text="Status: Waiting to start...")
        self.status_label.grid(row=1, column=0, padx=10, pady=5)

    def create_settings(self, parent):
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        settings_frame.grid_columnconfigure(0, weight=1)

        # Theme selection
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(theme_frame, text="Theme:").grid(row=0, column=0, padx=10, pady=5)
        self.theme_option = ctk.CTkComboBox(theme_frame, values=["System", "Dark", "Light"], command=self.change_theme)
        self.theme_option.set("System")
        self.theme_option.grid(row=0, column=1, padx=10, pady=5)

        # Color scheme selection
        color_frame = ctk.CTkFrame(settings_frame)
        color_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(color_frame, text="Color Scheme:").grid(row=0, column=0, padx=10, pady=5)
        self.color_option = ctk.CTkComboBox(color_frame, values=["Blue", "Green", "Purple"], command=self.change_color_scheme)
        self.color_option.set("Blue")
        self.color_option.grid(row=0, column=1, padx=10, pady=5)

    def select_source_directory(self):
        self.source_dir = filedialog.askdirectory(title="Select Source Directory")
        if self.source_dir:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, self.source_dir)
        else:
            messagebox.showerror("Error", "No source directory selected.")

    def select_destination_directory(self):
        self.destination_dir = filedialog.askdirectory(title="Select Destination Directory")
        if self.destination_dir:
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, self.destination_dir)
        else:
            messagebox.showerror("Error", "No destination directory selected.")

    def toggle_date_organize(self):
        self.organize_by_date = not self.organize_by_date
        if self.organize_by_date:
            self.size_option.deselect()
            self.extension_option.deselect()
            self.organize_by_size = False
            self.organize_by_extension = False

    def toggle_size_organize(self):
        self.organize_by_size = not self.organize_by_size
        if self.organize_by_size:
            self.date_option.deselect()
            self.extension_option.deselect()
            self.organize_by_date = False
            self.organize_by_extension = False

    def toggle_extension_organize(self):
        self.organize_by_extension = not self.organize_by_extension
        if self.organize_by_extension:
            self.date_option.deselect()
            self.size_option.deselect()
            self.organize_by_date = False
            self.organize_by_size = False

    def toggle_month_organize(self):
        self.organize_by_month = not self.organize_by_month

    def change_theme(self, choice):
        ctk.set_appearance_mode(choice)

    def change_color_scheme(self, choice):
        color_schemes = {
            "Blue": {"primary": "#3498db", "secondary": "#2980b9"},
            "Green": {"primary": "#4CAF50", "secondary": "#45a049"},
            "Purple": {"primary": "#9b59b6", "secondary": "#8e44ad"}
        }
        selected_scheme = color_schemes.get(choice, color_schemes["Blue"])
        self.start_button.configure(fg_color=selected_scheme["primary"],
                                    hover_color=selected_scheme["secondary"])

    def start_sorting(self):
        self.source_dir = self.source_entry.get()
        self.destination_dir = self.destination_entry.get()

        if not self.source_dir or not self.destination_dir:
            messagebox.showerror("Error", "Source or destination directory not selected.")
            return

        overwrite_option = self.overwrite_option.get()
        self.progress_bar.set(0)
        self.status_label.configure(text="Status: Sorting files...")

        # Use a separate thread for sorting to keep the UI responsive
        sorting_thread = threading.Thread(target=sort_files, args=(
            self.source_dir,
            self.destination_dir,
            overwrite_option,
            self.organize_by_date,
            self.organize_by_size,
            self.organize_by_extension,
            self.organize_by_month,
            self.update_progress,
            self.update_status
        ), daemon=True)
        sorting_thread.start()

    def update_progress(self, value):
        # Update progress bar in a thread-safe way using the after method
        self.after(0, self.progress_bar.set, value / 100)

    def update_status(self, message):
        # Update status label in a thread-safe way using the after method
        self.after(0, self.status_label.configure, {'text': f"Status: {message}"})
        if message == "File sorting completed.":
            self.after(0, lambda: messagebox.showinfo("Completed", "File sorting completed."))

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Default theme mode
    ctk.set_default_color_theme("blue")  # Default color theme
    app = ModernFileSorterApp()
    app.mainloop()
