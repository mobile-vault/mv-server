from handlers import (admin, checkin, enroll, login, main,
                    pass_verify, policies, pre_enroll, roles, teams,
                    update_token, batch_insert, user, os_type,
                    broadcast_message, logout, admin_activate, register)
from handlers.dashboard import logs as dashboard_logs

from handlers.dashboard import (device_count, enrollment_status,
                                            session, violations)

from handlers.samsung import (login as samsung_login,
                                   samsung_command_result)
import tornado.web
import vendor.command_controller.ios.ios_command_handler as ios_command_handler

url_patterns=[   
    (r"/", main.MainHandler),
    (r"/index.html", main.MainHandler),
    (r"/registration", register.RegisterHandler),
    (r"/activation/(.*)", admin_activate.ActivationLinkHandler),
    (r"/login/(.*)", login.LoginHandler),
    (r"/logout/", logout.LogoutRequestHandler),
    (r"/admin", admin.AdminRequestHandler),
    (r"/change_password", admin.AdminRequestHandler),
    (r"/command/ios", ios_command_handler.IOSCommandHandler),
    (r"/dashboard/devices", device_count.DashboardDeviceCountRequestHandler),
    (r"/dashboard/enrollment",
                    enrollment_status.DashboardEnrollmentStatusRequestHandler),
    (r"/dashboard/logs", dashboard_logs.DashboardLogsRequestHandler),
    (r"/dashboard/sessions", session.DashboardSessionRequestHandler),
    (r"/dashboard/violations", violations.DashboardViolationRequestHandler),
    (r"/dashboard/postmessage", broadcast_message.BroadCastMessageHandler),
    (r"/enroll/(.*)", checkin.CheckInRequestHandler),
    (r"/operating_system", os_type.OperatingSystemRequestHandler),
    (r"/passverify", pass_verify.PassVerifyRequestHandler),
    (r"/pre_enroll", pre_enroll.PreEnrollRequestHandler),
    (r"/policies/user/(.*)", policies.UserPolicyRequestHandler),
    (r"/policies/team/(.*)", policies.TeamPolicyRequestHandler),
    (r"/policies/role/(.*)", policies.RolePolicyRequestHandler),
    (r"/policies/company/(.*)", policies.CompanyPolicyRequestHandler),
    (r"/roles(.*)", roles.RolesRequestHandler),
    (r"/samsung/login", samsung_login.LoginHandler),
    (r"/samsung/save", samsung_command_result.SamsungCommandResultHandler),
    (r"/teams(.*)", teams.TeamsRequestHandler),
    (r"/user_bulk", batch_insert.BatchInsertRequestHandler),
    (r"/user_enroll(.*)", enroll.EnrollDeviceRequestHandler),
    (r"/users(.*)", user.UserRequestHandler),

    #(r"/demo/login", demo_login.DemoLoginRequestHandler),
    (r"/update_token", update_token.UpdateTokenRequestHandler),

    (r"/android_profile\.apk(.*)", tornado.web.StaticFileHandler,
            {'path':'/opt/toppatch/assets/android/MobileVaultAgent.apk'}),

    (r"/login.html(.*)", tornado.web.StaticFileHandler,
               {'path':'/opt/toppatch/mv/media/app/login.html'}),

    (r"/invalid.html", tornado.web.StaticFileHandler,
               {'path':'/opt/toppatch/mv/media/app/error_invalid.html'}),

    (r"/core/(.*)", tornado.web.StaticFileHandler,
                      {'path':'/opt/toppatch/mv/media/app/core/'}),

    (r"/css/(.*)", tornado.web.StaticFileHandler,
                {'path':'/opt/toppatch/mv/media/app/css/'}),

    (r"/fonts/(.*)", tornado.web.StaticFileHandler,
                {'path':'/opt/toppatch/mv/media/app/fonts/'}),

    (r"/images/(.*)", tornado.web.StaticFileHandler,
              {'path':'/opt/toppatch/mv/media/app/images/'}),

    (r"/vendor/(.*)", tornado.web.StaticFileHandler,
                  {'path':'/opt/toppatch/mv/media/app/vendor/'}),
]