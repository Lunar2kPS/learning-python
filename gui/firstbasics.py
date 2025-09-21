# WARNING: On Linux, you may need to run this first for TKinter to be included in your OS install of Python:
# sudo apt update
# sudo apt install python3-tk
# On Windows and MacOS, TKinter should be included by default.
# (And note, if you want to actually download/install all available updates, use `sudo apt upgrade -y` or `sudo apt full-upgrade -y` to include removing old versions and install new dependencies)

import tkinter as tk

class ExampleGUI:
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry("800x600")
        self.mainWindow.title("Search In Files")
        self.defaultFont="Arial"
        self.defaultFontSize = 16

        label = tk.Label(self.mainWindow, text="Search In Files", font=(self.defaultFont, self.defaultFontSize + 2))
        label.pack(padx=20, pady=10)

        self.mainFrame = tk.Frame(self.mainWindow)
        # for i in range(2):
        #     self.mainFrame.columnconfigure(i, weight=1) # NOTE: This makes each column stretch along the x-axis.

        self.mainFrame.columnconfigure(0, weight=0, minsize=150)
        self.mainFrame.columnconfigure(1, weight=1)

        self.patternLabel = tk.Label(self.mainFrame, text="Pattern", font=(self.defaultFont, self.defaultFontSize))
        self.patternLabel.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.patternField = tk.Entry(self.mainFrame)
        self.patternField.grid(row=0, column=1, sticky="we")

        self.folderLabel = tk.Label(self.mainFrame, text="Folder", font=(self.defaultFont, self.defaultFontSize))
        self.folderLabel.grid(row=1, column=0, sticky="w", padx=(0, 20))
        self.folderField = tk.Entry(self.mainFrame)
        self.folderField.grid(row=1, column=1, sticky="we")
        self.mainFrame.pack(fill="x", padx=30, pady=(0, 20)) # NOTE: (top, bottom) -- So this is 20px bottom padding.

        self.outputPathsLabel = tk.Label(self.mainFrame, text="Output Paths", font=(self.defaultFont, self.defaultFontSize))
        self.outputPathsLabel.grid(row=2, column=0, sticky="w", padx=(0, 20))

        self.submitButton = tk.Button(self.mainWindow, text="Search", font=(self.defaultFont, self.defaultFontSize))
        self.submitButton.pack()

        self.resultsTextArea = tk.Text(self.mainWindow, font=(self.defaultFont, self.defaultFontSize))
        self.resultsTextArea.pack(padx=20, pady=20)

    def run(self):
        self.mainWindow.mainloop()
