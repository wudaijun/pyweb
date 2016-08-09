# coding=utf8
import web
import sys

from pymongo import MongoClient
from web.contrib.template import render_jinja

web.config.debug = True

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



urls = (
    '/', 'All',
    '/all', 'All',
    '/new', 'New',
    '/info', 'Info'
)

render = render_jinja(
    'templates',
    encoding = 'utf-8',
)


class Info:
    def GET(self):
        name  = web.input().get('name')
        if name:
            c    = MongoClient()
            doc  = c.test.users.find_one({u'name':name})
            c.close()
            data = gen_data({"doc":doc})
            return render.info(data)
        else:
            return render.info()

    def POST(self):
        name  = web.input().get('name')
        desc  = web.input().get('desc')
        print(desc)
        c = MongoClient()
        c.test.users.update({u'name':name}, {u'name':name, u'desc':desc}),
        c.close()
        return web.seeother("/all")


class All:
    def GET(self):
        c   = MongoClient()
        docs = c.test.users.find()
        c.close()
        data = gen_data({"docs":docs, "nav":all})
        return render.all(data)

class New:
    def GET(self):
        name = web.input().get('name')
        desc = web.input().get('desc')
        if name:
            c   = MongoClient()
            if c.test.users.find_one({u'name':name}) == None:
                c.test.users.insert_one({u'desc':desc,u'name':name}),
                return web.seeother('/all')
            else:
                return render.new({u'lasterror':u'用户已存在!'})
        else:
          return render.new()

def gen_data(d):
    # add cookie or env here
    # myvalue = web.cookies.get('mykey')
    return d

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
