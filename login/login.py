from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
            <p><input name="username" type="text"></p>
            <p><input name="password" type="password"></p>
            <p><input type="submit" value="Sign In"></p>
            </form>
            '''


@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username'] =='admin' and request.form['password'] =='1':
        return '''
        <h3>Welcome admin!</h3>
               <a href='http://10.17.18.101:10046/'>进入管理界面</a>
        '''
    if request.form['username'] =='a' and request.form['password'] =='1':
        s="?username="+request.form['username']+"&password="+request.form['password']
        return        '''
        <h3>Welcome user!</h3>
               <a href='http://10.17.18.101:10047/'''+s+''''>管理自己的容器</a>
        '''

    return '<h3>Bad username or password!</h3>'


if __name__ == '__main__':

    app.run(host = '0.0.0.0',
    port = 8005,
    debug = True)