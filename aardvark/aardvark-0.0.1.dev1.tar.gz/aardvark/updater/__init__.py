from aardvark import create_app
from cloudaux.aws.iam import list_roles
from cloudaux.aws.sts import boto3_cached_conn
import requests
import json
import os
import urllib
import subprocess

federation_base_url = 'https://signin.aws.amazon.com/federation'


def update_account(account_number, role_name, arns):
    """
    Updates Access Advisor data for a given AWS account.
    
    1) Gets list of IAM Role ARNs in target account.
    2) Gets IAM credentials in target account.
    3) Exchanges IAM credentials for Signin Token.
    4) Calls PhantomJS to do the dirty work.
    5) Saves PhantomJS output to our DB.
    
    :return: None
    """
    conn_details = {
        'account_number': account_number,
        'assume_role': role_name,
        'session_name': 'aardvark',
        'region': 'us-east-1'
    }
    arns = get_arns(arns, conn_details)
    if not arns:
        app = create_app()
        with app.app_context():
            app.logger.warn("Zero ARNs collected. Exiting")
        exit(-1)

    creds = get_creds(account_number, role_name)
    token = get_signin_token(creds)
    output_file = 'iam_access_advisor_{acct}'.format(acct=account_number)
    if call_phantom(token, list(arns), output_file) == 0:
        persist(output_file)


def get_arns(arns, conn):
    """
    Gets a list of all Role ARNs in a given account, optionally limited by a list of ARNS passed in.
    
    :return: list of role ARNs
    """
    roles = list_roles(**conn)
    account_arns = set([role['Arn'] for role in roles])
    result_arns = set()
    for arn in arns:
        if arn.lower() == 'all':
            return account_arns

        if arn not in account_arns:
            app = create_app()
            with app.app_context():
                app.logger.warn("Provided ARN {arn} not found in account.".format(arn=arn))
            continue

        result_arns.add(arn)

    return list(result_arns)


def get_creds(account_number, role_name):
    """
    Assumes into the target account and obtains Access Key, Secret Key, and Token
    
    :return: URL-encoded dictionary containing Access Key, Secret Key, and Token
    """
    client, credentials = boto3_cached_conn(
        'iam', account_number=account_number, assume_role=role_name, return_credentials=True)

    creds = json.dumps(dict(
        sessionId=credentials['AccessKeyId'],
        sessionKey=credentials['SecretAccessKey'],
        sessionToken=credentials['SessionToken']
    ))
    creds = urllib.quote(creds, safe='')
    return creds


def get_signin_token(creds):
    """
    Exchanges credentials dictionary for a signin token.
    
    1) Creates URL using credentials dictionary.
    2) Sends a GET request to that URL and parses the response looking for
    a signin token.
    
    :return: Signin Token
    """
    url = '{base}?Action=getSigninToken&Session={creds}'
    url = url.format(base=federation_base_url, creds=creds)
    return requests.get(url).json()['SigninToken']


def call_phantom(token, arns, output_file):
    """
    shells out to phantomjs.
    - Writes ARNs to a file that phantomjs will read as an input.
    - Phantomjs exchanges the token for session cookies.
    - Phantomjs then navigates to the IAM page and executes JavaScript
    to call GenerateServiceLastAccessedDetails for each ARN.
    - Every 10 seconds, Phantomjs calls GetServiceLastAccessedDetails
    - Phantom saves output to a file that is used by `persist()`

    :return: Exit code from phantomjs subprocess
    """

    path = os.path.dirname(__file__)
    console_js = os.path.join(path, 'awsconsole.js')
    arns_file = os.path.join(path, '_arns.json')
    with open(arns_file, 'w') as jsondata:
        json.dump(arns, jsondata)
    app = create_app()
    with app.app_context():
        return subprocess.call(
            [
                app.config.get('PHANTOMJS'),
                console_js,
                token,
                arns_file,
                output_file
            ],
            shell=True
        )


def persist(output_file):
    """
    Reads access advisor JSON file & persists to our database
    """
    from aardvark.model import AWSIAMObject, AdvisorData

    with open(output_file) as file_data:
        aa = json.load(file_data)

    for arn, data in aa.items():
        item = AWSIAMObject.get_or_create(arn)
        for service in data:
            AdvisorData.create_or_update(item.id,
                                         service['lastAuthenticated'],
                                         service['serviceName'],
                                         service['serviceNamespace'])

