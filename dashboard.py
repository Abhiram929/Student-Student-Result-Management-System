from tkinter import *
from PIL import Image, ImageTk 
from tkinter import messagebox
import sqlite3
import os
import time
import math

# Importing the other files/classes
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # === Icons ===
        # Using the direct path shown in your terminal errors
        self.logo_dash = ImageTk.PhotoImage(file="SRMS/images/logo_p.png")

        # === Title ===
        title = Label(self.root, text="Student Result Management System", 
                      image=self.logo_dash, compound=LEFT, padx=10,
                      font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=0, y=0, relwidth=1, height=50)

        # === Menu Frame ===
        M_Frame = LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1330, height=80)

        # === Buttons ===
        btn_course = Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_course).place(x=20, y=5, width=200, height=40)
        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_student).place(x=240, y=5, width=200, height=40)
        btn_result = Button(M_Frame, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_result).place(x=460, y=5, width=200, height=40)
        btn_view = Button(M_Frame, text="View Student Results", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_report).place(x=680, y=5, width=200, height=40)
        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.logout).place(x=900, y=5, width=200, height=40)
        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.exit_).place(x=1120, y=5, width=200, height=40)

        # === Content Image ===
        self.bg_img = Image.open("SRMS/images/bg.png")
        self.bg_img = self.bg_img.resize((920, 350), Image.LANCZOS)
        self.prepare_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(self.root, image=self.prepare_img).place(x=400, y=180, width=920, height=350)

        # === Analog Clock ===
        self.lbl_analog = Label(self.root, bg="#081923", bd=5, relief=RIDGE)
        self.lbl_analog.place(x=10, y=180, width=350, height=450)

        lbl_clock_title = Label(self.lbl_analog, text="Analog Clock", font=("Book Antiqua", 25, "bold"), fg="white", bg="#081923").place(x=0, y=10, relwidth=1)

        # Clock Dial Image
        self.clock_dial_img = Image.open("SRMS/images/c.png")
        self.clock_dial_img = self.clock_dial_img.resize((300, 300), Image.LANCZOS)
        self.prepare_clock_dial = ImageTk.PhotoImage(self.clock_dial_img)

        self.canvas = Canvas(self.lbl_analog, bg="#081923", bd=0, highlightthickness=0)
        self.canvas.place(x=25, y=70, width=300, height=300)
        self.canvas.create_image(150, 150, image=self.prepare_clock_dial)

        # === Update Details (Labels) ===
        self.lbl_course = Label(self.root, text="Total Courses\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e43b06", fg="white")
        self.lbl_course.place(x=400, y=530, width=300, height=100)

        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#0676ad", fg="white")
        self.lbl_student.place(x=710, y=530, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#038074", fg="white")
        self.lbl_result.place(x=1020, y=530, width=300, height=100)

        # === Footer ===
        footer = Label(self.root, text="SRMS - Student Result Management System\nContact us for any Technical Issue: 987xxxxxxx", 
                       font=("goudy old style", 12), bg="#262626", fg="white").pack(side=BOTTOM, fill=X)

        self.update_content()
        self.working() # Call clock update

    # ================== Analog Clock Logic =================

    def clock_hands(self, hr, min_, sec_):
        h_angle = (hr + min_ / 60) * (360 / 12)
        m_angle = (min_ + sec_ / 60) * (360 / 60)
        s_angle = sec_ * (360 / 60)

        self.canvas.delete("hands")
        origin_x, origin_y = 150, 150

        # Hour Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 50 * math.sin(math.radians(h_angle)), origin_y - 50 * math.cos(math.radians(h_angle)), fill="white", width=4, tags="hands")
        # Minute Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 80 * math.sin(math.radians(m_angle)), origin_y - 80 * math.cos(math.radians(m_angle)), fill="white", width=3, tags="hands")
        # Second Hand
        self.canvas.create_line(origin_x, origin_y, origin_x + 90 * math.sin(math.radians(s_angle)), origin_y - 90 * math.cos(math.radians(s_angle)), fill="red", width=2, tags="hands")
        # Center Point
        self.canvas.create_oval(145, 145, 155, 155, fill="white", tags="hands")

    def working(self):
        h = int(time.strftime("%H"))
        m = int(time.strftime("%M"))
        s = int(time.strftime("%S"))
        if h > 12: h = h - 12
        self.clock_hands(h, m, s)
        self.canvas.after(1000, self.working)

    # ================== Database Functions =================

    def update_content(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            rows = cur.fetchall()
            self.lbl_course.config(text=f"Total Courses\n[ {str(len(rows))} ]")

            cur.execute("select * from student")
            rows = cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[ {str(len(rows))} ]")

            cur.execute("select * from result")
            rows = cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[ {str(len(rows))} ]")

            self.lbl_course.after(2000, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)

    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op == True:
            self.root.destroy()
            # This ensures that when you log out, the login page opens again
            os.system("python login.py")

    def exit_(self):
        op = messagebox.askyesno("Confirm", "Do you really want to Exit?", parent=self.root)
        if op == True: self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()