'''
This script mainly will be used to send mail to admin about the
violation done by any user.
'''
# from os.path import abspath, dirname
# from sys import path
#import ipdb

from os import environ
from boto import ses
# import json
from itsdangerous import TimedJSONWebSignatureSerializer

from logger import Logger
from db.helpers.violations import ViolationsDBHelper
from db.helpers.device import DeviceDBHelper
from db.helpers.user import UserDBHelper
from db.helpers.company import CompanyDBHelper
from db.helpers.base import DBHelper
# from tornado.template import Template
from tornado.template import Loader


ses_conn = ses.connect_to_region(
    'us-east-1',
    aws_access_key_id=environ.get('AWS_SES_ACCESS_KEY_ID'),
    aws_secret_access_key=environ.get('AWS_SES_SECRET_ACCESS_KEY'))

loader = Loader("/opt/toppatch/mv/media/app/")


def admin_mailer(device_id, violation_id, *args, **kwargs):

    TAG = 'admin mailer'
    base = DBHelper()
    cur = base.cursor
    log = Logger('AdminMailer')

    device = DeviceDBHelper()
    violation = ViolationsDBHelper()
    user = UserDBHelper()
    company = CompanyDBHelper()
    email_list = []

    device_os_mapper = {'ios': 'iOS', 'samsung': 'android'}
    ### Device information ###
    device_info = device.get_device(str(device_id), status=True)

    if device_info:
        device_os = device_info.get('os')
        device_os = device_os_mapper.get(device_os)
        device_os_version = device_info.get('os_version')
        user_info = user.get_user(str(device_info.get('user_id')))

    else:
        device_os = None
        device_os_version = None
        user_info = None

    ### User information ###
    if user_info:
        username = user_info.get('name')
        company_id = user_info.get('company_id')
        company_info = company.get_company(str(company_id))
    else:
        username = None
        company_info = None
        company_id = None

    ### Violation information ###
    violation_info = violation.get_violation(str(violation_id))

    if violation_info:
        violation_time = violation_info.get('timestamp')
        violation_time = violation_time.strftime('%d %b, %Y at %H:%M:%S')
    else:
        violation_time = None

    ### Company information ###

    if company_info:
        company_name = company_info.get('name')
        ### Query to get admin information for the particulat company ###
        try:
            cur.execute("""SELECT * FROM admin_profile
            WHERE company_id = {0}""".format(company_id))

        except Exception as err:
            log.e(TAG, 'Exception : ' + repr(err))

        if cur.rowcount > 0:
            rows = cur.fetchall()
            for row in rows:
                # ipdb.set_trace()
                email_list.append(row[1])

        else:
            log.i(
                TAG,
                """No admin user found for the violated device with company
id : {0}""".format(company_id))
            print "Query over admin went wrong"
    else:
        company_name = None

    if len(email_list) > 0 and all(
        x is not None for x in (
            username,
            company_name,
            violation_time,
            device_os)):
        message = loader.load('violation_mail.html').generate(
            username=username, company_name=company_name,
            violation_time=violation_time, device_os=device_os,
            device_os_version=device_os_version)

        try:
            ses_conn.send_email('mv@toppatch.com',
                                'User MDM Violations Notification',
                                message, email_list, format='html')
        except Exception as err:
            log.e(TAG, "Error in sending mail from ses side.")

    else:
        log.i(
            TAG,
            """No admin found for the violated device with company id :
{0}""".format(company_id))


def admin_signup(admin_id, company_id, admin_email, company_email):

    TAG = 'admin signup'
    log = Logger('AdminSignUp')

    salt_key = environ.get('salt_key')
    json_url_key = environ.get('json_url_key')

    company_id = str(company_id)
    admin_id = str(admin_id)

    danger_signer = TimedJSONWebSignatureSerializer(json_url_key)
    danger_signer.expires_in = 86400
    hash_url = danger_signer.dumps({'cmd_hash': company_id,
                                    'adm_hash': admin_id}, salt=salt_key)
    link_url = str(environ.get('SERVER_CNAME')) + '/activation/' + hash_url

    message = loader.load('verification_mail.html').generate(
        company_name=company_email, activation_link=link_url)

    try:
        ses_conn.send_email('mv@toppatch.com',
                            'MDM Trial Activation Link', message,
                            [admin_email], format='html')
    except Exception as err:
        log.e(TAG, "Error {0} in sending mail from ses side.".format(err))


if __name__ == '__main__':

    pass
