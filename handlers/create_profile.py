'''
This file can be used used to create a profile with name enrollID.mobileconfig
'''

from os import environ
import threading
# from xml.dom import minidom
from xml.dom.minidom import parse


'''
Server url will be dynamic to work same code on different servers
in case on user enrollment and iOS profile generation also.
'''
server_url = environ.get('SERVER_CNAME')

base_checkin_url = str(server_url) + '/enroll/'


class CreateProfileThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        print 'IN createProfile\'s init'
        self.name = name

    def run(self):

        check_in_url = base_checkin_url + self.name
        with open('/opt/toppatch/assets/ios/testconfig.xml',
                  'rb') as sample_file:
            dom = parse(sample_file)
            params = dom.getElementsByTagName("string")
            for param in params:
                if str(
                        param.firstChild.nodeValue) == (
                        str(server_url) +
                        '/enroll'):
                    print param.firstChild.nodeValue
                    param.firstChild.replaceWholeText(check_in_url)

        # print dom.toxml()

        # write to file
        self.name += '.mobileconfig'
        print 'file name = ' + self.name
        with open(self.name, "wb") as new_file:
            new_file.write(dom.toxml())
