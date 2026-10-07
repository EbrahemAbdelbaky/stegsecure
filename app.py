import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from stego.encoder import encode_text
from stego.decoder import decode_text


class StegSecureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegSecure")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.cover_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.password = tk.StringVar()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        encode_frame = ttk.Frame(self.notebook, padding=15)
        decode_frame = ttk.Frame(self.notebook, padding=15)

        self.notebook.add(encode_frame, text="Encode")
        self.notebook.add(decode_frame, text="Decode")

        # ---------- Encode UI ----------
        ttk.Label(encode_frame, text="Cover Image:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(encode_frame, textvariable=self.cover_path, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(encode_frame, text="Browse", command=self.choose_cover_image).grid(row=0, column=2)

        ttk.Label(encode_frame, text="Output Image:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(encode_frame, textvariable=self.output_path, width=60).grid(row=1, column=1, padx=5)
        ttk.Button(encode_frame, text="Save As", command=self.choose_output_path).grid(row=1, column=2)

        ttk.Label(encode_frame, text="Secret Message:").grid(row=2, column=0, sticky="nw", pady=5)
        self.encode_text = tk.Text(encode_frame, height=8, width=50)
        self.encode_text.grid(row=2, column=1, columnspan=2, padx=5, sticky="nsew")

        ttk.Label(encode_frame, text="Password (optional):").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(encode_frame, textvariable=self.password, width=60, show="*").grid(row=3, column=1, padx=5)

        ttk.Button(encode_frame, text="Encode Message", command=self.encode_message).grid(row=4, column=1, pady=15, sticky="w")

        # ---------- Decode UI ----------
        ttk.Label(decode_frame, text="Encoded Image:").grid(row=0, column=0, sticky="w", pady=5)
        self.decode_image_path = tk.StringVar()
        ttk.Entry(decode_frame, textvariable=self.decode_image_path, width=60).grid(row=0, column=1, padx=5)
        ttk.Button(decode_frame, text="Browse", command=self.choose_decoded_image).grid(row=0, column=2)

        ttk.Label(decode_frame, text="Password (optional):").grid(row=1, column=0, sticky="w", pady=5)
        self.decode_password = tk.StringVar()
        ttk.Entry(decode_frame, textvariable=self.decode_password, width=60, show="*").grid(row=1, column=1, padx=5)

        ttk.Label(decode_frame, text="Hidden Message:").grid(row=2, column=0, sticky="nw", pady=5)
        self.decode_result = tk.Text(decode_frame, height=12, width=50)
        self.decode_result.grid(row=2, column=1, columnspan=2, padx=5, sticky="nsew")

        ttk.Button(decode_frame, text="Decode Message", command=self.decode_message).grid(row=3, column=1, pady=15, sticky="w")

    def choose_cover_image(self):
        path = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            self.cover_path.set(path)

    def choose_output_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")]
        )
        if path:
            self.output_path.set(path)

    def choose_decoded_image(self):
        path = filedialog.askopenfilename(
            title="Select encoded image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if path:
            self.decode_image_path.set(path)

    def encode_message(self):
        cover = self.cover_path.get()
        output = self.output_path.get()
        message = self.encode_text.get("1.0", "end-1c")
        pwd = self.password.get()

        if not cover:
            messagebox.showerror("Error", "Please select a cover image.")
            return
        if not output:
            messagebox.showerror("Error", "Please choose an output image path.")
            return
        if not message.strip():
            messagebox.showerror("Error", "Please enter a secret message.")
            return

        try:
            encode_text(cover, output, message, password=pwd)
            messagebox.showinfo("Success", f"Secret message encoded successfully to:\n{output}")
        except Exception as exc:
            messagebox.showerror("Encoding failed", str(exc))

    def decode_message(self):
        image_path = self.decode_image_path.get()
        pwd = self.decode_password.get()

        if not image_path:
            messagebox.showerror("Error", "Please select an image to decode.")
            return

        try:
            text = decode_text(image_path, password=pwd)
            self.decode_result.delete("1.0", "end")
            self.decode_result.insert("1.0", text)
        except Exception as exc:
            messagebox.showerror("Decoding failed", str(exc))


def main():
    root = tk.Tk()
    app = StegSecureApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
