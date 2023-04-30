import tkinter as tk
from PIL import ImageGrab, ImageTk, Image
import os
import datetime

class ScreenshotApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.screenshot_count = 0
        self.region_defined = False

    def create_widgets(self):
        self.select_region_button = tk.Button(self, text="Select Region", command=self.select_region)
        self.select_region_button.pack(side="left")

        self.capture_region_button = tk.Button(self, text="Capture Region", command=self.capture_region)
        self.capture_region_button.pack(side="left")

    def select_region(self):
        self.master.withdraw()
        screenshot = ImageGrab.grab()
        self.overlay = tk.Toplevel(self.master)
        self.overlay.attributes("-alpha", 0.5)
        self.overlay.attributes("-fullscreen", True)
        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.overlay.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.master.deiconify()
        self.overlay.destroy()
        self.region_defined = True

    def capture_region(self):

        if not self.region_defined:
            error_message = tk.Label(self, text="No region selected!", fg="red")
            error_message.pack(side="left")

            self.after(5000, error_message.destroy)
            return

        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{date_string}.png"
        i = 1
        while os.path.exists(filename):
            filename = f"screenshot_{date_string}_{i}.png"
            i += 1

        if not os.path.exists('screenshots'):
            try:
                os.makedirs('screenshots')
            except OSError:
                return

        region = (self.start_x, self.start_y, self.end_x, self.end_y)

        dirpath = os.path.join("screenshots/",filename)
        screenshot = ImageGrab.grab(bbox=region)
        try:
            screenshot.save(dirpath)
        except (OSError, IOError):
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    app.mainloop()
