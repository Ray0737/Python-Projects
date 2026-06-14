from flask import Flask, render_template as rt, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')

        if username == 'cappu' and password == '12345':
            return rt('successful.html', username=username)
        else:
            return rt('login.html', error='เข้าสู่ระบบไม่สำเร็จ')
    return rt('login.html')

if __name__ == '__main__':
    app.run(debug=True)
