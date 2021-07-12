#!/usr/bin/python3

#//* Bartha Aron *//#

from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from tkinter import *
from io import BytesIO
from PIL import Image, ImageDraw
from sys import argv
from os import mkdir
from os.path import isdir, basename
from shutil import move
from time import gmtime, strftime, time, sleep
from glob import glob

pdfs = "PDFs"
backup = "Backup"
title1 = "Ez PDF Editor"
title2 = "PDF to Export"
title3 = "Preview"

def mv(List, Index1, Index2):
    List_Index1_ = List[Index1]
    List[Index1] = List[Index2]
    List[Index2] = List_Index1_

class ablak:
    w = 1000
    h =  250

    #def click(this, data):
        #print(data)
    
    def __init__(this, click):
        this.hidden = 0
        this.i =      0
        this.btn = list()
        this.photos = list()
        this.nums = list()
        this.selected = False
        this.ok = True
        this.click = click
        this.root = Tk()
        #this.root.title("Super PDF")
        this.root.geometry(f"{this.w}x{this.h}")
        this.root.resizable(1,0)

        this.scrollbar = Scrollbar(this.root, orient='horizontal')
        this.scrollbar.pack(side = BOTTOM, fill = BOTH)

        this.canvas = Canvas(this.root, xscrollcommand=this.scrollbar.set)
        this.canvas.pack(expand=True, fill=BOTH, side=LEFT)
        this.frame = Frame(this.canvas, height=this.h, relief=GROOVE, bd=1)
        #frame.pack(expand=True, fill=BOTH)
        this.window = this.canvas.create_window(0, 0, window=this.frame, anchor=NW, width=1)  #ln*150 + ln*2*2
        this.canvas.bind("<Configure>", lambda e: this.canvas.configure(scrollregion=this.canvas.bbox("all")))#2
        #this.canvas.bind("<Configure>", lambda e: print(e))   !!!csak 1X fut le!
        this.scrollbar.config(command = this.canvas.xview)

    def Pil2Photo(this, img):
        buffer = BytesIO()
        img.resize((150, 250)).save(buffer, format="png")
        buffer.seek(0)
        photo = PhotoImage(master=this.root, data=buffer.read())
        buffer.close()
        return photo
    def scrollUpdate(this):
        i = this.i - this.hidden
        sz = ( (i)*150 + (i)*2*2 ) if i != 0 else 1
        this.canvas.itemconfig(this.window, width=sz)
        this.canvas.configure(scrollregion=this.canvas.bbox("all"))

    def append(this, img, index):
        this.nums.append(index)
        this.photos.insert(this.i, this.Pil2Photo(img))
        this.btn.insert(this.i, Button(this.frame, borderwidth=0, image=this.photos[this.i], command=lambda arg=this.i: this.click(arg)))
        this.btn[this.i].pack(side=LEFT)
        this.i += 1
        this.scrollUpdate()
        #this.canvas.scale("all",0,0,sz,this.h)
        
    def update(this, img, index):
        this.photos[index] = this.Pil2Photo(img)
        this.btn[index].config(image=this.photos[index])
        #this.selected = index
    def delete(this, index):
        if index is False:
            return
        if index == this.selected:
            this.selected = False
        this.btn[index].destroy()
        del this.btn[index]
        del this.photos[index]
        del this.nums[index]
        this.i -= 1
        for i in range(index, this.i):
            this.btn[i].config(command=lambda arg=i: this.click(arg))
        this.scrollUpdate()
    def chPos(this, up):
        if this.selected is False:
            return False
        dst = (this.selected + 1) if up else (this.selected -1)
        if dst < 0 or dst >= this.i:
            return False
        #mv(this.btn, this.selected, dst)
        #mv(this.photos, this.selected, dst)
        mv(this.nums, this.selected, dst)
        #print(this.nums)
        this.btn[this.selected].config(command=lambda arg=this.selected: this.click(arg))
        this.btn[dst].config(command=lambda arg=dst: this.click(arg))
        this.click(dst)
        
