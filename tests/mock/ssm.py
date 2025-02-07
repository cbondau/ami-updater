import boto3
from python.tests import override_config

client = boto3.client('ssm', endpoint_url='http://localhost:4566')


class SSM:
    def __init__(self):
        self.parameter_name = override_config.current_ssm_parameter_name

    def create_parameter(self):
        platform = override_config.current_platform
        ami_age = override_config.ami_age
        name = self.parameter_name
        value = override_config.amis[platform][ami_age]['image_id']
        print(f'Creating SSM parameter: {name} with value: {value}')
        client.put_parameter(
            Name=name,
            Value=value,
            Type='String',
            Overwrite=True,
        )

    def create_shared_parameters(self):
        for os_version, cfg in override_config.amis.items():
            name = cfg['parameter']
            value = cfg['new']['image_id']
            print(f'Creating SSM parameter: {name} with value: {value}')
            client.put_parameter(
                Name=name,
                Value=value,
                Type='String',
                Overwrite=True,
            )

    def delete_shared_parameters(self):
        for os_version, cfg in override_config.amis.items():
            parameter = cfg['parameter']
            print(f'Deleting SSM parameter: {parameter}')
            client.delete_parameter(Name=parameter)

    def delete_parameter(self):
        print(f'Deleting SSM parameter: {self.parameter_name}')
        client.delete_parameter(Name=self.parameter_name)

    def get_ssm_parameter_value(self):
        response = client.get_parameter(Name=self.parameter_name)
        return response['Parameter']['Value']

    def update_parameter(self, value):
        print(f'Updating SSM parameter: {self.parameter_name}')
        client.put_parameter(
            Name=self.parameter_name,
            Value=value,
            Type='String',
            Overwrite=True,
        )
