import random
import matplotlib.pyplot as plt
import collections
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def roll_dice():
    return random.randint(1, 6)

def simulate_rolls(n):
    return [roll_dice() + roll_dice() for _ in range(n)]

def plot_results(sums):
    counter = collections.Counter(sums)
    keys = sorted(counter.keys())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(keys, [counter[k] for k in keys], color='blue', width=0.8)
    ax.set_xticks(keys)
    ax.set_xlabel("Augensumme", fontsize=20)
    ax.set_ylabel("Häufigkeit", fontsize=20)
    ax.set_title("Häufigkeit der Augensummen mit zwei Würfeln", fontsize=24)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig

def show_combinations():
    global frame, label_entry, entry, btn, label_error
    for widget in frame.winfo_children():
        widget.destroy()
    
    color_map = {2: "red", 12: "red", 3: "orange", 4: "orange", 5: "orange", 9: "orange", 10: "orange", 11: "orange", 6: "green", 7: "blue", 8: "green"}
    
    container = tk.Frame(frame)
    container.pack(pady=20)
    
    text_container = tk.Frame(container)
    text_container.pack(side="left", padx=20)
    
    legend_container = tk.Frame(container)
    legend_container.pack(side="right", padx=40)
    
    for s in range(2, 13):
        combinations = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s]
        text = f"{s}: " + "  ".join([f"({a},{b})" for a, b in combinations])
        label = tk.Label(text_container, text=text, font=("Arial", 18), fg=color_map[s], justify="left")
        label.pack(anchor="w")
    
    legend_text = "\nRot = Sehr unwahrscheinlich\nOrange = Unwahrscheinlich\nGrün = Wahrscheinlich\nBlau = Sehr wahrscheinlich"
    legend_label = tk.Label(legend_container, text=legend_text, font=("Arial", 18), fg="black", justify="left")
    legend_label.pack()

def toggle_view(event):
    global showing_combinations, frame, control_frame
    showing_combinations = not showing_combinations
    
    if showing_combinations:
        show_combinations()
    else:
        update_plot(False)
    
    control_frame.lift()

def update_plot(recalculate=True):
    global results
    try:
        n = int(entry.get())
        if n <= 0:
            raise ValueError
        
        if recalculate:
            results = simulate_rolls(n)
        
        fig = plot_results(results)
        
        for widget in frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except ValueError:
        label_error.config(text="Bitte eine gültige positive Zahl eingeben.")

def close_app(event):
    root.destroy()

showing_combinations = False
results = []

root = tk.Tk()
root.title("Würfelsimulation")
root.state("zoomed")
root.bind("x", close_app)
root.bind("n", toggle_view)

control_frame = tk.Frame(root)
control_frame.pack(side="top", fill="x")

label_entry = tk.Label(control_frame, text="Anzahl der Simulationen:", font=("Arial", 20))
label_entry.pack()
entry = ttk.Entry(control_frame, font=("Arial", 18))
entry.pack()
entry.insert(0, "50")

btn = ttk.Button(control_frame, text="New", command=lambda: update_plot(True))
btn.pack()

label_error = tk.Label(control_frame, text="", fg="red", font=("Arial", 16))
label_error.pack()

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

update_plot(True)
control_frame.lift()

root.mainloop()