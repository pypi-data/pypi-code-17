from ghost import Ghost

g = Ghost()

session = g.start()
session.set_viewport_size(3200, 2400)
session.open('http://jeanphix.me/2016/06/13/howto-cloudformation-ecs/')
session.print_to_pdf('test.pdf')
