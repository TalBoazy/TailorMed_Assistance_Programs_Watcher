import tkinter as tk
from tkinter import ttk
from UI_manager import UiManager

"""
Simple UI Class for the DB table
"""
class UI:

    def __init__(self):
        self.manager = UiManager()

    def present_table(self):
        """
        The GUI interface of the table
        :return: None
        """
        window = tk.Tk()
        window.geometry("500x500")
        window.pack_propagate(False)
        window.resizable(0,0)

        # frame for Treeview
        frame1 = tk.LabelFrame(window, text="Assistance Programs")
        frame1.place(height=250, width=500)

        # frame for buttons
        frame2 = tk.LabelFrame(window, text="Menu")
        frame2.place(height=100, width=400, rely=0.65,relx=0)
        # buttons
        button1 = tk.Button(frame2, text="update", command=lambda: load_df())
        button1.place(rely=0.65,relx=0.5)

        label_file=ttk.Label(frame2)
        label_file.place(rely=0, relx=0)

        # Treeview widget
        tv1=ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)

        treescrolly=tk.Scrollbar(frame1,orient="vertical", command=tv1.yview)
        treescrollx=tk.Scrollbar(frame1,orient="horizontal", command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        def load_df():
            new_table = self.manager.show()
            clear_data()
            tv1["column"]=list(new_table.columns)
            tv1["show"]="headings"
            for col in tv1["column"]:
                tv1.heading(col, text=col)
            table_rows = new_table.to_numpy().tolist()
            for row in table_rows:
                tv1.insert("", "end", values=row)

        def clear_data():
            children = tv1.get_children()
            if children:
                for child in children:
                    tv1.delete(child)

        window.mainloop()

