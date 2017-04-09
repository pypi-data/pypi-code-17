import ezrpy

if __name__ == '__main__':
    app = ezrpy.App('api')
    app.add_resource('test1')
    app.add_resource('test2')
    app.add_resource('test3')
    app.run()
