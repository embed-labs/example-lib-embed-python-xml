import embed_api as api

import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from PIL import Image, ImageTk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        api.configurar()    # Configuração da API

        # Variáveis de cores
        self.cor_fundo = "black"
        self.cor_botao = "green"
        self.cor_texto = "white"

        self.title("Embed")
        self.overrideredirect(False)  # Mostra a barra de título

        # Responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)  # Ocupa 4/5 da tela
        self.grid_columnconfigure(0, weight=1)

        self.header = HeaderFrame(self, bg=self.cor_fundo)
        self.header.grid(row=0, column=0, sticky="nsew")

        self.content = ContentFrame(self, bg=self.cor_fundo)
        self.content.grid(row=1, column=0, sticky="nsew")

        self.frames = {
            "TelaPrincipal": TelaPrincipal, 
            "TelaProcessamento": TelaProcessamento,
        }
        self.mostrar_frame("TelaPrincipal")

    def mostrar_frame(self, page_name):
        frame_class = self.frames[page_name]
        self.content.mostrar_frame(frame_class)

class HeaderFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_logo_index = 0
        self.logos = [
            Image.open("img/logo1.png"), 
            Image.open("img/logo2.png"),
            Image.open("img/logo3.png"),
        ]

        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label = tk.Label(self, image=self.logo_photo)
        self.logo_label.pack(pady=1)

        # Alterna entre as imagens do logo a cada segundo
        self.after(1000, self.toggle_logo)

    def toggle_logo(self):
        self.current_logo_index = (self.current_logo_index + 1) % len(self.logos)
        self.logo_photo = ImageTk.PhotoImage(self.logos[self.current_logo_index])
        self.logo_label.config(image=self.logo_photo)
        self.after(1000, self.toggle_logo)

class ContentFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.controller = None  # Será atribuído na chamada de mostrar_frame

    def mostrar_frame(self, frame_class):
        if self.controller:
            self.controller.destroy()

        self.controller = frame_class(self)
        self.controller.pack(fill="both", expand=True)

class TelaPrincipal(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        api.iniciar()   # Inicialização do produto XML

        self.label = tk.Label(self, text="Selecione o arquivo ou adicione o conteúdo:", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 26))
        self.label.pack()

        # Frame para agrupar o Entry e o botão Browse
        self.entry_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.entry_frame.pack(pady=10)

        self.textbox = tk.Entry(self.entry_frame, font=('Helvetica', 18))
        self.textbox.pack(side="left", fill="x", expand=True)

        self.browse_button = tk.Button(self.entry_frame, text="Browse", command=self.browse_file, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.browse_button.pack(side="left", padx=5)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=30, pady=10)

        self.zip_button = tk.Button(self.button_frame, text="ZIP", command=self.processar_zip, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.zip_button.pack(side="left", padx=10)

        self.rar_button = tk.Button(self.button_frame, text="RAR", command=self.processar_rar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.rar_button.pack(side="left", padx=10)

        self.path_button = tk.Button(self.button_frame, text="PATH", command=self.processar_path, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.path_button.pack(side="left", padx=10)
        
        self.xml_button = tk.Button(self.button_frame, text="XML", command=self.processar_xml, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.xml_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(side="left", padx=10)

    def browse_file(self):
        filename = filedialog.askdirectory()
        if filename:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0, filename)

    def processar_zip(self):
        valor = self.textbox.get()
        print("Caminho arquivo zip:", valor)

        result = api.zip(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def processar_rar(self):
        valor = self.textbox.get()
        print("Caminho arquivo rar:", valor)

        result = api.rar(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def processar_path(self):
        valor = self.textbox.get()
        print("Caminho arquivo path:", valor)

        result = api.path(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def processar_xml(self):
        valor = self.textbox.get()
        print("Conteúdo xml:", valor)

        result = api.xml(valor)
        if result == "1":
            self.parent.master.mostrar_frame("TelaProcessamento")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

class TelaProcessamento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent.master.cor_fundo)
        self.parent = parent

        self.label = tk.Label(self, text="Enviando XML para Datalake Embed", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.label.pack(pady=10)

        self.spinner = ttk.Progressbar(self, mode='indeterminate', )
        self.spinner.pack(pady=10)
        self.spinner.start()

        self.status_label = tk.Label(self, text="Aguardando processamento...", bg=self.parent.master.cor_fundo, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.status_label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg=self.parent.master.cor_fundo)
        self.button_frame.pack(padx=20)

        self.cancel_button = tk.Button(self.button_frame, text="Cancelar", command=self.cancelar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.cancel_button.pack(side="left", padx=10)

        self.voltar_button = tk.Button(self.button_frame, text="Voltar", command=self.voltar, bg=self.parent.master.cor_botao, fg=self.parent.master.cor_texto, font=('Helvetica', 18))
        self.voltar_button.pack(pady=10)

        self.process_thread = Thread(target=self.processar)
        self.process_thread.start()    
        
    def processar(self):
        while True:
            result = api.status()
            if result == "0":
                api.finalizar()

                self.label.pack_forget()
                self.spinner.pack_forget()
                self.button_frame.pack_forget()
                self.status_label.config(text="Envio realizado com sucesso!", font=('Helvetica', 26))

                time.sleep(3)
                self.voltar()
                break

    def cancelar(self):
        print("Cancelando operação")

    def voltar(self):
        self.parent.master.mostrar_frame("TelaPrincipal")

if __name__ == "__main__":
    app = Main()
    app.mainloop()
