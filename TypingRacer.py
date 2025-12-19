import tkinter as tk
from tkinter import ttk
import random
import time

# ----------------------------------------------------
# App Setup
# ----------------------------------------------------
root = tk.Tk()
root.title("typing racer - Edition")
root.geometry("1000x700")
root.configure(bg="#1e1e1e")

# ----------------------------------------------------
# Paragraph Library
# ----------------------------------------------------
paragraphs = {
    "Interstellar": [
        "Love is the one thing we're capable of perceiving that transcends dimensions of time and space.",
        "We used to look up at the sky and wonder at our place in the stars. Now we just look down and worry about our place in the dirt.",
        "We've always defined ourselves by the ability to overcome the impossible. And we count these moments.",
        "We're explorers, pioneers, not caretakers."
    ],
    "Harry Potter": [
        "It does not do to dwell on dreams and forget to live.",
        "Happiness can be found even in the darkest of times, if one only remembers to turn on the light.",
        "It is our choices that show what we truly are, far more than our abilities.",
        "We've all got both light and dark inside us."
    ],
    "Friends": [
        "Welcome to the real world. It sucks. You're gonna love it!",
        "We were on a break!",
        "I'm not great at the advice. Can I interest you in a sarcastic comment?",
        "How you doin?"
    ],
    "Taylor Swift": [
        "Cause baby now we got bad blood.",
        "I shake it off, I shake it off!",
        "I stay out too late, got nothing in my brain.",
        "We are never ever getting back together."
    ]
}
# ====================================================
# LOGIN PAGE
# ====================================================

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        login_error.config(text="Enter both username and password")
        return

    # Hide login page and show main UI
    login_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

    # Enable typing UI
    entry.config(state="normal")
    entry.focus()

    # Load initial quote
    category_var.set(list(paragraphs.keys())[0])
    load_quote(random.choice(paragraphs[category_var.get()]))

def back_to_login():
    # Hide main UI and show login page
    main_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)
    
    # Clear login fields
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_error.config(text="")
    
    # Reset typing state
    entry.config(state="disabled")
    entry.delete(0, tk.END)


login_frame = tk.Frame(root, bg="#1e1e1e")
login_frame.pack(fill="both", expand=True)

login_title = tk.Label(login_frame, text="LOGIN", font=("Arial Black", 32),
                       fg="#00d4ff", bg="#1e1e1e")
login_title.pack(pady=40)

username_label = tk.Label(login_frame, text="Username:", font=("Arial", 18),
                          fg="white", bg="#1e1e1e")
username_label.pack()
username_entry = tk.Entry(login_frame, font=("Arial", 18), width=25)
username_entry.pack(pady=10)

password_label = tk.Label(login_frame, text="Password:", font=("Arial", 18),
                          fg="white", bg="#1e1e1e")
password_label.pack()
password_entry = tk.Entry(login_frame, font=("Arial", 18), width=25, show="*")
password_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", font=("Arial", 18),
                         bg="#00d4ff", fg="black", width=12, command=login)
login_button.pack(pady=20)

login_error = tk.Label(login_frame, text="", font=("Arial", 14),
                       fg="#ff4d4d", bg="#1e1e1e")
login_error.pack()

# Bind Enter key to login
username_entry.bind("<Return>", lambda e: password_entry.focus())
password_entry.bind("<Return>", lambda e: login())
username_entry.focus()


# ====================================================
# MAIN APPLICATION (HIDDEN UNTIL LOGIN)
# ====================================================

main_frame = tk.Frame(root, bg="#1e1e1e")


# ----------------------------------------------------
# Global State
# ----------------------------------------------------
target_text = ""
start_time = None
timer_running = False
current_errors = 0
quote_history = []

personal_best_wpm = 0.0
personal_best_accuracy = 0.0
personal_best_time = 0.0

# ----------------------------------------------------
# Timer
# ----------------------------------------------------
def update_timer():
    if timer_running:
        elapsed = time.time() - start_time
        timer_label.config(text=f"Time: {elapsed:.2f}s")
        root.after(50, update_timer)

# ----------------------------------------------------
# Text Coloring
# ----------------------------------------------------
def update_text_display():
    user_input = entry.get()
    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)

    for i in range(len(target_text)):
        if i < len(user_input):
            if user_input[i] == target_text[i]:

                text_display.insert(tk.END, target_text[i], "correct")
            else:
                text_display.insert(tk.END, target_text[i], "incorrect")
        elif i == len(user_input):
            text_display.insert(tk.END, target_text[i], "current")
        else:
            text_display.insert(tk.END, target_text[i], "pending")

    text_display.config(state="disabled")

# ----------------------------------------------------
# Stats Update
# ----------------------------------------------------
def update_stats(event=None):
    global current_errors
    user_input = entry.get()
    current_errors = 0

    for i in range(min(len(user_input), len(target_text))):
        if user_input[i] != target_text[i]:
            current_errors += 1

    current_errors += abs(len(user_input) - len(target_text))

    if target_text:
        progress = (len(user_input) / len(target_text)) * 100
        progress_bar["value"] = min(100, progress)

    if start_time:
        elapsed = time.time() - start_time
        wpm = (len(user_input) / 5) / (elapsed / 60) if elapsed > 0 else 0
        accuracy = max(0, ((len(target_text) - current_errors) / len(target_text)) * 100)
        stats_label.config(text=f"WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}% | Errors: {current_errors}")
    else:
        stats_label.config(text=f"Errors: {current_errors}")

    update_text_display()

    if user_input == target_text and target_text:
        check_result()

