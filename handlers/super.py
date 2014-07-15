import tornado.web


class SuperHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie(name='user', max_age_days=1)
    
    def get_current_company(self):
        return self.get_secure_cookie(name='company', max_age_days=1)
    
    def get_current_company_name(self):
        return self.get_secure_cookie(name='company_name', max_age_days=1)