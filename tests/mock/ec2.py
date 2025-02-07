from botocore.stub import Stubber, ANY
from python.tests import override_config


class EC2:
    def __init__(self):
        self.stubber = None

    def override_configure_stubber(self, boto_client):
        """
        Mocks the response returned from ec2.describe_images() since Localstack
        doesn't provide an easy way to create dummy AMI values.

        This uses boto's built-in feature to stub a method with a method of or own,
        which simply returns a hard-coded response depending on the AMI's platform type.

        :return:
        """
        print('override_configuring EC2 stub function with dummy params and response.')
        self.stubber = Stubber(boto_client)

        # ANY indicates to boto that any parameter value is accepted
        expected_params = {'ImageIds': [ANY]}
        expected_response = self.describe_images_dummy()

        # Each call pops it from the boto stack.
        # Calls execute in a FIFO order.
        self.stubber.add_response(
            method='describe_images',
            expected_params=expected_params,
            service_response=expected_response,
        )

    def describe_images_dummy(self):
        return {
            "Images": [
                self.dummy_response(override_config.amis['red_hat']['old']),
                self.dummy_response(override_config.amis['red_hat']['new']),
                self.dummy_response(override_config.amis['windows_core']['old']),
                self.dummy_response(override_config.amis['windows_core']['new']),
                self.dummy_response(override_config.amis['windows_desktop']['old']),
                self.dummy_response(override_config.amis['windows_desktop']['new']),
            ]
        }

    def dummy_response(self, details):
        return {
            "Platform": details['platform'],
            "Name": details['name'],
            "ImageId": details['image_id'],
            "Architecture": "x86_64",
            "CreationDate": "2024-05-03T13:52:29.000Z",
            "ImageLocation": "amazon/getting-started",
            "ImageType": "machine",
            "Public": True,
            "KernelId": "None",
            "OwnerId": "000000000000",
            "RamdiskId": "ari-1a2b3c4d",
            "State": "available",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "DeleteOnTermination": False,
                        "SnapshotId": "snap-3afd59ed",
                        "VolumeSize": 15,
                        "VolumeType": "standard"
                    }
                }
            ],
            "Description": "Something",
            "Hypervisor": "xen",
            "ImageOwnerAlias": "Unknown",
            "RootDeviceName": "/dev/sda1",
            "RootDeviceType": "ebs",
            "Tags": [],
            "VirtualizationType": "hvm"
        }
