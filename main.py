import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Passing App")
        self.geometry("1000x800")

        # 1. Create central variables to store the data
        self.p1_name = ""
        self.p2_name = ""

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.frames = {}

        for ScreenClass in (ScreenOne, ScreenTwo):
            screen_name = ScreenClass.__name__
            frame = ScreenClass(parent=self.container, controller=self)
            self.frames[screen_name] = frame

        self.show_frame("ScreenOne")

    def show_frame(self, screen_name):
        frame = self.frames[screen_name]
        
        # 2. TRIGGER A REFRESH: If we are opening ScreenTwo, tell it to update its labels
        if screen_name == "ScreenTwo":
            frame.update_display()

        for f in self.frames.values():
            f.pack_forget()
        
        frame.pack(fill="both", expand=True)


class ScreenOne(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.p1_score_num = 0
        self.controller.p2_score_num = 0

        player1_label = ctk.CTkLabel(self, text="Player 1", font=("Arial",20,"bold"))
        player1_label.pack()

        self.player1_entry = ctk.CTkEntry(self, placeholder_text="Enter Name")
        self.player1_entry.pack()

        player2_label = ctk.CTkLabel(self, text="Player 2", font=("Arial",20,"bold"))
        player2_label.pack()

        self.player2_entry = ctk.CTkEntry(self, placeholder_text="Enter Name")
        self.player2_entry.pack(pady=0)

        self.submit_btn = ctk.CTkButton(self, text="Next", command=self.save_and_move)
        self.submit_btn.pack(pady=20)

    def save_and_move(self):
        # 3. Grab the data from entries and save it to the controller
        self.controller.p1_name = self.player1_entry.get()
        self.controller.p2_name = self.player2_entry.get()

        # Move to the next screen
        self.controller.show_frame("ScreenTwo")


class ScreenTwo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.p1_score_num = self.controller.p1_score_num
        self.p2_score_num = self.controller.p2_score_num
        
        # Back Button - Now calls go_back instead of directly changing frames
        back_btn = ctk.CTkButton(self, text="<--", command=self.go_back)
        back_btn.grid(row=0, column=0, columnspan=2, pady=20, sticky="nw")

        label = ctk.CTkLabel(self, text="Score", font=("Arial",35, "bold"))
        label.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.p1_label = ctk.CTkLabel(self, text=" ", font=("Arial",28))
        self.p1_label.grid(row=2, column=0, pady=25, padx=10, sticky="e")
        self.p1_score = ctk.CTkLabel(self, text=f"{self.p1_score_num}", font=("Arial",20))
        self.p1_score.grid(row=3, column=1, padx=0,sticky="w")
        
        self.p2_label = ctk.CTkLabel(self, text=" ", font=("Arial",28))
        self.p2_label.grid(row=2, column=4, padx=100,sticky="e")
        
        self.p2_score = ctk.CTkLabel(self, text=f"{self.p2_score_num}", font=("Arial",20))
        self.p2_score.grid(row=3, column=4, pady=25, padx=100, sticky="w")

        self.controller.bind("<w>", self.update_score_1)
        self.controller.bind("<Up>", self.update_score_2)
        self.controller.bind("<s>", self.lower_score_1)
        self.controller.bind("<Down>", self.lower_score_2)
    def go_back(self):
        # Reset the scores internally
        self.p1_score_num = 0
        self.p2_score_num = 0
        
        # Update the text on the labels to show 0
        self.p1_score.configure(text="0")
        self.p2_score.configure(text="0")
        
        # Switch back to ScreenOne
        self.controller.show_frame("ScreenOne")

    def update_display(self):
        # 4. Pull the saved data from the controller and show it on the UI
        p1_name = self.controller.p1_name
        p2_name = self.controller.p2_name
        
        self.p1_label.configure(text=p1_name)
        self.p2_label.configure(text=p2_name)
        
    def update_score_1(self, event):
        self.p1_score_num += 1
        self.p1_score.configure(text=f"{self.p1_score_num}")
        
    def update_score_2(self, event):
        self.p2_score_num += 1
        self.p2_score.configure(text=f"{self.p2_score_num}")
        
    def lower_score_1(self, event):
        self.p1_score_num -= 1
        self.p1_score.configure(text=f"{self.p1_score_num}")
        
    def lower_score_2(self, event):
        self.p2_score_num -= 1
        self.p2_score.configure(text=f"{self.p2_score_num}")


if __name__ == "__main__":
    app = App()
    app.mainloop()