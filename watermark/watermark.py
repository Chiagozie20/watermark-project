import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.show()


def preview_watermark():
    file_path = filedialog.askopenfilename()
    if file_path:
        watermark_text = watermark_entry.get()
        img = Image.open(file_path).convert("RGBA")
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))

        font = ImageFont.truetype("arial.ttf", 40)
        d = ImageDraw.Draw(txt)

        width, height = img.size
        text_bbox = d.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = get_position(width, height, text_width, text_height, position_var.get())

        if spread_var.get():
            spread_watermark(d, watermark_text, font, width, height, text_width, text_height)
        else:
            d.text(position, watermark_text, fill=color_var.get(), font=font)

        watermarked = Image.alpha_composite(img, txt)
        watermarked.show()


def get_position(width, height, text_width, text_height, position):
    if position == "top-left":
        return (10, 10)
    elif position == "top-right":
        return (width - text_width - 10, 10)
    elif position == "bottom-left":
        return (10, height - text_height - 10)
    else:  # bottom-right
        return (width - text_width - 10, height - text_height - 10)


def spread_watermark(draw, text, font, img_width, img_height, text_width, text_height):
    for y in range(0, img_height, text_height + 20):
        for x in range(0, img_width, text_width + 20):
            draw.text((x, y), text, fill=color_var.get(), font=font)


def save_watermarked_image(image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        image.save(file_path)


def add_watermark(image_path, watermark_text, position):
    img = Image.open(image_path).convert("RGBA")
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))

    font = ImageFont.truetype("arial.ttf", 40)
    d = ImageDraw.Draw(txt)

    width, height = img.size
    text_bbox = d.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    pos = get_position(width, height, text_width, text_height, position)

    if spread_var.get():
        spread_watermark(d, watermark_text, font, width, height, text_width, text_height)
    else:
        d.text(pos, watermark_text, fill=color_var.get(), font=font)

    watermarked = Image.alpha_composite(img, txt)
    watermarked.show()
    save_watermarked_image(watermarked)


def apply_watermark():
    try:
        file_path = filedialog.askopenfilename()
        if not file_path:
            raise ValueError("No file selected")

        watermark_text = watermark_entry.get()
        if not watermark_text:
            raise ValueError("Watermark text cannot be empty")

        position = position_var.get()
        add_watermark(file_path, watermark_text, position)
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Image Watermarking App")

frame = tk.Frame(root)
frame.pack(pady=10)

open_button = tk.Button(frame, text="Open Image", command=open_image)
open_button.grid(row=0, column=0, padx=5)

preview_button = tk.Button(frame, text="Preview Watermark", command=preview_watermark)
preview_button.grid(row=0, column=1, padx=5)

apply_button = tk.Button(frame, text="Apply Watermark", command=apply_watermark)
apply_button.grid(row=0, column=2, padx=5)

watermark_label = tk.Label(root, text="Enter Watermark Text:")
watermark_label.pack()

watermark_entry = tk.Entry(root)
watermark_entry.pack()

position_label = tk.Label(root, text="Select Watermark Position:")
position_label.pack()

position_var = tk.StringVar(value="bottom-right")
positions = ["top-left", "top-right", "bottom-left", "bottom-right"]
for pos in positions:
    tk.Radiobutton(root, text=pos, variable=position_var, value=pos).pack()

spread_var = tk.BooleanVar()
spread_check = tk.Checkbutton(root, text="Spread Watermark Across Image", variable=spread_var)
spread_check.pack()

color_label = tk.Label(root, text="Select Watermark Color:")
color_label.pack()

color_var = tk.StringVar(value="white")
colors = ["white", "red", "blue", "green", "yellow"]
for color in colors:
    tk.Radiobutton(root, text=color, variable=color_var, value=color).pack()

root.mainloop()
