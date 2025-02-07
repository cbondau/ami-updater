import importlib
import json

from python.tests import override_config
override_config.set_ami_poller_config()

from python.tests.fixtures import *
from python import ami_poller


"""
Functions beginning with `test_` are detected and executed by pytest.

The parameters to each of the functions use things called fixtures, which are
sets of Python functions providing specific functionality. They are located in `fixtures.py`.

Each time a test executes, it may create a fixture from scratch, or use a cached one across tests.
This is determined by each fixture's `scope` argument.
"""


@pytest.mark.parametrize("configure", [["red_hat", "new", "prod", "ami_poller"]], indirect=True)
def test_no_schedule_is_created(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_poller)
    ami_poller.handler(event=test_inputs['ami_poller'], context={})

    assert mock_scheduler.list_schedules() == []


@pytest.mark.parametrize("configure", [["red_hat", "old", "prod", "ami_poller"]], indirect=True)
def test_prod_schedule_is_created_n_days_from_now(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_poller)
    ami_poller.handler(event=test_inputs['ami_poller'], context={})

    assert mock_scheduler.get_created_schedule_name() == test_outputs.prod_scheduler_name


@pytest.mark.parametrize("configure", [["red_hat", "old", "stg", "ami_poller"]], indirect=True)
def test_stg_schedule_is_created_zero_days_from_now(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_poller)
    ami_poller.handler(event=test_inputs['ami_poller'], context={})

    assert mock_scheduler.get_created_schedule_name() == test_outputs.stg_scheduler_name


"""
The test below does not work since Localstack's `scheduler.create_schedule()` only creates
the 'Arn' parameter and not the 'RoleArn' and 'Input' parameters.
Rename this with a future Localstack version.
"""
@pytest.mark.parametrize("configure", [["red_hat", "old", "stg", "ami_poller"]], indirect=True)
def __test_stg_existing_schedule_is_recreated(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_poller)
    ami_poller.handler(event=test_inputs['ami_poller'], context={})

    assert mock_scheduler.list_schedules()[0]['Name'] == test_outputs.stg_scheduler_name

    # Update the SSM parameter, and run the ami_poller again
    mock_ssm.update_parameter('ami-987654')
    ami_poller.handler(event=test_inputs['ami_poller'], context={})

    sched = mock_scheduler.list_schedules()[0]
    target_input = json.loads(sched['Target']['Input'])
    assert sched['Name'] == test_outputs.stg_scheduler_name
    assert target_input['ImageId'] == 'ami-987654'
