def getInstanceIds(asgClient,asgName):
    asgDescription = asgClient.describe_auto_scaling_groups(AutoScalingGroupNames=[asgName])
    if asgDescription['AutoScalingGroups'] and asgDescription['AutoScalingGroups'][0]:
        instances = asgDescription['AutoScalingGroups'][0]['Instances']
        instanceIds = []
        for instance in instances:
            instanceIds.append(instance['InstanceId'])
        return instanceIds
    else:
        return []    
