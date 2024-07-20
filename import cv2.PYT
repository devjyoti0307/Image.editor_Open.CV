import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk


class ImageEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Editor")

        # Initialize OpenCV image object
        self.cv_img = None
        self.original_img = None

        # Create main frame
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10)

        # Buttons
        self.open_button = tk.Button(self.main_frame, text="Open Image", command=self.open_image)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.main_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.crop_button = tk.Button(self.main_frame, text="Crop Image", command=self.crop_image)
        self.crop_button.grid(row=0, column=2, padx=5, pady=5)

        self.resize_button = tk.Button(self.main_frame, text="Resize Image", command=self.resize_image)
        self.resize_button.grid(row=0, column=3, padx=5, pady=5)

        self.compress_button = tk.Button(self.main_frame, text="Compress Image", command=self.compress_image)
        self.compress_button.grid(row=0, column=4, padx=5, pady=5)

        # Image display
        self.image_label = tk.Label(self.main_frame)
        self.image_label.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

    def open_image(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.cv_img = cv2.imread(filename)
            self.original_img = self.cv_img.copy()
            self.display_image()

    def display_image(self):
        img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def save_image(self):
        if self.cv_img is None:
            messagebox.showerror("Error", "No image to save.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            cv2.imwrite(filename, self.cv_img)
            messagebox.showinfo("Success", "Image saved successfully.")

    def crop_image(self):
        if self.cv_img is None:
            messagebox.showerror("Error", "No image to crop.")
            return

        x, y, w, h = cv2.selectROI("Select ROI", self.cv_img, fromCenter=False, showCrosshair=True)
        if w > 0 and h > 0:
            self.cv_img = self.cv_img[y:y + h, x:x + w]
            self.display_image()

    def resize_image(self):
        if self.cv_img is None:
            messagebox.showerror("Error", "No image to resize.")
            return

        new_width = simpledialog.askinteger("Resize Image", "Enter new width:")
        new_height = simpledialog.askinteger("Resize Image", "Enter new height:")

        if new_width is not None and new_height is not None:
            self.cv_img = cv2.resize(self.cv_img, (new_width, new_height))
            self.display_image()

    def compress_image(self):
        if self.cv_img is None:
            messagebox.showerror("Error", "No image to compress.")
            return

        desired_pixels = simpledialog.askinteger("Compress Image", "Enter desired number of pixels:")
        if desired_pixels is not None:
            current_pixels = self.cv_img.shape[0] * self.cv_img.shape[1]
            ratio = (desired_pixels / current_pixels) ** 0.5
            new_width = int(self.cv_img.shape[1] * ratio)
            new_height = int(self.cv_img.shape[0] * ratio)
            self.cv_img = cv2.resize(self.cv_img, (new_width, new_height))
            self.display_image()


def main():
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()