from __future__ import absolute_import

from os.path import abspath, dirname
from sys import path

from celery import Celery

from vendor.command_controller.command_handler import CommandPerformer

celery = Celery('tasks', broker="amqp://guest:guest@localhost:5672")

'''
@celery.task
def create_ios_task(json_dict, device_id, device_udid):
#    Assigning tasks to ios command for notification or polling purpose only.

    command_instance = ios_command.IosCommand()
    print " starting the task execution by calling the method\n"
    command_instance.execute(json_dict, device_id, device_udid)
    print 'Execution completed\n'


@celery.task
def create_android_task(json_dict, device_id):
 #   Assigning tasks to Android Command handler to send commands to devices.

    command_instance = android_command.AndroidCommand()
    print " starting the task execution by calling the method"
    command_instance.execute(json_dict, device_id)
    print 'Execution completed'
'''

@celery.task
def create_command_handler_task(policy_dict):
    '''
    Assigning tasks to command performer class
    '''
    print " starting the task execution by calling the method \n"
    print 'printing the policy dict here \n', policy_dict
    CommandPerformer(policy_dict).perform()
    print 'Execution completed \n'
