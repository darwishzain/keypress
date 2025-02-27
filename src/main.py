import tkinter as tk
from pynput import keyboard
import threading
import time

# Function to clear the label after a timeout
def clearlabel():
    label.config(text="")

# This function will be called when a key is pressed
def onkeypress(key):
    try:
        # Display the key pressed in the label
        label.config(text=f"{key.char}")
    except AttributeError:
        label.config(text=f"{key.name}")

    # Reset the timer to clear the label after a timeout
    reset_timer()

# Function to reset the timer that clears the label
def reset_timer():
    global last_key_time
    last_key_time = time.time()

# Create the main window
root = tk.Tk()
root.title(" ")
root.geometry("300x150")
#root.overrideredirect(True)  # Remove window decorations (title bar, borders, etc.)
root.config(bg='white')  # Set background color of the window to black (invisible)

# Make the window background transparent (for Linux or macOS, this works; for Windows, you may need a workaround)
#root.attributes("-transparentcolor", "black")  # Make black color transparent

# Create a label to display the pressed key
label = tk.Label(root, text="", font=("Helvetica", 30),fg="black", bg="white")
label.pack(pady=50)

# Timer variable to check for inactivity
last_key_time = time.time()

# Function to check for inactivity and clear the label
def idle():
    global last_key_time
    while True:
        time.sleep(0.1)  # Check every 100ms for inactivity
        if time.time() - last_key_time > 0.5:  # 0.5 seconds of inactivity
            clearlabel()

# Set up the listener for the keyboard
def startlistener():
    with keyboard.Listener(on_press=onkeypress) as listener:
        listener.join()

# Start the key listener in a separate thread
listener_thread = threading.Thread(target=startlistener, daemon=True)
listener_thread.start()

# Start the inactivity check in a separate thread
inactivity_thread = threading.Thread(target=idle, daemon=True)
inactivity_thread.start()

# Start the Tkinter main loop
root.mainloop()
