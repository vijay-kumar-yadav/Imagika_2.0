from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import fetch_image
from threading import Thread

size_row = 3
size_column = 6
index = 0
win_counter = 0
DIR = "_browserCache_"

dict = {}
for i in range(size_row):
    for j in range(size_column):
        dict[index] = (i, j)
        index += 1


def image_loader(path, height, width):
    img = Image.open(path).resize((width, height))
    image = ImageTk.PhotoImage(image=img)
    return image


def img_callback(args):
    btn_spreader("%s/" % (DIR) + args[0], args[1])


def btn_spreader(path, count):
    Lb_countImage.configure(
        text="Total images in search %d" % (count),
        font=("Calibri Light BOLD", 15),
        bg="#D7DFF4",
        fg="black",
    )
    tup = dict.get(count - 1)
    # print(tup[0], tup[1])
    img = image_loader(path, 200, 200)
    img.tk = img
    btns[count - 1] = Button(
        contentFrame,
        image=img,
        bd=0,
        command=lambda: image_selected(path),
        cursor="hand2",
    )
    btns[count - 1].grid(row=tup[0], column=tup[1], padx=(10, 10), pady=(5, 5))


onBtnCallback = None


def image_search(query):
    # progress.pack(anchor=W)
    Lb_Loading.place(x=20, y=85)
    Lb_Loading.configure(text="Loading Image .....",
                         font=("Calibri Light", 15),
                         bg="#E4E9F7",
                         fg="black")
    fetch_image.bing_image_search(query, img_callback, size_row * size_column)
    Lb_Loading.place_forget()


def search(query):
    if query == "Search here..." or query.strip() == "":
        Lb_info.configure(text='*Search bar is empty')
        return
    global thread

    thread = Thread(target=image_search, args=(query, ))
    thread.start()
    Lb_info.configure(text="*Click on image to upload in Imagika")
    Lb_info.place(x=1200, y=60)

    


def image_selected(path):
    global win_counter
    res = messagebox.askyesno("Exit", "You want to upload this image?")
    if res:
        try:
            if thread.is_alive():
                messagebox.showinfo("Thread",
                                    "Please wait image is still loading")
            else:
                root.destroy()
                win_counter = 0
                onBtnCallback(path)
        except Exception as e:
            root.destroy()
            win_counter = 0
    else:
        root.focus()


def on_closing():
    global win_counter
    res = messagebox.askquestion("Exit", "Are you sure you want to exit")
    if res == "yes":
        try:
            if thread.is_alive():
                messagebox.showinfo("Thread",
                                    "Please wait image is still loading")
            else:
                root.destroy()
                win_counter = 0

        except Exception as e:
            root.destroy()
            win_counter = 0

def onEnter(e):
    # print(e)
    search(searchBox.get())


def focusIn(e):
    if searchBox.get() == "Search here...":
        searchBox.delete(0, "end")  # delete all the text in the searchBox
        searchBox.insert(0, "")  # Insert blank for user input
        searchBox.config(fg="black")


def focusOut(e):
    if searchBox.get() == "":
        searchBox.insert(0, "Search here...")
        searchBox.config(fg="grey")


def main(onBtnCallbackArg):
    global win_counter, searchBox
    if win_counter < 1:
        global root, Lb_Loading, Lb_countImage, contentFrame, btns, onBtnCallback,Lb_info
        onBtnCallback = onBtnCallbackArg

        root = Toplevel()
        root.title(" 𝕴𝖒𝖆𝖌𝖎𝖐𝖆 𝕾𝖊𝖆𝖗𝖈𝖍")
        root.state("zoomed")
        root.minsize(1500, 700)
        root.config(bg="#E4E9F7")

        # window count
        win_counter += 1

        logo = image_loader("image/parrot_sketch.png", 45, 40)
        logo.imgtk = logo
        Label(root, image=logo, bg="#E4E9F7").place(x=10, y=20)

        Lb_title = Label(
            root,
            text="Imagika",
            font=("Times New Roman BOLD", 25),
            bg="#E4E9F7",
            fg="#638BD1",
            bd=0,
        )
        Lb_title.place(x=60, y=30)

        searchBox = Entry(root, relief=FLAT, font=("Arial", 15),fg="grey")
        searchBox.insert(0, "Search here...")
        searchBox.place(x=182, y=30, height=40)

        searchBox.bind("<FocusIn>", focusIn)
        searchBox.bind("<FocusOut>", focusOut)

        search_btn = image_loader("image/search.png", 30, 30)
        search_btn.cfg = search_btn
        searchBtn = Button(
            root,
            # text="Search Image",
            image=search_btn,
            command=lambda: search(searchBox.get()),
            relief=FLAT,
            bg="white",
            # fg="white",
            activebackground="#D7DFF4",
        )
        searchBtn.place(x=400, y=30, height=40)
        searchBox.bind('<Return>',onEnter)

        Lb_info = Label(
            root,
            font=("Calibri Light BOLD", 15),
            bg="#E4E9F7",
            fg="#197592",
            bd=0,
        )
        Lb_info.place(x=1200, y=60)


        Lb_countImage = Label(root, bd=0)
        Lb_countImage.pack(anchor=SE)

        Lb_Loading = Label(root, bd=0)

        # content
        contentFrame = Frame(root, bg="#217AC0")
        contentFrame.pack(side=TOP, pady=(100, 0))

        # labelBtns = [Label()]*(size_row*size_column)
        btns = [Button()] * (size_row * size_column)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    else:
        messagebox.showinfo("Info", "Window already opened in background")

    # progress.pack_forget()


# from tkinter.ttk import Progressbar
# import numpy
# progress['value'] = args[1]*(100/(size_row*size_column))
# print(dict)
# dict = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3), 9: (
#     2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3), 13: (3, 0), 14: (3, 1), 15: (3, 2), 16: (3, 3),}

# labelBtns[count-1] = Label(contentFrame, image=img, bd=0)
# labelBtns[count-1].grid(row=tup[0], column=tup[1],
#                         padx=(5, 5), pady=(5, 5))

# def btns():

#   for i in range(size):
#       for j in range(size):
#           index=size*i+j
#          loader(index)
#           img.tk=img
#           buttons[i][j] = Button(canvasFrame,image=img ,
#                   command=lambda i=i, j=j: image_selected(i,j))
#           buttons[i][j].grid(row=i, column=j)

# main(None)

# header
# headerFrame = Frame(root, bg="#D7DFF4", height=500)
# headerFrame.pack(fill=X, pady=(0, 100))
# taskbar label
# threads = []

# canvas = Canvas(contentFrame, bg='green')
# canvas.pack(side=LEFT, fill=BOTH, expand=1)

# scroll_bar = Scrollbar(contentFrame, orient=VERTICAL, command=canvas.yview)
# scroll_bar.pack(side=RIGHT, fill=Y)

# canvas.configure(yscrollcommand=scroll_bar.set)
# canvas.bind('<Configure>', lambda e: canvas.configure(
#     scrollregion=canvas.bbox('all')))

# canvasFrame = Frame(canvas, bg='orange')
# canvas.create_window(0, 0, window=canvasFrame, anchor=NW)
# progress bar
# progress = Progressbar(headerFrame)

# main(None)