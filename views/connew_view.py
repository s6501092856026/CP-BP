import tkinter as tk
from tkinter import ttk

class ConnewView(ttk.Frame):

    def __init__(self, controller, app):
        super().__init__(app)
        self.controller = controller

       # Window

        self.entry_amout = ttk.Entry(self)
        self.entry_amout.grid(row=3,column=2, padx=10, pady=10, sticky='NEW')

        self.label_unit = ttk.Label(self, text = "Unit", justify='center')
        self.label_unit.grid(row=3,column=2, padx=10, pady=10)

        self.back_button = ttk.Button(self, text="Back")
        self.back_button.grid(row=0, column=0, padx=5, pady=10, sticky='W')

        self.add_button = ttk.Button(self, text="Add")
        self.add_button.grid(row=4,column=2, padx=10, pady=10, sticky='NEW')

        self.delete_button = ttk.Button(self, text="Delete")
        self.delete_button.grid(row=4,column=2, padx=10, pady=10, sticky='EW')
        
        self.bp_button = ttk.Button(self, text="Break-even Point")
        self.bp_button.grid(row=5, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky='NEW')

        self.complete_button = ttk.Button(self, text="Complete")
        self.complete_button.grid(row=5, column=2, padx=10, pady=10, ipadx=10, ipady=20, sticky='SEW')

        # Budgets
        self.list_treeview = ttk.Treeview(self, columns=("ID", "Name"), show="headings")
        self.list_treeview.heading("ID", text="ID" )
        self.list_treeview.heading("Name", text="Name")
        self.list_treeview.grid(row=3, rowspan=3, column=0, padx=5, pady=5, ipadx=40, ipady=75)
        self.list_treeview.insert("", "end")
        
# Create the main application window
root = tk.Tk()
root.title("Your Window Title")

# Create an instance of the ConnewView class and pass the controller and app as parameters
app = ConnewView(controller=None, app=root)

# Run the Tkinter main loop
root.mainloop()