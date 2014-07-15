--Policies Table

--insert into policies(attributes) values ('[{"data": {"allowCamera": true ,"allowiTunes": false} ,"type":  "restrictions"}]');
--insert into policies(attributes) values ('[{"data": {"allowCamera": true } ,"type":  "restrictions"}]');
--insert into policies(attributes) values ('[{"data": {"allowiTunes": false} ,"type":  "restrictions"}]');
--insert into policies(attributes) values ('[{"data": {"allowCamera": true ,"allowiTunes": false, "allowSafari": true} ,"type":  "restrictions"}]');
 
 
--Company table 

insert into companies(name, policy_id) values ('Toppatch',1);

--Login Table

insert into logins(username,password,company_id) values('admin','admin',1);


--Role Table

insert into roles(name,company_id) values('Developer',1);
insert into roles(name,company_id,policy_id,created_on,modified_on) values('Manager',1,2,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');
insert into roles(name,company_id,policy_id,created_on,modified_on) values('Lead',1,3,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');
insert into roles(name,company_id,policy_id,created_on,modified_on) values('Designer',1,4,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');


--Teams Table

insert into teams(name,company_id) values('Server',1);
insert into teams(name,company_id,policy_id,created_on,modified_on) values('Mangement',1,2,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');
insert into teams(name,company_id,policy_id,created_on,modified_on) values('iOS',1,3,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');
insert into teams(name,company_id,policy_id,created_on,modified_on) values('Android',1,4,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');
insert into teams(name,company_id,policy_id,created_on,modified_on) values('UI',1,4,'2014-01-03 18:50:00+02','2014-01-03 18:50:00+02');


--User Table

insert into users(email,name,role_id,team_id, company_id, deleted) values('atul@codemymobile.com','Atul',1,1,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('nitesh@codemymobile.com','Nitesh',1,1,2,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('aman@codemymobile.com','Aman',3,4,3,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('sandeep@codemymobile.com','Sandeep',4,4,4,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('ravi@codemymobile.com','Ravi',1,4,1,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('popli@codemymobile.com','Popli',1,4,2,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('akshat@codemymobile.com','Akshat',1,4,3,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('swati@codemymobile.com','Swati',2,2,4,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('ankit@codemymobile.com','Ankit',2,4,1,1,False);
insert into users(email,name,role_id,team_id, policy_id, company_id, deleted) values('shiva@codemymobile.com','Shiva',1,4,2,1,False);


--Session Table

insert into sessions(user_id,created_on,ip, invalid, user_agent) values(1,'2014-01-03 18:50:00+02','192.168.2.150',False,'Chrome browser');


--Violation Table

insert into violations(user_id,timestamp) values(10,'2014-01-03 17:59:00+02');
insert into violations(user_id,timestamp) values(1,'2014-01-03 18:59:00+02');


--Device Table

insert into devices(user_id, udid, os, deleted, os_version) values(1,'12344','ios', False, '7.0');
insert into devices(user_id, udid, os, deleted, os_version) values(2,'34554','ios', False, '6.1.3');
insert into devices(user_id, udid, os, deleted, os_version) values(3,'3546246','ios', False, '6.4');
insert into devices(user_id, udid, os, deleted, os_version) values(4,'646536','ios', False, '7.1');
insert into devices(user_id, udid, os, deleted, os_version) values(5,'2525254','ios', False, '5.0');
insert into devices(user_id, udid, os, deleted, os_version) values(6,'5575764','ios', False, '4.0');
insert into devices(user_id, udid, os, deleted, os_version) values(7,'2532577','ios', False, '3.1');
insert into devices(user_id, udid, os, deleted, os_version) values(8,'7898968','ios', False, '5.6');
insert into devices(user_id, udid, os, deleted, os_version) values(9,'1234354544','ios', False, '6.0');
insert into devices(user_id, udid, os, deleted, os_version) values(10,'958343646','ios', False, '4.4');
insert into devices(user_id, udid, os, deleted, os_version) values(4,'89707946','android-touchwiz', False, '16');
insert into devices(user_id, udid, os, deleted, os_version) values(7,'357580353','android-touchwiz', False, '14');
insert into devices(user_id, udid, os, deleted, os_version) values(9,'976958485','android-touchwiz', False, '15');
insert into devices(user_id, udid, os, deleted, os_version) values(8,'24646426','android-touchwiz', False, '15');
insert into devices(user_id, udid, os, deleted, os_version) values(3,'21432675','android-touchwiz', False, '16');

--Enrollment Table

insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(1,1,'1234', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(2,2,'233', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(3,3,'143343234', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(4,4,'5354', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(5,5,'6565', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(6,6,'6556', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(7,7,'7676', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(8,8,'5665', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(9,9,'5666', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);
insert into enrollments(user_id, device_id, password, enrolled_on, sent_on, is_enrolled) values(10,10,'5656', '2014-01-03 18:50:00+02', '2014-01-03 18:50:00+02', True);

--Logs Table

insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('user', 1, 'info', NULL, 'Messaage is the real message', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('user', 2, 'warning', NULL, 'Messaage is the real message P2', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('role', 1, 'error', NULL, 'Messaage is the real message P3', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('role', 4, 'warning', NULL, 'Messaage is the real message P$', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('team', 2, 'info', NULL, 'Messaage is the real message P%', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('team', 3, 'error', NULL, 'Messaage is the real message P6', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('company', 1, 'error', NULL, 'Messaage is the real message P7', NULL, 1, '2014-01-08 18:20:00+02');
insert into logs(component_type, component_id, level, tag, message,raw, company_id, timestamp) values('company', 1, 'info', NULL, 'Messaage is the real message P8', NULL, 1, '2014-01-08 18:20:00+02');