##    def mvFocus(this, up):
##        if this.selected is False:
##            if up:
##                dst = this.i - 1
##            else:
##                dst = 0
##        else:
##            print("else")
##            dst = (this.selected + 1) if up else (this.selected -1)
##        print(dst)
##        if dst < 0 or dst >= this.i:
##            return False
##        print("click")
##        this.click(dst)

    def deleteAll(this, e=None):
        this.selected = False
        for i in range(this.i-1,0-1,-1):
            this.btn[i].destroy()
            del this.btn[i]
            del this.photos[i]
            del this.nums[i]
        this.i = 0
        this.scrollUpdate()
        
    def autoclick(this, e=None):
        if this.selected is False:
            return False
        this.click(this.selected)
        

class preview:
    photo = None
    wh = 750
    def __init__(this):
        #im = images[0]
        
        #x, y = im.size

        this.root = Tk()
        #this.root.title("Preview")
        this.root.geometry(f"{this.wh}x{this.wh}")
        this.root.resizable(0,0)
        this.label = Label(this.root, width=this.wh, height=this.wh)
        this.label.pack(side=LEFT)

        #sz = (int(this.wh*x/y), this.wh) if x < y else (this.wh, int(this.wh*y/x))
        #buffer = BytesIO()
        #im.resize(sz).save(buffer, format="png")
        #buffer.seek(0)
        #this.photo = PhotoImage(master=this.root,file="a.png")
        #buffer.close()
        #this.label.config(image=this.photo)
    def update(this, im):
        x, y = im.size
        sz = (int(this.wh*x/y), this.wh) if x < y else (this.wh, int(this.wh*y/x))
        buffer = BytesIO()
        im.resize(sz).save(buffer, format="png")
        buffer.seek(0)
        this.photo = PhotoImage(master=this.root, data=buffer.read())
        buffer.close()

        this.label.config(image=this.photo)

class save:
    w=500
    h=50
    def __init__(this):
        this.response = ""
        this.root = Tk()
        this.root.title("Save")
        this.root.geometry(f"{this.w}x{this.h}+250+100")
        this.root.resizable(0,0)

        Label(this.root, text="FileName:   ").pack(side=LEFT)
        this.box = Entry(this.root, width=40)
        this.box.pack(side=LEFT, fill=X)
        Button(this.root, text="Save!", command=this.click).pack(side=RIGHT)

        this.box.focus()
        this.root.bind("<Return>", this.click)
        this.root.bind("<Escape>", lambda e:this.root.destroy() )
        this.root.bind("<Control-Key-q>", lambda e:this.root.destroy() )
        
        while True:
            try:
                this.root.update()
            except:
                break
            
    def click(this, e=None):
        this.response = this.box.get()
        this.root.destroy()

def ab1Click(e, start=False):
    #print(ab1.nums, ab2.nums)
    dbl = e is ab1.selected
    if not ab1.selected is False:
        ab1.update(images[ab1.selected], ab1.selected)
    
    im = images[e].resize((150, 250))
    x, y = im.size
    dr = ImageDraw.Draw(im)
    
    dr.line((1, 1, x-1, 1), width=5, fill="red")
    dr.line((1, 1, 1, y-1), width=5, fill="red")
    dr.line((x-1, 1, x-1, y-1), width=5, fill="red")
    dr.line((1, y-17, x-1, y-17), width=5, fill="red")

    ab1.update(im, e)
    ab1.selected = e
    ab3.update(images[e])

    if dbl and not start:
        if ab1.ok:
            #print(e)
            ab2.append(images[e].copy(), e)
            ab2.root.title(f"{title2} - {ab2.i} page(s)")
            ab1.ok = False
    else:
        ab3.root.title(f"{title3} - Selected page: {e+1}")
        ab1.ok = True
    
    
