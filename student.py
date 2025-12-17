from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class studentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # === Title ===
        title = Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # === Variables ===
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_admission = StringVar()
        self.var_course = StringVar()
        self.var_search = StringVar()

        # === Column 1 ===
        lbl_roll = Label(self.root, text="Roll No.", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=60)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=100)
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=140)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=180)
        
        self.txt_roll = Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_roll.place(x=150, y=60, width=200)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=150, y=100, width=200)
        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=150, y=140, width=200)
        
        self.txt_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)

        # === Column 2 ===
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15, 'bold'), bg='white').place(x=360, y=60)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15, 'bold'), bg='white').place(x=360, y=100)
        lbl_admission = Label(self.root, text="Admn. Date", font=("goudy old style", 15, 'bold'), bg='white').place(x=360, y=140)
        lbl_course = Label(self.root, text="Course", font=("goudy old style", 15, 'bold'), bg='white').place(x=360, y=180)

        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=480, y=60, width=200)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=480, y=100, width=200)
        txt_admission = Entry(self.root, textvariable=self.var_admission, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=480, y=140, width=200)
        
        self.course_list = []
        self.fetch_course() # Fetch dynamic list from Database
        self.txt_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, font=("goudy old style", 15, 'bold'), state='readonly', justify=CENTER)
        self.txt_course.place(x=480, y=180, width=200)
        self.txt_course.set("Select")

        # === Address Section ===
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15, 'bold'), bg='white').place(x=10, y=220)
        self.txt_address = Text(self.root, font=("goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_address.place(x=150, y=220, width=530, height=100)

        # === Buttons ===
        self.btn_add = Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=350, width=110, height=40)
        self.btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2").place(x=270, y=350, width=110, height=40)
        self.btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2").place(x=390, y=350, width=110, height=40)
        self.btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2").place(x=510, y=350, width=110, height=40)

        # === Search Panel ===
        lbl_search_roll = Label(self.root, text="Roll No.", font=("goudy old style", 15, 'bold'), bg='white').place(x=720, y=60)
        txt_search_roll = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, 'bold'), bg='lightyellow').place(x=870, y=60, width=180)
        btn_search = Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=1060, y=60, width=120, height=28)

        # === Student Table ===
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=460, height=330)

        self.StudentTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "address"))
        self.StudentTable.heading("roll", text="Roll No.")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable.heading("contact", text="Contact")
        self.StudentTable.heading("admission", text="Admn. Date")
        self.StudentTable.heading("course", text="Course")
        self.StudentTable.heading("address", text="Address")
        
        self.StudentTable["show"] = 'headings'
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ================== Database Logic =================

    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select name from course")
            rows = cur.fetchall()
            self.course_list.append("Select")
            if len(rows) > 0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. should be required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Roll No. already present")
                else:
                    cur.execute("insert into student (roll, name, email, gender, dob, contact, admission, course, address) values(?,?,?,?,?,?,?,?,?)", (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_admission.get(),
                        self.var_course.get(),
                        self.txt_address.get("1.0", END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. should be required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select Student from list")
                else:
                    cur.execute("update student set name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, address=? where roll=?", (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_contact.get(),
                        self.var_admission.get(),
                        self.var_course.get(),
                        self.txt_address.get("1.0", END),
                        self.var_roll.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Updated Successfully")
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll No. should be required")
            else:
                cur.execute("select * from student where roll=?", (self.var_roll.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select Student from list")
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?")
                    if op:
                        cur.execute("delete from student where roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Student deleted Successfully")
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("Select")
        self.var_search.set("")
        self.txt_address.delete('1.0', END)
        self.txt_roll.config(state=NORMAL)
        self.show()

    def get_data(self, ev):
        self.txt_roll.config(state='readonly')
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content['values']
        self.var_roll.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_dob.set(row[4])
        self.var_contact.set(row[5])
        self.var_admission.set(row[6])
        self.var_course.set(row[7])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[8])

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from student")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from student where roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row != None:
                self.StudentTable.delete(*self.StudentTable.get_children())
                self.StudentTable.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

if __name__ == "__main__":
    root = Tk()
    obj = studentClass(root)
    root.mainloop()