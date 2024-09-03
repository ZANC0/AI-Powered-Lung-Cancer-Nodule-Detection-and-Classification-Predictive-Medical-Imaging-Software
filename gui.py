import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ct
from PIL import Image, ImageTk
import pydicom as pyd

WIDTH = 1280
HEIGHT = 720
# Thinking like when an image is uploaded, it creates a new object that has its own methods to select the image to display on the
# main page
class SelectImageButton(ct.CTkButton):
    def __init__(self, master, image_path, get_callback,del_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.image_path = image_path
        self.get_callback = get_callback
        self.del_callback = del_callback
        self.configure(command=self.on_click,corner_radius=0,fg_color="#23335e")

        close_thumbnail = openImage("close-btn.png")
        close_thumbnail = ct.CTkImage(close_thumbnail, close_thumbnail, size=(10,10))

        
        self.close_btn = ct.CTkButton(
                self,
                width=5,
                height=20,
                image=close_thumbnail,
                text="",
                fg_color="red",
                bg_color="transparent",
                corner_radius=0,
                border_spacing=0,
                command=self.remove_image
                
            )
        self.close_btn.place_forget()
        self.bind("<Enter>", self.show_close_btn)
        self.bind("<Leave>",self.hide_close_btn)
        self.close_btn.bind("<Enter>", self.show_close_btn)
        self.close_btn.bind("<Leave>", self.check_leave)
    

    def on_click(self):
        self.get_callback(self.image_path)  # Using image path as a parameter for the callback function setPreviewImage

    def remove_image(self):
        self.destroy()
        self.del_callback(self.image_path)

    def show_close_btn(self, e=None):
        self.close_btn.place(x=0,y=0)

    def hide_close_btn(self, e=None):
        self.close_btn.place_forget()

    def check_leave(self, event=None):
        # Check if the cursor is still within the widget or the close button
        if not (self.winfo_containing(event.x_root, event.y_root) == self or 
                self.winfo_containing(event.x_root, event.y_root) == self.close_btn):
            self.hide_close_btn()
        
    

class ImageSelection(ct.CTkScrollableFrame):
    def __init__(self, master, uploaded_images, select_image_callback, delete_image_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.uploaded_images = uploaded_images
        self.select_image_callback = select_image_callback
        self.delete_image_callback = delete_image_callback
        self.update_image_buttons()

    def update_image_buttons(self):
        # Clear existing buttons
        for widget in self.winfo_children():
            widget.destroy()
        # Create a new button for each image
        for i, img_path in enumerate(self.uploaded_images):
            img = openImage(img_path)
            img_thumbnail = ct.CTkImage(img, img, size=(128,128))
            img_button = SelectImageButton(
                self,
                image_path=img_path,
                get_callback=self.select_image_callback,
                del_callback=self.delete_image_callback,
                image=img_thumbnail,
                text="",
                width=128,
                height=128
            )
            img_button.grid(row=i, column=0, pady=5)

        
class App(ct.CTk):
    def __init__(self):
        super().__init__()
        # window configure
        self.title("PMIS (Predictive Medical Imaging Software) by Zanco Farrell")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.configure(background="red")
                
        self.default_img = "image-icon.png"
        self.selectedImagePath = "File Path"
        self.uploaded_images = []

        self.mainframe = ct.CTkFrame(
            self,
            fg_color="#16213e",
            width=WIDTH,
            height=HEIGHT
        )
        self.file_path_entry = ct.CTkLabel(
            self,
            text=self.selectedImagePath,
            text_color="gray",
            fg_color="#23335e",
            width=200,
            height=50
        )
        self.show_image = ct.CTkButton(
            self,
            fg_color="#16213e",
            border_width=0,
            corner_radius=0,
            hover=False,
            image=ct.CTkImage(Image.open(self.default_img),size=(160,160)),
            width=WIDTH-200,
            height=HEIGHT,
            text="",
            command=self.uploadImage
        )
        
        self.selection = ImageSelection(
            master=self,
            uploaded_images=self.uploaded_images,
            select_image_callback=self.setPreviewImage,
            delete_image_callback=self.remove_uploaded_image,
            width=180,
            height=HEIGHT-100,
            fg_color="transparent",
        )
        
        self.enable_preprocessing = ct.CTkCheckBox(
            self,
            command=self.show_preprocessing
        )

        self.mainframe.grid(row=0, column=0)
        self.file_path_entry.grid(row=0, column=0, padx=0, pady=5, ipady=0, sticky="nw")
        self.show_image.grid(row=0, column=0, padx=0, pady=0, ipady=0,ipadx=0, sticky="e")
        self.selection.place(x=0,y=75)
        self.enable_preprocessing.place(x=500,y=600)

    def remove_uploaded_image(self, path):
        self.uploaded_images.remove(path)
        prev_image = len(self.uploaded_images)-1
        if len(self.uploaded_images) == 0:
            self.returnDefaultImage()
        else:
            self.file_path_entry.configure(text=self.getfilename(self.uploaded_images[prev_image]))
            self.setPreviewImage(self.uploaded_images[prev_image])

    def getfilename(self, path):
        path_split = path.split('/')
        return path_split[len(path_split)-1]
    
    def setPreviewImage(self, path):
        img = openImage(path)
        img = ct.CTkImage(light_image=img, dark_image=img, size=(512,512))
        self.show_image.configure(image=img, bg_color="black")
        path = path.split('/')
        self.file_path_entry.configure(text=path[len(path)-1])

    def returnDefaultImage(self):
        img = openImage(self.default_img)
        img = ct.CTkImage(light_image=img, dark_image=img, size=(160,160))
        self.show_image.configure(image=img, bg_color="transparent")
        self.file_path_entry.configure(text="File Name")

    def uploadImage(self):
        try:
            filename = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Upload Image",
                filetypes=(("png images", "*.png"), ("jpg images", "*.jpg"), ("jpeg images", "*.jpeg"), ("dcm images", "*.dcm"))            
            )
            if filename:
                self.uploaded_images.append(filename)
                self.selection.update_image_buttons()  # Update the image selection list with the new image
                self.setPreviewImage(filename)  # Optionally, you can set the newly uploaded image as the preview
        except:
            pass

    def show_preprocessing(self):
        print(self.enable_preprocessing._check_state)


def openImage(path):
    if ".dcm" in path:
        img = pyd.dcmread(path)
        img = img.pixel_array
        img = Image.fromarray(img)
    else:
        img = Image.open(path)
    return img
        




newapp = App()
newapp.mainloop()

