import sys
import threading
from pynput import keyboard
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# A worker class that will listen for key presses in a separate thread
class KeyPressWorker(QObject):
    # Define a signal to send key press data to the main GUI thread
    key_pressed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def on_key_press(self, key):
        """Callback function for key press events."""
        try:
            # Capture the key as text (for normal keys like a-z)
            key_text = key.char
        except AttributeError:
            # For special keys like Enter, Shift, etc.
            key_text = str(key)

        # Emit the key pressed signal
        self.key_pressed.emit(key_text)

    def start_listening(self):
        """Start listening for key press events in a separate thread."""
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

class KeyPressWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Key Press Display")
        self.setGeometry(100, 100, 300, 200)

        # Create a label to display the key presses
        self.label = QLabel("Press any key", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Create the worker for key press events
        self.worker = KeyPressWorker()

        # Connect the signal to update the label in the main GUI thread
        self.worker.key_pressed.connect(self.update_label)

        # Start the key press listener in a separate thread
        self.listener_thread = threading.Thread(target=self.worker.start_listening)
        self.listener_thread.daemon = True  # Ensure thread exits when the program exits
        self.listener_thread.start()

    def update_label(self, key_text):
        """Slot to update the label text with the pressed key."""
        self.label.setText(f"Key Pressed: {key_text}")

def main():
    app = QApplication(sys.argv)

    window = KeyPressWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
