import importlib

from python.tests import override_config
override_config.set_ami_updater_config()

from python.tests.fixtures import *
from python import ami_updater


@pytest.mark.parametrize("configure", [["red_hat", "new", "prod", "ami_updater"]], indirect=True)
def test_ssm_has_latest_ami(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_updater)
    os = 'red_hat'
    ami_updater.handler(event=test_inputs['ami_updater'][os], context=C)

    assert mock_ssm.get_ssm_parameter_value() == override_config.amis[os]['new']['image_id']


@pytest.mark.parametrize("configure", [["red_hat", "old", "prod", "ami_updater"]], indirect=True)
def test_ssm_is_updated_with_new_ami_red_hat(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_updater)
    os ='red_hat'
    ami_updater.handler(event=test_inputs['ami_updater'][os], context=C)

    assert mock_ssm.get_ssm_parameter_value() == override_config.amis[os]['new']['image_id']



@pytest.mark.parametrize("configure", [["windows_core", "old", "prod", "ami_updater"]], indirect=True)
def test_ssm_is_updated_with_new_ami_windows_core(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_updater)
    os = 'windows_core'
    ami_updater.handler(event=test_inputs['ami_updater'][os], context=C)

    assert mock_ssm.get_ssm_parameter_value() == override_config.amis[os]['new']['image_id']


@pytest.mark.parametrize("configure", [["windows_desktop", "old", "prod", "ami_updater"]], indirect=True)
def test_ssm_is_updated_with_new_ami_windows_desktop(configure, mock_ssm, mock_scheduler, test_inputs, test_outputs):
    importlib.reload(ami_updater)
    os = 'windows_desktop'
    ami_updater.handler(event=test_inputs['ami_updater'][os], context=C)

    assert mock_ssm.get_ssm_parameter_value() == override_config.amis[os]['new']['image_id']


class C:
    # Simulates Lambda's `context` parameter
    invoked_function_arn = 'abc'
