from flask import Flask, render_template, request, redirect, url_for
 
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        repeat_password = request.form['repeat_password']
       
        if password == '12345' and password == repeat_password:
            return redirect(url_for('register'))
        else:
            return render_template('index.html', error="Wrong password")
   
    return render_template('index.html')

 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            "full_name": request.form['full_name'],
            "nickname": request.form['nickname'],
            "age": request.form['age'],
            "gender": request.form['gender'],
            "phone": request.form['phone'],
            "occupation": request.form['occupation'],
            "birthday": request.form['birthday'],
            "religion": request.form['religion'],
            "nationality": request.form['nationality'],
            "address": request.form['address'],
            "education": request.form['education'],
        }
        return render_template('information.html', user_data=user_data)
   
    return render_template('register.html')
 
if __name__ == '__main__':
    app.run(debug=True)
 