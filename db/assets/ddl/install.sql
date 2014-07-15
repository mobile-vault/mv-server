create table users( id serial primary key);
create table teams( id serial primary key);
create table roles( id serial primary key);
create table devices( id serial primary key);
create table violations( id serial primary key);
create table enrollments( id serial primary key);
create table policies( id serial primary key);
create table companies( id serial primary key);
create table logins( id serial primary key);
create table sessions( id serial primary key);
create table logs( id serial primary key);
create table ios_commands( id serial primary key);
create table admin_profile(id serial primary key);
CREATE TABLE device_details(id serial primary key);
CREATE TABLE samsung_commands(id serial primary key);


alter table admin_profile add column email text unique;
alter table admin_profile add column company_id integer references companies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table admin_profile add column login_id integer references logins(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table admin_profile add column name text;
alter table admin_profile add column created_on timestamp without time zone DEFAULT now();
alter table admin_profile add column modified_on timestamp without time zone DEFAULT now();
ALTER TABLE admin_profile ADD COLUMN deleted boolean DEFAULT true;


alter table device_details add column device_id integer references devices(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table device_details add column extras json;


alter table users add column email text unique;
alter table users add column name text;
alter table users add column role_id integer references roles(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table users add column team_id integer references teams(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table users add column policy_id integer references policies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table users add column company_id integer references companies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table users add column deleted boolean DEFAULT False;
alter table users add column created_on timestamp without time zone DEFAULT now();
alter table users add column modified_on timestamp without time zone DEFAULT now();
ALTER TABLE users ALTER COLUMN deleted SET DEFAULT false;


alter table teams add column name text;
alter table teams add column company_id integer references companies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table teams add column policy_id integer references policies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table teams add column deleted boolean DEFAULT False;
alter table teams add column created_on timestamp without time zone DEFAULT now();
alter table teams add column modified_on timestamp without time zone DEFAULT now();
ALTER TABLE teams ALTER COLUMN deleted SET DEFAULT false;


alter table devices add column name text;
alter table devices add column user_id integer references users(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table devices add column udid text;
alter table devices add column os text;
alter table devices add column deleted boolean DEFAULT False;
alter table devices add column os_version text;
alter table devices add column created_on timestamp without time zone DEFAULT now();
alter table devices add column modified_on timestamp without time zone DEFAULT now();
ALTER TABLE devices ALTER COLUMN deleted SET DEFAULT false;


alter table violations add column device_id integer references devices(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table violations add column timestamp timestamp without time zone DEFAULT now();
alter table violations add column deleted boolean DEFAULT False;


alter table enrollments add column user_id integer references users(id)  ON DELETE NO ACTION ON UPDATE CASCADE;
alter table enrollments add column device_id integer references devices(id)  ON DELETE NO ACTION ON UPDATE CASCADE;
alter table enrollments add column password text;
alter table enrollments add column enrolled_on timestamp without time zone DEFAULT now();
alter table enrollments add column sent_on timestamp without time zone DEFAULT now();
alter table enrollments add column is_enrolled boolean DEFAULT False;


alter table policies add column new_attributes json;
alter table policies add column old_attributes json;
alter table policies add column created_on timestamp without time zone DEFAULT now();
alter table policies add column modified_on timestamp without time zone DEFAULT now();
alter table policies add column deleted boolean DEFAULT False;


alter table roles add column name text;
alter table roles add column company_id integer references companies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table roles add column policy_id integer references policies(id) ON DELETE NO ACTION ON UPDATE CASCADE ;
alter table roles add column created_on timestamp without time zone DEFAULT now();
alter table roles add column modified_on timestamp without time zone DEFAULT now();
alter table roles add column deleted boolean DEFAULT False;


alter table companies add column name text;
alter table companies add column email text unique;
alter table companies add column address text;
alter table companies add column contact text;
alter table companies add column policy_id integer references policies(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table companies add column created_on timestamp without time zone DEFAULT now();
alter table companies add column modified_on timestamp without time zone DEFAULT now();
alter table companies add column deleted boolean DEFAULT true;


alter table logins add column password text;
alter table logins add column created_on timestamp without time zone DEFAULT now();
alter table logins add column modified_on timestamp without time zone DEFAULT now();
alter table logins add column deleted boolean DEFAULT False;


alter table sessions add column user_id integer references admin_profile(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table sessions add column created_on timestamp without time zone DEFAULT now();
alter table sessions add column destroyed_on timestamp without time zone DEFAULT now();
alter table sessions add column ip text;
alter table sessions add column invalid boolean;
alter table sessions add column user_agent text;


alter table logs add column component_type text;
alter table logs add column component_id integer;
alter table logs add column level text;
alter table logs add column tag text;
alter table logs add column message text;
alter table logs add column raw text;
alter table logs add column company_id integer references companies(id)  ON DELETE NO ACTION ON UPDATE CASCADE;
alter table logs add column timestamp timestamp without time zone DEFAULT now();


alter table ios_commands add column command_uuid text;
alter table ios_commands add column executed boolean;
alter table ios_commands add column device_id integer references devices(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table ios_commands add column action text;
alter table ios_commands add column result text;
alter table ios_commands add column attribute json;
alter table ios_commands add column sent_on timestamp without time zone DEFAULT now();
alter table ios_commands add column executed_on timestamp without time zone DEFAULT now();


alter table samsung_commands add column command_uuid text;
alter table samsung_commands add column device_id integer references devices(id) ON DELETE NO ACTION ON UPDATE CASCADE;
alter table samsung_commands add column executed boolean;
alter table samsung_commands add column action text;
alter table samsung_commands add column result text;
alter table samsung_commands add column attribute json;
alter table samsung_commands add column sent_on timestamp without time zone DEFAULT now();
alter table samsung_commands add column executed_on timestamp without time zone DEFAULT now();
-- drop table policies NO ACTION;
-- drop table users NO ACTION;
-- drop table teams NO ACTION;
-- drop table roles NO ACTION;
-- drop table devices NO ACTION;
-- drop table violations NO ACTION;
-- drop table enrollments NO ACTION;
-- drop table companies NO ACTION;
-- drop table logins NO ACTION;
--
-- drop table sessions NO ACTION;
-- drop table logs NO ACTION;
-- drop table device_details NO ACTION;
-- drop table ios_commands NO ACTION;
