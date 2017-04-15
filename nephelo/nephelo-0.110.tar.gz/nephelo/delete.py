import os
import boto3

def deleteStack(config, stage):
    regions = config.get("regions")
    stack_name = stage + config.get("project")
    for region in regions:
        cloudformation = boto3.client('cloudformation', region_name=region)
        cloudformation.delete_stack(
            StackName=stack_name
        )
    return None