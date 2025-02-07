from python.tests import override_config


def get_ami_poller_payload():
    return {
        "version": "0",
        "id": "0fcc021b-5298-e4f2-493c-ccf9f9e25a8d",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "account": "foo",
        "time": "2023-08-24T10:00:00Z",
        "region": "ap-southeast-2",
        "resources": [
            "arn:aws:events:ap-southeast-2::rule/some-scheduled-rule"
        ],
        "detail": {}
    }


def get_ami_updater_payload(platform):
    return {
        "ImageId": override_config.amis[platform]['new']['image_id']
    }
