import tornado.web
import json

class LoginTestRequestHandler(tornado.web.RequestHandler):
    
    def post(self):
        gcm = self.get_argument('gcm', None)
        if gcm is not None:
            print gcm
        res = dict()
        res['pass']= True
        res['key']= '89A4DE09F576AC09D86A39F706F8823195151D9427EE8B4E1444ACD117C1837E3E1406F8020A8C42D662280349F0731E3B3ADCEF14B1792A2993A0CA3D3F5363'
        self.write(json.dumps(res))