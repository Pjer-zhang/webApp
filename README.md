# Web App
一个基于flask的网页应用

##About
get source code：
```
git clone https://github.com/Pjer-zhang/webApp.git
```

##Detail
### Day one
让app跑起来

依赖：
数据库：**MySql**
python：**flask,python-mysql,flask-mysql**


安装方式：

#### _Linux:_
基本环境：
```
sudo apt-get install mysql-client mysql-server python-dev build-essential
```
同时为了能在python里畅通地链接mysql服务还需要：
```
sudo apt-get install mysql-devel python-mysqldb
```
然后是python环境：（安装并创建虚拟环境并激活）
```
sudo apt-get install python-pip
sudo pip install virtualenv
virtualenv --no-site-packages -p /usr/bin/python2.7 ~/.venv/python2.7
. ~/.venv/python2.7/bin/activate
```
在已经激活的python虚拟环境里安装需要的包：
```
pip install flask mysql-python flask-mysql
```

#### _Windows:_
去官网下安装包 -_-|||

#### 测试一下
至此环境该有的已经都有了，测试一下flask能不能用：

新建一个app.py（在刚才pip安装了flask的virtualenv下）
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "<h1>Boya</h1>"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port='5001')
```

然后用浏览器访问 127.0.0.1:5001 可以看到 Boya！的话，说明flask监听在本机localhost（127.0.0.1）的5001端口，并且在访问‘/’根目录的时候正确地返回了一段html代码。
