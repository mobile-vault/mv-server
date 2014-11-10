from xlrd import open_workbook
from db.constants import Constants as C
from db.helpers.role import RoleDBHelper
from db.helpers.team import TeamDBHelper
from db.helpers.user import UserDBHelper
import threading
from db.helpers.enrollment import EnrollmentDBHelper
from handlers.markov_passwords import generate_password


class ExcelParser(threading.Thread):

    def __init__(self, path=None, company=None, company_name=None,
                 callback=None, user_added_callback=None, group=None,
                 target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(
            self,
            group=group,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            verbose=verbose)
        self.path = path
        self.company = company
        self.company_name = company_name
        self.callback = callback
        self.user_added_callback = user_added_callback

    def run(self):
        self.parse(excel_path=self.path, company=self.company,
                   company_name=self.company_name, callback=self.callback,
                   user_added_callback=self.user_added_callback)

    def parse(self, excel_path, company, company_name=None, callback=None,
              user_added_callback=None):
        COMPANY = company
        company_name = company_name
        book = open_workbook(filename=excel_path)
        sheet = book.sheet_by_index(0)

        users = list()
        for row_index in range(sheet.nrows):
            user = dict()
            for col_index in range(sheet.ncols):
                cell = sheet.cell(row_index, col_index).value
                if col_index == 0:
                    user[C.USER_TABLE_EMAIL] = cell
                elif col_index == 1:
                    user[C.USER_TABLE_NAME] = cell
                elif col_index == 2:
                    user[C.USER_TABLE_TEAM] = cell
                elif col_index == 3:
                    user[C.USER_TABLE_ROLE] = cell
            users.append(user)
        roles_list = list()
        teams_list = list()
        for user in users:
            if C.USER_TABLE_ROLE in user:
                roles_list.append(user[C.USER_TABLE_ROLE])
            if C.USER_TABLE_TEAM in user:
                teams_list.append(user[C.USER_TABLE_TEAM])

        # get a set to get the unique elements.
        roles = dict()
        teams = dict()

        roles_helper = RoleDBHelper()
        teams_helper = TeamDBHelper()
        users_helper = UserDBHelper()
        enrollment_helper = EnrollmentDBHelper()

        for role_name in set(roles_list):
            role = dict()
            role[C.ROLE_TABLE_COMPANY] = COMPANY
            role[C.ROLE_TABLE_NAME] = role_name
            roles[role_name] = roles_helper.add_role(role)

        for team_name in set(teams_list):
            team = dict()
            team[C.TEAM_TABLE_COMPANY] = COMPANY
            team[C.TEAM_TABLE_NAME] = team_name
            team[C.TEAM_TABLE_DELETED] = False
            teams[team_name] = teams_helper.add_team(team)

        # Now we have id for all teams and roles... Insert the users now.
        for user in users:
            user_obj = dict()
            user_obj[C.USER_TABLE_COMPANY] = COMPANY
            user_obj[C.USER_TABLE_EMAIL] = user[C.USER_TABLE_EMAIL]
            user_obj[C.USER_TABLE_NAME] = user[C.USER_TABLE_NAME]
            user_obj[C.USER_TABLE_ROLE] = roles[user[C.USER_TABLE_ROLE]]
            user_obj[C.USER_TABLE_TEAM] = teams[user[C.USER_TABLE_TEAM]]
            user['id'] = users_helper.add_user_if_not_exists(user_obj)[0]
            if user_added_callback is not None:
                user_added_callback(user_obj)

        for user in users:
            enrollment = dict()
            enrollment[C.ENROLLMENT_TABLE_USER] = user['id']
            enrollment[C.ENROLLMENT_TABLE_PASSWORD] = generate_password()
            enrollment[C.ENROLLMENT_TABLE_IS_ENROLLED] = False
            user['passcode'] = enrollment[C.ENROLLMENT_TABLE_PASSWORD]
            print 'adding enrollment ', enrollment
            user['enrollment_id'] = enrollment_helper.add_enrollment(
                enrollment)
            user['company_name'] = company_name
        if callback is not None:
            callback(users)
        return users


def send_mail(users):
    print 'callback' + str(users)

if __name__ == '__main__':
    parser = ExcelParser()
    parser.parse(
        excel_path='/home/amangautam/data_mac.xlsx',
        company='1',
        callback=send_mail)
