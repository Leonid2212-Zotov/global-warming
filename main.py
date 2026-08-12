#Импорт
from flask import Flask, redirect, render_template, request, session, url_for



app = Flask(__name__)
QUESTIONS = [
    {
        'question': 'Какой язык используется для Flask?',
        'options': ['Java', 'Python', 'C++'],
        'answer': 1,
    },
    {
        'question': 'Что такое Flask?',
        'options': ['Фреймворк', 'База данных', 'Операционная система'],
        'answer': 0,
    },
]
def result_calculate(size, lights, device):
    #Переменные для энергозатратности приборов
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5
    return size * home_coef + lights * light_coef + device * devices_coef

#Первая страница
@app.route('/')
def index():
    return render_template('index.html')
#Вторая страница
@app.route('/<size>')
def lights(size):
    return render_template(
                            'lights.html',
                            size=size
                           )

#Третья страница
@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
                            'electronics.html',
                            size = size,
                            lights = lights
                           )

#Расчет
@app.route('/<size>/<lights>/<device>')
def end(size, lights, device):
    return render_template('end.html',
                            result=result_calculate(int(size),
                                                    int(lights),
                                                    int(device)
                                                    )
                        )
#Форма
@app.route('/form')
def form():
    return render_template('form.html')

#Результаты формы
@app.route('/submit', methods=['POST'])
def submit_form():
    #Создай переменные для сбора информации
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    address = request.form['address']
    # здесь вы можете сохранить данные или отправить их по электронной почте
    return render_template('form_result.html',
                           #Помести переменные
                           name=name,
                           email=email,
                           date=date,
                           address=address
                           )
@app.route('/global_warming')
def global_warming():
    return render_template('global_warming.html')
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
  if 'score' not in session or 'index' not in session:
    session['score'] = 0
    session['index'] = 0

  if request.method == 'POST':
    selected = int(request.form.get('answer'))
    current_index = session['index']

    if selected == QUESTIONS[current_index]['answer']:
      session['score'] += 1

    session['index'] += 1
    return redirect(url_for('quiz'))

  index = session['index']
  if index < len(QUESTIONS):
    q_data = QUESTIONS[index]
    return render_template(
        'quiz.html', question=q_data['question'], options=q_data['options']
    )
  else:
    score = session['score']
    total = len(QUESTIONS)
    session.clear()
    return render_template('result.html', score=score, total=total)
app.run(debug=True)
