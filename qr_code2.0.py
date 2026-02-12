import qrcode
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def choose_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(
        title="Select Logo Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if logo_path:
        logo_label.config(text=f"✅ Logo Selected: {logo_path.split('/')[-1]}")

def generate_qr():
    data = entry.get()
    
    
    if not data:
        messagebox.showwarning("Warning", "Please enter text or URL!")
        return

    # Create QR code
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Add logo if selected
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo_size = qr_img.size[0] // 5  # logo = 20% of QR size
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add logo: {e}")

    # Save QR code
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        qr_img.save(save_path)
        messagebox.showinfo("Success", f"QR Code saved as:\n{save_path}")

# GUI setup
root = tk.Tk()
root.title("QR Code Generator with Logo")
root.geometry("400x300")
root.resizable(False, False)

logo_path = None

tk.Label(root, text="Enter text or URL:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, width=40, font=("Arial", 11))
entry.pack(pady=5)

tk.Button(root, text="Choose Logo", command=choose_logo, bg="#4CAF50", fg="white", width=20).pack(pady=10)
logo_label = tk.Label(root, text="No logo selected", fg="gray")
logo_label.pack()

tk.Button(root, text="Generate QR Code", command=generate_qr, bg="#2196F3", fg="white", width=20).pack(pady=20)

root.mainloop()