import boto3
from python.tests import config

client = boto3.client('codepipeline', endpoint_url='http://localhost:4566')

"""
NOTICE
------
This service is not yet implemented by Localstack.
See https://docs.localstack.cloud/references/coverage
"""

class CodePipeline:
    def __init__(self):
        self.pipeline_name = config.codepipeline_name

    def create_pipeline(self):
        print("Creating CodePipeline pipeline.")

        # This example is taken from `aws codepipeline create-pipeline help`
        client.create_pipeline(
            pipeline={
                "name": self.pipeline_name,
                "roleArn": "arn:aws:iam::111111111111:role/AWS-CodePipeline-Service",
                "stages": [
                    {
                        "name": "Source",
                        "actions": [
                            {
                                "inputArtifacts": [],
                                "name": "Source",
                                "actionTypeId": {
                                    "category": "Source",
                                    "owner": "AWS",
                                    "version": "1",
                                    "provider": "S3"
                                },
                                "outputArtifacts": [
                                    {
                                        "name": "MyApp"
                                    }
                                ],
                                "configuration": {
                                    "S3Bucket": "awscodepipeline-demo-bucket",
                                    "S3ObjectKey": "aws-codepipeline-s3-aws-codedeploy_linux.zip"
                                },
                                "runOrder": 1
                            }
                        ]
                    },
                    {
                        "name": "Beta",
                        "actions": [
                            {
                                "inputArtifacts": [
                                    {
                                        "name": "MyApp"
                                    }
                                ],
                                "name": "CodePipelineDemoFleet",
                                "actionTypeId": {
                                    "category": "Deploy",
                                    "owner": "AWS",
                                    "version": "1",
                                    "provider": "CodeDeploy"
                                },
                                "outputArtifacts": [],
                                "configuration": {
                                    "ApplicationName": "CodePipelineDemoApplication",
                                    "DeploymentGroupName": "CodePipelineDemoFleet"
                                },
                                "runOrder": 1
                            }
                        ]
                    }
                ],
                "artifactStore": {
                    "type": "S3",
                    "location": "codepipeline-us-east-1-11EXAMPLE11"
                },
                "version": 1
            }
        )

    def delete_pipeline(self):
        print(f'Deleting CodePipeline pipeline: {self.pipeline_name}')
        client.delete_pipeline(Name=self.pipeline_name)

    def list_pipelines(self):
        return client.list_pipelines()['pipelines']
