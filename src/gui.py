import zipfile
import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class ZipExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip File Extractor")
        self.root.geometry("500x300")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        ttk.Label(main_frame, text=".zip File -->:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.file_path, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=1, column=1, padx=5)
        
        # Output folder selection
        ttk.Label(main_frame, text="Enter output folder name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=3, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=3, column=1, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Extract button
        ttk.Button(main_frame, text="Extract Files", command=self.extract_files).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Zip File",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            # Set default output folder
            self.output_path.set(os.path.splitext(filename)[0])

    def browse_output(self):
        foldername = filedialog.askdirectory(title="Select Output Folder")
        if foldername:
            self.output_path.set(foldername)

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def extract_files(self):
        zip_path = self.file_path.get()
        output_folder = self.output_path.get()
        
        if not zip_path or not output_folder:
            messagebox.showerror("Error", "Please select both a zip file and output folder")
            return
            
        try:
            # Create output folder
            os.makedirs(output_folder, exist_ok=True)
            
            # Get file extensions
            file_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf')
            file_counter = 1
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get total number of files to extract
                total_files = sum(1 for f in zip_ref.namelist() 
                                if f.lower().endswith(file_extensions))
                if total_files == 0:
                    messagebox.showinfo("Info", "No image or PDF files found in the zip")
                    return
                    
                extracted = 0
                file_list = zip_ref.namelist()
                
                for file in file_list:
                    if file.lower().endswith(file_extensions):
                        filename = os.path.basename(file)
                        output_path = os.path.join(output_folder, filename)
                        
                        # Handle duplicates
                        while os.path.exists(output_path):
                            name, ext = os.path.splitext(filename)
                            output_path = os.path.join(output_folder, f"{name}_{file_counter}{ext}")
                            file_counter += 1
                        
                        # Extract file
                        with zip_ref.open(file) as source, open(output_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                        
                        extracted += 1
                        progress = (extracted / total_files) * 100
                        self.progress['value'] = progress
                        self.update_status(f"Extracting: {filename} ({extracted}/{total_files})")
            
            messagebox.showinfo("Success", f"Successfully extracted {extracted} files to:\n{output_folder}")
            self.progress['value'] = 0
            self.update_status("Ready")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_status("Error occurred")

def main():
    root = tk.Tk()
    app = ZipExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 