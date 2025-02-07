import os

current_ssm_parameter_name = '/current/ami/id'
codepipeline_name = 'example-pipeline'

# Set by fixtures.py during tests
current_platform = ''  # red_hat | windows
ami_age = ''           # new | old
env = ''


def set_function_config(function):
    if function == 'ami_poller':
        set_ami_poller_config()
    elif function == 'ami_updater':
        set_ami_updater_config()
    else:
        print(f'ERROR - no such function: {function}')
        exit(1)


def set_ami_poller_config():
    """
    Variables used by `ami_poller.py`
    :return:
    """
    os.environ['AMI_SSM_PARAMETER_NAME'] = current_ssm_parameter_name
    os.environ['LOCAL'] = '1'  # Configures the Lambda to use Localstack
    os.environ['ENVIRONMENT'] = env
    os.environ['DEPLOYMENT_SCHEDULE_IN_DAYS'] = '8' if env == 'prod' else '0'
    os.environ['LAMBDA_AMI_UPDATER_ROLE_ARN'] = 'arn:aws:iam::123456789012:role/service-role/some-iam-role'
    os.environ['LAMBDA_AMI_UPDATER_FUNCTION_ARN'] = 'arn:aws:lambda:ap-southeast-2:123456789012:function:ami-updater'
    os.environ['OS_PLATFORM'] = current_platform
    os.environ['SOURCE_AWS_ACCOUNT_ID'] = '000000000000'


def set_ami_updater_config():
    """
    Variables used by `ami_updater.py`
    :return:
    """
    os.environ['AMI_SSM_PARAMETER_NAME'] = current_ssm_parameter_name
    os.environ['LOCAL'] = '1'  # Configures the Lambda to use Localstack
    os.environ['ENVIRONMENT'] = env
    os.environ['OS_PLATFORM'] = current_platform
    os.environ['PIPELINE_NAME'] = codepipeline_name
    os.environ['PIPELINE_PROVIDER'] = 'CodePipeline'
    os.environ['SOURCE_AWS_ACCOUNT_ID'] = '000000000000'


amis = {
    'red_hat': {
        'parameter': '/cba-soe/ami-rhel-8-latest',
        'old': {
            'platform': 'Red Hat Enterprise Linux',
            'name': 'CNS-AWS-RHEL-8-2024-W14-12-34-45-67',
            'image_id': 'ami-rhel-old-123',
        },
        'new': {
            'platform': 'Red Hat Enterprise Linux',
            'name': 'CNS-AWS-RHEL-8-2024-W14-87-65-43-21',
            'image_id': 'ami-rhel-new-456',
        }
    },
    'windows_desktop': {
        'parameter': '/cba-soe/ami-windows2019desktop-latest',
        'old': {
            'platform': 'Windows',
            'name': 'CNS-AWS-WINDOWS-DESKTOP-19-2024-W08-12-34-45-67',
            'image_id': 'ami-win-desktop-old-123',
        },
        'new': {
            'platform': 'Windows',
            'name': 'CNS-AWS-WINDOWS-DESKTOP-19-2024-W08-87-65-43-21',
            'image_id': 'ami-win-desktop-new-456',
        }
    },
    'windows_core': {
        'parameter': '/cba-soe/ami-windows2019core-latest',
        'old': {
            'platform': 'Windows',
            'name': 'CNS-AWS-WINDOWS-CORE-19-2024-W08-12-34-45-67',
            'image_id': 'ami-win-core-old-123',
        },
        'new': {
            'platform': 'Windows',
            'name': 'CNS-AWS-WINDOWS-CORE-19-2024-W08-87-65-43-21',
            'image_id': 'ami-win-core-new-456',
        }
    }
}
