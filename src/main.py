#import tkinter as tk
from pynput import keyboard
import json,os,sys,threading,time
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton,QVBoxLayout

def fullpath(relative_path):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, relative_path)

def openjson(filename):
    file = fullpath(filename)
    with open(file) as f:
        jsondata = json.load(f)
    return(jsondata)

config = openjson(fullpath('config.json'))
# Main Window Class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle(config['title'])
        self.setGeometry(100, 100, 300, 200)
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel("Welcome", self)
        self.label.setStyleSheet("font-size: 40px;color:"+config['foreground']+";")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #! START
        self.listener = keyboard.Listener(on_press=self.onkeypress)
        self.listener.start()
        #self.clearkeytext()

    def onkeypress(self,key):
        try:
            # Get the key's text and update the label
            keytext = key.char
        except AttributeError:
            # For special keys like space, enter, etc.
            keytext = str(key)

        self.label.setText(f"Key Pressed: {keytext}")

    def changekeytext(self):
        self.label.setText("BTN")

    def clearkeytext(self):
        self.label.setText("")

# Main function to run the app
def main():
    app = QApplication(sys.argv)  # Create the application object
    window = MainWindow()         # Create the main window
    window.show()                 # Show the window
    sys.exit(app.exec())          # Start the event loop

# Run the application
if __name__ == "__main__":
    main()
