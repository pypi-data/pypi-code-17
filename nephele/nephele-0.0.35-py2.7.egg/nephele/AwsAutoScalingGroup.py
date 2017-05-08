from AwsProcessor import *
from awsHelpers.AwsConnectionFactory import AwsConnectionFactory
from CommandArgumentParser import *
from joblib import Parallel, delayed

import boto3
import stdplus

class AwsAutoScalingGroup(AwsProcessor):
    def __init__(self,scalingGroup,parent):
        AwsProcessor.__init__(self,parent.raw_prompt + "/asg:" + scalingGroup,parent)
        self.client = AwsConnectionFactory.getAsgClient()
        self.scalingGroup = scalingGroup
        
        self.do_printInstances('-r')
        
    def do_printInstances(self,args):
        """Print the list of instances in this auto scaling group. printInstances -h for detailed help"""
        parser = CommandArgumentParser("stack")
        parser.add_argument(dest='filters',nargs='*',default=["*"],help='Filter instances');
        parser.add_argument('-a','--addresses',action='store_true',dest='addresses',help='list all ip addresses');
        parser.add_argument('-t','--tags',action='store_true',dest='tags',help='list all instance tags');
        parser.add_argument('-d','--allDetails',action='store_true',dest='details',help='print all instance details');
        parser.add_argument('-r','--refresh',action='store_true',dest='refresh',help='refresh');
        args = vars(parser.parse_args(args))
        filters = args['filters']
        
        client = AwsConnectionFactory.getEc2Client()
        addresses = args['addresses']
        tags = args['tags']
        details = args['details']
        needDescription = addresses or tags or details

        if args['refresh']:
            self.scalingGroupDescription = self.client.describe_auto_scaling_groups(AutoScalingGroupNames=[self.scalingGroup])
        
        # print "AutoScaling Group:{}".format(self.scalingGroup)
        print "=== Instances ==="
        instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']

        instances = filter( lambda x: fnmatches(x['InstanceId'],filters),instances)
        
        index = 0
        for instance in instances:
            print "* {0:3d} {1} {2} {3}".format(index,instance['HealthStatus'],instance['AvailabilityZone'],instance['InstanceId'])
            description = None
            if needDescription:
                description = client.describe_instances(InstanceIds=[instance['InstanceId']])
            if addresses:
                networkInterfaces = description['Reservations'][0]['Instances'][0]['NetworkInterfaces']
                number = 0
                print "      Network Interfaces:"
                for interface in networkInterfaces:
                    print "         * {0:3d} {1}".format(number, interface['PrivateIpAddress'])
                    number +=1
            if tags:
                tags = description['Reservations'][0]['Instances'][0]['Tags']
                print "      Tags:"
                for tag in tags:
                    print "        * {0} {1}".format(tag['Key'],tag['Value'])
            if details:
                pprint(description)
                
            index += 1

    def do_rebootInstance(self,args):
        """Restart specified instance"""
        parser = CommandArgumentParser("rebootInstance")
        parser.add_argument(dest='instance',help='instance index or name');
        args = vars(parser.parse_args(args))

        instanceId = args['instance']
        try:
            index = int(instanceId)
            instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
            instanceId = instances[index]
        except ValueError:
            pass

        client = AwsConnectionFactory.getEc2Client()
        client.reboot_instances(InstanceIds=[instanceId['InstanceId']])

        
    def do_setDesiredCapacity(self,args):
        """Set the desired capacity"""
        parser = CommandArgumentParser("setDesiredCapacity")
        parser.add_argument(dest='value',type=int,help='new value');
        args = vars(parser.parse_args(args))

        value = int(args['value'])
        print "Setting desired capacity to {}".format(value)
        client = AwsConnectionFactory.getAsgClient()
        client.set_desired_capacity(AutoScalingGroupName=self.scalingGroup,DesiredCapacity=value,HonorCooldown=True)
        print "Scaling activity in progress"

    def do_run(self,args):
        """SSH to each instance in turn and run specified command"""
        parser = CommandArgumentParser("run")
        parser.add_argument('-R','--replace-key',dest='replaceKey',default=False,action='store_true',help="Replace the host's key. This is useful when AWS recycles an IP address you've seen before.")
        parser.add_argument('-Y','--keyscan',dest='keyscan',default=False,action='store_true',help="Perform a keyscan to avoid having to say 'yes' for a new host. Implies -R.")
        parser.add_argument(dest='command',nargs='+',help="Command to run on all hosts.") # consider adding a filter option later
        parser.add_argument('-v',dest='verbosity',default=0,action=VAction,nargs='?',help='Verbosity. The more instances, the more verbose');        
        parser.add_argument('-j',dest='jobs',type=int,default=1,help='Number of hosts to contact in parallel');        
        args = vars(parser.parse_args(args))

        replaceKey = args['replaceKey']
        keyscan = args['keyscan']
        verbosity = args['verbosity']
        jobs = args['jobs']

        instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
        # if replaceKey or keyscan:
        #     for instance in instances:
        #         stdplus.resetKnownHost(instance)
        
        Parallel(n_jobs=jobs)(
            delayed(ssh)(instance['InstanceId'],0,[],replaceKey,keyscan,False,verbosity," ".join(args['command'])) for instance in instances
        )
        
    def do_ssh(self,args):
        """SSH to an instance. ssh -h for detailed help"""
        parser = CommandArgumentParser("ssh")
        parser.add_argument(dest='instance',help='instance index or name');
        parser.add_argument('-a','--address-number',default='0',dest='interface-number',help='instance id of the instance to ssh to');
        parser.add_argument('-L',dest='forwarding',nargs='*',help="port forwarding string of the form: {localport}:{host-visible-to-instance}:{remoteport} or {port}")
        parser.add_argument('-R','--replace-key',dest='replaceKey',default=False,action='store_true',help="Replace the host's key. This is useful when AWS recycles an IP address you've seen before.")
        parser.add_argument('-Y','--keyscan',dest='keyscan',default=False,action='store_true',help="Perform a keyscan to avoid having to say 'yes' for a new host. Implies -R.")
        parser.add_argument('-B','--background',dest='background',default=False,action='store_true',help="Run in the background. (e.g., forward an ssh session and then do other stuff in aws-shell).")
        parser.add_argument('-v',dest='verbosity',default=0,action=VAction,nargs='?',help='Verbosity. The more instances, the more verbose');        
        args = vars(parser.parse_args(args))

        interfaceNumber = int(args['interface-number'])
        forwarding = args['forwarding']
        replaceKey = args['replaceKey']
        keyscan = args['keyscan']
        background = args['background']
        verbosity = args['verbosity']
        try:
            index = int(args['instance'])
            instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
            instance = instances[index]
            ssh(instance['InstanceId'],interfaceNumber,forwarding,replaceKey,keyscan,background,verbosity)
        except ValueError:
            ssh(args['instance'],interfaceNumber,forwarding,replaceKey,keyscan,background)

    def do_startInstance(self,args):
        """Start specified instance"""
        parser = CommandArgumentParser("startInstance")
        parser.add_argument(dest='instance',help='instance index or name');
        args = vars(parser.parse_args(args))

        instanceId = args['instance']
        force = args['force']
        try:
            index = int(instanceId)
            instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
            instanceId = instances[index]
        except ValueError:
            pass

        client = AwsConnectionFactory.getEc2Client()
        client.start_instances(InstanceIds=[instanceId['InstanceId']])
            
    def do_stopInstance(self,args):
        """Stop specified instance"""
        parser = CommandArgumentParser("stopInstance")
        parser.add_argument(dest='instance',help='instance index or name');
        parser.add_argument('-f','--force',action='store_true',dest='force',help='instance index or name');
        args = vars(parser.parse_args(args))

        instanceId = args['instance']
        force = args['force']
        try:
            index = int(instanceId)
            instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
            instanceId = instances[index]
        except ValueError:
            pass

        client = AwsConnectionFactory.getEc2Client()
        client.stop_instances(InstanceIds=[instanceId['InstanceId']],Force=force)
            
    def do_terminateInstance(self,args):
        """Terminate an EC2 instance"""
        parser = CommandArgumentParser("terminateInstance")
        parser.add_argument(dest='instance',help='instance index or name');
        args = vars(parser.parse_args(args))

        instanceId = args['instance']
        try:
            index = int(instanceId)
            instances = self.scalingGroupDescription['AutoScalingGroups'][0]['Instances']
            instanceId = instances[index]
        except ValueError:
            pass

        client = AwsConnectionFactory.getEc2Client()
        client.terminate_instances(InstanceIds=[instanceId['InstanceId']])
        self.do_printInstances("-r")
            
    def do_updateCapacity(self,args):
        """Set the desired capacity"""
        parser = CommandArgumentParser("updateMinMax")
        parser.add_argument('-m','--min',dest='min',type=int,help='new values');
        parser.add_argument('-M','--max',dest='max',type=int,help='new values');
        parser.add_argument('-d','--desired',dest='desired',type=int,help='desired');
        args = vars(parser.parse_args(args))

        minSize = args['min']
        maxSize = args['max']
        desired = args['desired']
        
        print "Setting desired capacity to {}-{}, {}".format(minSize,maxSize,desired)
        client = AwsConnectionFactory.getAsgClient()
        client.update_auto_scaling_group(AutoScalingGroupName=self.scalingGroup,MinSize=minSize,MaxSize=maxSize,DesiredCapacity=desired)
        #client.set_desired_capacity(AutoScalingGroupName=self.scalingGroup,DesiredCapacity=value,HonorCooldown=True)
        print "Scaling activity in progress"
            
