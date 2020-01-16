# #主业务逻辑中的视图和路由的定义
# import datetime
# import os
#
import datetime
import os
import json
from flask import render_template, request, session, redirect, url_for
# #导入蓝图程序，用于构建路由
from . import main
# #导入db，用于操作数据库
from .. import db
# #导入实体类，用于操作数据库
from ..models import *

APP_ROOT = os.path.dirname(os.path.dirname(__file__))

@main.route('/login',methods=['GET','POST'])
def login_views():
  if request.method == 'GET':
      return render_template('login.html')
  else:
      username = request.form.get('username')
      password = request.form.get('password')
      email = request.form.get('e-mail')
      phone = request.form.get('phone')
    # #使用接收的用户名和密码到数据库中查询
      user = Users.query.filter_by(username=username,password=password,email=email,phone=phone).first()
    # #如果用户存在，将信息保存进session并重定向回首页，否则重定向回登录页
      if user:
          session['uid'] = user.id
          session['username'] = user.username
          
          return redirect('/')
      else:
          errMsg = "登陆信息不正确"
          return render_template('login.html',errMsg=errMsg)
@main.route('/logout')
def logout_views():
    if 'uid' in session and 'username' in session:
        del session['uid']
        del session['username']
    return redirect('/')
#　注册页面的访问路径
@main.route('/register',methods=['GET','POST'])
def register_views():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    # 获取文本框的值并赋值给user实体对象
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('e-mail')
    phone = request.form.get('phone')
    user = Users(username, password, email, phone)

    # 将数据保存进数据库　-　注册
    db.session.add(user)
    # 手动提交，目的是为了获取提交后的user的id
    db.session.commit()

    # 完成登录的操作
    session['uid'] = user.id
    session['username'] = user.username
    return redirect('/')

@main.route('/',methods=['GET','POST'])
def index_views():
    Topic_tp=[]
    num = 3
    dic = dict()

    categories = Category.query.all()
    topics = Topic.query.filter(Topic.category_id>2).all()
    top_topic = Topic.query.filter(Topic.category_id==3).limit(3).all()
    topic_date = Topic.query.order_by('pub_date desc').limit(5).all()
    topic_num = Topic.query.order_by('read_num desc').limit(5).all()
    while True:
        if num<7:
            topic_tp = Topic.query.order_by('id desc').filter(Topic.category_id==num).limit(1).all()
            num+=1
            Topic_tp +=topic_tp
        else:
            break
    for topic in topics:
        with open(os.path.join(APP_ROOT,'static',topic.content),'rb') as f:
            file = f.read().decode()
            dic[topic.id] = file
            # print(dic[topic.id])

    # for mtopic in topic_date:
    #     with open(os.path.join(APP_ROOT,'static',mtopic.content),'rb') as f:
    #
    #         mfile = f.readline().decode()
    #         mdic[mtopic.id] = mfile

    # for ntopic in topic_num:
    #     with open(os.path.join(APP_ROOT, 'static', ntopic.content), 'rb') as f:
    #         nfile = f.readline().decode()
    #         ndic[ntopic.id] = nfile

    if 'uid' in session and 'username' in session:
        user = Users.query.filter_by(id=session.get('uid')).first()
    return render_template('index.html',params=locals())


@main.route('/about')
def about_views():
    num = 3
    Topic_tp = []
    while True:
        if num<7:
            topic_tp = Topic.query.order_by('id desc').filter(Topic.category_id==num).limit(1).all()
            num+=1
            Topic_tp +=topic_tp
        else:
            break
    # r = url_for('main.index_views')
    # (r)
    if 'uid' in session and 'username' in session:
        user = Users.query.filter_by(id=session.get('uid')).first()
    return render_template('about.html',params = locals())


@main.route('/fengmian')
def fengmian_views():
    # mdic = {}
    # ndic = {}
    Topic_tp = []
    categories = Category.query.filter().all()
    topics = Topic.query.all()
    num = 3
    num1 = 3
    t=()
    while True:
        topics_group = Topic.query.filter(Topic.category_id==num).limit(3).all()
        num+=1
        # t+=(topics_group,)
        if topics_group !=[]:
            t += (topics_group,)
        else:
            break
    while True:
        if num1<7:
            topic_tp = Topic.query.order_by('id desc').filter(Topic.category_id==num1).limit(1).all()
            num1+=1
            Topic_tp +=topic_tp
        else:
            break

    topic_date = Topic.query.order_by('pub_date desc').limit(5).all()
    topic_num = Topic.query.order_by('read_num desc').limit(5).all()

    # for mtopic in topic_date:
    #     with open(os.path.join(APP_ROOT,'static',mtopic.content),'rb') as f:
    #
    #         mfile = f.readline().decode()
    #         mdic[mtopic.id] = mfile
    #
    # for ntopic in topic_num:
    #     with open(os.path.join(APP_ROOT, 'static', ntopic.content), 'rb') as f:
    #         nfile = f.readline().decode()
    #         ndic[ntopic.id] = nfile
    if 'uid' in session and 'username' in session:
        user = Users.query.filter_by(id=session.get('uid')).first()
    return render_template('fengmian.html',params = locals())

