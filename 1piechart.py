import random
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

is_paused = False
update_running = False  # Verhindert doppelte Updates

def update_chart():
    global count_K, count_W, canvas, ax, mode, probabilities, is_paused, update_running

    if not update_running:
        return  # Falls das Update gestoppt wurde (z. B. durch Pause)

    if not is_paused:
        flip = random.choice(['K', 'W'])
        if flip == 'K':
            count_K += 1
        else:
            count_W += 1

        total = count_K + count_W
        probabilities.append(count_K / total * 100)

    ax.clear()
    if mode == "pie":
        wedges, texts, autotexts = ax.pie(
            [count_K, count_W], labels=["Kopf", "Wappen"],
            autopct='%1.1f%%', colors=["blue", "red"],
            textprops={'fontsize': max(16, int(root.winfo_width() * 0.02)), 'weight': 'bold'}
        )
        for autotext in autotexts:
            autotext.set_color("yellow")
            autotext.set_fontsize(max(20, int(root.winfo_width() * 0.02)))
            autotext.set_weight("bold")
        ax.set_title("Münzwurf-Verteilung", fontsize=max(20, int(root.winfo_width() * 0.03)))
    else:
        ax.plot(range(1, total + 1), probabilities, label="% Kopf", color="blue")
        ax.axhline(y=50, color="red", linestyle="dashed", label="50% Erwartungswert")
        ax.set_xlabel("Anzahl der Würfe")
        ax.set_ylabel("% Kopf")
        ax.set_title("Wahrscheinlichkeitsentwicklung")
        ax.legend()

    canvas.draw()

    count_label.config(
        text=f"Kopf (K): {count_K} | Wappen (W): {count_W} | Insgesamt: {total}",
        font=("Arial", max(16, int(root.winfo_width() * 0.025))),
    )

    if update_running:  # Nur wenn nicht gestoppt, soll es weiterlaufen
        root.after(100, update_chart)

def close_app(event=None):
    global update_running
    update_running = False  # Stoppt den Update-Loop
    root.destroy()

def resize(event):
    fig.set_size_inches(root.winfo_width() / 100, root.winfo_height() / 100)
    canvas.get_tk_widget().config(width=root.winfo_width(), height=root.winfo_height() - 50)
    canvas.draw()

def switch_chart(event=None):
    global mode 
    mode = "line" if mode == "pie" else "pie"
    update_chart()

def start_simulation():
    global count_K, count_W, probabilities, is_paused, update_running
    count_K = 0
    count_W = 0
    probabilities = []
    is_paused = False
    update_running = True  # Wieder Updates erlauben
    update_chart()

def toggle_pause(event=None):
    global is_paused
    is_paused = not is_paused
    if not is_paused:  # Wenn wieder gestartet wird, update erneut auslösen
        update_chart()

root = tk.Tk()
root.title("Live Münzwurf Simulation")
root.state("zoomed")

# Key-Bindings korrigiert
root.bind("<Escape>", close_app)  # Escape zum Beenden
root.bind("<Configure>", resize)
root.bind("n", switch_chart)
root.bind("p", toggle_pause)

count_K = 0
count_W = 0
probabilities = []
mode = "pie"

count_label = tk.Label(root, text=f"Kopf (K): {count_K} | Wappen (W): {count_W}", font=("Arial", 20))
count_label.pack(pady=10)

fig, ax = plt.subplots(figsize=(8, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.after(100, start_simulation)
root.mainloop()