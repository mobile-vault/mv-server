import logger
from db.constants import Constants as C
from db.helpers.base import DBHelper


class AuthenticationDBHelper(DBHelper):

    def __init__(self):
        DBHelper.__init__(self)
        self.log = logger.Logger('AuthenticationDBHelper')

    def check_authentication(self, email, passcode):
        TAG = 'check_authentication'
        if email is not None and passcode is not None:
            from db.helpers.user import UserDBHelper
            user_helper = UserDBHelper()
            users = user_helper.get_user_with_email(email)

            if isinstance(users, dict):
                user = users
                from db.helpers.enrollment import EnrollmentDBHelper
                enrollment_helper = EnrollmentDBHelper()
                enrollment_filter = {C.ENROLLMENT_TABLE_USER: user['id']}
                enrollments = enrollment_helper.get_enrollments(
                    enrollment_filter, status=False)
                if enrollments is not None:
                    for enrollment in enrollments:
                        if str(enrollment[C.ENROLLMENT_TABLE_PASSWORD]) == str(
                                passcode):
                            self.log.i(TAG, 'Passcodes match')
                            return enrollment
                        else:
                            self.log.i(TAG,
                                       'Invalid passcode email combination')
                    return None
                else:
                    self.log.e(TAG,
                               'No entry found in user table corresponding \
                               to email ' + email)
                    return None
            else:
                self.log.e(TAG, 'No user with email address ' + email + '\
                           found')
                return None
        else:
            return None

if __name__ == '__main__':
    auth = AuthenticationDBHelper()
    print auth.check_authentication('ravi@codemymobile.com', '6565')
