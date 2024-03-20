# python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# imports

import os
import json
import shutil
import warnings
from threading import Thread
from dotenv import load_dotenv
from libembed import configurar, iniciar, processar, finalizar, obter_valor
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
COLOR_BG_FRAME = "#000000"  # Dark purple
COLOR_BG_LABEL = "#000000"  # Dark purple
COLOR_FG_LABEL = "#80ff80"  # White
COLOR_BG_ENTRY = "#000000"  # Dark gray
COLOR_BG_BUTTON = "#80ff80"  # Light purple
COLOR_FG_BUTTON = "#000000"  # White
COLOR_BG_BUTTON_DISABLED = "#80ff80"
COLOR_FG_BUTTON_DISABLED = "#666666"

# =========================================
# | =========  PÁGINA PRINCIPAL ========= |
# =========================================


class XmlApp:
    # =========================================
    # | ===========  BEGIN LAYOUT =========== |
    # =========================================
    def __init__(self, root):
        self.root = root
        self.root.title("Demo XML")
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
        self.buttons["btn_cancel"]["state"] = "disabled"

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
            text="XML",
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
        lbl_content.grid(column=0, row=2, sticky=W, pady=(5, 5))

        lbl_path = Label(
            self.value_frame,
            text="Caminho Completo do XML",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_path.grid(column=0, row=3, sticky=W, pady=(5, 5))

        lbl_zip = Label(
            self.value_frame,
            text="Caminho Completo do ZIP (1 MB)",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_zip.grid(column=0, row=4, sticky=W, pady=(5, 5))

        lbl_loop = Label(
            self.value_frame,
            text="Diretorio para Envio (Loop)",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_loop.grid(column=0, row=5, sticky=W, pady=(5, 5))

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

        btns["btn_config"] = Button(
            self.value_frame,
            text="Configurar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.configurar,
        )
        btns["btn_config"].grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_enviar"] = Button(
            self.value_frame,
            text="Enviar XML",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento_enviar,
        )
        btns["btn_enviar"].grid(column=0, row=6, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        btns["btn_cancel"] = Button(
            self.operator_frame,
            text="Cancelar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.cancelamento,
        )
        btns["btn_cancel"].grid(column=1, row=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        return btns

    def create_xmls_text(self):
        self.xml_content = StringVar()
        entry_content = Text(
            self.value_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
            height=2,
        )
        entry_content.grid(column=1, row=2, sticky=NS, padx=10, pady=10)
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
        entry_path.grid(column=1, row=3, sticky=NS, padx=10, pady=10)
        entry_path.insert(END, "")

        self.xml_zip = StringVar()
        entry_zip = Text(
            self.value_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
            height=2
        )
        entry_zip.grid(column=1, row=4, sticky=NS, padx=10, pady=10)
        entry_zip.insert(END, "")

        self.xml_loop = StringVar()
        entry_loop = Text(
            self.value_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
            height=2
        )
        entry_loop.grid(column=1, row=5, sticky=NS, padx=10, pady=10)
        entry_loop.insert(END, "")

        return [entry_content, entry_path, entry_zip, entry_loop]

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
    # | ==============  XML  ============== |
    # =======================================
    def error(self, text):
        self.lbl_operator_text.set("Aconteceu algum erro na operacao: " + text)

    def configurar(self):
        result = self.e_configurar()
        self.lbl_operator_text.set(result)
        self.root.update()

    def pagamento_enviar(self):
        self.buttons["btn_config"]["state"] = "disabled"
        self.buttons["btn_enviar"]["state"] = "active"
        self.buttons["btn_cancel"]["state"] = "active"
        self.running = True
        self.process_thread = Thread(target=self.enviar)
        self.process_thread.start()

    def cancelamento(self):
        self.running = False
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_enviar"]["state"] = "active"
        self.buttons["btn_cancel"]["state"] = "active"
        self.lbl_operator_text.set("Cancelado")

    def enviar(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error("Erro ao iniciar")
        if "Sucesso" not in self.e_enviar():
            return self.error("Erro ao enviar")
        if "Sucesso" not in finalizar(""):
            return self.error("Erro ao finalizar")

        self.buttons["btn_enviar"]["state"] = "active"
        self.buttons["btn_config"]["state"] = "active"
        self.lbl_operator_text.set("Enviar")
        self.root.update()

    def e_configurar(self):
        self.lbl_operator_text.set("configurando produto xml")
        
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
        self.lbl_operator_text.set("iniciando XML")

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
        self.lbl_operator_text.set("enviando XML ao server")

        OPERACAO    = 'enviar_xml'                      
        CONTENT     = self.xml_texts[0].get("1.0", END).rstrip('\n') 
        PATH        = self.xml_texts[1].get("1.0", END).rstrip('\n')
        ZIP         = self.xml_texts[2].get("1.0", END).rstrip('\n') 
        LOOP        = self.xml_texts[3].get("1.0", END).rstrip('\n') 
        print("contnet: " + self.xml_texts[0].get("1.0", END).rstrip('\n') + 
              " path: " + self.xml_texts[1].get("1.0", END).rstrip('\n') + 
              " zip: " + self.xml_texts[2].get("1.0", END).rstrip('\n')) 


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
        elif ZIP and ZIP != "\n":
            input_data = {
                "processar": {
                    "operacao": OPERACAO,   
                    "zip": ZIP,
                }
            }
        elif LOOP and LOOP != "\n":
            return self.e_enviar_loop()
        else:
            print("Nenhum conteudo ou path informado")
            return "Nenhum conteudo ou path informado"
        input_json = json.dumps(input_data)
        res = processar(input_json)

        self.xml_texts[0].delete("1.0", END)
        self.xml_texts[1].delete("1.0", END)
        self.xml_texts[2].delete("1.0", END)
        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        message = obter_valor(res, "mensagem")
        status_code = obter_valor(res, "resultado.status_code")
        if status_code == "0":
            self.lbl_operator_text.set("Enviado com Sucesso")
            self.root.update()
        else:
            print("error in response ")
            self.lbl_operator_text.set("Ocorreu algum erro ao enviar XML")
        
        return message
    
    
    def e_enviar_loop(self): 
        diretorio   = self.xml_texts[3].get("1.0", END).rstrip('\n')
         # Itera sobre os arquivos no diretório
        for filename in os.listdir(diretorio):
            self.lbl_operator_text.set("enviando arquivo " + filename)
            filepath = os.path.join(diretorio, filename)
            # Verifica se é um arquivo XML
            if os.path.isfile(filepath) and filename.lower().endswith('.xml'):
                OPERACAO    = 'enviar_xml'    
                PATH        = filepath
                
                input_data = {
                        "processar": {
                        "operacao": OPERACAO,   
                        "path": PATH,
                    }
                }

                input_json = json.dumps(input_data)
                res = processar(input_json)

                self.write_logs("PROCESSAR")
                self.write_logs(res)
                
                message = obter_valor(res, "mensagem")
                status_code = obter_valor(res, "resultado.status_code")
                if status_code == "0":
                    self.lbl_operator_text.set("Enviado com Sucesso")
                    self.root.update()
                else:
                    self.lbl_operator_text.set("erro com arquivo " + filename)
                    shutil.move(filepath, "xmls/errors")

        self.xml_texts[3].delete("1.0", END)
        return message

    # =======================================
    # | ============  END Xml  ============ |
    # =======================================

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = XmlApp(Tk())
    app.run()
