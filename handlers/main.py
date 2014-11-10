import tornado

from .super import SuperHandler


class MainHandler(SuperHandler):

    def get(self):
        print 'Main Handler with user ', self.current_user
        if not self.current_user:
            self.redirect("/login.html")
            return
        # name = tornado.escape.xhtml_escape(self.current_user)
        self.render('index.html')