@main.route('/info')
def info_views():
    # mdic = {}
    # ndic = {}
    Topic_tp =[]
    num = 3
    topic_id = request.args.get('topic_id')
    topics = Topic.query.limit(9).all()
    topic = Topic.query.filter_by(id = topic_id).first()
    topic_date = Topic.query.order_by('pub_date desc').limit(5).all()
    topic_num = Topic.query.order_by('read_num desc').limit(5).all()

    topic.read_num +=  1
    db.session.add(topic)
    prevTopic = Topic.query.order_by('id desc').filter(Topic.id < topic_id).first()
    nextTopic = Topic.query.filter(Topic.id > topic_id).first()
    with open(os.path.join(APP_ROOT, 'static', topic.content), 'rb') as f:
        file = f.read().decode()


    while True:
        if num<7:
            topic_tp = Topic.query.order_by('id desc').filter(Topic.category_id==num).limit(1).all()
            num+=1
            Topic_tp +=topic_tp
        else:
            break

    # for mtopic in topic_date:
    #     with open(os.path.join(APP_ROOT,'static',mtopic.content),'rb') as f:
    #
    #         mfile = f.readline().decode()
    #         mdic[mtopic.id] = mfile
    #
    # for ntopic in topic_num:
    #     with open(os.path.join(APP_ROOT, 'static', ntopic.content), 'rb') as f:
    #         nfile = f.readline().decode()
    #         ndic[ntopic.id] = nfile

    if 'uid' in session and 'username' in session:
        user = Users.query.filter_by(id=session.get('uid')).first()
    return render_template('info.html',params=locals())

@main.route('/time')
def time_views():
    topics = Topic.query.all()
    if 'uid' in session and 'username' in session:
        user = Users.query.filter_by(id=session.get('uid')).first()
    return render_template('time.html',params = locals())

@main.route('/release',methods=['GET','POST'])
def release_views():
  if request.method == 'GET':
    #权限验证：验证用户是否有发表博客的权限即必须是登录用户并且is_author的值必须为1
    if 'uid' not in session or 'username' not in session:
      return redirect('/login')
    else:
      user = Users.query.filter_by(id=session.get('uid')).first()
      if user.is_author != 1:
        return redirect('/')

    #查询category和blogtype
    categories = Category.query.all()
    blogTypes = BlogType.query.all()
    return render_template('release.html',params=locals())
  else:
    topics = Topic.query.order_by('id desc').first()
    # 处理post请求即发表博客的处理
    topic = Topic()
    #为title赋值
    topic.title = request.form.get('author')
    #为blogtype_id赋值
    topic.blogtype_id = request.form.get('list')
    #为category_id赋值
    topic.category_id = request.form.get('category')
    #为user_id赋值
    topic.user_id = session.get('uid')
    #为content赋值
    content = (request.form.get('content')).encode('utf-8').decode('utf-8')

    filename = str(topics.id)+'.txt'
    with open(os.path.join(APP_ROOT, 'static/upload', filename), 'w',encoding='utf-8') as f:
        f.write(content)
    topic.content = 'upload/'+filename
    #为pub_date赋值
    topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # print("%s,%s,%s,%s,%s,%s" % (topic.title,topic.blogtype_id,topic.category_id,topic.user_id,topic.content,topic.pub_date))

    #选择性的为 images 赋值
    if request.files:
      print('有文件上传')
      # 取出文件
      f = request.files['picture']
      # 处理文件名称,将名称赋值给topic.images
      # 获取当前时间，作为文件名
      ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
      # 获取文件的扩展名
      ext = f.filename.split('.')[1]
      filename = ftime+"."+ext
      topic.images = 'upload/'+filename
      # 将文件保存至服务器
      basedir = os.path.dirname(os.path.dirname(__file__))
      upload_path = os.path.join(basedir,'static/upload',filename)
      print(upload_path)
      f.save(upload_path)

    db.session.add(topic)
    return redirect('/')