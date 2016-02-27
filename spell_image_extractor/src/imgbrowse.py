#!/usr/bin/env python
from Tkinter import *
from PIL import Image, ImageTk
import glob
import os
import shutil
import xml.etree.ElementTree as ET

class Viewer:
    def __init__(self, master, filelist, namelist):
        self.top = master
        self.files = filelist
        self.names = namelist
        self.index = 0
        #display first image
        filename = filelist[0]
        if not os.path.exists(filename):
            print "Unable to find %s" % filename
            self.top.quit()

        lframe = Frame(master)
        lframe.pack(side='left')
        self.title = Label(lframe, text=os.path.basename(filename))
        self.title.pack()
        
        self.im = Image.open(filename)
        self.size = self.im.size
        self.tkimage = ImageTk.PhotoImage(self.im)
        
        self.lbl = Label(lframe, image=self.tkimage)
        self.lbl.pack(side='top')

        # the button frame
        fr = Frame(lframe)
        fr.pack(side='top', expand=1, fill='x')
        back = Button(fr, text="back", command=lambda : self.nextframe(-1))
        back.grid(row=0, column=0, sticky="w", padx=4, pady=4)

        ilabel = Label(fr, text="image number:")
        ilabel.grid(row=0, column=1, sticky="e", pady=4)

        self.evar = IntVar()
        self.evar.set(1)
        entry = Entry(fr, textvariable=self.evar)
        entry.grid(row=0, column=2, sticky="w", pady=4)
        entry.bind('<Return>', self.getimgnum)
        
        rframe = Frame(master)
        rframe.pack(side='left', fill='y')
        lbframe = Frame(rframe)
        lbframe.pack(side='top', fill='y')
        scrollbar = Scrollbar(lbframe)
        self.listbox = Listbox(lbframe, width=60, height=22, font=("Courier",))
        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(side='left', fill='y')
        scrollbar['command'] = self.listbox.yview 
        self.listbox['yscrollcommand'] = scrollbar.set
        for name in namelist:
            self.listbox.insert(END, name)
        
        button = Button(rframe, text='Assign name', command=lambda: self.assign_name())
        button.pack(side='top')
        next = Button(fr, text="next", command=lambda : self.nextframe(1))
        next.grid(row=0, column=3, sticky="e", padx=4, pady=4)
        self.listbox.bind('<Return>', self.assign_name)
        self.listbox.bind('<Left>', lambda x : self.nextframe(-1))
        self.listbox.bind('<Right>', lambda x : self.nextframe(1))

    def nextframe(self,i=1, imgnum=-1):
        if imgnum == -1:
            self.index += i
        else:
            self.index = imgnum - 1
        if self.index >= len(self.files):
            self.index = 0
        elif self.index < 0:
            self.index = len(self.files) - 1
        filename = self.files[self.index]
        if not os.path.exists(filename):
            print "Unable to find %s" % filename
            self.top.quit()
        self.title.configure(text=os.path.basename(filename))
        self.evar.set(self.index+1)
        
        self.im = Image.open(filename)
        self.tkimage = ImageTk.PhotoImage(self.im)
        self.lbl.configure(image=self.tkimage)
        
    def getimgnum(self, event=None):
        self.nextframe(imgnum=self.evar.get())
        
    def assign_name(self, unused_event=None):
        old_name = self.files[self.evar.get() - 1]
        box_line = self.listbox.get(ACTIVE)
        box_line_num = self.listbox.curselection()
        new_name = box_line.split('|')[2]
        new_path = 'named_images/' + new_name + '.png'
        shutil.copy(old_name, new_path)
        print 'Saved', old_name, 'to', new_name
        self.files.remove(old_name)
        self.names.remove(box_line)
        cursel = self.listbox.curselection()
        self.listbox.delete(cursel, cursel)
        self.nextframe(0)
        self.listbox.selection_set(box_line_num)

if __name__ == "__main__":
    cards_xml = ET.parse('data/cards.xml')
    units = cards_xml.find('.').findall('unit')
    bundled = []
    pic_names = []
    if not os.path.exists('named_images'): os.mkdir('named_images')
    for unit in units:
        ab = unit.find('asset_bundle')
        if unit.find('picture') is not None and os.path.exists('named_images/' + unit.find('picture').text + '.png'):
            continue
        if ab is None:
            print unit.find('name').text, 'No asset_bundle, setting to 0(resources.assets)'
            ab = '0'
        else:
            ab = ab.text
        if unit.find('picture') is None: print unit.find('name').text, 'No picture'
        if ab is not None and unit.find('picture') is not None and unit.find('picture').text not in pic_names:
            bundled.append(ab.rjust(3) + '| ' + unit.find('name').text.ljust(21) + '|' + unit.find('picture').text)
            pic_names.append(unit.find('picture').text)
    bundled.sort(key=lambda x:(int(x.split('|')[0]), x.split('|')[2]))

    filelist = glob.glob('images/*_*.png')
    filelist.sort(key=lambda x:map(int, x.split(os.path.sep)[1].split('.')[0].split('_')))
    print len(bundled), 'in card data for', len(filelist), 'images'
    root = Tk()
    app = Viewer(root, filelist, bundled)
    root.mainloop()
