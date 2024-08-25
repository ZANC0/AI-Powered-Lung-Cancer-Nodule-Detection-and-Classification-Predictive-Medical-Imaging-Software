import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ct
from PIL import Image, ImageTk

WIDTH = 640
HEIGHT = 360
class interface(ct.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.default_img = "image-icon.png"
        self.selectedImagePath = "File Path"

        # window configure
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self._set_appearance_mode("dark")
        
        def setPreviewImage(path=self.default_img):
            img = Image.open(path)
            img = ct.CTkImage(light_image=img, dark_image=img, size=(320,160))
            self.show_image = ct.CTkLabel(
                self,
                image=img,
                text=""
            )
            self.selectedImagePath = path.split("/")[len(path.split("/"))-1]
            self.file_path_entry.configure(text=self.selectedImagePath)
            self.show_image.grid(row=1, column=0, columnspan=3,padx=5, pady=5, ipady=0, sticky="nswe")
            
        
        def selectImage():
            filename = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title = "Upload Image",
                filetypes=(("png images", "*.png"),("jpg images", "*.jpg"),("jpeg images", "*.jpeg"))            
            )
            
            setPreviewImage(filename)


        # self.upload_btn = ct.CTkButton(self,width=100,height=50, text="Upload")
        self.file_path_entry = ct.CTkLabel(
            self,
            fg_color="navy",
            text=self.selectedImagePath,
            text_color="gray",
            width=200
        )
        self.show_image = ct.CTkButton(
            self,
            fg_color="transparent",
            hover=False,
            image=ct.CTkImage(Image.open(self.default_img),size=(160,160)),
            width=160,
            height=160,
            text="",
            command=selectImage,
        )


        self.file_path_entry.grid(row=0, column=0, padx=1, pady=5, ipady=0, sticky="n")
        self.show_image.grid(row=0, column=1,columnspan=3, padx=5, pady=5, ipady=0, sticky="w")

app = interface()
app.mainloop()

