from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial
import tkinter as tk
import time

# ------global variables
dis_g = np.array([])
temp_g = np.array([])
pwm_g = np.array([])
cond = False
m = 30
global ser
ser = serial.Serial("COM3", 115200)
time.sleep(4)
mandar = "5"
enviar = mandar.encode("utf-8")
ser.write(enviar)

# -----plot data-----
def plot_data():
    global cond, dis_g, temp_g, pwm_g, m, ax, ser

    if (cond == True):

        a = ser.readline().decode('utf-8')
        lista = a.split(',')

        if (len(dis_g) < m + 1):
            dis_g = np.append(dis_g, float(lista[0]))
            temp_g = np.append(temp_g, float(lista[1]))
        else:

            dis_g[0:m] = dis_g[1:m + 1]
            dis_g[m] = float(lista[0])
            temp_g[0:m] = temp_g[1:m + 1]
            temp_g[m] = float(lista[1])
            pwm_g[0:m] = pwm_g[1:m + 1]
            m = m + 1
            ax.set_xlim(0, m - 1)

        lines.set_xdata(np.arange(0, len(dis_g)))
        lines.set_ydata(dis_g)
        lines1.set_xdata(np.arange(0, len(temp_g)))
        lines1.set_ydata(temp_g)

        canvas.draw()
        # print(dis_g, temp_g, pwm_g)

    root.after(1, plot_data)


def plot_start():
    global cond, ser
    cond = True


def plot_stop():
    global cond, ser
    cond = False
    ser.close()



# -----Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background='white')
root.geometry("720x600")  # set the window size

# ------create Plot object on GUI----------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

# ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('Serial Data');
ax.set_xlabel('Número de muestra')
ax.set_ylabel('\nDistancia (cm)\nTemperatura(°C)')
ax.set_xlim(0, m)
ax.set_ylim(-0.5, 280)
lines = ax.plot([], [])[0]
lines1 = ax.plot([], [])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x=10, y=120, width=600, height=400)
canvas.draw()

# ----------create button---------
root.update();
start = tk.Button(root, text="Start", font=('calbiri', 12), command=lambda: plot_start())
start.place(x=100, y=550)

root.update();
stop = tk.Button(root, text="Stop", font=('calbiri', 12), command=lambda: plot_stop())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=550)

label_d = tk.Label(root, text='Distancia', bg='Blue', fg='White')
label_d.pack(padx=10, pady=10)
label_a = tk.Label(root, text='Temperatura', bg='Orange', fg='White')
label_a.pack(padx=20, pady=10)

# ----start serial port----


root.after(1, plot_data)
root.mainloop()