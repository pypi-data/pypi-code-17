#!python
"""f2_rest : a REST API to access an F2 database.
   Th.Estier - aout 2014
   version 0.1
   
   uses web.py framework, a great piece of soft from Aaron Schwartz (see webpy.org)
"""
import web
import F2

render = web.template.render('templates/', base='layout')

urls = (
    '/', 'index',
    '/trans/(.+)', 'transaction'
    )
app = web.application(urls, globals())

class index:
    """F2 server: root welcoming page"""
    def GET(self):
        f2 = get_f2_database()
        i = web.input(dbName=None, clName=None)
        db = f2.Database(name=i.dbName)
        if db: db = db[0]
        cl = f2.CLASS(className=i.clName, db=db)
        if cl: cl = cl[0]
        return render.index(db, cl, f2)

class transaction:
    """F2 server: actions to apply to transactions"""
    def GET(self, action):
        if action not in ('commit', 'rollback', 'sync'):
            raise web.notfound('no such action for transaction: {0}'.format(action))
        else: 
            f2 = get_f2_database()
            transactionMethod = getattr(f2, action)
            transactionMethod()
            raise web.seeother('/')
        	
# F2 database connection
F2_DB_URL = 'rpc:127.0.0.1:8081'

def get_f2_database():
    "get f2 connection from config"
    if web.config.get('f2'):
        return web.config.f2
    else:
        f2c = F2.connect(F2_DB_URL)
        web.config.f2 = f2c
        return f2c

if __name__ == '__main__':
    app.run()
