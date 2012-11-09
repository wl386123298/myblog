#coding ='utf-8'

__author__ = 'Administrator'

import web
import datetime

render =web.template.render('templates/')

db =web.database(dbn='mysql',db='news',user='root',pw='root')

urls =('/',"test",
       '/commit','commit',
       '/error','error'
       )

app =web.application(urls,globals())

class test:
    def GET(self):
        web.header("Content-Type","text/html;charset=utf-8")
        return render.test()

class commit:
    def POST(self):
        i =web.input()
        t =i.title
        a =i.author
        c =i.content
        if i =='' or a =='' or c =='':
            raise  web.seeother('/error')
        else:
            result =db.insert('tb_news',title =t,author=a,new_date=datetime.datetime.now(),content =c)
            return render.commit(result)
class error:
    def GET(self):
        return render.error()

if __name__ == "__main__":
        app.run()
