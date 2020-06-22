from flask import Flask
from flask import request
import pymysql
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "<h1>Home</h1><a href='http://10.17.18.101:10045/signin'>sign in</a>"

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
            <h2>Docker</h2>
            <p><input name="username" type="text"></p>
            <p><input name="password" type="password"></p>
            <p><input type="submit" value="Sign In"></p>
            </form>
            '''


@app.route('/signin', methods=['POST'])
def signin():
    username=request.form['username']
    password=request.form['password']
    db = pymysql.connect(host='172.17.0.3', port=8004, user='root', passwd='123', db='docker', charset='utf8')
    cursor = db.cursor()
    sql = " select * from user where username = '"+username+"' "
    cursor.execute(sql)
    data = cursor.fetchone()
    if data[1]!=password:
        return '<h3>Bad username or password!</h3>'
    if data[2] =='admin' :
        s = "?username=" + username + "&password=" + password
        return '''
        <h3>Welcome admin!</h3>
               <a href='http://10.17.18.101:10046/'''+s+'''''>进入后台界面</a>
        '''
    if data[2] =='user':
        s="?username="+username+"&password="+password
        return        '''
        <h3>Welcome user!</h3>
               <a href='http://10.17.18.101:10047/'''+s+''''>管理自己的容器</a>
        '''

    return '<h3>未知错误</h3>'


if __name__ == '__main__':

    app.run(host = '0.0.0.0',
    port = 8005,
    debug = True)