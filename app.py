from flask import Flask, render_template, request, jsonify

app = Flask('Agenda')

# Lista para armazenar os eventos (simulando um banco de dados)
events = []

# Tela padrão do aplicativo
@app.route('/')
def home():
    return render_template('index.html')

# Tela aonde se encontra o fullcalendar
@app.route('/calendario')
def calendario():
    return render_template('calendario.html', events=events)  # Passa a lista de eventos para o template

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    start_date = request.form.get('startDate')
    description = request.form.get('description')

    # Adiciona o evento à lista de eventos
    event = {
        'title': title,
        'start': start_date,
        'description': description
    }
    events.append(event)

    # Retorna a resposta para o frontend
    return jsonify(event)

@app.route('/get_events', methods=['GET'])
def get_events():
    return jsonify(events)  # Retorna a lista de eventos no formato JSON

if __name__ == '__main__':
    app.run(debug=True)
