#coding=utf-8

__author__ = 'Administrator'

import  web
import datetime

render =web.template.render('templates/')

db1 =web.database(dbn='mysql',db='news',user='root',pw='root')
sql ="select *from tb_news order by new_date desc"

urls =('/',"hello",
       '/results','login',
       '/login','login_index',
       '/about','about',
       '/todo/(\d+)','NavNumContent',
       '/(\d+)','content',
       '/(\d+)/edit','edit',
       '/(\d+)/update','update',
       '/(\d+)/delete','delete',
       '/(\d+)/leave_message','message',

      )

app =web.application(urls,globals())

#NavNum表示最多显示的数量
NavNum =3

def page():
    """
    分页,pages为分页的数
    """
    results = db1.query("SELECT COUNT(*) AS NEWSCOUNT FROM tb_news")
    news_count = results[0].NEWSCOUNT
    #print "总条数:",news_count

    if not news_count % NavNum:
        pages = news_count / NavNum

    else:
        pages = news_count / NavNum + 1

    #print "分的页数:",pages

    return pages

class hello:
    def GET(self):
        data =db1.query(sql)
        data_1 =db1.query(sql)
        pages =page()
        return render.index(data_1,data,pages)

class NavNumContent:
    def GET(self,id):
        off = (int(id)-1) * NavNum
        #print "第",id,"页\n-----"
        re = db1.select('tb_news',order='new_date desc',limit=NavNum,offset=off)
        pages =page()
        return render.index_content(re,pages)

class content:
    def GET(self,name):
        data_1 =db1.query("select *from tb_news where id="+str(name))
        return render.contents(data_1)

class about:
    def GET(self):
        return render.about()

class edit:
    def GET(self,name):
        data_2 =db1.query("select *from tb_news where id="+str(name))
        return render.edit_new(data_2)

class message:
    def POST(self,name):
        get_message =web.input().lmessage

        if get_message =='':
            raise web.seeother('/'+str(name))
        else:
            result =db1.insert('news_message',id =name,date=datetime.datetime.now(),mcontent =get_message)
            return web.seeother('/'+str(name))


class update:
    def POST(self,name):
        get_data =web.input()
        t =get_data.new_title
        a =get_data.new_author
        c =get_data.new_content
        t =get_data.tag
        if get_data.new_title ==''or get_data.new_author=='' or get_data.new_content =='':
            raise  web.seeother('/error')
        else:
            result =db1.update('tb_news',where='id='+str(name),title=t,author=a,new_date=datetime.datetime.now(),content =c,tag_name =t)
            return  render.update_data(result)

class delete:
    def GET(self,name):
        db1.delete('tb_news',where='id='+str(name))
        raise web.seeother('/','true')

class login:
    def POST(self):
        get_user =web.input()
        user =get_user.username
        get_password =get_user.psw

        sql ="select *from user"
        user_data =db1.query(sql)

        if user == '' or get_password =='':
            raise web.seeother("/login")

        for data in user_data:
            if data.username ==user and data.password ==str(get_password):
                print "success"

            print 'failed'


class login_index:
    def GET(self):
        return render.login()


if __name__ =="__main__":
    app.run()
