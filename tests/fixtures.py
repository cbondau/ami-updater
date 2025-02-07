import pytest
from python.tests.mock import ec2, ssm, scheduler
from python.tests.data.inputs import eventbridge_events
from python.tests.data.outputs import values
from python.tests import override_config
# from python import ami_updater

ssm_mocker = ssm.SSM()
ec2_mocker = ec2.EC2()
scheduler_mocker = scheduler.Scheduler()

"""
The scope of each fixture below determines the stage at which it runs.
For example, scope='module' means that the function runs once per set of
tests in a single Python module.

The `configure_platform` sets the platform based on the `params` argument.
All other functions then base their configuration off this value.

The `autouse` tells pytest to automatically include the fixture in each test.
"""


@pytest.fixture(scope='function')
def configure(request):
    print('configuring test with:', request.param)
    platform, ami_age, env, func = request.param

    override_config.current_platform = platform
    override_config.ami_age = ami_age
    override_config.env = env
    override_config.set_function_config(func)


@pytest.fixture(scope='module')
def test_inputs():
    return {
        'ami_poller': eventbridge_events.get_ami_poller_payload(),
        'ami_updater': {platform: eventbridge_events.get_ami_updater_payload(platform) for platform in ['red_hat', 'windows_core', 'windows_desktop']
        }
    }


@pytest.fixture(scope='module')
def test_outputs():
    return values


# @pytest.fixture(scope='function')
# def mock_ec2(request):
#     ec2_mocker.configure_stubber(boto_client=ami_updater.ec2_client)
#     return ec2_mocker


@pytest.fixture(scope='module')
def mock_ssm_module_level(request):
    """
    Runs once per module; initialises the shared SSM params.

    :param request:
    :return:
    """
    ssm_mocker.create_shared_parameters()

    def clean_up():
        ssm_mocker.delete_shared_parameters()

    # Runs at the end of each test
    request.addfinalizer(clean_up)
    yield ssm_mocker


@pytest.fixture(scope='function')
def mock_ssm(request, mock_ssm_module_level):
    ssm_mocker.create_parameter()

    def clean_up():
        ssm_mocker.delete_parameter()

    # Runs at the end of each test
    request.addfinalizer(clean_up)
    yield ssm_mocker


@pytest.fixture(scope='function')
def mock_scheduler(request):
    def clean_up():
        scheduler_mocker.delete_schedules()

    request.addfinalizer(clean_up)
    yield scheduler_mocker
