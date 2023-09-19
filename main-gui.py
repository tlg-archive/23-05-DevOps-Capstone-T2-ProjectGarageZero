import tkinter as tk

class ProjectZeroGUI:
    def __init__(self):

        #initilize the tkinter window and size
        self.root = tk.Tk()
        self.root.geometry("500x500")

        #general label settings
        self.label = tk.Label(self.root, text="Hello World")
        self.label.pack()

        #example button
        self.start_button = tk.Button(self.root, text="Start Game")
        self.start_button.pack()

        #display the window
        self.root.mainloop()

    #define functions below

if __name__ == "__main__":
    ProjectZeroGUI()