import matplotlib

from configs.variables_sim import NUM_NEURONAS_EX, NUM_NEURONAS_IN

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Tkinter import *


master1 = Tk()
master1.title("Simulacion")
TAMANIO_VENTANA_W = master1.winfo_screenwidth()
TAMANIO_VENTANA_H = master1.winfo_screenheight()

TAMANIO_CANVAS = TAMANIO_VENTANA_H * 0.80
# PARAMETROS PARA PINTAR NEURONAS
TAM_SEPARACION_EX = TAMANIO_CANVAS / NUM_NEURONAS_EX
TAM_SEPARACION_IN = TAMANIO_CANVAS/ NUM_NEURONAS_IN

SEPARACION_CELL_EX = [TAM_SEPARACION_EX * 0.2, TAM_SEPARACION_EX * 0.8 ]
SEPARCACION_CELL_IN = [TAM_SEPARACION_IN * 0.6, TAM_SEPARACION_IN * 0.4 ]
master1.geometry("%dx%d" % (TAMANIO_VENTANA_W, TAMANIO_VENTANA_H))
canvas_1 = Canvas(master1, width=40, height=30)
canvas_1.grid(row=1, column=1)
Label(master1, text="Zona CA3", font="Helvetica 10 bold").grid(row=1, column=2)
Label(master1, text=" ").grid(row=1, column=3)
Label(master1, text="Zona CA1", font="Helvetica 10 bold").grid(row=1, column=4)
canvas_1 = Canvas(master1, width=40, height=60).grid(row=2, column=1)
fca3 = plt.figure(figsize=(9, 4),dpi=100, facecolor='black')
ACA3 = fca3.add_subplot(111,facecolor="#000000")
ACA3.set_ylim(-100, -30)
ACA3.set_xlim(0, 10)
plt.rc('font', size=5)
plt.subplots_adjust(left=0.04, right=1, top=0.94, bottom=0.03)
ACA3.tick_params(axis='y', colors='#25fa04')
ACA3.set_yticklabels("")
canvas_figCA3 = FigureCanvasTkAgg(fca3, master=master1)
canvas_figCA3.get_tk_widget().config(width=TAMANIO_CANVAS, height=30,background='black',  highlightcolor='black', highlightbackground='black')
canvas_figCA3.get_tk_widget().grid(row=2,column=2)
canvas_1 = Canvas(master1, width=40, height=60).grid(row=2, column=3)

fca1 = plt.figure(figsize=(9, 4),dpi=100, facecolor='black')
ACA1 = fca1.add_subplot(111,facecolor="#000000")
ACA1.set_ylim(-85, -45)
ACA1.set_xlim(0, 10)
plt.rc('font', size=5)
plt.subplots_adjust(left=0.04, right=1, top=0.94, bottom=0.03)
ACA1.tick_params(axis='y', colors='#25fa04')
canvas_figCA1 = FigureCanvasTkAgg(fca1, master=master1,)
canvas_figCA1.get_tk_widget().config(width=TAMANIO_CANVAS, height=30,background='black',  highlightcolor='black', highlightbackground='black')
canvas_figCA1.get_tk_widget().grid(row=2,column=4)

canvas_1 = Canvas(master1, width=40, height=TAMANIO_CANVAS)
canvas_1.grid(row=3, column=1)
canvas_ca3 = Canvas(master1, width=TAMANIO_CANVAS, height=TAMANIO_CANVAS, bg="black")
canvas_ca3.grid(row=3, column=2)
canvas_1 = Canvas(master1, width=40, height=TAMANIO_CANVAS)
canvas_1.grid(row=3, column=3)
canvas_ca1 = Canvas(master1,
                        width=TAMANIO_CANVAS, height=TAMANIO_CANVAS, bg="black" )
canvas_ca1.grid(row=3, column=4)

