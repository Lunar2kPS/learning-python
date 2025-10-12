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
        print("[WARNING] Skipping file (can't decode in UTF-8): " + path)
        return ""

async def readFileAsync(path: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, readFile, path)

def getFiles(path: str) -> list:
    innerFiles = []
    for f in os.listdir(path):
        fullPath = os.path.join(path, f)
        if (os.path.isfile(fullPath)):
            innerFiles.append(f)
    return innerFiles

def getFilesRecursively(path: str) -> list:
    relativeFiles = []
    for subfolder, folders, files in os.walk(path):
        if re.search(r"\.git", subfolder):
            continue
        for fileName in files:
            fullPath = os.path.join(subfolder, fileName)
            relativePath = os.path.relpath(fullPath, path)
            relativeFiles.append(relativePath)
    return relativeFiles

async def searchInFiles(path: str, searchPattern: str) -> list:
    relativePaths = []
    for innerPath, folders, files in os.walk(path):
        if re.search(r"\.git", innerPath):
            continue
        for fileName in files:
            fullPath = os.path.join(innerPath, fileName)
            relativePath = os.path.relpath(fullPath, path)
            fileText = await readFileAsync(relativePath)
            if re.search(searchPattern, fileText):
                relativePaths.append(relativePath)
    return relativePaths

class ExampleGUI:
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry("800x600")
        self.mainWindow.title("Search In Files")
        self.defaultFont="Arial"
        self.defaultFontSize = 14

        self.label = tk.Label(self.mainWindow, text="Search In Files", font=(self.defaultFont, self.defaultFontSize + 2))
        self.label.pack(padx=20, pady=10)

        self.mainFrame = tk.Frame(self.mainWindow)
        # for i in range(2):
        #     self.mainFrame.columnconfigure(i, weight=1) # NOTE: This makes each column stretch along the x-axis.

        self.mainFrame.columnconfigure(0, weight=0, minsize=150)
        self.mainFrame.columnconfigure(1, weight=1)

        self.patternLabel = tk.Label(self.mainFrame, text="Pattern", font=(self.defaultFont, self.defaultFontSize))
        self.patternLabel.grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.patternField = tk.Entry(self.mainFrame, font=(self.defaultFont, self.defaultFontSize))
        self.patternField.grid(row=0, column=1, sticky="we")

        self.folderLabel = tk.Label(self.mainFrame, text="Folder", font=(self.defaultFont, self.defaultFontSize))
        self.folderLabel.grid(row=1, column=0, sticky="w", padx=(0, 20))
        self.folderField = tk.Entry(self.mainFrame, font=(self.defaultFont, self.defaultFontSize))
        self.folderField.grid(row=1, column=1, sticky="we")
        self.mainFrame.pack(fill="x", padx=30, pady=(0, 20)) # NOTE: (top, bottom) -- So this is 20px bottom padding.

        self.outputPathsLabel = tk.Label(self.mainFrame, text="Output Paths Type", font=(self.defaultFont, self.defaultFontSize))
        self.outputPathsLabel.grid(row=2, column=0, sticky="w", padx=(0, 20))

        self.submitButton = tk.Button(self.mainWindow, text="Search", font=(self.defaultFont, self.defaultFontSize), command=self.onClick)
        self.submitButton.pack()

        self.resultsTextArea = tk.Text(self.mainWindow, font=(self.defaultFont, self.defaultFontSize))
        self.resultsTextArea.pack(padx=20, pady=20)

    def onClick(self):
        # NOTE: "1.0" means Line 1, Index 0.
        self.resultsTextArea.delete("1.0", tk.END)
        self.resultsTextArea.insert("1.0", "Pattern: " + self.patternField.get() + "\nFolder: " + self.folderField.get() + "\n")
        print("CLICKED!")

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

    async def onClickAsync(self, searchPattern: str, folderPath: str):
        results = await searchInFiles(folderPath, searchPattern)
        for filePath in results:
            print("filePath = " + filePath)


    def run(self):
        self.mainWindow.mainloop()
