import os

# Example
directory = "C:/Users/Stranger/Documents"
file_name = "example.txt"

# Join path and file name
full_path = os.path.join(directory, file_name)
print(full_path)  # Output: C:/Users/Stranger/Documents/example.txt
