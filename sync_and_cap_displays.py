#############################################################################
#
# (C) 2021 Cadence Design Systems, Inc. All rights reserved worldwide.
#
# This sample script is not supported by Cadence Design Systems, Inc.
# It is provided freely for demonstration purposes only.
# SEE THE WARRANTY DISCLAIMER AT THE BOTTOM OF THIS FILE.
#
#############################################################################


#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from pointwise import GlyphClient, GlyphError
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk, ImageFont, ImageDraw

class PreviewDialog:
    def __init__(self, parent, filename):
        top = self.top = Toplevel(parent)
        top.title('Capture: {0}'.format(filename))
        top.preview = ImageTk.PhotoImage(file=filename)
        Label(top, image=top.preview).pack()

class Application(Frame):
    def __init__(self, master=None):
        self.port1 = StringVar()
        self.port1.set(os.environ.get('PWI_GLYPH_SERVER_PORT', ''))
        self.auth1 = StringVar()
        self.auth1.set(os.environ.get('PWI_GLYPH_SERVER_AUTH', ''))
        self.desc1 = StringVar()
        self.desc1.set('Not Connected')

        self.port2 = StringVar()
        self.port2.set('')
        self.auth2 = StringVar()
        self.auth2.set('')
        self.desc2 = StringVar()
        self.desc2.set('Not Connected')

        self.label1 = StringVar()
        self.label1.set('')
        self.label2 = StringVar()
        self.label2.set('')
        self.imgFg1 = StringVar()
        self.imgFg1.set('Color')
        self.imgBg1 = StringVar()
        self.imgBg1.set('Color')
        self.imgFg2 = StringVar()
        self.imgFg2.set('Color')
        self.imgBg2 = StringVar()
        self.imgBg2.set('Color')
        self.imgWidth = StringVar()
        self.imgWidth.set('600')
        self.imgHeight = StringVar()
        self.imgHeight.set('600')
        self.imgFilename = StringVar()
        self.imgFilename.set('screen.png')
        self.imgOutput = StringVar()
        self.imgOutput.set('Side By Side')

        Frame.__init__(self, master)
        self.createWidgets()

        if self.port1.get():
            self.connect1()

    def createWidgets(self):
        topframe = Frame(padx=2, pady=2)
        topframe.pack()

        frame = LabelFrame(topframe, text='Pointwise 1', padx=2, pady=2)
        frame.pack(side='left', fill='both', expand='yes')
        Label(frame, text='Port:').grid(row=0, column=0, sticky=E)
        Entry(frame, textvariable=self.port1, width=10).grid(row=0, column=1, sticky=W)
        Label(frame, text='Auth:').grid(row=0, column=2, sticky=E)
        Entry(frame, textvariable=self.auth1, width=10).grid(row=0, column=3, sticky=W)
        Button(frame, text='Check', command=self.connect1).grid(row=1, column=0)
        Label(frame, textvariable=self.desc1).grid(row=1, column=1, columnspan=4)
        Frame(frame, height=2, borderwidth=2, relief=RIDGE).grid(padx=5, pady=5, row=2, column=0, columnspan=5, sticky=EW)
        Label(frame, text='Label:').grid(row=3, column=0, sticky=E)
        Entry(frame, width=30, textvariable=self.label1).grid(row=3, column=1, columnspan=4, sticky=W)
        Label(frame, text='Fg/Bg:').grid(row=4, column=0, sticky=E)
        OptionMenu(frame, self.imgFg1, 'Color', 'Grayscale', 'White', 'Black').grid(row=4, column=1, sticky=W)
        OptionMenu(frame, self.imgBg1, 'Color', 'Grayscale', 'White', 'Black', 'Transparent').grid(row=4, column=2, columnspan=2, sticky=W)

        frame = Frame(topframe, padx=5, pady=10)
        frame.pack(side='left', fill='both', expand='yes')
        Button(frame, text='1 -> 2', command=self.sync1to2).pack()
        Button(frame, text='1 <- 2', command=self.sync2to1).pack()

        frame = LabelFrame(topframe, text='Pointwise 2', padx=2, pady=2)
        frame.pack(side='left', fill='both', expand='yes')
        Label(frame, text='Port:').grid(row=0, column=0, sticky=E)
        Entry(frame, textvariable=self.port2, width=10).grid(row=0, column=1, sticky=W)
        Label(frame, text='Auth:').grid(row=0, column=2, sticky=E)
        Entry(frame, textvariable=self.auth2, width=10).grid(row=0, column=3, sticky=W)
        Button(frame, text='Check', command=self.connect2).grid(row=1, column=0)
        Label(frame, textvariable=self.desc2).grid(row=1, column=1, columnspan=4)
        Frame(frame, height=2, borderwidth=2, relief=RIDGE).grid(padx=5, pady=5, row=2, column=0, columnspan=5, sticky=EW)
        Label(frame, text='Label:').grid(row=3, column=0, sticky=E)
        Entry(frame, width=30, textvariable=self.label2).grid(row=3, column=1, columnspan=4, sticky=W)
        Label(frame, text='Fg/Bg:').grid(row=4, column=0, sticky=E)
        OptionMenu(frame, self.imgFg2, 'Color', 'Grayscale', 'White', 'Black').grid(row=4, column=1, sticky=W)
        OptionMenu(frame, self.imgBg2, 'Color', 'Grayscale', 'White', 'Black', 'Transparent').grid(row=4, column=2, columnspan=2, sticky=W)

        frame = LabelFrame(text='Screen Capture', padx=2, pady=2)
        frame.pack(fill='both', expand='yes')
        Label(frame, text='W x H:').grid(row=0, column=0, sticky=E)
        Entry(frame, width=5, textvariable=self.imgWidth).grid(row=0, column=1, sticky=W)
        Label(frame, text='x').grid(row=0, column=2, sticky=E)
        Entry(frame, width=5, textvariable=self.imgHeight).grid(row=0, column=3, sticky=W)
        Frame(frame, width=2).grid(padx=5, row=0, column=4, sticky=NS)
        Label(frame, text='Output:').grid(row=0, column=5, sticky=E)
        OptionMenu(frame, self.imgOutput, 'Side By Side', 'Top And Bottom', 'Blend').grid(row=0, column=6, sticky=W)
        Frame(frame, width=2).grid(padx=5, row=0, column=7, sticky=NS)
        Label(frame, text='Filename:').grid(row=0, column=8, sticky=E)
        Entry(frame, width=20, textvariable=self.imgFilename).grid(row=0, column=9, sticky=W)
        Frame(frame, width=2).grid(padx=5, row=0, column=10, sticky=NS)
        Button(frame, text='Capture', command=self.capture).grid(row=0, column=11)

    def connect1(self):
        glf = self.connectAndUpdateDesc(self.port1.get(), self.auth1.get(), self.desc1)
        if glf:
            glf.close()

    def connect2(self):
        glf = self.connectAndUpdateDesc(self.port2.get(), self.auth2.get(), self.desc2)
        if glf:
            glf.close()

    def connectAndUpdateDesc(self, port, auth, descVar):
        glf = None
        desc = 'Not Connected'
        if port:
            glf = GlyphClient(port=port, auth=auth)
            if glf.connect():
                try:
                    desc = glf.eval('pw::Application getVersion')
                except:
                    desc = 'Error getting version'
                    glf.close()
                    glf = None
            elif glf.is_busy():
                desc = 'GlyphServer is busy'
                glf.close()
                glf = None
            elif glf.auth_failed():
                desc = 'Authentication failed'
                glf.close()
                glf = None
        descVar.set(desc)
        return glf

    def sync1to2(self):
        glf1 = self.connectAndUpdateDesc(self.port1.get(), self.auth1.get(), self.desc1)
        glf2 = self.connectAndUpdateDesc(self.port2.get(), self.auth2.get(), self.desc2)
        if glf1 and glf2:
            self._syncDisplay(glf1, glf2)
        if glf1:
            glf1.close()
        if glf2:
            glf2.close()

    def sync2to1(self):
        glf2 = self.connectAndUpdateDesc(self.port2.get(), self.auth2.get(), self.desc2)
        glf1 = self.connectAndUpdateDesc(self.port1.get(), self.auth1.get(), self.desc1)
        if glf2 and glf1:
            self._syncDisplay(glf2, glf1)
        if glf2:
            glf2.close()
        if glf1:
            glf1.close()

    def _syncDisplay(self, glfFrom, glfTo):
        view = None
        try:
            view = glfFrom.eval('pw::Display getCurrentView')
        except GlyphError as e:
            view = None
            msg = 'Failed to get the current view from Pointwise:\n'
            msg += str(e)
            messagebox.showerror('Error', msg)

        if view:
            try:
                glfTo.eval('pw::Display setCurrentView [list {0}]'.format(view))
            except GlyphError as e:
                msg = 'Failed to set the current view in Pointwise:\n'
                msg += str(e)
                messagebox.showerror('Error', msg)

    def capture(self):
        filename = self.imgFilename.get()
        filename = os.path.abspath(filename)
        basename, ext = os.path.splitext(filename)
        if not ext:
            ext = '.png'
        filename = basename + ext
        output = self.imgOutput.get()

        bg1 = self.imgBg1.get()
        bg2 = self.imgBg2.get()

        tempfile1 = ''
        tempfile2 = ''
        glf1 = self.connectAndUpdateDesc(self.port1.get(), self.auth1.get(), self.desc1)
        glf2 = self.connectAndUpdateDesc(self.port2.get(), self.auth2.get(), self.desc2)
        if glf1 and glf2:
            tempfile1 = '{0}_tmp1{1}'.format(basename, ext)
            if not self.saveDisplay(glf1, self.imgFg1.get(), bg1, tempfile1):
                os.unlink(tempfile1)
                tempfile1 = ''

            tempfile2 = '{0}_tmp2{1}'.format(basename, ext)
            if not self.saveDisplay(glf2, self.imgFg2.get(), bg2, tempfile2):
                os.unlink(tempfile2)
                tempfile2 = ''

        if glf1:
            glf1.close()
        if glf2:
            glf2.close()
        
        if tempfile1 and tempfile2:
            font = ImageFont.load_default()
            image1 = Image.open(tempfile1)
            (width1, height1) = image1.size
            image2 = Image.open(tempfile2)
            (width2, height2) = image2.size
            imageout = None

            if output != 'Blend':
                drawer = ImageDraw.Draw(image1)
                img_text = self.desc1.get()
                if self.label1.get():
                    img_text += "\n" + self.label1.get()
                size = drawer.textsize(img_text, font=font)
                drawer.rectangle((0, 0, size[0], size[1]), (255,255,255))
                drawer.text((0, 0), img_text, (0,0,0), font=font)

                drawer = ImageDraw.Draw(image2)
                img_text = self.desc2.get()
                if self.label2.get():
                    img_text += "\n" + self.label2.get()
                size = drawer.textsize(img_text, font=font)
                drawer.rectangle((0, 0, size[0], size[1]), (255,255,255))
                drawer.text((0, 0), img_text, (0,0,0), font=font)
            

            if output == 'Side By Side':
                new_width = width1 + width2
                new_height = max(height1, height2)

                imageout = Image.new('RGB', (new_width, new_height))
                imageout.paste(im=image1, box=(0, 0))
                imageout.paste(im=image2, box=(width1, 0))

            elif output == 'Top And Bottom':
                new_width = max(width1, width2)
                new_height = height1 + height2

                imageout = Image.new('RGB', (new_width, new_height))
                imageout.paste(im=image1, box=(0, 0))
                imageout.paste(im=image2, box=(0, height1))

            elif output == 'Blend':
                new_size = (max(width1, width2), max(height1, height2))
                image1 = image1.resize(new_size)
                image2 = image2.resize(new_size)
                if bg1 == 'Transparent' and bg2 == 'Transparent':
                    imageout = Image.new('RGBA', new_size, (0,0,0,0))
                    imageout.paste(im=image1, box=(0, 0), mask=image1)
                    imageout.paste(im=image2, box=(0, 0), mask=image2)
                elif bg1 == 'Transparent' and bg2 != 'Transparent':
                    imageout = Image.new('RGBA', new_size, (0,0,0,0))
                    imageout.paste(im=image2, box=(0, 0))
                    imageout.paste(im=image1, box=(0, 0), mask=image1)
                elif bg1 != 'Transparent' and bg2 == 'Transparent':
                    imageout = Image.new('RGBA', new_size, (0,0,0,0))
                    imageout.paste(im=image1, box=(0, 0))
                    imageout.paste(im=image2, box=(0, 0), mask=image2)
                else:
                    imageout = Image.blend(image1.resize(new_size), image2.resize(new_size), 0.5)

            if imageout:
                imageout.save(filename, 'PNG')
                imageout.close()

                self.preview = PreviewDialog(self, filename)
            
            image1.close()
            image2.close()

            if tempfile1:
                os.unlink(tempfile1)
            if tempfile2:
                os.unlink(tempfile2)


    def saveDisplay(self, glf, fg, bg, filename):
        width = float(self.imgWidth.get()) / 72.0
        height = float(self.imgHeight.get()) / 72.0

        result = False
        command = 'pw::Display saveImage'
        command += ' -foreground {0}'.format(fg)
        command += ' -background {0}'.format(bg)
        command += ' -dpi 72 -size [list {0} {1}]'.format(width, height)
        command += ' "{0}"'.format(filename.replace('\\', '\\\\'))
        try:
            result = glf.eval(command)
            result = (result == '1')
        except GlyphError as e:
            msg = 'Failed to do screen capture in Pointwise:\n'
            msg += str(e)
            messagebox.showerror('Error', msg)
            result = False
        return result


root = Tk()
root.title("Sync And Cap Displays")
app = Application(master=root)
app.mainloop()


#############################################################################
#
# This file is licensed under the Cadence Public License Version 1.0 (the
# "License"), a copy of which is found in the included file named "LICENSE",
# and is distributed "AS IS." TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE
# LAW, CADENCE DISCLAIMS ALL WARRANTIES AND IN NO EVENT SHALL BE LIABLE TO
# ANY PARTY FOR ANY DAMAGES ARISING OUT OF OR RELATING TO USE OF THIS FILE.
# Please see the License for the full text of applicable terms.
#
#############################################################################
