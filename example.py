# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("youtube.db",check_same_thread=False)
cur = conn.cursor()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search',methods = ['POST','GET'])
def search():
    search = []
    if request.method == 'GET':
        channel_name = request.args.get('NAME')
        cur.execute('SELECT title,thumbnail_link FROM video_info where channel_title = "%s"' %channel_name)
        result = cur.fetchall()
    for row in result:
        if row not in search:
            search.append(row)
    return render_template('search.html', search = search)

@app.route('/charts')
def charts():
    cur.execute('SELECT title FROM popularity order by views desc ' )
    charts = cur.fetchall()
    videotitle = []
    i = 0 
    for row in charts:
        if i <10:
            if row not in videotitle :
                videotitle.append(row)
                i += 1 
    return render_template('charts.html',videotitle = videotitle)

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/category_data',methods=['POST','GET'])
def category_data():
      if request.method == 'GET':
        req_category = request.args.get('id')
        cur.execute('SELECT title FROM category_info where category_id = "%s"' %req_category)
        title = cur.fetchall()
        videotitle = []
        for row in title:
            videotitle.append(row)
        return render_template('category_data.html', videotitle = videotitle)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,use_reloader=False)