import tkinter as tk
import customtkinter as ct

w = 1600
h = 900
class interface(ct.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{w}x{h}")
        self.
        self.displaybg = ct.CTkFrame(self,fg_color="gray",width=1400,height=h)
        self.displaybg.grid(row=0,column=0,padx=500,pady=0)
        
        self.sidebar = ct.CTkFrame(self,fg_color="white",width=200,height=h)
        self.sidebar.grid(row=1,column=0)
        

        
    def define_previews(self):
        for i in range(5):
            self.sidebar_block = ct.CTkFrame(self,fg_color='red',width=50,height=50)
            self.sidebar_block.grid(row=i,column=0,padx=0,pady=0,sticky='ew')
    def load(self):
        self.define_previews()
app = interface()
app.load()
app.mainloop()

