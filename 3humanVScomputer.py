import random
import tkinter as tk
from tkinter import ttk

def close_program(event):
    root.destroy()

def simulate_coin_flips(n = 100):
    return [random.choice(["K", "W"]) for _ in range(n)]

def human_like_coin_flips(n = 100, cols = 10):
    sequence = []
    last = None
    for i in range(n):
        row, col = divmod(i, cols)
        if last is None:
            last = random.choice(["K", "W"])
        else:
            neighbors = []
            if col > 0:
                neighbors.append(sequence[i - 1])
            if row > 0:
                neighbors.append(sequence[i - cols])
            if len(neighbors) > 0 and random.random() < 0.85:
                last = "K" if "W" in neighbors else "W"
            else:
                last = random.choice(["K", "W"])
        sequence.append(last)
    return sequence

def highlight_clusters(grid_values, label_refs, threshold = 5):
    rows = len(grid_values)
    cols = len(grid_values[0] if rows > 0 else 0)
    visited = set()

    def get_cluster(r, c):
        stack = [(r, c)]
        cluster = []
        value = grid_values[r][c]
        while stack:
            x, y = stack.pop()
            if (x, y) not in visited:
                visited.add((x, y))
                if grid_values[x][y] == value:
                    cluster.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if (nx, ny) not in visited:
                                stack.append((nx, ny))
        return cluster
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                cluster = get_cluster(r, c)
                if len(cluster) >= threshold:
                    cluster_value = grid_values[r][c]
                    color = "lightblue" if cluster_value == "K" else "red"
                    for (cx, cy) in cluster:
                        label_refs[cx][cy].config(bg=color)

def display_table():
    results = human_like_coin_flips() if human_mode else simulate_coin_flips()

    for widget in frame.winfo_children():
        widget.destroy()

    title_text = "Menschlich simulierte Münzwürfe" if human_mode else "Computergenerierte Münzwürfe"
    title_label = tk.Label(frame, text=title_text, font=("Helvetica", 24, "bold"), fg="#222", bg="#ddd", pady=10)
    title_label.pack()

    num_cols = 10
    num_rows = len(results) // num_cols
    if len(results) % num_cols != 0:
        num_rows += 1

    grid_values = [[None for _ in range(num_cols)] for _ in range(num_rows)]
    label_refs = [[None for _ in range(num_cols)] for _ in range(num_rows)]

    grid_frame = tk.Frame(frame, bg="#ddd")
    grid_frame.pack(pady=20)

    def fill_cell(index):
        if index < len(results):
            row, col = index // num_cols, index % num_cols
            cell_value = results[index]
            grid_values[row][col] = cell_value
            bg_color = "#f0f0f0" if row % 2 == 0 else "#ffffff"
            cell_label = tk.Label(grid_frame, text=cell_value, borderwidth=1, relief="solid",
                                  bg = bg_color, font=("Helvetica", 16), width=4, height=2)
            cell_label.grid(row=row, column=col, padx=5, pady=5)
            label_refs[row][col] = cell_label
            root.after(10, lambda: fill_cell(index + 1))
        else:
            count_K = results.count("K")
            count_W = results.count("W")
            count_label = tk.Label(frame, text=f"Kopf (K): {count_K} | Wappen (W): {count_W}",
                                   font=("Helvetica", 14), fg="#444")
            count_label.pack(pady=15)
            highlight_clusters(grid_values, label_refs, threshold=5)

    fill_cell(0) 

def toggle_mode(event):
    global human_mode
    human_mode = not human_mode
    display_table()

def show_typing_effect(text, label, index=0):
    if index < len(text):
        label.config(text=label.cget("text") + text[index])
        root.after(10, lambda: show_typing_effect(text, label, index + 1))

def show_message(event):
    for widget in frame.winfo_children():
        widget.destroy()
    message_label = tk.Label(frame, text="", font=("Arial", 24), fg="black", pady=200)
    message_label.pack(anchor="center")
    text = "Menschen neigen dazu, Zufallsfolgen gleichmäßiger zu verteilen\n als sie tatsächlich wären, da unser Gehirn\n unbewusst Muster vermeidet. Computer hingegen folgen reinen\n Wahrscheinlichkeiten, sodass ungewöhnlich erscheinende\n Sequenzen - wie mehrfach gleiche Werte hintereinander - völlig normal\n sind. Mathematisch gesehen sind solche Muster durch\n die Unabhängigkeit der Ereignisse erklärbar: Die Wahrscheinlichkeit\n einer bestimmten Sequenz bleibt immer \ngleich, unabhängig von vorherigen Würfen."
    show_typing_effect(text, message_label)

root = tk.Tk()
root.title("Münzwurf Ergebnisse")
root.attributes("-fullscreen", True)

human_mode = True

tk.Frame(root).pack(expand=True)
frame = tk.Frame(root, bg="#ddd", padx=20, pady=20)
frame.pack()

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16), padding=10)
restart_btn = ttk.Button(root, text="Neustart", command=display_table, style="TButton")
restart_btn.pack(pady=20)

display_table()

root.bind("x", close_program)
root.bind("n", toggle_mode)
root.bind("m", show_message)

root.mainloop()