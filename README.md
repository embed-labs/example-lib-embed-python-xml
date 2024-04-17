# example-lib-embed-python-xml

Exemplo demonstrativo para o uso da `lib-embed` no envio de XML ao nosso server de armazenamento.

## Instalação

### Requisitos

É necessário ter o Python 3 instalado em sua máquina.

### Clonar

```git
git clone git@github.com:org-dev-embed/example-lib-embed-python-xml.git
```

### Configurações 

Acessar o diretório, modificar o arquivo .env.example, renomeando para .env e colocando os valores passados pelo time de integração

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

```mermaid
graph TD;
    A(1 - embed_configurar) -->B(2 - embed_iniciar);    
    B --> C(3 - embed_processar);
    C --> D{4 - embed_processar};
    D --> |processando|D;
    D --> E(5 - embed_finalizar);
```

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
            "token": "",    // gerado pelo time integração
            "email": "",    // informado pelo parceiro
            "pdv": ""       // informado pelo parceiro
        }
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
"xml;1;token;email;pdv"
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
  "mensagem": "Sucesso"
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

Temos três modalidades de envio de XML que podem ser realizadas:
1. por conteúdo (string)
2. por caminho absoluto (path)
3. por caminho do arquivo compactado (zip)

Estas modalidades podem ser parametrizadas de duas formas

1. Json
```json
// Conteúdo (String)
{
    "processar": {
        "operacao": "enviar_xml",   
        "conteudo": "",     // string do arquivo XML
    }
}
// Caminho absoluto do arquivo (Path)
{
    "processar": {
        "operacao": "enviar_xml",   
        "path": "",         // caminho do arquivo xml
    }
}
// Caminho do arquivo compactado (Zip)
{
    "processar": {
        "operacao": "enviar_xml",   
        "zip": "",          // caminho do arquivo zip
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
// Conteúdo (String)
"enviar_xml;conteudo;string_xml"
// Caminho absoluto do arquivo (Path)
"enviar_xml;path;path_arquivo_xml"
// Caminho do arquivo compactado (Zip)
"enviar_xml;zip;path_zip_xml"
```
###### 3.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
  "codigo": 0,
  "mensagem": "Sucesso"
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
