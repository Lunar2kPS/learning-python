import tkinter as tk

mainWindow = tk.Tk()

mainWindow.geometry("800x600")
mainWindow.title("My First Python Program")

label = tk.Label(mainWindow, text="Hello World!", font=('Arial', 18))
label.pack(padx=20, pady=20)

# (tk.Text(...) is a multi-line text area)
textbox = tk.Text(mainWindow, font=('Arial', 16), height = 3)
textbox.pack(padx=10)

# (tk.Entry(...) is a ONE-line text field)
entry = tk.Entry(mainWindow)
entry.pack(padx=10, pady=10)

button = tk.Button(mainWindow, text="Click Me!", font=('Arial', 16))
button.pack(padx=10, pady=10)

mainWindow.mainloop()
