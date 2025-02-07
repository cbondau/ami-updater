import boto3
from python.tests import override_config
from python.tests.data.outputs import values

client = boto3.client('scheduler', endpoint_url='http://localhost:4566')


class Scheduler:
    def __init__(self):
        pass

    def delete_schedules(self):
        print(f'Deleting Scheduler schedules.')
        for sched in [values.prod_scheduler_name, values.stg_scheduler_name]:
            try:
                # Listing and deleting takes 2 seconds from some reason
                client.delete_schedule(Name=sched)
            except Exception as e:
                pass

    def get_created_schedule_name(self):
        response = client.list_schedules()['Schedules']
        if len(response) > 0:
            return response[0]['Name']
        else:
            return None

    def list_schedules(self):
        return client.list_schedules()['Schedules']
