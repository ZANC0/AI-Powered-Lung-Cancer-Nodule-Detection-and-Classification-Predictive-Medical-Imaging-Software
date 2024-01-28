import tkinter as tk
import customtkinter as ct

w = 1600
h = 900
class interface(ct.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{w}x{h}")
        self.sidebar = ct.CTkFrame(self,fg_color="white",width=200,height=h)
        self.sidebar.grid(row=1,column=0)
        self.sidebar_block = ct.CTkFrame(self,fg_color='red')
        self.sidebar_block.grid(row=0,column=0,padx=0,pady=0)

        self.displaybg = ct.CTkFrame(self,fg_color="gray")
        self.displaybg.grid(row=1,column=0,padx=220,pady=20)
        
app = interface()
app.mainloop()

