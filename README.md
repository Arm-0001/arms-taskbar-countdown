# Taskbar Countdown Timer

## Overview

**Taskbar Countdown Timer** is a Python-based application that allows users to set a countdown to a specific date and time. The application resides in the system tray (taskbar) and displays the total minutes remaining until the target time. It provides a user-friendly interface for selecting dates and times and notifies the user when the countdown completes.

## Features

- **Graphical Date and Time Picker:** Easily select the target date using a calendar widget and set the target time using spinboxes.
- **System Tray Integration:** Displays the total minutes remaining in the tray icon.
- **Real-Time Updates:** Continuously updates the tray icon every minute.
- **Tooltip Information:** Hover over the tray icon to see the full time remaining in `HH:MM:SS` format.
- **Notifications:** Receive a notification when the countdown reaches zero.
- **Context Menu:** Right-click the tray icon to access options like "Show" and "Exit."

## Installation

### Prerequisites

- **Python 3.6 or Later:** Download from [python.org](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/yourusername/taskbar-countdown.git
cd taskbar-countdown
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
python main.py
```

### Set the Countdown

Select Date: Click on the date field to choose your target date.
Select Time: Use the spinboxes to set the target hour, minute, and second.
Start Countdown: Click the "Start Countdown" button. The main window will hide, and a tray icon will appear showing the total minutes remaining.
Monitor the Countdown:

Tray Icon: Displays the total minutes remaining (e.g., "90m").
Tooltip: Hover over the tray icon to see the full time remaining (e.g., "Time Remaining: 1:30:00").
Manage the Countdown:

Show: Right-click the tray icon and select "Show" to reopen the main window.
Exit: Right-click the tray icon and select "Exit" to close the application.
Completion Notification:

When the countdown reaches zero, a notification balloon will appear, and the main window will reappear to inform you that the target time has been reached.
Packaging with AutoPyToExe
To distribute the application as a standalone executable, use AutoPyToExe:

## License

This project is licensed under the MIT License.
