import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import time
import threading
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arm's Taskbar Countdown Timer")
        self.root.geometry("600x250")
        self.root.resizable(True, True)

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        # Date Picker Frame
        self.date_frame = ttk.Frame(root)
        self.date_frame.pack(pady=(20, 10), fill='x', padx=20)

        # Date Picker Label
        self.lbl_date = ttk.Label(self.date_frame, text="Select Date:")
        self.lbl_date.pack(side=tk.LEFT, padx=(0, 10))

        # DateEntry Widget
        self.date_entry = DateEntry(self.date_frame, width=15, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.date_entry.pack(side=tk.LEFT)

        # Time Picker Frame
        self.time_frame = ttk.Frame(root)
        self.time_frame.pack(pady=10, fill='x', padx=20)

        # Hour Picker
        self.lbl_hour = ttk.Label(self.time_frame, text="Hour:")
        self.lbl_hour.grid(row=0, column=0, padx=20, pady=5, sticky='e')
        self.hour_var = tk.StringVar()
        self.hour_spinbox = ttk.Spinbox(self.time_frame, from_=0, to=23, textvariable=self.hour_var, width=5, format="%02.0f")
        self.hour_spinbox.grid(row=0, column=1, padx=10, pady=5)
        self.hour_spinbox.set("00")

        # Minute Picker
        self.lbl_minute = ttk.Label(self.time_frame, text="Minute:")
        self.lbl_minute.grid(row=0, column=2, padx=20, pady=5, sticky='e')
        self.minute_var = tk.StringVar()
        self.minute_spinbox = ttk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.minute_var, width=5, format="%02.0f")
        self.minute_spinbox.grid(row=0, column=3, padx=10, pady=5)
        self.minute_spinbox.set("00")

        # Second Picker
        self.lbl_second = ttk.Label(self.time_frame, text="Second:")
        self.lbl_second.grid(row=0, column=4, padx=20, pady=5, sticky='e')
        self.second_var = tk.StringVar()
        self.second_spinbox = ttk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.second_var, width=5, format="%02.0f")
        self.second_spinbox.grid(row=0, column=5, padx=10, pady=5)
        self.second_spinbox.set("00")

        # Start Button
        self.start_button = ttk.Button(root, text="Start Countdown", command=self.start_countdown)
        self.start_button.pack(pady=20)

        # Initialize variables
        self.target_datetime = None
        self.icon = None
        self.stop_event = threading.Event()

    def start_countdown(self):
        try:
            selected_date = self.date_entry.get_date()
            selected_hour = int(self.hour_var.get())
            selected_minute = int(self.minute_var.get())
            selected_second = int(self.second_var.get())

            self.target_datetime = datetime.combine(selected_date, datetime.min.time()).replace(
                hour=selected_hour, minute=selected_minute, second=selected_second
            )

            if self.target_datetime <= datetime.now():
                messagebox.showerror("Invalid Date/Time", "Please select a future date and time.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please ensure all time fields are correctly filled.")
            return

        # Start the system tray icon in a separate thread
        threading.Thread(target=self.create_tray_icon, daemon=True).start()

        # Hide the main window
        self.root.withdraw()

    def create_image(self, minutes):
        """
        Create an image for the tray icon displaying the total minutes remaining.

        :param minutes: Integer representing the total minutes remaining.
        :return: PIL Image object.
        """
        # Create an image for the icon with the remaining minutes
        img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))  # Transparent background
        d = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 120)
        except IOError:
            font = ImageFont.load_default()

        # Convert minutes to string
        text = f"{minutes}"

        # Calculate text size using font.getbbox
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((128 - text_width) // 2, (128 - text_height) // 2)
        d.text(position, text, font=font, fill=(255, 255, 255, 255))
        return img

    def update_icon(self, icon):
        while not self.stop_event.is_set():
            remaining = self.target_datetime - datetime.now()
            if remaining.total_seconds() <= 0:
                icon.notify(message="The target time has been reached!", title="Countdown Timer")
                self.stop_event.set()
                icon.stop()
                self.root.deiconify()
                break

            # Calculate total remaining minutes
            total_seconds = int(remaining.total_seconds())
            total_minutes = total_seconds // 60
            # Round up if there are remaining seconds
            if total_seconds % 60 > 0:
                total_minutes += 1

            time_str = f"{total_minutes}"

            # Update the icon's image and tooltip
            icon.icon = self.create_image(total_minutes)
            icon.title = f"Time Remaining: {remaining_str(remaining)}"

            time.sleep(1)

    def on_exit(self, icon, item):
        self.stop_event.set()
        icon.stop()
        sys.exit()

    def on_show(self, icon, item):
        self.root.deiconify()
        self.stop_event.set()
        icon.stop()

    def create_tray_icon(self):
        # Initial icon with 0 minutes
        initial_image = self.create_image(0)

        # Define menu
        menu = (
            item('Show', self.on_show),
            item('Exit', self.on_exit)
        )

        # Create the tray icon
        self.icon = pystray.Icon("countdown", initial_image, "Countdown Timer", menu)
        # Start the icon
        self.icon.run_detached()

        # Start updating the icon
        self.update_icon(self.icon)

def remaining_str(remaining):
    """
    Format the remaining timedelta as HH:MM:SS.

    :param remaining: timedelta object representing the remaining time.
    :return: String in HH:MM:SS format.
    """
    total_seconds = int(remaining.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02}:{seconds:02}"

def main():
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
