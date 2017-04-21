from AwsProcessor import AwsProcessor
from awsHelpers.AwsConnectionFactory import AwsConnectionFactory

from pprint import pprint

class AwsLogGroup(AwsProcessor):
    def __init__(self,stackResource,parent):
        """Construct an AwsLogGroup command processor"""
        AwsProcessor.__init__(self,parent.raw_prompt + "/logGroup:" + stackResource.logical_id,parent)
        self.stackResource = stackResource
        self.logStreamNamePrefix = None
        self.orderBy = 'LogStreamName'
        self.descending = False
        self.do_refresh('')

    def do_refresh(self,args):
        """Refresh the view of the log group"""
        # prints all the groups: pprint(AwsConnectionFactory.getLogClient().describe_log_groups())

        response = AwsConnectionFactory.getLogClient().describe_log_groups(logGroupNamePrefix=self.stackResource.physical_resource_id)
        if not 'logGroups' in response:
            raise Exception("Expected log group description to have logGroups entry. Got {}".format(response))

        # pprint(response)
        descriptions = [x for x in response['logGroups'] if x['logGroupName'] == self.stackResource.physical_resource_id]
        if not descriptions:
            raise Exception("Could not find log group {} in list {}".format(self.stackResource.physical_resource_id,response['logGroups']))

        self.description = descriptions[0]
        
        self.logStreamsResponse = AwsConnectionFactory.getLogClient().describe_log_streams(logGroupName=self.stackResource.physical_resource_id,
                                                                                           #logStreamNamePrefix=self.logStreamNamePrefix,
                                                                                           orderBy=self.orderBy,
                                                                                           descending=self.descending)
        
        print "stackResource: {}".format(self.stackResource)
        print "description: {}".format(self.description)
        print "== log streams"
        pprint(self.logStreamsResponse)
