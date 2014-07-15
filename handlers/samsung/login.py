from tornado.web import RequestHandler
from handlers.constants import Constants
from db.constants import Constants as C
from db.helpers import enrollment, samsung_command
from db.helpers import device_details
from db.helpers.violations import ViolationsDBHelper
import json
import uuid
import tornado
import config
from vendor.command_controller.android.android_command import AndroidCommand

class LoginHandler(RequestHandler):

    def post(self):
        print '\n\nSamsung login\n\n'
        email = self.get_argument(Constants.SAMSUNG_LOGIN_EMAIL, None)
        passcode = self.get_argument(Constants.SAMSUNG_LOGIN_PASSCODE, None)
        gcm = self.get_argument(Constants.SAMSUNG_LOGIN_GCM, None)
        imei = self.get_argument('imei', None)
        print email, passcode, gcm, imei

        if email and passcode and gcm and imei:
            # Boolena flag to track enrollment status
            enrolled_status = False
            #Check in the database helper..
            from db.helpers.authentication import AuthenticationDBHelper
            auth = AuthenticationDBHelper()
            auth_result = auth.check_authentication(email, passcode)
            print auth_result
            if auth_result is not None:
                print "\n reached here \n"
                result = dict()
                result['uuid'] = str(uuid.uuid4())
                from db.helpers import device
                #Insert a row in device table and set the enrollment row[is_enrolled]=true
                device_helper = device.DeviceDBHelper()
                enrollment_helper = enrollment.EnrollmentDBHelper()
                device_details_helper = device_details.DeviceDetailsDBHelper()

                enrollment_id = str(auth_result['id'])
                devices = device_helper.get_device_with_udid(str(imei),
                                                         status=True)
                enrollment_dict = enrollment_helper.get_enrollment(
                                        enrollment_id)

                device_id = enrollment_dict.get(C.ENROLLMENT_TABLE_DEVICE)

                if device_id:

                    device_helper.update_device(str(device_id),
                             {C.DEVICE_TABLE_DELETED: False,
                                C.DEVICE_TABLE_UDID: str(imei)})
                    device_details_helper.update_device_details(str(device_id),
                                                {'gcm':gcm})
                    enrolled_status = True

                elif devices:
                    device_id = devices[0][C.DEVICE_TABLE_ID]
                    device_helper.update_device(str(device_id),
                             {C.DEVICE_TABLE_DELETED: False,
                              C.DEVICE_TABLE_USER: auth_result.get('user_id')})
                    device_details_helper.update_device_details(str(device_id),
                                                    {'gcm':gcm})
                    enrollment_helper.update_enrollment(enrollment_id,
                                {C.ENROLLMENT_TABLE_DEVICE : str(device_id)})
                    enrollment_helper.set_enrolled(enrollment_id)
                    enrolled_status = True

                else:

                    print "\nIn new device conditions\n"
                    device_dict = dict()
                    device_dict[C.DEVICE_TABLE_OS] = 'samsung'
                    device_dict[C.DEVICE_TABLE_UDID] = imei
                    device_dict[C.DEVICE_TABLE_USER] = str(
                                auth_result['user_id'])
                    device_id = device_helper.add_device(device_dict)

                    #Set it as enrolled in enrollment table
                    enrollment_helper.update_enrollment(enrollment_id,
                            {C.ENROLLMENT_TABLE_DEVICE : str(device_id)})
                    enrollment_helper.set_enrolled(str(auth_result['id']))
                    enrolled_status = True

                    samsung_command_helper = samsung_command.SamsungCommandsDBHelper()
                    command = dict()
                    command[C.SAMSUNG_COMMANDS_TABLE_ACTION] = C.SAMSUNG_COMMANDS_TABLE_ACTION_SETUP
                    command[C.COMMAND_TABLE_COMMAND_UUID] = result['uuid']
                    command[C.SAMSUNG_COMMANDS_TABLE_DEVICE] = device_id
                    command[C.SAMSUNG_COMMANDS_TABLE_ATTRIBUTE] = ''

                    ## separate implementation for getting os version using
                    ## devcie_information command

                    android_engine = AndroidCommand()
                    command_dict = {}
                    command_dict['action_command'] = 'device_information'

                    #Save GCM. This is an important part.
                    device_details_helper = device_details.DeviceDetailsDBHelper()
                    device_dict = dict()
                    device_dict[C.DEVICE_DETAILS_TABLE_DEVICE] = str(device_id)
                    device_dict[C.DEVICE_DETAILS_TABLE_EXTRAS] = {'gcm':gcm}
                    if device_details_helper.add_device_detail(device_dict):
                        #Now update the os of the device as samsung. very important!!!
                        d = dict()
                        d[C.DEVICE_TABLE_OS] = 'samsung'
                        device_helper.update_device(str(device_id), d)
                        result['pass'] = True
                        result['key'] = config.SAMSUNG_LICENSE
                        result['id'] = samsung_command_helper.add_command(
                            command)
                        #self.write(json.dumps(result))

                        ## now send the device information command to device
                        android_engine.execute(command_dict, device_id)
                    else:
                        result['pass'] = False
                        result['message'] = 'Could not update on the server'
                        self.write(json.dumps(result))

                if not enrolled_status:
                    result['pass']=False
                    result['message']='Could not update on the server'
                    self.write(json.dumps(result))
                else:
                    result['pass']= True
                    result['key']= config.SAMSUNG_LICENSE
                    self.write(json.dumps(result))
                    violation = ViolationsDBHelper()
                    violation_status = violation.update_violations(
                                            str(device_id))
                    if violation_status:
                        print "Violation table updated for device_id"+ str(device_id)
                    else:
                        print "Violation table not updated for device_id"+ str(device_id)
            else:
                result = dict()
                result['pass']= False
                result['message']= 'Invalid email passcode combination'
                self.write(json.dumps(result))
        elif not gcm:
            result= dict()
            result['pass']=False
            result['message']='No GCM information sent'
            self.write(json.dumps(result))
        else:
            result = dict()
            result['pass']= False
            result['message']= 'Email ='+str(email)+ ' Passcode ='+str(passcode)+' is not valid'
            self.write(json.dumps(result))

if __name__ == '__main__':
    app = tornado.web.Application([(r"/",LoginHandler)])
    app.listen(8076)
    tornado.ioloop.IOLoop.instance().start()
