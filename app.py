from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from bs4 import BeautifulSoup
##################fetching data from Gfinance

def get_stock_dataN(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:INDEXNSE"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='').text
    
    return [stock_name,stock_price,symbol]
  
def get_stock_dataNB(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:NSE"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
 
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='').text
    
    return [stock_name,stock_price,symbol]

def get_stock_dataB(symbol):
    url = f"https://www.google.com/finance/quote/{symbol}:INDEXBOM"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
 
    stock_name = soup.find('div', class_='zzDege').text
    stock_price = soup.find('div', class_='YMlKec fxKbKc').text
    #proloss = soup.find('div', class_='P2Luy Ebnabc ZYVHBb').text
    #stock_profit = soup.find('div', class_='JwB6zf').text
    #print(f"{stock_name} ({symbol}): {stock_price}")    
    return [stock_name,stock_price,symbol]
 

#####################end of data fetch functionfrom flask_mail import Mail, Message
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')
@app.route('/appdata', methods = ['POST'])
def 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        nifty = get_stock_dataN('NIFTY_50')
        sensex =  get_stock_dataB('SENSEX')
        sbi = get_stock_dataN('NIFTY_BANK')
        hdfc = get_stock_dataN('NIFTY_IT')
        data = [nifty,sensex,sbi,hdfc]
        return render_template('home.html', username=session['username'],data = data)
    
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/stats')
def stockDashboard():
    if 'user_id' in session:
        return render_template('stockDashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/compare')
def compareDashboard():
    if 'user_id' in session:
        return render_template('compareDashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/filter')
def filterDashboard():
    if 'user_id' in session:
        return render_template('filterDashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/sendMail', methods=['POST'])
def send_mail():
    email = request.form.get('email')

    response_message = 'Thanks for subscribing!'

    return jsonify(message=response_message)



if __name__ == '__main__':
    app.run(debug=True)
