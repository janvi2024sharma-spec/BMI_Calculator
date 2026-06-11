
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, os
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except:
    pd = None

FILE_NAME = "bmi_data.csv"

class AdvancedBMI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e1e")

        title = tk.Label(root,text="ADVANCED BMI CALCULATOR",
                         bg="#1e1e1e",fg="cyan",
                         font=("Arial",20,"bold"))
        title.pack(pady=10)

        frame = tk.Frame(root,bg="#1e1e1e")
        frame.pack()

        self.name=tk.Entry(frame,width=25)
        self.weight=tk.Entry(frame,width=25)
        self.height=tk.Entry(frame,width=25)

        tk.Label(frame,text="Name",bg="#1e1e1e",fg="white").grid(row=0,column=0,padx=5,pady=5)
        tk.Label(frame,text="Weight (kg)",bg="#1e1e1e",fg="white").grid(row=1,column=0,padx=5,pady=5)
        tk.Label(frame,text="Height (m)",bg="#1e1e1e",fg="white").grid(row=2,column=0,padx=5,pady=5)

        self.name.grid(row=0,column=1)
        self.weight.grid(row=1,column=1)
        self.height.grid(row=2,column=1)

        tk.Button(frame,text="Calculate BMI",command=self.calculate).grid(row=3,column=0,pady=10)
        tk.Button(frame,text="Delete Selected",command=self.delete_record).grid(row=3,column=1,pady=10)
        tk.Button(frame,text="Show Graph",command=self.show_graph).grid(row=3,column=2,pady=10)
        tk.Button(frame,text="Export CSV",command=self.export_csv).grid(row=3,column=3,pady=10)

        self.result=tk.Label(root,text="",bg="#1e1e1e",fg="yellow",
                             font=("Arial",12,"bold"))
        self.result.pack()

        cols=("Date","Name","Weight","Height","BMI","Category")
        self.tree=ttk.Treeview(root,columns=cols,show="headings",height=18)

        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=130)

        self.tree.pack(fill="both",expand=True,padx=10,pady=10)

        self.create_file()
        self.load_data()

    def create_file(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME,"w",newline="") as f:
                csv.writer(f).writerow(
                    ["Date","Name","Weight","Height","BMI","Category"]
                )

    def category(self,bmi):
        if bmi < 18.5: return "Underweight"
        if bmi < 25: return "Normal"
        if bmi < 30: return "Overweight"
        return "Obese"

    def calculate(self):
        try:
            name=self.name.get().strip()
            weight=float(self.weight.get())
            height=float(self.height.get())

            bmi=round(weight/(height**2),2)
            cat=self.category(bmi)

            self.result.config(
                text=f"BMI: {bmi} | Category: {cat}"
            )

            row=[
                datetime.now().strftime("%Y-%m-%d"),
                name,weight,height,bmi,cat
            ]

            with open(FILE_NAME,"a",newline="") as f:
                csv.writer(f).writerow(row)

            self.load_data()

        except:
            messagebox.showerror(
                "Error",
                "Enter valid values."
            )

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        with open(FILE_NAME,"r") as f:
            reader=csv.reader(f)
            next(reader,None)
            for row in reader:
                self.tree.insert("",tk.END,values=row)

    def delete_record(self):
        selected=self.tree.selection()
        if not selected:
            return

        values=self.tree.item(selected[0])["values"]

        rows=[]
        with open(FILE_NAME,"r") as f:
            rows=list(csv.reader(f))

        rows=[r for r in rows if r != [str(v) for v in values]]

        with open(FILE_NAME,"w",newline="") as f:
            csv.writer(f).writerows(rows)

        self.load_data()

    def show_graph(self):
        if pd is None:
            messagebox.showinfo(
                "Install",
                "pip install pandas matplotlib"
            )
            return

        df=pd.read_csv(FILE_NAME)

        if len(df)==0:
            return

        plt.figure(figsize=(6,4))
        plt.plot(df.index,df["BMI"],marker="o")
        plt.title("BMI History")
        plt.xlabel("Record")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.show()

    def export_csv(self):
        path=filedialog.asksaveasfilename(
            defaultextension=".csv"
        )

        if path:
            import shutil
            shutil.copy(FILE_NAME,path)
            messagebox.showinfo(
                "Success",
                "CSV Exported Successfully"
            )

root=tk.Tk()
app=AdvancedBMI(root)
root.mainloop()
