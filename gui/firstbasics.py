# WARNING: On Linux, you may need to run this first for TKinter to be included in your OS install of Python:
# sudo apt update
# sudo apt install python3-tk
# On Windows and MacOS, TKinter should be included by default.
# (And note, if you want to actually download/install all available updates, use `sudo apt upgrade -y` or `sudo apt full-upgrade -y` to include removing old versions and install new dependencies)

import asyncio
import threading
import os
import re
import tkinter as tk

def readFile(path: str) -> str:
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # print("[WARNING] Skipping file (can't decode in UTF-8): " + path)
        return ""

async def readFileAsync(path: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, readFile, path)

async def searchInFiles(path: str, searchPattern: str) -> list:
    absoluteFiles = []
    for innerPath, folders, files in os.walk(path):
        if re.search(r"\.git", innerPath):
            continue
        for fileName in files:
            fullPath = os.path.join(innerPath, fileName).replace("\\", "/")
            # relativePath = os.path.relpath(fullPath, path).replace("\\", "/")
            fileText = await readFileAsync(fullPath)
            if re.search(searchPattern, fileText):
                absoluteFiles.append(fullPath)
    return absoluteFiles

class ExampleGUI:
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry("1024x800")
        self.mainWindow.title("Search In Files")
        self.defaultFont="Arial"
        self.defaultFontSize = 10

        # FIELDS:
        self.titleLabel = tk.Label(self.mainWindow, text="Search In Files", font=(self.defaultFont, self.defaultFontSize + 2))

        self.mainFrame = tk.Frame(self.mainWindow)
        self.patternLabel = tk.Label(self.mainFrame, text="Pattern", font=(self.defaultFont, self.defaultFontSize))
        self.patternField = tk.Entry(self.mainFrame, font=(self.defaultFont, self.defaultFontSize))

        self.folderLabel = tk.Label(self.mainFrame, text="Folder", font=(self.defaultFont, self.defaultFontSize))
        self.folderField = tk.Entry(self.mainFrame, font=(self.defaultFont, self.defaultFontSize))

        self.submitButton = tk.Button(self.mainWindow, text="Search", font=(self.defaultFont, self.defaultFontSize), command=self.onClick)
        self.resultsTextArea = tk.Text(self.mainWindow, font=(self.defaultFont, self.defaultFontSize))

        # LAYOUT:
        self.titleLabel.pack(padx=20, pady=10)
        self.mainFrame.columnconfigure(0, weight=0, minsize=150)
        self.mainFrame.columnconfigure(1, weight=1)

        self.patternLabel.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.patternField.grid(row=0, column=1, sticky="we")
        self.folderLabel.grid(row=1, column=0, sticky="w", padx=(0, 20))
        self.folderField.grid(row=1, column=1, sticky="we")

        self.mainFrame.pack(fill="x", padx=30, pady=(0, 20)) # NOTE: (top, bottom) -- So this is 20px bottom padding.

        self.submitButton.pack(ipadx=20)
        self.resultsTextArea.pack(fill="both", expand=True, padx=20, pady=20) # NOTE: expand=True makes it respond to extra space from window resize events.

    def onClick(self):
        # NOTE: "1.0" means Line 1, Index 0.
        self.resultsTextArea.delete("1.0", tk.END)
        self.resultsTextArea.insert("1.0", "Pattern: " + self.patternField.get() + "\nFolder: " + self.folderField.get() + "\n")

        # NOTE: Read the current values in the main UI thread:
        pattern = self.patternField.get()
        folder = self.folderField.get()

        # Pass the values to the thread:
        def runTask(pattern, folder):
            asyncio.run(self.onClickAsync(pattern, folder))

        # NOTE: This runs a thread with runTask(),
        #   which itself runs a new temporary event loop (asyncio.create_task(runTask()) would REQUIRE an already-existing, running event loop),
        #   and that event loop is able to run asynchronously with our onClickAsync(...).
        threading.Thread(target=lambda: runTask(pattern, folder)).start()

    # TODO: Gracefully handle RuntimeError if we're still running the event loop as the user clicks the Close button (Alt + F4) to quit the program. "Cannot schedule new futures after shutdown"
    async def onClickAsync(self, searchPattern: str, folderPath: str):
        results = await searchInFiles(folderPath, searchPattern)
        
        def updateUIResults():
            self.resultsTextArea.delete("1.0", tk.END)
            for filePath in results:
                self.resultsTextArea.insert(tk.END, filePath + "\n")

        # NOTE: This uses TKinter's .after() method to schedule something to
        #   happen next on the main UI thread, where we can safely access TKinter GUI!
        self.mainWindow.after(0, updateUIResults)

    def run(self):
        try:
            self.mainWindow.mainloop()
        except KeyboardInterrupt:
            return
