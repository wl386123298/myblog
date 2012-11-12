__author__ = 'Administrator'

import  web
import datetime

render =web.template.render('templates/')

db1 =web.database(dbn='mysql',db='news',user='root',pw='root')
sql ="select *from tb_news order by id"

urls =('/',"hello",
       '/results','login',
       '/login','login_index',
       '/about','about',
       '/(\d+)','content',
       '/(\d+)/edit','edit',
       '/(\d+)/update','update',
       '/(\d+)/delete','delete',
       '/(\d+)/leave_message','message',

      )

app =web.application(urls,globals())

class hello:
    def GET(self):
        data =db1.query(sql)
        return render.index(data)

class content:
    def GET(self,name):
        data_1 =db1.query("select *from tb_news where id="+str(name))
        data_2 =db1.query("select *from news_message where id="+str(name))
        return render.contents(data_1,data_2)

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
        if get_data.new_title ==''or get_data.new_author=='' or get_data.new_content =='':
            raise  web.seeother('/error')
        else:
            result =db1.update('tb_news',where='id='+str(name),title=t,author=a,new_date=datetime.datetime.now(),content =c)
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