def ab2Click(e):
    #print(ab1.nums, ab2.nums)
    dbl = e is ab2.selected
    if not ab2.selected is False:
        ab2.update(images[ab2.nums[ab2.selected]], ab2.selected)
    ab2.selected = e
    
    im = images[ab2.nums[e]].resize((150, 250))
    x, y = im.size
    dr = ImageDraw.Draw(im)
    
    dr.line((1, 1, x-1, 1), width=5, fill="red")
    dr.line((1, 1, 1, y-1), width=5, fill="red")
    dr.line((x-1, 1, x-1, y-1), width=5, fill="red")
    dr.line((1, y-17, x-1, y-17), width=5, fill="red")

    ab2.update(im, e)
    #ab3.update(images[e])

    if dbl:
        if ab2.ok:
            ab2.delete(e)
            ab2.root.title(f"{title2} - {ab2.i} page(s)")
    else:
        ab2.ok = True
        ab2.root.title(f"{title2} - {ab2.i} page(s), Selected page: {e+1}")

def reset1(e=None):
    if not ab1.selected is False:
        ab1.update(images[ab1.selected], ab1.selected)
    ab1.selected = False
    ab3.update(Image.new('RGB',(1,1),(46,46,46)))
    ab1.ok=True
    ab3.root.title(title3)
def reset2(e=None):
    if not ab2.selected is False:
        ab2.update(images[ab2.nums[ab2.selected]], ab2.selected)
    ab2.selected = False
    ab2.ok=True
    ab2.root.title(f"{title2} - {ab2.i} page(s)")

def hidePage(e):
    index = ab1.selected
    if index is False:
        return
    ab1.selected = False
    ab1.btn[index].pack_forget()
    ab1.hidden += 1
    ab1.scrollUpdate()
    ab1.root.title(f"{title1} - {ln-ab1.hidden} page(s)")
def restore():
    ab1.hidden = 0
    ab1.deleteAll()
    for i in range(0,ln): #inputpdf.getNumPages
        ab1.append(images[i], i)
    ab1.root.title(f"{title1} - {ln} page(s)")

def export(e=None):
    name = save().response
    if name == "":
        return
    if not name.endswith(".pdf"):
        name = name + ".pdf"
    #print(ab2.nums, name)
    writer = PdfFileWriter()
    for i in ab2.nums:
        val = patch(i)
        writer.addPage(inputpdf[val[0]].getPage(val[1]))
    with open(pdfs + '/' + name, 'wb') as outfile:
        writer.write(outfile)
        outfile.close()
    ab1.i = False
    reset1()
    ab2.deleteAll()

def patch(num):
    suma = 0
    for i in range(0, len(lns)):
        suma += lns[i]
        if suma > num:
            return (i, num-(suma-lns[i]))
        elif suma == num:
            return (i+1, num-suma)
    return None

def autorun():
    tme = strftime("%b.%d.%Y_%H.%M.%S", gmtime())
    if not isdir(pdfs):
        mkdir(pdfs)
    if not isdir(pdfs + '/' + backup):
        mkdir(pdfs + '/' + backup)
    pdf = glob(pdfs + "/*.pdf")
    for i in pdf:
        nme = basename(i).split('.')
        nme.pop()
        nme.append(tme)
        nme.append('pdf')
        move(i, pdfs + '/' + backup + '/' + '.'.join(nme))
    
#toexport = []
start = ' ' * 9
eq = 15
animation = ['|', '/', '-', '\\']
wChar = '\u2591'
bChar = '\u2593'
oChar = '\u2713'
lenani = len(animation)

def progress(index, maxim):
    procente = round(index*100/maxim,1)
    black = round(index*eq/maxim)
    white = (eq - black)
    print(f"{start}{black * bChar}{white * wChar}   {procente}%   ({index}/{maxim})", end='\r')
def progress2(index):
    print(f"{start}[{animation[index%lenani]}]", end='\r')

