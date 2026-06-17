import customtkinter as ctk 
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Passing App")
        self.geometry("1000x800")

        # 1. Central variables to store global state
        self.p1_name = ""
        self.p2_name = ""
        self.p1_score_num = 0
        self.p2_score_num = 0

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.frames = {}

        # Loop initializes both screens cleanly with uniform parameters
        for ScreenClass in (ScreenOne, ScreenTwo):
            screen_name = ScreenClass.__name__
            frame = ScreenClass(parent=self.container, controller=self)
            self.frames[screen_name] = frame

        self.show_frame("ScreenOne")

    def show_frame(self, screen_name):
        frame = self.frames[screen_name]
        
        # TRIGGER A REFRESH: Fetch updated controller names/scores when entering ScreenTwo
        if screen_name == "ScreenTwo":
            frame.update_display()

        for f in self.frames.values():
            f.pack_forget()
        
        frame.pack(fill="both", expand=True)


class ScreenOne(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        player1_label = ctk.CTkLabel(self, text="Player 1", font=("Arial",20,"bold"))
        player1_label.pack(pady=(20, 5))

        self.player1_entry = ctk.CTkEntry(self, placeholder_text="Enter Name")
        self.player1_entry.pack(pady=5)

        player2_label = ctk.CTkLabel(self, text="Player 2", font=("Arial",20,"bold"))
        player2_label.pack(pady=(20, 5))

        self.player2_entry = ctk.CTkEntry(self, placeholder_text="Enter Name")
        self.player2_entry.pack(pady=5)

        self.submit_btn = ctk.CTkButton(self, text="Next", command=self.save_and_move)
        self.submit_btn.pack(pady=20)

    def save_and_move(self):
        # Grab data from entry fields and save to central controller
        self.controller.p1_name = self.player1_entry.get() or "Player 1"
        self.controller.p2_name = self.player2_entry.get() or "Player 2"

        # Advance screen
        self.controller.show_frame("ScreenTwo")

    def clear_entries(self):
        """Helper function called by ScreenTwo to clear fields when going back"""
        self.player1_entry.delete(0, tk.END)
        self.player2_entry.delete(0, tk.END)


# Inherit safely from CTkFrame only
class ScreenTwo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Back Button
        back_btn = ctk.CTkButton(self, text="<--", command=self.go_back)
        back_btn.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="nw")

        label = ctk.CTkLabel(self, text="Score", font=("Arial",35, "bold"))
        label.grid(row=1, column=0, columnspan=5, pady=10)
        
        self.p1_label = ctk.CTkLabel(self, text=" ", font=("Arial",28))
        self.p1_label.grid(row=2, column=1, pady=25, padx=20, sticky="e")
        
        self.p1_score = ctk.CTkLabel(self, text="0", font=("Arial",20))
        self.p1_score.grid(row=3, column=1, padx=20, sticky="n")
        
        self.p2_label = ctk.CTkLabel(self, text=" ", font=("Arial",28))
        self.p2_label.grid(row=2, column=3, pady=25, padx=20, sticky="w")
        
        self.p2_score = ctk.CTkLabel(self, text="0", font=("Arial",20))
        self.p2_score.grid(row=3, column=3, padx=20, sticky="n")

        # Configure columns so things split up beautifully
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Key bindings
        self.controller.bind("<w>", self.update_score_1)
        self.controller.bind("<Up>", self.update_score_2)
        self.controller.bind("<s>", self.lower_score_1)
        self.controller.bind("<Down>", self.lower_score_2)

    def go_back(self):
        # Reset controller scores
        self.controller.p1_score_num = 0
        self.controller.p2_score_num = 0
        
        # Clear entries on ScreenOne by accessing it through the controller map
        self.controller.frames["ScreenOne"].clear_entries()
        
        # Go back home
        self.controller.show_frame("ScreenOne")

    def update_display(self):
        # Dynamically draw names and scores from controller
        self.p1_label.configure(text=self.controller.p1_name)
        self.p2_label.configure(text=self.controller.p2_name)
        self.p1_score.configure(text=str(self.controller.p1_score_num))
        self.p2_score.configure(text=str(self.controller.p2_score_num))

    def check_game_over(self):
        """Helper to determine if someone has officially won (reached 11 and leads by 2)"""
        s1 = self.controller.p1_score_num
        s2 = self.controller.p2_score_num
        
        if s1 >= 11 and (s1 - s2) >= 2:
            return True
        if s2 >= 11 and (s2 - s1) >= 2:
            return True
        return False
        
    def update_score_1(self, event):
        # If someone already won, don't allow more points
        if self.check_game_over(): 
            return
            
        self.controller.p1_score_num += 1
        self.p1_score.configure(text=str(self.controller.p1_score_num))
        
    def update_score_2(self, event):
        if self.check_game_over(): 
            return
            
        self.controller.p2_score_num += 1
        self.p2_score.configure(text=str(self.controller.p2_score_num))
        
    def lower_score_1(self, event):
        # Prevent score from going below 0
        if self.controller.p1_score_num > 0:
            self.controller.p1_score_num -= 1
            self.p1_score.configure(text=str(self.controller.p1_score_num))
        
    def lower_score_2(self, event):
        # Prevent score from going below 0
        if self.controller.p2_score_num > 0:
            self.controller.p2_score_num -= 1
            self.p2_score.configure(text=str(self.controller.p2_score_num))

if __name__ == "__main__":
    app = App()
    app.mainloop()
