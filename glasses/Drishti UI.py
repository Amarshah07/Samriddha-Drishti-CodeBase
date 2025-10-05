import customtkinter as ctk
import subprocess
import threading
import time

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

processes = {}

def toggle_mode(mode, script, loading_label):
    if mode_states[mode].get():
        loading_label.configure(text="Starting...", text_color="yellow")
        
        def start_script():
            time.sleep(0.5) 
            processes[mode] = subprocess.Popen(["python", script])
            loading_label.configure(text="Running...", text_color="green")

        threading.Thread(target=start_script, daemon=True).start()

    else:
       
        if mode in processes:
            processes[mode].terminate()
            processes[mode] = None
        
        
        loading_label.configure(text="", text_color="red")


root = ctk.CTk()
root.title("Samriddha Drishti - AI Glasses Mode Selector")
root.geometry("700x550")


title_label = ctk.CTkLabel(root, text="🔹 Samriddha Drishti - AI Glasses 🔹", 
                           font=("Arial", 18, "bold"), text_color="white")
title_label.pack(pady=15)


modes = {
    "ObjectFinder": "object detection.py",
    "Face Recognition": "face recognition.py",
    #"Reading Mode": "Reading.py",
    "Drishti Vision": "gemini_scene.py",
    "QR Scanner": "QR code.py",
    "Navigation ": "IN Nav.py",


}

mode_states = {}

# Create Buttons for Each Mode
for mode, script in modes.items():
    mode_states[mode] = ctk.BooleanVar(value=False)

    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, padx=20, fill="x")

    label = ctk.CTkLabel(frame, text=mode, font=("Arial", 14, "bold"), text_color="white")
    label.pack(side="left", padx=15)

    # Loading label for status
    loading_label = ctk.CTkLabel(frame, text="", font=("Arial", 12), text_color="red")
    loading_label.pack(side="left", padx=10)

    switch = ctk.CTkSwitch(frame, text="ON / OFF", variable=mode_states[mode], 
                           font=("Arial", 12), 
                           command=lambda m=mode, s=script, l=loading_label: toggle_mode(m, s, l))
    switch.pack(side="right", padx=15)

# Run GUI
root.mainloop()
