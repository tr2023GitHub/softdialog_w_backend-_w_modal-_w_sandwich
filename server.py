import smtplib, threading
from flask import Flask, render_template, request, session, g , url_for, redirect, jsonify
import sqlite3
import Base
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# создаем приложение/Объекта Flask
app = Flask(__name__)
# настройки приложения
app.config['DATABASE'] = "static/bd/softOffers.db"
app.secret_key = "asdf1234"             # ключ для кеширования, для Flask он обязан быть

def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row         # выведит в виде словарика, а не картежей
    return con
   

# проверка уже есть подключение БД в этом приложение, g отвечает за взаимодействия контекста данного приложения;
# пользователи работают с контекстом(копия) прлиложения ; если нет подключения g=0
def get_connect():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

navMenu = [
    {"link": "/main_list", "name": "Каталог решений"},
    {"link": "/company", "name": "Компания"},
    {"link": "/partners", "name": "Наши партнеры"}
]

@app.route("/main_list",methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def main_list(): 
    con = get_connect()
    # base = Base.ProductDB(con)
    cursor = con.cursor()

     # Получаем все уникальные значения name_class для фильтра
    cursor.execute('SELECT DISTINCT  name_class, id FROM class')
    classes = cursor.fetchall()

    # selected_classes = request.form.getlist('class_filter')
    # clear_filter = 'clear_filter' in request.form

    # Получаем все уникальные значения industry.name_ind для фильтра
    cursor.execute('SELECT DISTINCT  name_ind, id FROM industry')
    industries = cursor.fetchall()

    # selected_industries = request.form.getlist('ind_filter')
    # clear_filter = 'clear_filter' in request.form

    # Получаем сохраненные значения фильтров из сессии
    selected_classes = session.get('selected_classes', [])
    selected_industries = session.get('selected_industries', [])
    # clear_filter = 'clear_filter' in request.form

    # # Сбрасываем фильтры только при первом входе на страницу "/main_list"
    # if request.path == "/main_list" and not request.args:
    #     selected_classes = []
    #     selected_industries = []
    # Проверяем, был ли это первый запрос на страницу или переход между страницами
    if not request.referrer or request.referrer.endswith("/main_list"):
        # Сбрасываем фильтры только при первом входе на страницу "/main_list"
        selected_classes = []
        selected_industries = []


    # Обработка POST-запроса
    if request.method == 'POST':
    # Если выбран чекбокс "Clear All", сбрасываем все фильтры
        if 'clear_filter' in request.form:
            selected_classes = []
            selected_industries = []
        else:
            selected_classes = request.form.getlist('class_filter')
            selected_industries = request.form.getlist('ind_filter')
   
    # Если выбраны классы, фильтруем данные
    if selected_classes:
        placeholders = ', '.join(['?'] * len(selected_classes))
        query = f'SELECT * FROM class WHERE name_class IN ({placeholders})'
        cursor.execute(query, selected_classes)
        data = cursor.fetchall()
    else:
        # Если ничего не выбрано, отображаем все данные
        cursor.execute('SELECT * FROM class')
        data = cursor.fetchall()
    
    # Если выбраны отрасли, фильтруем данные
    if selected_industries:
        placeholders = ', '.join(['?'] * len(selected_industries))
        query = f'SELECT * FROM industry WHERE name_ind IN ({placeholders})'
        cursor.execute(query, selected_industries)
        data_ind = cursor.fetchall()
    else:
        # Если ничего не выбрано, отображаем все данные
        cursor.execute('SELECT * FROM industry')
        data_ind = cursor.fetchall()

    # Сохраняем выбранные значения фильтров в сессии
    session['selected_classes'] = selected_classes
    session['selected_industries'] = selected_industries

    # con.close()

    # return render_template('main_list.html', classes=classes, data=data, selected_classes=selected_classes)
    base = Base.ProductDB(con)
    return render_template("main_list.html", menu=navMenu, cards = base.getAllProduct(), classes=classes, data=data, selected_classes=selected_classes,
                           industries = industries, data_ind = data_ind, selected_industries = selected_industries)
 # от render_template получаем шаблон и выводим в браузере; передаем аргумент файл html и что надо в шаблон подставить
    
  
@app.route("/company")
def company():
    con = get_connect()
    base = Base.ProductDB(con)
    return render_template("company.html", menu=navMenu, cards = base.getAllProduct())

@app.route("/partners")
def partners():
    return render_template("partners.html", menu=navMenu)

@app.route("/card/<int:value>")
def prod(value):
    con = get_connect()
    base = Base.ProductDB(con)
    product = base.getProduct(value)
    max_dsc = "/static/files/test_dsc"+str(product["id"])+".html"

    # nav_value = request.args.get('nav_value', 'description')
    
    #создать шаблон и вызвать его тут
    # return render_template("card.html", menu=navMenu, name = product["name"], des = product["description"], 
    #                        img=product["img"], price=product["price"], trip=product["trip"], img1=product["img1"], img2=product["img2"])
    return render_template("card.html", menu=navMenu, name_soft=product["name_soft"], class_soft=product["name_class"],ind_soft=product["name_ind"],
                           min_dsc=product["min_description"],max_dsc=max_dsc, logo_com=product["logo"], site_com=product["site"],
                           offer_id = product["id"])


@app.route('/question')
def show_question_form():
    return render_template("question.html")
@app.route('/send_email', methods=['POST'])
def send_email():
    print("Запрос получен на /send_email")
    name = request.form.get('name')
    email = request.form.get('email')
    comment = request.form.get('comment')
    agreement = request.form.get('agreement')

    if not name or not email or not agreement:
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Все обязательные поля должны быть заполнены.'}), 400

    # Формируем email
    msg = MIMEText(f"""
    Имя: {name}<br>
    Email: {email}<br><br>
    <hr>
    Вопрос: {comment}
    """, 'html')
    msg['Subject'] = 'Новый вопрос с сайта'
    msg['From'] = 't.reva@scadasystems.ru' # Устанавливаем адрес отправителя равным адресу аутентификации
    msg['Reply-To'] = email
    msg['To'] = 't.reva@scadasystems.ru'

    try:
        # Настройки SMTP
        smtp_server = 'smtp.mail.ru'
        smtp_port = 465
        smtp_username = 't.reva@scadasystems.ru'
        smtp_password = 'hf324gyLLdRbadSFKSTf'

        # Отправка email
        print("Инициализация SMTP...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        print("Логин в SMTP...")
        server.login(smtp_username, smtp_password)
        
        print("Отправка письма...")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        
        print("Закрытие SMTP соединения...")
        server.quit()

        print("Email успешно отправлен")


        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")  # Выводим ошибку в консоль
        return jsonify({'status': 'error', 'message': str(e)}), 500

# разрыв подключения
@app.teardown_appcontext 
def close_connect(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
    

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run()