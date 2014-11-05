import tornado.web


class LogoutRequestHandler(tornado.web.RequestHandler):

    def get(self):
        print "in logout"
        self.clear_cookie('user')
        self.clear_cookie('company')
        self.clear_cookie('company_name')
        self.redirect('/login.html')
