from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def root():
    return "hello world"

@app.route('/login')
def login():
    return 'login page'

@app.route('/logout')
def logout():
    return 'logout_page'

app.run()