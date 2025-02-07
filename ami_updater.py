# Author: Callum Bond
# Description: Checks `ami-id` SSM parameter and replaces it with newest matching AMI, then triggers app CodePipeline build

"""
Lambda 2: SSM updater + pipeline triggerer
- Copy the value for the appropriate OS type into our own SSM parameter copy.
- Trigger a CodePipeline/GitHub Actions pipeline
"""

import boto3
import json

from python.shared.config import load_ami_updater_config
config = load_ami_updater_config()

ssm_client = boto3.client('ssm', endpoint_url=config['endpoint_url'])
codepipeline_client = boto3.client('codepipeline', endpoint_url=config['endpoint_url'])


def handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    new_ami_id = event['ImageId']
    update_ami_id_ssm_param(new_ami_id)
    trigger_deployment()


def update_ami_id_ssm_param(new_ami_id):
    """
    Update the SSM param with the newest matching AMI ID.
    """
    print(f"Updating SSM parameter: {config['ami_ssm_parameter_name']} with new AMI ID: {new_ami_id}")
    ssm_client.put_parameter(
        Name=config['ami_ssm_parameter_name'],
        Value=new_ami_id,
        Type='String',
        Overwrite=True,
    )


def trigger_deployment():
    if config['pipeline_provider'] == 'CodePipeline':
        print('Triggering CodePipeline deployment.')
        if config['is_local']:
            # CodePipeline is not yet implemented in Localstack.
            return
        codepipeline_client.start_pipeline_execution(name=config['pipeline_name'])
    elif config['pipeline_provider'] == 'GitHub':
        pass
