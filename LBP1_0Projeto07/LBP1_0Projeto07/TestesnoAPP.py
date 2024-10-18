from flask import Blueprint, render_template, request, session, redirect, url_for, make_response,Flask
from model.model import usuarios

app = Flask(__name__)


# Area dos Cookies
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie has been set!")
    resp.set_cookie('username', 'Cazz', max_age=60*60*24)

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
     return f'The username is {username}'
    else:
        return 'No cookie found!'
    
@app.route('/delete_cookie')
def delete_cookie():
    resp = make_response("Cookie has been deleted!")
    resp.set_cookie('username', '', expires=0)
    return resp

if __name__ == "__main__":
    app.run(debug=True)
