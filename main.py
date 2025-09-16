# WARNING: On Linux, you may need to run this first for TKinter to be included in your OS install of Python:
# sudo apt update
# sudo apt install python3-tk
# On Windows and MacOS, TKinter should be included by default.
# (And note, if you want to actually download/install all available updates, use `sudo apt upgrade -y` or `sudo apt full-upgrade -y` to include removing old versions and install new dependencies)

import tkinter as tk


class ExampleGUI:
    def __init__(self):
        print("Constructor!")
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry("800x600")
        self.mainWindow.title("My First Python Program")

        label = tk.Label(self.mainWindow, text="Hello World!", font=('Arial', 18))
        label.pack(padx=20, pady=20)

        # (tk.Text(...) is a multi-line text area)
        textbox = tk.Text(self.mainWindow, font=('Arial', 16), height = 3)
        textbox.pack(padx=10)

        # (tk.Entry(...) is a ONE-line text field)
        entry = tk.Entry(self.mainWindow)
        entry.pack(padx=10, pady=10)

        button = tk.Button(self.mainWindow, text="Click Me!", font=('Arial', 16))
        button.pack(padx=10, pady=10)

    def run(self):
        print("Running!")
        self.mainWindow.mainloop()

gui = ExampleGUI()
gui.run()
