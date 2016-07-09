# Web App
[![Build Status](https://travis-ci.org/Pjer-zhang/webApp.svg?branch=master)](https://travis-ci.org/Pjer-zhang/webApp)


一个基于flask的网页应用

##About
get source code：
```
git clone https://github.com/Pjer-zhang/webApp.git
```
内容：使用flask作为框架，mysql数据库来存储用户信息数据的一个换物平台

##Detail
### Day 1
**让app跑起来**

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

### Day 2
**database**
添加数据库和相应的接口，这里数据库使用MySql，安装过mysql之后为了能在python的flask环境中调用需要添加flask-mysql支持，
```python
from flask.ext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
```

同时为了能在数据库中插入和使用中文还要有这样一个声明：
```python
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
```
完成了必要的import之后可以开始在数据库端初始化数据库了：数据库端建表，一些基础的SQL建表语句：
```sql
use users;
CREATE TABLE `users`.`ring_users` (
  `user_id` BIGINT UNIQUE not NULL AUTO_INCREMENT,
  `user_name` VARCHAR(200) UNIQUE NULL,
  `user_username` VARCHAR(200) UNIQUE NULL,
  `user_password` VARCHAR(200) NULL,
  PRIMARY KEY (`user_id`));
```
建立相对严谨的关系数据库，设定严格不冲突的逻辑主键，详细内容视情况而定。总之这部分需要花点心思，逻辑上严谨而少冗余的数据库对于整个应用有重大意义

然后是应用端的初始化
```python
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'i wont tell you'
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'client'
app.config['MYSQL_DATABASE_PASSWORD'] = 'passwd'
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_CHARSET'] =  'utf8'
mysql.init_app(app)
```
一个sql数据库query的小tip是尽量少用select * ... 只请求需要的数据列，安全且高效