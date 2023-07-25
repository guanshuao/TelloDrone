import tkinter as tk
import os
import subprocess

def run_script(path):
    subprocess.Popen(['python', path])

root = tk.Tk()
root.title("Python Script Runner")

# Set window size
root.geometry("500x500")

# Define the paths
paths = [
    './Mapping/Mapping.py',
    './Surveillance/Surveillance.py',
    './ObjectDetection/ObjectDetectionDemo.py',
    './BodyFollowing/BodyDetectionDemo.py',
    './ColorObjectTracking/ColorObjectTrackingDemo.py',
    './FaceFollowing/FaceDetection.py',
    './SelfieDrone/GestureDetectionDemo.py',
    './HandGestureControl/HandGesture.py'
]

# Define the button names
button_names = [
    'Mapping',
    'Surveillance',
    'ObjectDetection',
    'BodyFollowing',
    'ColorObjectTracking',
    'FaceFollowing',
    'SelfieDrone',
    'HandGestureControl'
]

# Generate the buttons
for i in range(8):
    button = tk.Button(root, text=button_names[i], command=lambda path=paths[i]: run_script(path), height = 2, width = 20)
    button.pack(pady = 10)

root.mainloop()
