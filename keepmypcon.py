import tkinter as tk
from pynput.mouse import Controller, Button
from tkinter import messagebox

# Program to autoclick every 30 seconds. Before each click,
# cursor moves to tkinter widget to avoid clicking on something bad

class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # Click loop settings
        self.click_delay = 10_000 # ms
        self.click_times = 0

        self.mouse = Controller()

        self.instructions = f"This is a program to keep your PC awake during a download. It autoclicks every {self.click_delay//1000} seconds to make your PC think you are still using it. Before each click, the cursor moves to the blue square to avoid clicking on something bad."

        self.main_frm = tk.Frame(self.root, background="#FFFFFF")

        self.info_btn = tk.Button(self.main_frm, text="?", width=3, command=self.open_info)

        self.options_frm = tk.Frame(self.main_frm)
        self.time_frm = tk.Frame(self.options_frm)
        self.time_lbl = tk.Label(self.time_frm, text="Time (minutes)")
        self.time_ent = tk.Entry(self.time_frm)

        self.click_cvs = tk.Canvas(self.main_frm, background="#0091FF", width=300, height=300)
    
        self.packall()
        self.bindall()
    
    def packall(self):
        self.pack_full(self.main_frm)
        self.info_btn.pack()
        self.pack_full(self.options_frm)
        self.time_frm.pack()
        self.time_lbl.pack(side=tk.LEFT)
        self.time_ent.pack(side=tk.RIGHT)
        self.click_cvs.pack(side=tk.BOTTOM)

    @staticmethod
    def pack_full(widget: tk.Widget):
        widget.pack(fill=tk.BOTH, expand=True)
    
    def bindall(self):
        self.time_ent.bind("<Return>", self.submit_time)
    
    def submit_time(self, event):
        times = (int(self.time_ent.get()) / (self.click_delay // 1000)) * 60
        self.click_times = times
        self.start_loop()

    def start_loop(self):
        self.time_ent.config(state="disabled")
        self.root.attributes("-topmost", True)
        self.move_cursor_loop()
    
    def open_info(self):
        messagebox.showinfo("KMPCO info", self.instructions)

    def move_cursor(self):
        # Update geometry info
        self.click_cvs.update_idletasks()

        # Get widget's position relative to the screen
        x = self.click_cvs.winfo_rootx()
        y = self.click_cvs.winfo_rooty()
        w = self.click_cvs.winfo_width()
        h = self.click_cvs.winfo_height()

        # Move cursor to center
        self.mouse.position = (x + w // 2, y + h // 2)
    
    def click_mouse(self):
        self.mouse.click(Button.left)
    
    def move_cursor_loop(self):
        self.move_cursor()
        self.click_mouse()
        if self.click_times > 0:
            self.root.after(self.click_delay, self.move_cursor_loop)  # schedule itself again after 30 seconds
        else:
            messagebox.showinfo("KMPCO time out", "KMPCO is done clicking")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()