import tkinter
import tkinter.messagebox
import customtkinter
import serial
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):

    WIDTH = 900
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.title("CERRADURA AUTOMATIZADA")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Control Puerta:\n"
                                                   "(Solo modo manual)",
                                              text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Abrir",
                                                command=self.envia3)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Cerrar",
                                                command=self.envia4)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Apariencia:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Bienvenido al sistema de control\n" +
                                                        "de la puerta automática del laboratorio\n" +
                                                        "de robótica.",
                                                   text_font=("Roboto Medium", -16),
                                                   height=100,
                                                   corner_radius=10,
                                                   fg_color=("white", "gray38"),
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="CONTROL DE VOLUMEN AL ABRIR LA PUERTA",
                                                   text_font=("Roboto Medium", -13),
                                                   height=40,
                                                   corner_radius=4,
                                                   fg_color=("white", "gray38"),
                                                   justify=tkinter.CENTER)
        self.label_info_2.grid(column=0, row=4, sticky="nwe", padx=90, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=2, column=0, sticky="ew", padx=15, pady=15)

        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="OPCIONES:",
                                                        text_font=("Roboto Medium", -16))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=20, padx=10, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(text="Manual", master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=0, command=self.envia)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="nw")

        self.radio_button_2 = customtkinter.CTkRadioButton(text="Automático", master=self.frame_right,
                                                           variable=self.radio_var,
                                                           value=1, command=self.envia1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="nw")

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
                                                command=self.progressbar.set)
        self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Permitir uso de tarjeta")
        self.switch_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["USUARIO 1", "USUARIO 2", "USUARIO 3"])
        self.combobox_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Comentarios")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Gráficas",
                                                border_width=2,
                                                fg_color=None,
                                                command=self.button_event3)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.optionmenu_1.set("Dark")
        self.combobox_1.set("Elegir Usuario")
        self.radio_button_1.select()
        self.slider_2.set(0.7)
        self.progressbar.set(0.5)

    def button_event(self):
        print("Encendido")

    def button_event2(self):
        print("Apagado")

    def button_event3(self):
        import grafico.py

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def envia(self):
        ser = serial.Serial("COM3", 115200)
        time.sleep(2)
        print("Manual")
        mandar = "2"
        enviar = mandar.encode("utf-8")
        ser.write(enviar)
        ser.close()

    def envia1(self):
        ser = serial.Serial("COM3", 115200)
        time.sleep(2)
        print("Automatico")
        mandar = "1"
        enviar = mandar.encode("utf-8")
        ser.write(enviar)
        ser.close()

    def envia3(self):
        ser = serial.Serial("COM3", 115200)
        time.sleep(2)
        print("Abierta")
        mandar = "3"
        enviar = mandar.encode("utf-8")
        ser.write(enviar)
        ser.close()

    def envia4(self):
        ser = serial.Serial("COM3", 115200)
        time.sleep(2)
        print("Cerrada")
        mandar = "4"
        enviar = mandar.encode("utf-8")
        ser.write(enviar)
        ser.close()


if __name__ == "__main__":

    app = App()

    app.mainloop()
