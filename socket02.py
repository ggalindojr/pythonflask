from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO, send, emit
import requests
import time
import mybd

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('projteste/flask02.html')

# Selcionar dados e carregar página
@app.route('/dash') 
def dash():
    dados = mybd.select('*', 'testedev')
    return render_template('projteste/dash.html', nomes=dados)

# Inserir dados no banco
@app.route('/salva', methods=['POST'])
def salva():
    desc = request.form['descricao']
    desc2 = request.form['descricao2']
    values = [ "DEFAULT,'" + desc + "','" + desc2 + "'" ]
    mybd.insert(values, 'testedev')
    return redirect(url_for('dash'))

# Alterar dados no banco
@app.route('/atualiza', methods=['POST'])
def atualiza():
    idt = request.form['idtestedev']
    desc = request.form['descricao']
    desc2 = request.form['descricao2']
    values = { "descricao": desc, "descricao2": desc2 }
    mybd.update(values, "testedev", "idtestedev = " + idt)
    return redirect(url_for('dash'))

# Deletar dados no banco
@app.route('/deleta/<string:idt>', methods=['GET'])
def deleta(idt):
    mybd.delete("testedev", "idtestedev = " + idt)
    return redirect(url_for('dash'))

# Recebe dados enviados da página flask02
@socketio.on('messageC')
def messageC(data):
    print(data, '{}'.format(time.ctime()))
    send_messageS()

# Envia dados para a página flask02
def send_messageS():
    socketio.emit('messageS', 12)

# Recebe dados enviados da página Dash
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json)

if __name__ == '__main__':
    socketio.run(app, host="localhost", port="80")
