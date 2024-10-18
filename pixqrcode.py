import crcmod
import qrcode
import os
from flask import Flask, request, jsonify, url_for, render_template
from datetime import datetime
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

# Configurações estáticas
nome = 'Smart Park'
chavepix = '9a89ebe2-2969-4a85-98f9-24010cd55644'  # Chave PIX 
cidade = 'Campinas'
txtId = 'EstacionamentoCS'
diretorio = './static/qrcodes'  # Diretório para salvar o QR Code

def gerar_payload(nome, chavepix, valor, cidade, txtId):
    valor_float = float(valor)  # Converter o valor para float
    valor_str = f"{valor_float:.2f}"  # Formatar o valor com 2 casas decimais

    nome_tam = len(nome)
    chavepix_tam = len(chavepix)
    valor_tam = len(valor_str)  
    cidade_tam = len(cidade)
    txtId_tam = len(txtId)

    # Montar partes do payload
    merchantAccount_tam = f'0014BR.GOV.BCB.PIX01{chavepix_tam:02}{chavepix}'
    transactionAmount_tam = f'{valor_tam:02}{valor_str}'
    addDataField_tam = f'05{txtId_tam:02}{txtId}'

    # Formatação do payload
    payloadFormat = '000201'
    merchantAccount = f'26{len(merchantAccount_tam):02}{merchantAccount_tam}'
    merchantCategCode = '52040000'
    transactionCurrency = '5303986'
    transactionAmount = f'54{transactionAmount_tam}'
    countryCode = '5802BR'
    merchantName = f'59{nome_tam:02}{nome}'
    merchantCity = f'60{cidade_tam:02}{cidade}'
    addDataField = f'62{len(addDataField_tam):02}{addDataField_tam}'
    crc16 = '6304'

    # Montar o payload completo
    payload = (
        f'{payloadFormat}'
        f'{merchantAccount}'
        f'{merchantCategCode}'
        f'{transactionCurrency}'
        f'{transactionAmount}'
        f'{countryCode}'
        f'{merchantName}'
        f'{merchantCity}'
        f'{addDataField}'
        f'{crc16}'
    )

    return payload

def gerar_crc16(payload):
    crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
    crc16Code = hex(crc16(str(payload).encode('utf-8')))
    crc16Code_formatado = str(crc16Code).replace('0x', '').upper().zfill(4)
    return f'{payload}{crc16Code_formatado}'

def gerar_qrcode(payload, diretorio, id_usuario):
    # Criar o diretório se não existir
    dir = os.path.expanduser(diretorio)
    os.makedirs(dir, exist_ok=True)

    # Gerar um nome de arquivo único com base no timestamp e id_usuario
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'pixqrcode_{id_usuario}_{timestamp}.png'
    qrcode_img_path = os.path.join(dir, filename)

    # Gerar e salvar o QR Code
    qrcode_img = qrcode.make(payload)
    qrcode_img.save(qrcode_img_path)

    # Substituir barras invertidas por barras normais para garantir a URL correta
    qrcode_img_path = qrcode_img_path.replace("\\", "/")

    return qrcode_img_path

@app.route('/gerar_qrcode', methods=['POST'])
def criar_qrcode():
    valor = request.json.get('valor')  # Obter o valor da requisição
    id_usuario = request.json.get('id_usuario')  # Obter o ID do usuário da requisição

    if valor is None or id_usuario is None:
        return jsonify({"error": "Valor ou ID do usuário não fornecido."}), 400

    # Gerar payload e QR Code
    payload = gerar_payload(nome, chavepix, valor, cidade, txtId)
    payload_completo = gerar_crc16(payload)
    qrcode_path = gerar_qrcode(payload_completo, diretorio, id_usuario)

    # Substituir barras invertidas por barras normais na URL
    qrcode_url = url_for('static', filename=os.path.join('qrcodes', os.path.basename(qrcode_path)).replace("\\", "/"), _external=True)

    # Retornar o payload e a URL da imagem do QR Code
    return jsonify({
        "payload": payload_completo,
        "url_qrcode": qrcode_url
    })

# Rota para exibir a página HTML com o QR Code
@app.route('/exibir_qrcode/<filename>')
def exibir_qrcode(filename):
    # Gera a URL completa da imagem do QR Code
    qrcode_url = url_for('static', filename=os.path.join('qrcodes', filename), _external=True)
    return render_template('qrcode.html', qrcode_url=qrcode_url)

if __name__ == '__main__':
    app.run(debug=True)
