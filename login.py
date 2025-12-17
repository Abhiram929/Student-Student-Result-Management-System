from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os
import time
import math

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Base Path for Images ===
        self.base_path = os.path.dirname(__file__)
        img_dir = os.path.join(self.base_path, "images")

        # === 1. Top Bar (Text Only) ===
        # Removed the date and time strings from this label
        self.lbl_clock = Label(self.root, text="Welcome to Student Result Management System", 
                                font=("times new roman", 15), bg="#0676ad", fg="white")
        self.lbl_clock.place(x=0, y=0, relwidth=1, height=35)

        # === 2. Left Side: Analogue Clock ===
        self.lbl_analog = Label(self.root, bg="#081923", bd=3, relief=RIDGE)
        self.lbl_analog.place(x=150, y=100, width=350, height=500)
        
        lbl_clock_title = Label(self.lbl_analog, text="Analogue Clock", font=("Book Antiqua", 25, "bold"), fg="white", bg="#081923").place(x=0, y=10, relwidth=1)

        # Loading the Dial (clock_new.png)
        self.clock_dial = Image.open(os.path.join(img_dir, "clock_new.png"))
        self.clock_dial = self.clock_dial.resize((280, 280), Image.LANCZOS)
        self.prepare_dial = ImageTk.PhotoImage(self.clock_dial)

        self.canvas = Canvas(self.lbl_analog, bg="#081923", bd=0, highlightthickness=0)
        self.canvas.place(x=35, y=100, width=280, height=280)
        
        # Background dial stays static
        self.canvas.create_image(140, 140, image=self.prepare_dial)

        # === 3. Right Side: Login Frame ===
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=100, width=400, height=500)

        title = Label(login_frame, text="LOGIN", font=("Elephant", 30, "bold"), bg="white", fg="#033054").place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Username", font=("Andalus", 15), bg="white", fg="gray").place(x=50, y=140)
        self.var_user = StringVar()
        txt_user = Entry(login_frame, textvariable=self.var_user, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=170, width=300, height=35)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="gray").place(x=50, y=240)
        self.var_pass = StringVar()
        txt_pass = Entry(login_frame, textvariable=self.var_pass, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=270, width=300, height=35)

        btn_login = Button(login_frame, text="Log In", command=self.login, font=("Arial Black", 15), bg="#007bff", fg="white", cursor="hand2", activebackground="#007bff", activeforeground="white").place(x=50, y=350, width=300, height=45)
        
        btn_reg = Button(login_frame, text="Register New Account?", command=self.register_window, font=("times new roman", 13), bg="white", bd=0, fg="#00759E", cursor="hand2", activebackground="white").place(x=50, y=420)

        # Start the clock updates (for hands only)
        self.update_clocks()

    # ================== CLOCK LOGIC =================

    def draw_hands(self, hr, min_, sec_):
        h_angle = (hr + min_ / 60) * (360 / 12)
        m_angle = (min_ + sec_ / 60) * (360 / 60)
        s_angle = sec_ * (360 / 60)

        # Only delete elements with the "hands" tag
        self.canvas.delete("hands")
        origin_x, origin_y = 140, 140

        # Hour Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 50 * math.sin(math.radians(h_angle)), origin_y - 50 * math.cos(math.radians(h_angle)), fill="white", width=4, tags="hands")
        # Minute Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 75 * math.sin(math.radians(m_angle)), origin_y - 75 * math.cos(math.radians(m_angle)), fill="white", width=3, tags="hands")
        # Second Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 90 * math.sin(math.radians(s_angle)), origin_y - 90 * math.cos(math.radians(s_angle)), fill="red", width=2, tags="hands")
        # Center circle
        self.canvas.create_oval(135, 135, 145, 145, fill="white", tags="hands")

    def update_clocks(self):
        # Update Analogue Hands only
        h = int(time.strftime("%H"))
        m = int(time.strftime("%M"))
        s = int(time.strftime("%S"))
        if h > 12: h = h - 12
        self.draw_hands(h, m, s)
        self.root.after(200, self.update_clocks)

    # ================== SYSTEM LOGIC =================

    def login(self):
        if self.var_user.get() == "" or self.var_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("select * from user where id_no=? and pass=?", (self.var_user.get(), self.var_pass.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Credentials", parent=self.root)
                else:
                    self.root.destroy()
                    os.system("python dashboard.py")
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def register_window(self):
        self.root.destroy()
        os.system("python register.py")

if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()