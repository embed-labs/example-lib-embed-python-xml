import os
import dotenv
import embed_lib as lib

STATUS_CODE = "resultado.status_code"

def configurar():
    dotenv.load_dotenv()

    PRODUTO = "xml"                         # produto atual xml
    SUB_PRODUTO = "1"                       # produto atual datalake
    ACCESS_KEY = os.getenv('ACCESS_KEY')    # fonecido pela integração
    SECRET_KEY = os.getenv('SECRET_KEY')    # fonecido pela integração
    ID_PDV = os.getenv('ID_PDV')            # fonecido pela integração
    
    input = f"{PRODUTO};{SUB_PRODUTO};{ACCESS_KEY};{SECRET_KEY};{ID_PDV}"
    output = lib.configurar(input)
    print(f"configurar = {output}")

def iniciar():
    OPERACAO = "xml" # produto para processamento
    output = lib.iniciar(OPERACAO)
    print(f"iniciar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def zip(path_zip):
    OPERACAO = 'enviar_xml' # operação para realizar envio de xml
    TIPO_ENVIO = "zip"      # tipo do envio de xml
    VALOR = path_zip        # conteudo/path para envio

    input = f"{OPERACAO};{TIPO_ENVIO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def rar(path_rar):
    OPERACAO = 'enviar_xml' # operação para realizar envio de xml
    TIPO_ENVIO = "rar"      # tipo do envio de xml
    VALOR = path_rar        # conteudo/path para envio

    input = f"{OPERACAO};{TIPO_ENVIO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def path(path_file):
    OPERACAO = 'enviar_xml' # operação para realizar envio de xml
    TIPO_ENVIO = "path"     # tipo do envio de xml
    VALOR = path_file       # conteudo/path para envio

    input = f"{OPERACAO};{TIPO_ENVIO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result
    
def xml(content):
    OPERACAO = 'enviar_xml' # operação para realizar envio de xml
    TIPO_ENVIO = "xml"      # tipo do envio de xml
    VALOR = content         # conteudo/path para envio

    input = f"{OPERACAO};{TIPO_ENVIO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def status():
    OPERACAO = 'get_status' # obtem o status do pagamento
    output = lib.processar(OPERACAO)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def finalizar():
    OPERACAO = '' # finaliza a API
    output = lib.finalizar(OPERACAO)
    print(f"finalizar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result