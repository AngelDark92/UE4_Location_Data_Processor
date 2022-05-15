import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as cl
from tkinter import *
from tkinter.ttk import *
# import the askopenfilename and askyesno functions from tkinter
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import imageio
import os

root = Tk()
root.resizable(False, False)
root.iconbitmap("openicon.ico")
root.title("Position Data Unpacker")
root.geometry("300x100")

l= Label(root, wraplength = 250, justify = LEFT, text = "Open file positionData.csv for each person and convert it to HeatMap and animated .gif file.")
l.config(font =("Times New Roman", 11))

def open_file():
    file = askopenfilename(title="Find positionData.csv", filetypes=[("positionData", "positionData.csv")])
    if not (len(file)) == 0:
        transform(file)

btn = Button(root, text ="Unpack", command = lambda:open_file())
btn.pack(side = BOTTOM, pady = 10)

l.pack()
btn.pack()


def transform(file):
    #create a string variable with the path to the open file
    filpath = file[:-17] + "/UnpackedData"
    if not os.path.exists(filpath):
        os.mkdir(filpath)
        func(file, filpath)
    else:
        answer = askyesno(title='Folder already exists', message='Are you sure that you want to rebuild it?')
        if answer:
            func(file, filpath)
        else:
            pass

#this is the main function, it accepts the file itself and the filepath to save the gif and png's in            
def func(file, filpath):
    pos1 = []
    xmin = -338.278
    xmax = 778.277
    ymin = -798.278
    ymax = 308.277
    with open(file, newline='') as csvfile:
        position = csv.DictReader(csvfile)
        for row in position:
            for a, b in row.items():
                b=b.replace("X", "")
                b=b.replace("Y", "")
                b=b.replace("Z", "")
                b=b.replace("=", "")
                pos1.append(b.rsplit(" "))
    pos2 = np.array(pos1, dtype=float)
    #position in time
    Roft = pos2[:,0:2]

    #HEAT MAP

    #set number of subdivisions per axis
    sub = 15

    xmint = np.floor(xmin)
    xmaxt = np.ceil(xmax)
    ymint = np.floor(ymin)
    ymaxt = np.ceil(ymax)

    count = np.zeros((sub,sub))
    sizex = (xmaxt-xmint)/(sub)
    sizey = (ymaxt-ymint)/(sub)
    for r in Roft:
        count[int(np.floor((r[0]-xmint)/sizex)), int(np.floor((r[1]-ymint)/sizey))] = count[int(np.floor((r[0]-xmint)/sizex)), int(np.floor((r[1]-ymint)/sizey))] + 1

    plt.imshow(np.transpose(count), cmap='hot', interpolation='gaussian')
    ax1 = plt.gca()
    ax1.invert_yaxis()
    ax1.invert_xaxis()
    ax1.axes.xaxis.set_visible(False)
    ax1.axes.yaxis.set_visible(False)
    plt.draw()
    plt.savefig(filpath + '/Heatmap.png')
    plt.close()

    #PATH IN TIME

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1)
    ax.axes.set_aspect('equal', adjustable='box')
    ax.invert_xaxis()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    fig.show()
    fig.canvas.draw()
    images = []

    #initialize segments
    seg = [ [(Roft[0,0],Roft[0,1]), (Roft[1,0],Roft[1,1])] ]

    for i in range(len(Roft)-2):
        ax.axes.clear()
        seg.append([(Roft[i+1,0],Roft[i+1,1]), (Roft[i+2,0],Roft[i+2,1])])
        lc = cl.LineCollection(seg)
        fig, ax = plt.subplots()
        ax.set_xlim(xmin-50,xmax+50)
        ax.set_ylim(ymin-50,ymax+50)
        plt.gca().set_aspect('equal', adjustable='box')
        ax.invert_xaxis()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        ax.add_collection(lc)
        plt.draw()
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        kwargs_write = {'fps':5.0, 'quantizer':'nq'}
        images.append(image)
        plt.close()
        



    imageio.mimsave(filpath + '/Animation.gif', images, fps=5)
    plt.close()

mainloop()