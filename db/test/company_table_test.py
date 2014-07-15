from tornado import *
from tornado.testing import *
import unittest
from toppatch_db.helpers.company import *
from toppatch_db.constants import Constants as c

################# Test cases for is_company_valid(id)  ###################################

#All OK
class MyTestCase1(AsyncTestCase):
    def test_http_fetch(self):
        company1 = CompanyDBHelper()
        id = company1.is_company_valid('0')
        self.assertEqual(True, id) 
    
# Company is not '0'
class MyTestCase2(AsyncTestCase):
    def test_http_fetch(self):
        company1 = CompanyDBHelper()
        id = company1.is_company_valid('1')
        self.assertEqual(False, id) 
        
# Company is blank
class MyTestCase3(AsyncTestCase):
    def test_http_fetch(self):
        company1 = CompanyDBHelper()
        id = company1.is_company_valid('')
        self.assertEqual(False, id) 
        
# Company is NULL
class MyTestCase4(AsyncTestCase):
    def test_http_fetch(self):
        company1 = CompanyDBHelper()
        id = company1.is_company_valid(None)
        self.assertEqual(False, id) 
        
# Company is not string
class MyTestCase5(AsyncTestCase):
    def test_http_fetch(self):
        company1 = CompanyDBHelper()
        id = company1.is_company_valid(['0'])
        self.assertEqual(False, id) 

