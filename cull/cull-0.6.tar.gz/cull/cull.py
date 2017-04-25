import fire
import boto3

EC2 = boto3.resource('ec2')


class Cull(object):
    def ec2(self, cloud, service):
        """
        Parse EC2 instances
        
        :param cloud: String 
        :param service: String
        :return: None
        """

        filters = [{'Name': 'tag:Name', 'Values': ["{0}_{1}_*".format(cloud, service)]}]

        instance_names = [tag['Value'] for instance in EC2.instances.filter(Filters=filters) for tag in instance.tags if
                          tag['Key'] == 'Name']

        instance_ips = [instance.private_ip_address for instance in EC2.instances.filter(Filters=filters)]

        for index, name in enumerate(instance_names):
            print "Name:", name, "ssh://ubuntu@" + instance_ips[index]


def main():
    fire.Fire(Cull)


if __name__ == '__main__':
    main()