# ----------------------------------------------------
# Start Timer on First Key
# ----------------------------------------------------
def start_timer(event):
    global start_time, timer_running
    if start_time is None and target_text:
        start_time = time.time()
        timer_running = True
        update_timer()

# ----------------------------------------------------
# Load Quote
# ----------------------------------------------------
def load_quote(text):
    global target_text, start_time, timer_running, current_errors
    if target_text:
        quote_history.append(target_text)

    target_text = text
    start_time = None
    timer_running = False
    current_errors = 0

    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.focus()

    text_display.config(state="normal")
    text_display.delete("1.0", tk.END)
    text_display.insert("1.0", target_text, "pending")
    text_display.config(state="disabled")

    timer_label.config(text="Time: 0.00s")
    stats_label.config(text="Errors: 0")
    result_label.config(text="")
    progress_bar["value"] = 0

# ----------------------------------------------------
# Buttons
# ----------------------------------------------------
def random_from_category():
    cat = category_var.get()
    load_quote(random.choice(paragraphs[cat]))

def randomize_all():
    cat = random.choice(list(paragraphs.keys()))
    category_var.set(cat)
    load_quote(random.choice(paragraphs[cat]))

def restart_test():
    if target_text:
        load_quote(target_text)

def go_back():
    if quote_history:
        load_quote(quote_history.pop())

# ----------------------------------------------------
# Final Result
# ----------------------------------------------------
def check_result(event=None):
    global timer_running, personal_best_wpm, personal_best_accuracy, personal_best_time

    timer_running = False
    elapsed = time.time() - start_time if start_time else 0
    user_input = entry.get()

    errors = sum(
        1 for i in range(min(len(user_input), len(target_text)))
        if user_input[i] != target_text[i]
    ) + abs(len(user_input) - len(target_text))

    wpm = (len(user_input) / 5) / (elapsed / 60) if elapsed > 0 else 0
    accuracy = max(0, ((len(target_text) - errors) / len(target_text)) * 100)

    if wpm > personal_best_wpm:
        personal_best_wpm = wpm
    if accuracy > personal_best_accuracy:
        personal_best_accuracy = accuracy
    if personal_best_time == 0 or elapsed < personal_best_time:
        personal_best_time = elapsed

    pb_label.config(
        text=f"Personal Best: {personal_best_wpm:.1f} WPM | {personal_best_accuracy:.1f}%"
    )

    result_label.config(
        text=f"Final — WPM: {wpm:.1f} | Accuracy: {accuracy:.1f}% | Time: {elapsed:.2f}s"
    )

    entry.config(state="disabled")
    progress_bar["value"] = 100

# ----------------------------------------------------
# UI
# ----------------------------------------------------
tk.Label(main_frame, text="Type Racer", font=("Arial Black", 32),
         fg="#00d4ff", bg="#1e1e1e").pack(pady=20)

top = tk.Frame(main_frame, bg="#1e1e1e")
top.pack()

tk.Label(top, text="Category:", fg="white",
         bg="#1e1e1e", font=("Arial", 14)).grid(row=0, column=0)

category_var = tk.StringVar(value="Interstellar")
tk.OptionMenu(top, category_var, *paragraphs.keys()).grid(row=0, column=1)

btns = tk.Frame(main_frame, bg="#1e1e1e")
btns.pack(pady=10)

tk.Button(btns, text="Random All", command=randomize_all).grid(row=0, column=0, padx=5)
tk.Button(btns, text="Random Category", command=random_from_category).grid(row=0, column=1, padx=5)
tk.Button(btns, text="Back", command=go_back).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Restart", command=restart_test).grid(row=0, column=3, padx=5)
tk.Button(btns, text="Back to Login", command=back_to_login, 
          bg="#ff4d4d", fg="white", activebackground="#ff6666").grid(row=0, column=4, padx=5)

text_display = tk.Text(main_frame, height=6, font=("Courier New", 16),
                       bg="#292929", fg="white", state="disabled")
text_display.pack(padx=20, pady=10, fill=tk.BOTH)

text_display.tag_config("correct", foreground="#7dff7d")
text_display.tag_config("incorrect", foreground="#ff4d4d")
text_display.tag_config("current", foreground="#00d4ff", underline=True)
text_display.tag_config("pending", foreground="#888888")

entry = tk.Entry(main_frame, font=("Courier New", 18), width=70, state="disabled")
entry.pack(pady=10)

entry.bind("<KeyPress>", start_timer)
entry.bind("<KeyRelease>", update_stats)
entry.bind("<Return>", check_result)

progress_bar = ttk.Progressbar(main_frame, length=600)
progress_bar.pack(pady=5)

stats_frame = tk.Frame(main_frame, bg="#1e1e1e")
stats_frame.pack()
    
timer_label = tk.Label(stats_frame, text="Time: 0.00s",
                       fg="#00d4ff", bg="#1e1e1e", font=("Arial", 14))
timer_label.grid(row=0, column=0, padx=10)

stats_label = tk.Label(stats_frame, text="Errors: 0",
                       fg="#ff4d4d", bg="#1e1e1e", font=("Arial", 14))
stats_label.grid(row=0, column=1, padx=10)

result_label = tk.Label(main_frame, text="", fg="#7dff7d",
                        bg="#1e1e1e", font=("Arial", 16, "bold"))
result_label.pack(pady=10)

pb_label = tk.Label(main_frame, text="Personal Best: None",
                    fg="#888888", bg="#1e1e1e", font=("Arial", 12))
pb_label.pack()

root.mainloop()