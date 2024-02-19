# python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# imports

import time
import json
import io
import os
import base64
from libembed import configurar, iniciar, processar, finalizar, obter_valor
from PIL import Image, ImageTk
import warnings
from dotenv import load_dotenv
from threading import Thread
from tkinter import (
    Button,
    Tk,
    Label,
    Frame,
    Text,
    StringVar,
    Scrollbar,
    VERTICAL,
    NSEW,
    NS,
    W,
    FLAT,
    SUNKEN,
    END,
    RAISED,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --------------------------------------------------------------------------------------------

LARGE_FONT_STYLE = ("Roboto", 12, "bold")  # brandon, musc, montserrat, coco goose
SMALL_FONT_STYLE = ("Roboto", 11, "bold")
BUTTON_FONT_STYLE = ("Roboto", 9)
COLOR_BG_FRAME = "#282a36"  # Dark purple
COLOR_BG_LABEL = "#282a36"  # Dark purple
COLOR_FG_LABEL = "#f8f8f2"  # White
COLOR_BG_ENTRY = "#44475a"  # Dark gray
COLOR_BG_BUTTON = "#6272a4"  # Light purple
COLOR_FG_BUTTON = "#f8f8f2"  # White

# =========================================
# | =========  PÁGINA PRINCIPAL ========= |
# =========================================


class PixApp:
    # =========================================
    # | ===========  BEGIN LAYOUT =========== |
    # =========================================
    def __init__(self, root):
        self.root = root
        self.root.title("Exemplo Pix")
        self.root.resizable(width=False, height=False)
        self.root.minsize(700, 400)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame = self.create_main_frame()
        self.value_frame = self.create_value_frame()
        self.operator_frame = self.create_operator_frame()
        self.logs_frame = self.create_logs_frame()
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()
        self.logs_text = self.create_logs_text()
        self.xml_texts = self.create_xmls_text()
        self.buttons["canc"]["state"] = "disabled"

    def create_main_frame(self):
        frame = Frame(self.root, bg=COLOR_BG_FRAME, borderwidth=2, border=10)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(5, 5), pady=(5, 5))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        return frame

    def create_value_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        return frame

    def create_operator_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=1, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        return frame

    def create_logs_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=1, row=0, rowspan=2, sticky=NS, padx=(1, 1), pady=(1, 1))
        return frame

    def create_labels(self):
        self.lbl_value_text = StringVar()
        self.lbl_value_text.set("")
        lbl_value = Label(
            self.value_frame,
            text="Xml teste",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_value.grid(column=0, row=0, sticky=W, pady=(0, 0))

        lbl_content = Label(
            self.value_frame,
            text="Conteudo do XML",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_content.grid(column=0, row=1, sticky=W, pady=(35, 0))

        lbl_path = Label(
            self.value_frame,
            text="Caminho do XML",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_path.grid(column=0, row=2, sticky=W, pady=(0, 0))

        lbl_operator_title = Label(
            self.operator_frame,
            text="Operador",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_operator_title.grid(column=0, row=0, columnspan=2, sticky=W, pady=(10, 0))

        lbl_logs = Label(
            self.logs_frame,
            text="Logs Exemplos",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_logs.grid(column=0, row=0, sticky=W, pady=(10, 0))

        self.lbl_operator_text = StringVar()
        self.lbl_operator_text.set("Status")
        lbl_operator = Label(
            self.operator_frame,
            textvariable=self.lbl_operator_text,
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=SMALL_FONT_STYLE,
        )
        lbl_operator.grid(column=0, row=1, columnspan=2, sticky=W, pady=(10, 0))

        return lbl_operator

    def create_buttons(self):
        btns = {}

        btns["configs"] = Button(
            self.value_frame,
            text="Configurar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.configurar,
        )
        btns["configs"].grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_enviar"] = Button(
            self.value_frame,
            text="Enviar XML",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento_enviar,
        )
        btns["btn_enviar"].grid(column=0, row=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        btns["canc"] = Button(
            self.operator_frame,
            text="Cancelar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.cancelamento,
        )
        btns["canc"].grid(column=1, row=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        return btns

    def create_xmls_text(self):
        self.xml_content = StringVar()
        entry_content = Text(
            self.value_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
            height=1,
        )
        entry_content.grid(column=1, row=1, sticky=NS, padx=10, pady=10)
        entry_content.insert(END, "")

        self.xml_path = StringVar()
        entry_path = Text(
            self.value_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
            height=2
        )
        entry_path.grid(column=1, row=2, sticky=NS, padx=10, pady=10)
        entry_path.insert(END, "")

        return [entry_content, entry_path]

    def create_logs_text(self):
        self.logs = StringVar()
        logs_entry = Text(
            self.logs_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
        )
        logs_entry.grid(column=0, row=1, sticky=NS, padx=(10, 0), pady=(10, 20))
        logs_entry.insert(END, "")

        sb_ver = Scrollbar(self.logs_frame, orient=VERTICAL)
        sb_ver.grid(column=1, row=1, sticky=NS, pady=(10, 20))

        logs_entry.config(yscrollcommand=sb_ver.set)
        sb_ver.config(command=logs_entry.yview)
        return logs_entry

    def write_logs(self, logs: str, div=True):
        if div:
            logs = "\n=======================================\n" + logs
        self.logs_text.insert(END, logs)
        self.logs_text.yview(END)
        self.root.update()

    # =======================================
    # | ===========  END LAYOUT =========== |
    # =======================================

    # =======================================
    # | ==============  PIX  ============== |
    # =======================================
    def error(self, text):
        self.lbl_operator_text.set("Aconteceu algum erro na operacao: " + text)

    def configurar(self):
        result = self.e_configurar()
        self.lbl_operator_text.set(result)
        self.root.update()

    def pagamento_enviar(self):
        self.buttons["configs"]["state"] = "disabled"
        self.buttons["btn_enviar"]["state"] = "disabled"
        self.buttons["canc"]["state"] = "active"
        self.running = True
        self.process_thread = Thread(target=self.enviar)
        self.process_thread.start()

    def cancelamento(self):
        self.running = False
        self.buttons["configs"]["state"] = "active"
        self.buttons["btn_enviar"]["state"] = "active"
        self.buttons["canc"]["state"] = "disabled"
        self.lbl_operator_text.set("Cancelled")

    def enviar(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error("Erro ao iniciar")
        if "Sucesso" not in self.e_enviar():
            return self.error("Erro ao enviar")
        if "Sucesso" not in finalizar(""):
            return self.error("Erro ao finalizar")

        self.buttons["btn_enviar"]["state"] = "active"
        self.buttons["configs"]["state"] = "active"
        self.lbl_operator_text.set("Enviar")
        self.root.update()

    def e_configurar(self):
        self.lbl_operator_text.set("configurando produto pos")
        
        load_dotenv()

        PRODUTO = "xml"     # produto de pagamento (atual pos)
        SUB_PRODUTO = os.getenv('SUB_PRODUTO')   # fornecedor/banco/parceiro (atual 1)
        TOKEN = os.getenv('TOKEN')  # token de acesso
        EMAIL = os.getenv('EMAIL')
        PDV = os.getenv('PDV')

        # JSON 
        input_data = {
            "configs": {
                "produto": PRODUTO,                                        
                "sub_produto": SUB_PRODUTO,                                       
                "infos": {
                    "token": TOKEN,
                    "email": EMAIL,
                    "pdv": PDV
                }
            }
        }
        input_json = json.dumps(input_data)
        res = configurar(input_json)

        self.write_logs("CONFIGURAR")
        self.write_logs(res)

        result = obter_valor(res, "mensagem")
        return result

    def e_iniciar(self):
        self.lbl_operator_text.set("iniciando pos")

        OPERACAO = "xml" # produto que será executado (atual pos)

        # JSON
        input_data = {
            "iniciar": {
                "operacao": OPERACAO
            }
        }
        input_json = json.dumps(input_data)
        res = iniciar(input_json)

        self.write_logs("INICIAR")
        self.write_logs(res)

        return res

    def e_enviar(self):
        self.lbl_operator_text.set("pedindo transacao para 1 real")

        OPERACAO    = 'enviar_xml'                      # obtem o qrcode
        CONTENT     = self.xml_texts[0].get("1.0", END).rstrip('\n') # valor sempre em centavos
        PATH        = self.xml_texts[1].get("1.0", END).rstrip('\n') # path do xml
        print("contnet: " + self.xml_texts[0].get("1.0", END).rstrip('\n') + 
              " path: " + self.xml_texts[1].get("1.0", END).rstrip('\n'))

        # JSON 
        if CONTENT and CONTENT != "\n":
            input_data = {
                "processar": {
                    "operacao": OPERACAO,   
                    "conteudo": CONTENT,
                }
            }
        elif PATH and PATH != "\n":
            input_data = {
                "processar": {
                    "operacao": OPERACAO,   
                    "path": PATH,
                }
            }
        else:
            print("Nenhum conteudo ou path informado")
            return "Nenhum conteudo ou path informado"
        input_json = json.dumps(input_data)
        res = processar(input_json)

        self.xml_texts[0].delete("1.0", END)
        self.xml_texts[1].delete("1.0", END)
        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        status_code = obter_valor(res, "resultado.status_code")
        message = obter_valor(res, "mensagem")

        if status_code == "0":
            self.lbl_operator_text.set("Enviado com Sucesso")
            self.root.update()
        else:
            print("error in response ")
            self.lbl_operator_text.set("Ocorreu algum erro ao obter o qrcode")
        return message

    # =======================================
    # | ============  END PIX  ============ |
    # =======================================

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PixApp(Tk())
    app.run()
