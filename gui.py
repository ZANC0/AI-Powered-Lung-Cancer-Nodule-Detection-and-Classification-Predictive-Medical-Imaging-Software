import tkinter as tk
import customtkinter as ct

WIDTH = 1600
HEIGHT = 900
class interface(ct.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # window configure
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{WIDTH}x{HEIGHT}")


        # background
        self.displaybg = ct.CTkFrame(self,fg_color="gray",width=WIDTH,height=HEIGHT)
        self.displaybg.grid(row=0,column=0,padx=0,pady=0)
        self.displaybg.rowconfigure(0,weight=1)
        self.displaybg.columnconfigure(0,weight=1)
        
        # components
        self.sidebar = ct.CTkFrame(self,fg_color="white",width=200,height=HEIGHT)
        self.sidebar.grid(row=0,column=0, rowspan=3 ,padx=0,pady=0)
        self.sidebar.rowconfigure(1,weight=1)
        self.sidebar.columnconfigure(1,weight=5)

                
        # for i in range(5):
        #     self.sidebar_block = ct.CTkFrame(self,fg_color='red',width=50,height=50)
        #     self.sidebar_block.grid(row=i,column=1,padx=0,pady=0)

app = interface()
app.mainloop()

