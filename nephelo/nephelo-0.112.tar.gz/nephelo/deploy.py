import boto3
import os
s3 = boto3.client('s3', region_name="us-east-1")

def deploy(config, stage):
    regions = config.get("regions")
    stack_name = stage + config.get("project")
    bucket_name = config.get("bucket_name")

    # check if the bucket exists in the account and if it doesn't then create it
    getBucket(bucket_name)

    # transfer the distribution files to the bucket
    uploaded_files = uploadDistFiles(bucket_name, stack_name, stage)
    print uploaded_files
    stacks = []
    notification_arns = config.get("notification_arns", [])
    role_arn = config.get("role_arn")
    for region in regions:
        cloudformation = boto3.client('cloudformation', region_name=region)

        # check if the stack exists in this region
        disablerollback = config.get("disable_rollback", False)
        try:
            cloudformation.describe_stacks(
                StackName=stack_name
            )
            if role_arn is None:
                stack_details = cloudformation.update_stack(
                    StackName=stack_name,
                    TemplateURL="http://" + bucket_name + ".s3.amazonaws.com/" + stack_name + "/" + stage + "/" + region + ".json",
                    NotificationARNs=notification_arns
                )
            else:
                stack_details = cloudformation.update_stack(
                    StackName=stack_name,
                    TemplateURL="http://" + bucket_name + ".s3.amazonaws.com/" + stack_name + "/" + stage + "/" + region + ".json",
                    NotificationARNs=notification_arns,
                    RoleARN=role_arn
                )
            # The stack exists, we need to try and update the stack
            stacks.append(stack_details.get("StackId"))
        except Exception as e:
            print "CloudFormation Exception"
            print e
            # The stack doesn't exist, so we need to create it
            if role_arn is None:
                stack_details = cloudformation.create_stack(
                    StackName=stack_name,
                    TemplateURL="http://" + bucket_name + ".s3.amazonaws.com/" + stack_name + "/" + stage + "/" + region + ".json",
                    DisableRollback=disablerollback,
                    NotificationARNs=notification_arns
                )
            else:
                stack_details = cloudformation.create_stack(
                    StackName=stack_name,
                    TemplateURL="http://" + bucket_name + ".s3.amazonaws.com/" + stack_name + "/" + stage + "/" + region + ".json",
                    DisableRollback=disablerollback,
                    NotificationARNs=notification_arns,
                    RoleARN=role_arn
                )
            stacks.append(stack_details.get("StackId"))


    return stack_details


def getBucket(bucket_name):
    try:
        s3.head_bucket(
            Bucket=bucket_name
        )
    except Exception as e:
        print "Exception"
        print e
        s3.create_bucket(
            ACL="private",
            Bucket=bucket_name
        )
    return bucket_name


def uploadDistFiles(bucket_name, stack_name, stage):
    files_to_upload = []
    for level in os.walk("./dist"):
        for filename in level[2]:
            filepath = level[0]
            if filepath[-1] != "/":
                filepath += "/"
            files_to_upload.append(filepath + filename)
    for file in files_to_upload:
        s3.upload_file(file, bucket_name, stack_name + "/" + file.replace("./dist/", ""))
    uploaded_files = map(lambda x: stack_name + "/" + x, files_to_upload)
    return uploaded_files
