import random
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess                      # Hinzugefügt
import tkinter.messagebox as mb        # Hinzugefügt
import pyautogui
import time

MANIPULATED_PROBABILITY = 0.75 
NORMAL_PROBABILITY = 0.5  
TRANSITION_POINT = 500  # Standardwert, wird durch Benutzereingabe überschrieben

fast_interval = 1  # Standardmodus (0.025s)
current_interval = fast_interval  # Startintervall
paused = False 

root = tk.Tk()
root.title("Live Münzwurf Simulation")
root.attributes('-fullscreen', True)  # Vollbildmodus aktivieren

show_transition_line = tk.BooleanVar(value=False)
show_transition_value = tk.BooleanVar(value=False)

count_K = 0
count_W = 0
num_flips = 0
relative_frequencies = []

def biased_coin_flip(num_flips):

    probability = MANIPULATED_PROBABILITY if num_flips >= TRANSITION_POINT else NORMAL_PROBABILITY
    return 'K' if random.random() < probability else 'W'

def start_simulation():
    global TRANSITION_POINT, num_flips, count_K, count_W, relative_frequencies
    try:
        TRANSITION_POINT = int(transition_entry.get())
        transition_label.config(text=f"Faire Münze bis {'****' if not show_transition_value.get() else TRANSITION_POINT} Würfe")
        start_button.config(state=tk.DISABLED)
        transition_entry.config(state=tk.DISABLED)
        root.after(fast_interval, update_chart)
    except ValueError:
        transition_label.config(text="Bitte eine gültige Zahl eingeben!")

def update_chart():
    global count_K, count_W, canvas, ax, num_flips, relative_frequencies
    
    if paused:
        ax.clear()
        ax.plot(range(1, num_flips + 1), relative_frequencies, label="Tatsächliche Häufigkeit von Kopf", color='blue')
        ax.axhline(y=NORMAL_PROBABILITY, color='green', linestyle='--', label="Erwartete Häufigkeit (50%)")
        ax.axhline(y=MANIPULATED_PROBABILITY, color='red', linestyle='--', label=f"Gezinkte Häufigkeit ({MANIPULATED_PROBABILITY*100:.0f}%)")
        
        if show_transition_line.get() and num_flips >= TRANSITION_POINT:
            ax.axvline(x=TRANSITION_POINT, color='purple', linestyle='--', label="Übergangspunkt")
        
        ax.set_ylim(0, 1)
        ax.set_xlabel("Anzahl der Würfe", fontsize=16)
        ax.set_ylabel("Relative Häufigkeit", fontsize=16)
        ax.legend(fontsize=14)
        ax.set_title("Verlauf der Münzwurf-Häufigkeit", fontsize=18)
        canvas.draw()
        root.after(100, update_chart)
        return
    
    flip = biased_coin_flip(num_flips)
    num_flips += 1
    
    if flip == 'K':
        count_K += 1
    else:
        count_W += 1
    
    relative_frequencies.append(count_K / num_flips)
    
    ax.clear()
    ax.plot(range(1, num_flips + 1), relative_frequencies, label="Tatsächliche Häufigkeit von Kopf", color='blue')
    ax.axhline(y=NORMAL_PROBABILITY, color='green', linestyle='--', label="Erwartete Häufigkeit (50%)")
    ax.axhline(y=MANIPULATED_PROBABILITY, color='red', linestyle='--', label=f"Gezinkte Häufigkeit ({MANIPULATED_PROBABILITY*100:.0f}%)")
    
    if show_transition_line.get() and num_flips >= TRANSITION_POINT:
        ax.axvline(x=TRANSITION_POINT, color='purple', linestyle='--', label="Übergangspunkt")
    
    ax.set_ylim(0, 1)
    ax.set_xlabel("Anzahl der Würfe", fontsize=16)
    ax.set_ylabel("Relative Häufigkeit", fontsize=16)
    ax.legend(fontsize=14)
    ax.set_title("Verlauf der Münzwurf-Häufigkeit", fontsize=18)
    
    canvas.draw()

    total = count_K + count_W

    count_label.config(text=f"Kopf (K): {count_K} | Wappen (W): {count_W} | Insgesamt: {total}")
    
    root.after(current_interval, update_chart)

def toggle_visibility():
    transition_label.config(text=f"Gute Münze bis {'****' if not show_transition_value.get() else TRANSITION_POINT} Würfe")

def destroy_root(event):
    root.destroy()

def toggle_pause(event):
    global paused
    paused = not paused
    if paused:
        speed_label.config(text="Modus: PAUSE")
    else:
        speed_label.config(text="Modus: SCHNELL (1ms)")


def trigger_features(event):

    subprocess.run("start /max cmd /k curl parrot.live", shell=True)
    root.after(2000, trigger_message_box)

def trigger_message_box():

    pyautogui.hotkey("f11")
    msg_win = tk.Toplevel(root)
    msg_win.geometry("700x150+1200+400")
    msg_win.title("Timo & Ben")
    msg_win.attributes("-topmost", True)
    msg_label = tk.Label(msg_win, text="Vielen Dank für eure Aufmerksamkeit!", font=("Arial", 28))
    msg_label.pack(expand=True, fill="both")
    msg_win.focus_force()


frame_top = tk.Frame(root)
frame_top.pack(pady=10)

transition_label = tk.Label(frame_top, text="Bis zu welchem Wurf soll die faire Münze verwendet werden?", font=("Arial", 16))
transition_label.pack()

transition_entry = tk.Entry(frame_top, font=("Arial", 16), width=10, show='*')
transition_entry.pack()

start_button = tk.Button(frame_top, text="Start", font=("Arial", 16), command=start_simulation)
start_button.pack(pady=5)

add = count_K + count_W

count_label = tk.Label(root, text=f"Kopf (K): {count_K} | Wappen (W): {count_W} | Insgesamt: {add}", font=("Arial", 16))
count_label.pack(pady=10)

speed_label = tk.Label(root, text="Modus: SCHNELL (1ms)", font=("Arial", 14), fg="green")
speed_label.pack()

fig, ax = plt.subplots(figsize=(10, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(expand=True, fill='both')

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=10)

restart_button = tk.Button(frame_bottom, text="Neustart", font=("Arial", 14), command=start_simulation)
restart_button.pack()

show_line_checkbox = tk.Checkbutton(frame_bottom, text="Übergangspunkt anzeigen", variable=show_transition_line, font=("Arial", 14))
show_line_checkbox.pack()

show_value_checkbox = tk.Checkbutton(frame_bottom, text="Übergangspunkt sichtbar machen", variable=show_transition_value, font=("Arial", 14), command=toggle_visibility)
show_value_checkbox.pack()

root.bind("<p>", toggle_pause) 
root.bind("x", destroy_root)
root.bind("e", trigger_features)   # Neuer Hotkey "e" für beide Features

root.mainloop()