if __name__ == '__main__':
    autorun()
    
    path = argv.copy()
    del path[0]
    images = []
    inputpdf = []
    #images2 = None
    #correct = None
    lns = []
    ln = 0

    if len(path) > 0:
        tme = time()

        print("Loading files:")
        lnPath = len(path)

        progress(0, lnPath)

        for i in range(0, lnPath):
            i1 = i + 1
            
            file = path[i]
            PDFimg = convert_from_path(file)
            images = images + PDFimg
            inputpdf.append( PdfFileReader(open(file, "rb")) )
            lns.append(len(PDFimg))
            ln += len(PDFimg)
            progress(i1, lnPath)
        #correct = [0 for i in range(ln)]
        #images2 = images.copy()
        print(f"[{oChar}]:")
        print("Loading windows...")
        progress2(0)

        ab1 = ablak(ab1Click)
        ab2 = ablak(ab2Click)
        ab2.root.title(title2)
        ab1.root.title(f"{title1} - {ln} page(s)")
        ab3 = preview()
        #ab3.root.title(title3)

        ab1.root.bind('<Escape>', reset1)
        #ab1.root.bind('<a>', lambda e: ab1.mvFocus(0))
        #ab1.root.bind('<d>', lambda e: ab1.mvFocus(1))
        ab2.root.bind('<Escape>', reset2)
        ab2.root.bind('<Right>', lambda e: ab2.chPos(1))
        ab2.root.bind('<Left>',  lambda e: ab2.chPos(0))
        ab2.root.bind('<Delete>', ab2.autoclick)
        ab1.root.bind('<Delete>', hidePage)
        ab1.root.bind('<Return>', ab1.autoclick)
        ab2.root.bind('<Control-Key-d>', ab2.deleteAll)
        
        ab1.root.bind('<Control-Key-q>', lambda e: ab1.root.destroy() )
        ab2.root.bind('<Control-Key-q>', lambda e: ab2.root.destroy() )
        ab3.root.bind('<Control-Key-q>', lambda e: ab3.root.destroy() )

        ab1.root.bind('<Control-Key-s>', export)
        ab1.root.bind('<Control-Key-e>', export)
        ab2.root.bind('<Control-Key-s>', export)
        ab2.root.bind('<Control-Key-e>', export)
        ab3.root.bind('<Control-Key-s>', export)
        ab3.root.bind('<Control-Key-e>', export)

        menu = Menu(ab2.root)
        menu.add_command(label="Export", command=export)
        menu.add_command(label="Delete", command=ab2.deleteAll)
        menu.add_command(label="Reload", command=restore)
        menu.add_command(label="Quit", command=ab2.root.destroy)
        ab2.root.config(menu=menu)

        ab1.root.geometry("+0+310")
        ab2.root.geometry("+0+0")
        ab3.root.geometry("+1005+0")
        #print(ln)
        
        for i in range(0,ln): #inputpdf.getNumPages
           ab1.append(images[i], i)
           progress2(i)

        print(f"[{oChar}]:")
        print(f"Total loading time: {round(time()-tme,4)} s.")

        """wh=500

        ab3 = Tk()
        ab3.title("Preview")
        ab3.geometry(f"{wh}x{wh}")
        ab3.resizable(0,0)

        im=images[0]
        x, y = im.size
        sz = (int(wh*x/y), wh) if x < y else (wh, int(wh*y/x))
        buffer = BytesIO()
        im.resize(sz).save(buffer, format="png")
        buffer.seek(0)
        photof = PhotoImage(master=ab3, data=buffer.read())
        buffer.close()

        label = Label(ab3, width=wh, height=wh, image=photof)
        label.pack(side=LEFT)"""

        ab1Click(0, True)

        while True:
            try:
                ab1.root.update()
                ab2.root.update()
                ab3.root.update()
            except:
                try:
                    ab1.root.destroy()
                except:
                    pass
                try:
                    ab2.root.destroy()
                except:
                    pass
                try:
                    ab3.root.destroy()
                except:
                    pass
                break
            sleep(0.05)
        print('Bye!')
    else:
        print("Need some PDFs")
        input()
