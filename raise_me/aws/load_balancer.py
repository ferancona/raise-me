import boto3


class AWSLoadBalancer:
    def __init__(self, boto_session=None) -> None:
        self.session = (boto_session if boto_session is not None 
            else boto3.Session())
        self.client = self.session.client("elb")

    def describe_load_balancers(self):
        paginator = self.client.get_paginator('describe_load_balancers')
        return [load_balancer 
            for response in paginator.paginate()
            for load_balancer in response['LoadBalancerDescriptions']]
    
    @classmethod
    def format_lb_to_arn(self, name, region=None, account_id=None):
        region = (region if region is not None 
            else boto3.Session().region_name)
        account_id = (account_id if account_id is not None 
            else boto3.client('sts').get_caller_identity()['Account'])
        return 'arn:aws:elasticloadbalancing:{}:{}:loadbalancer/{}'.format(
            region, # ? Perhaps use 'raise-config.yaml'.
            account_id,
            name)