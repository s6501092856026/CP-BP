import tkinter as tk

def open_dialog():
    dialog = tk.Toplevel()  # Create a top-level window (modal)
    dialog.title("Custom Dialog")

    label = tk.Label(dialog, text="Enter your message:")
    label.pack()

    entry = tk.Entry(dialog)
    entry.pack()

    def submit_message():
        message = entry.get()
        # Process the message (e.g., display in main window)
        print("Message:", message)
        dialog.destroy()  # Close the dialog

    submit_button = tk.Button(dialog, text="Submit", command=submit_message)
    submit_button.pack()

root = tk.Tk()

dialog_button = tk.Button(root, text="Open Dialog", command=open_dialog)
dialog_button.pack()

root.mainloop()