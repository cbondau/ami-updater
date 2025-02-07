import os

"""
The functions below load the environment variables into the config.
This is used by the Lambda functions and Pytest tests.
They are called whenever the environment variables change, e.g.
through `from override_config import set_ami_poller_config`
"""


def load_ami_updater_config():
    return {
        **default_values(),
        'ami_ssm_parameter_name': os.environ['AMI_SSM_PARAMETER_NAME'],
        'env': os.environ['ENVIRONMENT'],
        'os_platform': os.environ['OS_PLATFORM'],
        'pipeline_name': os.environ['PIPELINE_NAME'],
        'pipeline_provider': os.environ['PIPELINE_PROVIDER'],  # CodePipeline | GitHub
        'source_aws_account_id': os.environ['SOURCE_AWS_ACCOUNT_ID'],
    }


def load_ami_poller_config():
    return {
        **default_values(),
        'ami_ssm_parameter_name': os.environ['AMI_SSM_PARAMETER_NAME'],
        'deployment_schedule_in_days': os.environ['DEPLOYMENT_SCHEDULE_IN_DAYS'],
        'env': os.environ['ENVIRONMENT'],
        'lambda_ami_updater_role_arn': os.environ['LAMBDA_AMI_UPDATER_ROLE_ARN'],
        'lambda_ami_updater_function_arn': os.environ['LAMBDA_AMI_UPDATER_FUNCTION_ARN'],
        'os_platform': os.environ['OS_PLATFORM'],
        'source_aws_account_id': os.environ['SOURCE_AWS_ACCOUNT_ID'],
    }


def default_values():
    return {
        'is_local': os.environ.get('LOCAL') == '1',

        # Point boto3 at Localstack if running locally; otherwise use AWS
        'endpoint_url': 'http://localhost:4566' if os.environ.get('LOCAL') == '1' else None,

        # SSM parameter names
        'platforms': {
            'red_hat': {
                'ssm_parameter': '/cba-soe/ami-rhel-8-latest',
            },
            'windows_core': {
                'ssm_parameter': '/cba-soe/ami-windows2019core-latest',
            },
            'windows_desktop': {
                'ssm_parameter': '/cba-soe/ami-windows2019desktop-latest',
            },
        }
    }


config = {
    **default_values(),
}
