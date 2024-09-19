![embed](https://github.com/user-attachments/assets/17888b6f-4cd6-4972-8a7b-e610fb67ec35)

Exemplo demonstrativo para o uso da `lib-embed` no envio de XML ao nosso server de armazenamento.

## Instalação

### Requisitos

É necessário ter o Python 3 instalado em sua máquina.

#### Dependências 
- python3-tk
- python3-pip
- Pillow (via pip)
- python-dotenv (via pip)

### Clonar

```git
git clone git@github.com:embed-labs/example-lib-embed-python-xml.git
```

### Configurações 

Acessar o diretório, modificar o arquivo .env.example, renomeando para .env e adicionando os valores passados pelo time de integração

```
cd example-lib-embed-python-xml
mv .env.example .env
```

Feito isso, executar o programa com python

```
python3 embed_example.py
```

## API

### Fluxo
Vamos definir o fluxo que deve ser seguido para que sua implementação seja realizada 
seguindo as melhores práticas no uso da nossa API

![geral](https://github.com/user-attachments/assets/b9b10d61-34a8-4fa0-bb64-8c26ee08bc74)
![xml-string](https://github.com/user-attachments/assets/946c9922-3e2f-477b-9447-779ab76c3c32)
![xml-path](https://github.com/user-attachments/assets/9c400fbb-bb41-4afb-b0db-341f3df9270f)
![xml-zip](https://github.com/user-attachments/assets/cec42bb3-09cf-403a-9b1e-10ea4e33fb57)
![xml-rar](https://github.com/user-attachments/assets/060a6068-bcd9-40a3-bd48-7c7bdd7f2586)

### Métodos

#### 1. Configurar 

Este método realiza a configuração do produto, para este caso XML

##### 1.1. Assinatura

```c++
char* embed_configurar(char* input);
```

##### 1.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 1.2.1. Input

Pode ser parametrizado de duas maneiras:

1. Json
```json
{
    "configs": {
        "produto": "xml",                                        
        "sub_produto": "1",                                       
        "infos": {
            "access_key": "",   // gerado pelo time integração
            "secret_key": "",   // gerado pelo time integração
            "id_pdv": ""        // gerado pelo time integração
        }
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
"xml;1;access_key;secret_key;id_pdv"
```

###### 1.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
  "codigo": 0,
  "mensagem": "Sucesso"
}
```

#### 2. Iniciar

Este método realiza a inicialização do produto, para este caso XML

##### 2.1. Assinatura

```c++
char* embed_iniciar(char* input);
```

##### 2.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 2.2.1. Input

Pode ser parametrizado de duas maneiras:

1. Json
```json
{
    "iniciar": {
        "operacao": "xml"
    }
}
```
2. Metaparâmetro
```c
"xml"
```

###### 2.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 0,
        "status_message": "iniciado"
    }
}
```

#### 3. Processar

Este método realiza o processamento de envio para o XML

Estes XMLs podem ser dos seguintes tipos:
1. NFC-e
2. NF-e
3. S@T

##### 3.1. Assinatura

```c++
char* embed_processar(char* input);
```

##### 3.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 3.2.1. Input

Temos quatro modalidades de envio de XML que podem ser realizadas e uma para consultar status do envio:
1. por conteúdo xml (string)
2. por caminho absoluto (path)
3. por caminho do arquivo compactado zip
4. por caminho do arquivo compactado rar
5. consultar status do arquivo ou conteudo enviado

Estas modalidades podem ser parametrizadas de duas formas

1. Json
```json
// Conteúdo XML (String)
{
    "processar": {
        "operacao": "enviar_xml",   
        "xml": "",  // string do arquivo xml
    }
}
// Caminho absoluto do arquivo (Path)
{
    "processar": {
        "operacao": "enviar_xml",   
        "path": "", // caminho do arquivo xml
    }
}
// Caminho do arquivo compactado (Zip)
{
    "processar": {
        "operacao": "enviar_xml",   
        "zip": "",  // caminho do arquivo zip
    }
}
// Caminho do arquivo compactado (Rar)
{
    "processar": {
        "operacao": "enviar_xml",   
        "rar": "",  // caminho do arquivo rar
    }
}
// Consultar status do envio atual
{
    "processar": {
        "operacao": "get_status",   
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
// Conteúdo XML (String)
"enviar_xml;xml;string_xml"
// Caminho absoluto do arquivo (Path)
"enviar_xml;path;path_arquivo_xml"
// Caminho do arquivo compactado (Zip)
"enviar_xml;zip;path_zip_xml"
// Caminho do arquivo compactado (Rar)
"enviar_xml;rar;path_rar_xml"
// Consultar status do envio atual
"get_status"
```

###### 3.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 1,
        "status_message": "processando"
    }
}
```

#### 4. Obter Valor

Este método responsável por buscar um valor contido em uma chave ou objeto de um json válido. 

##### 4.1. Assinatura

```c++
char* embed_obter_valor(char* json, char* key);
```

##### 4.2. Parâmetros

Aqui estão as definições para os _inputs_ e _output_ para este método.

###### 4.2.1. Input

Deve ser informado sempre um String com conteúdo Json.

```json
// Json
{
    "key1": "value1",
    "key2": {
        "key21": "value21",
        "key22": "value22",
        "key23": "value23",
        "key24": "value24",
        "key25": "value25"
    }
}
```
```c
// Key
"key2.key25"
```

###### 4.2.2. Output

Será um String com valor informado em _key_ se conter em _json_ 

```c
// Value
"value25"
```

### Retornos

Os possíveis retornos para estes métodos são:

| codigo | mensagem |
| --- | ----------- |
| 0 | Sucesso |
| -1 | Erro |
| -2 | Deserialize |
| -3 | ProviderError |
| -41 | XmlError |
| -42 | XmlMissingParameter |
| -43 | XmlInvalidOperation |
| -44 | XmlInputBadFormat |

| status_code | status_message |
| - | - |
| -1 | erro |
| 0 | iniciado & finalizado |
| 1 | processando |
