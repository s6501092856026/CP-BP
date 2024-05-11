import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_graph():
    x = [1, 2, 3, 4, 5]
    y = [2, 3, 5, 7, 11]

    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    plot.plot(x, y)

    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Matplotlib Graph in Tkinter")

plot_button = ttk.Button(root, text="Plot Graph", command=plot_graph)
plot_button.pack(pady=10)

root.mainloop()