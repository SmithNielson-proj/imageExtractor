import zipfile
import os
import shutil
import platform

def get_zip_path():
    """Get the zip file path in a cross-platform way"""
    if platform.system() == 'Windows':
        # For Windows, show an example with backslashes
        print("Example path: C:\\Users\\username\\Downloads\\file.zip")
    else:
        # For macOS/Linux, show an example with forward slashes
        print("Example path: /Users/username/Downloads/file.zip")
    
    return input("Enter the path to the zip file: ").strip('"\'')

def create_output_folder(zip_path):
    """Create output folder in a cross-platform way"""
    # Convert path separators to the correct format for the current OS
    zip_path = os.path.normpath(zip_path)
    output_folder = os.path.splitext(zip_path)[0]
    
    # Create the output folder
    try:
        os.makedirs(output_folder, exist_ok=True)
        return output_folder
    except Exception as e:
        print(f"Error creating output folder: {str(e)}")
        return None

def main():
    try:
        zip_path = get_zip_path()
        output_folder = create_output_folder(zip_path)
        
        if not output_folder:
            return
            
        # Include both image and PDF extensions
        file_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf')
        file_counter = 1

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            for file in file_list:
                if file.lower().endswith(file_extensions):
                    filename = os.path.basename(file)
                    output_path = os.path.join(output_folder, filename)
                    
                    # Handle duplicate filenames
                    while os.path.exists(output_path):
                        name, ext = os.path.splitext(filename)
                        # file counter adds _1, _2, etc to the end of duplicate files 
                        output_path = os.path.join(output_folder, f"{name}_{file_counter}{ext}")
                        file_counter += 1
                    
                    # Extract the file
                    with zip_ref.open(file) as source, open(output_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                    
                    print(f"Extracted: {filename}")

        print(f"\nAll files have been extracted to: {output_folder}")

    except FileNotFoundError:
        print(f"Error: The file '{zip_path}' was not found.")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_path}' is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


