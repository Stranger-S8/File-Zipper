import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import ttk, filedialog, messagebox
import os
import re
from DEFLATE import deflate
import time

class FileZipper(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.find_center()

        self.title("ZAM Zipper")
        self.resizable(False, False)
        self.geometry(f"800x600+{self.c_x}+{self.c_y}")

        self.a = deflate()

        self.path = []

        self.main_page()
    
    def find_center(self):

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        self.c_x = int(width/2 - 800/2)
        self.c_y = int(height/2 - 600/2)
    
    def add_file_fn(self):
        
        file = filedialog.askopenfilename(title="Select File")
            
        if file:
            if file not in self.path:
                self.path.append(file)
                f_name = os.path.basename(file)
                f_type = os.path.splitext(file)[1][1:] or "UnKnown"
                f_size = round(os.path.getsize(file) / 1024, 2)

                self.tree.insert("", "end", values=(f_name.split(".")[0], f_type, f"{f_size} KB"))
                self.extract_btn.configure(state="normal")
                self.compress_btn.configure(state="normal")
        
    def add_folder_fn(self):
        folderPath = filedialog.askdirectory(title="Select Folder")
        
        if folderPath:
            for root_dir, _, files in os.walk(folderPath):
                for file in files:
                    if file not in self.path:
                        self.path.append((os.path.join(folderPath, file)).replace("\\", "/"))
                        file_path = os.path.join(root_dir, file)
                        f_name = os.path.basename(file_path)
                        f_type = os.path.splitext(file_path)[1][1:] or "UnKnown"
                        f_size = round(os.path.getsize(file_path) / 1024, 2)
                        self.tree.insert("", "end", values=(f_name.split(".")[0], f_type, f"{f_size} KB"))
        
        if len(self.path) > 0:
                self.extract_btn.configure(state="normal")
                self.compress_btn.configure(state="normal")
            
    def delete_fn(self):
        selected_id = self.tree.selection()

        if selected_id:
            values = self.tree.item(selected_id, "values")
            for i in self.path:
                if values[0] in i and values[1] in i:
                    self.path.remove(i)

            self.tree.delete(selected_id)
        
        if len(self.path) == 0:
            self.extract_btn.configure(state="disabled")
            self.compress_btn.configure(state="disabled")
            
    def clear_fn(self):
        if not hasattr(self, "tree"):
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.path.clear()

        
        self.extract_btn.configure(state="disabled")
        self.compress_btn.configure(state="disabled")
    
    def start_fn(self, choice = 0):
        if choice == 0:
            if len(self.path) > 0:
                for i in self.path:
                    a = i.split("/")[-1].split(".")[0]
                    self.update_progress_fn(20)
                    self.a.compress_file(i, f"output/compression/ZAM_{a}.zlib")
                    self.update_progress_fn(100)
                messagebox.showinfo("Success", "Compression Successful")
                self.clear_fn()
                self.update_progress_fn(0)

        elif choice == 1:
            if len(self.path) > 0:
                for i in self.path:
                    a = i.split("/")[-1]
                    if a:
                        self.update_progress_fn(20)
                        self.a.decompress_file(i, f"output/decompression/ZAM_{a}")
                        self.update_progress_fn(100)
                messagebox.showinfo("Success", "Decompression Successful")
                self.clear_fn()
                self.update_progress_fn(0)
                

    def extract_fn(self):
        self.start_fn(1)
    
    def compress_fn(self):
        self.start_fn(0)

    def update_progress_fn(self, progress, delay=0.1):
        self.prog_status["value"] = progress
        self.update_idletasks()
        time.sleep(delay)
        
    def main_page(self):
        self.main_frame  = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.upper_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=0, border_color="#627581", border_width=1)
        self.upper_frame.place(relx=0.002, rely=0, relwidth=0.995, relheight=0.2)

        compress_img = ctk.CTkImage(light_image=(Image.open("data/images/zip.png")), size=(45, 45))
        extract_img = ctk.CTkImage(light_image=(Image.open("data/images/unzip.png")), size=(45, 45))
        del_img = ctk.CTkImage(light_image=(Image.open("data/images/delete.png")), size=(45, 45))
        clear_img = ctk.CTkImage(light_image=(Image.open("data/images/brush.png")), size=(45, 45))
        file = ctk.CTkImage(light_image=(Image.open("data/images/file.png")), size=(45, 45))
        folder = ctk.CTkImage(light_image=(Image.open("data/images/folder.png")), size=(45, 45))

        self.file_btn = ctk.CTkButton(self.upper_frame, text="Add File", image=file, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.add_file_fn)
        self.file_btn.place(relx=0.01, rely=0.1)

        self.folder_btn = ctk.CTkButton(self.upper_frame, text="Add Folder", image=folder, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.add_folder_fn)
        self.folder_btn.place(relx=0.1450, rely=0.1)
        
        self.compress_btn = ctk.CTkButton(self.upper_frame, text="Compress", image=compress_img, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.compress_fn)
        self.compress_btn.place(relx=0.28, rely=0.1)

        self.extract_btn = ctk.CTkButton(self.upper_frame, text="Extract", image=extract_img, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.extract_fn)
        self.extract_btn.place(relx=0.41, rely=0.1)

        self.del_btn = ctk.CTkButton(self.upper_frame, text="Delete", image=del_img, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.delete_fn
                                     )
        self.del_btn.place(relx=0.53, rely=0.1)

        self.clear_btn = ctk.CTkButton(self.upper_frame, text="Clear All", image=clear_img, compound="top", cursor="hand2",
                                     hover=False, fg_color="#ffffff", text_color="#000000", font=("Roboto", 12, "bold"),
                                     command=self.clear_fn)
        self.clear_btn.place(relx=0.65, rely=0.1)

        self.main_center_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=0, border_color="#627581", border_width=1)
        self.main_center_frame.place(relx=0.002, rely=0.2, relwidth=0.995, relheight=0.7)

        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=0, border_color="#627581", border_width=1)
        self.progress_frame.place(relx=0.002, rely=0.9, relwidth=0.995, relheight=0.05)

        columns = ["Name", "Type", "Size"]
        self.tree = ttk.Treeview(self.main_center_frame, columns=columns, show="headings", height=50)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial Black", 12, "bold") )

        for i in columns:
            self.tree.heading(i, anchor="center", text=i)
            self.tree.column(i, anchor="center", stretch=True)
        
        self.tree.pack(fill="both", expand=True)
        
        footer_label = ctk.CTkLabel(self.main_frame, text="Zam Zipper | The Vision and Ownership of Ahmad Mustafa & Zeeshan Abbas",
                                    font=("Arial", 12, "italic"), text_color="gray")
        footer_label.place(relx=0.2, rely=0.96)

        self.prog_status = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=300, mode="determinate")
        self.prog_status.place(relx=0.02, rely=0.12)
        
        self.extract_btn.configure(state="disabled")
        self.compress_btn.configure(state="disabled")





