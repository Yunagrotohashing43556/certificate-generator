import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class CertificateGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")

        # Variables
        self.template_path = tk.StringVar()
        self.names_file = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.font_path = tk.StringVar(value=r"C:\Users\AZUZ\Downloads\rsufont\RSU_BOLD.ttf")
        self.font_size = tk.IntVar(value=40)
        self.position_x = tk.IntVar(value=1015)
        self.position_y = tk.IntVar(value=500)
        self.count_per_type = tk.IntVar(value=1)
        self.preview_image = None

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Template path selection
        tk.Label(self.root, text="Template Path:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.template_path, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_template).grid(row=0, column=2)

        # Names file selection
        tk.Label(self.root, text="Names File:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.names_file, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_names_file).grid(row=1, column=2)

        # Output folder selection
        tk.Label(self.root, text="Output Folder:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.output_folder, width=50).grid(row=2, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_output_folder).grid(row=2, column=2)

        # Font settings
        tk.Label(self.root, text="Font Path:").grid(row=3, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.font_path, width=50).grid(row=3, column=1)
        tk.Label(self.root, text="Font Size:").grid(row=4, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.font_size).grid(row=4, column=1)

        # Position settings
        tk.Label(self.root, text="Position X:").grid(row=5, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.position_x).grid(row=5, column=1)
        tk.Label(self.root, text="Position Y:").grid(row=6, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.position_y).grid(row=6, column=1)

        # Number of certificates
        tk.Label(self.root, text="Number of Certificates:").grid(row=7, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.count_per_type).grid(row=7, column=1)

        # Preview Button
        tk.Button(self.root, text="Preview", command=self.preview_certificate).grid(row=8, column=0, columnspan=3)

        # Generate Button
        tk.Button(self.root, text="Generate Certificates", command=self.generate_certificates).grid(row=9, column=0, columnspan=3)

        # Preview area
        self.preview_label = tk.Label(self.root)
        self.preview_label.grid(row=10, column=0, columnspan=3)

    def browse_template(self):
        self.template_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def browse_names_file(self):
        self.names_file.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]))

    def browse_output_folder(self):
        self.output_folder.set(filedialog.askdirectory())

    def preview_certificate(self):
        if not self.template_path.get():
            messagebox.showerror("Error", "Please select a template file.")
            return

        template = Image.open(self.template_path.get())
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(self.font_path.get(), self.font_size.get())

        # Sample name for preview
        sample_name = "Sample Name"

        bbox = draw.textbbox((0, 0), sample_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = self.position_x.get() - text_width // 2
        text_y = self.position_y.get() - text_height // 2

        draw.text((text_x, text_y), sample_name, font=font, fill="black")

        # Update preview
        self.preview_image = ImageTk.PhotoImage(template.resize((400, 300), Image.Resampling.LANCZOS))
        self.preview_label.config(image=self.preview_image)

    def generate_certificates(self):
        if not self.template_path.get() or not self.names_file.get() or not self.output_folder.get():
            messagebox.showerror("Error", "Please fill out all required fields.")
            return

        # Load names
        with open(self.names_file.get(), 'r', encoding='utf-8') as file:
            names = file.readlines()
        
        names = [name.strip() for name in names]

        used_names = set()
        template = Image.open(self.template_path.get())
        font = ImageFont.truetype(self.font_path.get(), self.font_size.get())

        for i in range(self.count_per_type.get()):
            if names:
                name = names.pop()
                if name in used_names:
                    continue
                used_names.add(name)

                cert = template.copy()
                draw = ImageDraw.Draw(cert)

                bbox = draw.textbbox((0, 0), name, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = self.position_x.get() - text_width // 2
                text_y = self.position_y.get() - text_height // 2

                draw.text((text_x, text_y), name, font=font, fill="black")

                output_path = os.path.join(self.output_folder.get(), f"{name}_{i+1}.png")
                cert.save(output_path)
                print(f"Generated certificate for {name}")

        messagebox.showinfo("Success", "Certificates generated successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGeneratorApp(root)
    root.mainloop()
