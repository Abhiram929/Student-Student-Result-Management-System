from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Background Image ===
        self.base_path = os.path.dirname(__file__)
        self.side_img = Image.open(os.path.join(self.base_path, "images/side.png"))
        self.side_img = self.side_img.resize((400, 500), Image.LANCZOS)
        self.prepare_side = ImageTk.PhotoImage(self.side_img)
        Label(self.root, image=self.prepare_side).place(x=150, y=100)

        # === Register Frame ===
        reg_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        reg_frame.place(x=550, y=100, width=500, height=500)

        title = Label(reg_frame, text="REGISTER HERE", font=("times new roman", 25, "bold"), bg="white", fg="#033054").place(x=0, y=30, relwidth=1)

        # === Fields ===
        lbl_user = Label(reg_frame, text="Username", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=100)
        self.var_uname = StringVar()
        txt_user = Entry(reg_frame, textvariable=self.var_uname, font=("times new roman", 15), bg="lightgray").place(x=50, y=130, width=400)

        lbl_pass = Label(reg_frame, text="Password", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=200)
        self.var_pass = StringVar()
        txt_pass = Entry(reg_frame, textvariable=self.var_pass, show="*", font=("times new roman", 15), bg="lightgray").place(x=50, y=230, width=400)

        lbl_sec = Label(reg_frame, text="Security Question", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=300)
        self.var_quest = StringVar()
        txt_quest = Entry(reg_frame, textvariable=self.var_quest, font=("times new roman", 15), bg="lightgray").place(x=50, y=330, width=400)

        # === Button ===
        btn_reg = Button(reg_frame, text="REGISTER NOW", command=self.register_data, font=("times new roman", 15, "bold"), bg="#033054", fg="white", cursor="hand2").place(x=50, y=420, width=400, height=40)

    def register_data(self):
        if self.var_uname.get()=="" or self.var_pass.get()=="":
            messagebox.showerror("Error", "All fields are required")
        else:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("insert into user (id_no, pass, question) values(?,?,?)", (self.var_uname.get(), self.var_pass.get(), self.var_quest.get()))
                con.commit()
                messagebox.showinfo("Success", "Registration Successful")
                self.root.destroy()
                os.system("python SRMS/login.py")
            except Exception as ex:
                messagebox.showerror("Error", f"Error: {str(ex)}")

if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()