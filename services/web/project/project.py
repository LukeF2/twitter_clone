from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
     
    return 'logout_page'

app.run(port=1147)