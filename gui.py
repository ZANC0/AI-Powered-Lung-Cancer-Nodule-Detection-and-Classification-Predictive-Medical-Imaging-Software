import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ct
from PIL import Image, ImageTk
import pydicom as pyd

WIDTH = 1280
HEIGHT = 720
class App(ct.CTk):
    def __init__(self):
        super().__init__()
        # window configure
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.configure(background="red")
                
        self.default_img = "image-icon.png"
        self.selectedImagePath = "File Path"
        
        
        def setPreviewImage(path=self.default_img):
            if ".dcm" in path:
                img = pyd.dcmread(path)
                img = img.pixel_array
                img = Image.fromarray(img)
            else:
                img = Image.open(path)
            
            img = ct.CTkImage(light_image=img, dark_image=img, size=(512,512))
            self.show_image.configure(image=img, bg_color="black")
            self.selectedImagePath = path.split("/")[len(path.split("/"))-1]
            self.file_path_entry.configure(text=self.selectedImagePath)

        def selectImage():
            try:
                filename = filedialog.askopenfilename(
                    initialdir=os.getcwd(),
                    title = "Upload Image",
                    filetypes=(("png images", "*.png"),("jpg images", "*.jpg"),("jpeg images", "*.jpeg"),("dcm images","*.dcm"))            
                )
                setPreviewImage(filename)
            except:
                pass

        def loadIcons():
            for i in range(3):
                self.icon = ct.CTkFrame(
                    self,
                    width=64,
                    height=64,
                    fg_color="white",
                    border_color="black"

                    
                )
                self.icon.grid(row=0,column=0,pady=i*10, padx=0,ipady=0)

        self.mainframe = ct.CTkFrame(
            self,
            fg_color="#23335e",
            width=WIDTH,
            height=HEIGHT
        )
        self.mainframe.grid(row=0, column=0)

        # self.upload_btn = ct.CTkButton(self,width=100,height=50, text="Upload")
        self.file_path_entry = ct.CTkLabel(
            self,
            text=self.selectedImagePath,
            text_color="gray",
            fg_color="transparent",
            bg_color="transparent",
            width=200,
            height=50
        )
        self.show_image = ct.CTkButton(
            self,
            fg_color="#16213e",
            border_width=1,
            hover=False,
            image=ct.CTkImage(Image.open(self.default_img),size=(160,160)),
            width=512,
            height=512,
            text="",
            command=selectImage,
        )
        loadIcons()


        self.file_path_entry.grid(row=0, column=0, padx=0, pady=5, ipady=0, sticky="nw")
        self.show_image.grid(row=0, column=0, padx=0, pady=0, ipady=0,ipadx=0, sticky="e")




newapp = App()
newapp.mainloop()

