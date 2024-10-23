# Gerador-de-QrCode-Pix-

Este projeto é uma aplicação web simples em Flask que gera QR Codes para pagamentos via PIX. O sistema permite que o usuário forneça um valor e um ID, e a partir dessas informações, gera um payload no formato especificado e cria um QR Code correspondente.

## Funcionalidades

- Geração de payload para pagamentos PIX
- Cálculo do CRC16 para validação do payload
- Criação de QR Code e armazenamento em um diretório específico
- Interface web para visualizar o QR Code gerado

## Tecnologias Utilizadas

- Python
- Flask
- Flask-CORS
- qrcode
- crcmod

## Estrutura do Projeto:

```ph
.
├── pixqrcode.py                # Arquivo principal da aplicação
├── static                # Diretório para arquivos estáticos
│   └── qrcodes           # Diretório para armazenar os QR Codes gerados
└── templates             # Diretório para templates HTML
    └── qrcode.html       # Template para exibir o QR Code
```

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- Python 3.x
- Pip (gerenciador de pacotes Python)

## Instalação
1. Navegue até o diretório do projeto:

```bash
cd Gerador-de-QrCode-Pix-
```

2. Instale as dependências necessárias. Você pode usar o seguinte comando bash para instalar as bibliotecas:

```bash
pip install Flask Flask-CORS qrcode crcmod
```

## Uso
1. Execute a aplicação com o seguinte comando:
   
   ```bash
   python pixqrcode.py
   ```
   O servidor será iniciado no endereço `http://127.0.0.1:5000/`.
   
3. Faça uma requisição POST para o endpoint /gerar_qrcode com um JSON contendo os parâmetros valor e id_usuario. Exemplo usando curl:
   
   ```bash
   curl -X POST http://localhost:5000/gerar_qrcode -H "Content-Type: application/json" -d '{"valor": "100.00", "id_usuario": "123"}'
   ```

4. A resposta será um JSON contendo o payload gerado e a URL do QR Code, como no exemplo abaixo:
   
   ```json
   {
    "payload": "000201...6304XXXX",
    "url_qrcode": "http://localhost:5000/static/qrcodes/pixqrcode_123_20231022123000.png"
   }
   ```


5. Para visualizar o QR Code, você pode acessar a URL retornada na resposta.

```http
http://127.0.0.1:5000/exibir_qrcode/nome_do_arquivo.png
```

Substitua `nome_do_arquivo.png` pelo nome do arquivo retornado na resposta.

