import subprocess
import os 
import json


def ecr_login():
    cmd = subprocess.Popen(['aws', 'ecr', 'get-login'], stdout=subprocess.PIPE)
    output, stderr = cmd.communicate()

    if cmd.returncode == 0:
        return subprocess.Popen([output],shell=True).communicate()

def ecr_describe_create(repo_name):
    cmd = subprocess.Popen(['aws', 'ecr', 'describe-repositories', '--repository-names', repo_name],
            stdout=subprocess.PIPE)
    output, stderr = cmd.communicate()
    print(output, stderr) 
    if cmd.returncode != 0:
        print('Repository does not exist. Creating...')
        cmd_create = subprocess.Popen(['aws', 'ecr', '--repository-name', repo_name])
        cmd_create.communicate()
        out = json.loads(cmd_create.communicate()[0])    
    else:
        out = json.loads(output)    
        
    return out['repositories'][0]['repositoryUri'] 

def s3_get(url, path='/tmp/'):
    return subprocess.Popen(['aws', 's3', 'cp', url, path]).communicate()

def docker_import(path_to_file, tag):
    return subprocess.Popen(['docker', 'import', path_to_file, tag]).communicate()

def docker_push(tag):
    return subprocess.Popen(['docker', 'push', tag]).communicate()

def docker_rmi(tag):
    return subprocess.Popen(['docker', 'rmi', tag]).communicate()

def docker_tag(old_tag, new_tag):
    return subprocess.Popen(['docker', 'tag', old_tag, new_tag]).communicate()

def main():

    print('---------------- S3 to ECS transfer tool -----------------')
    url = input('S3 Url:')
    repo_name = input('ECS Repository Name:')
    version = input('Version Label:')

    filename = url.split('/')[-1].strip()
    
    if len(filename) == 0:
        raise ValueError('Could not determine a valid filename from the S3 url provided.')
    
    path_to_file = os.path.join('/tmp', filename)

    ecr_login() 
    repo_uri = ecr_describe_create(repo_name) 
    tag = f'{repo_uri}:{version}'
    latest_tag = f'{repo_uri}:latest'
    s3_get(url=url)
    docker_import(path_to_file=path_to_file, tag=tag)
    docker_push(tag=tag)
    docker_tag(old_tag=tag, new_tag=latest_tag)
    docker_push(latest_tag)
    
    # Clean up 
    print('Clean up...')
    print('Removing Docker archive...')
    os.remove(path_to_file)
    print(f'Removing Docker image: {tag}')
    docker_rmi(tag)
    print(f'Removing Docker image: {latest_tag}')
    docker_rmi(latest_tag)
    
    print('Done.')

if __name__ == '__main__':
    sys.exit(main())
