from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')

        if username == 'cappu' and password == '12345':
            return render_template('final.html')
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
