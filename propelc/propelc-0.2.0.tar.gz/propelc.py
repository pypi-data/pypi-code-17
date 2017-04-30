"""
PROPELC

PropelC is a python deployment tool using Ansible on the client side, and Propel on the Server.
Hence 'C' is for Client in PropelC
"""

import os
import re
import sys
import sh
import yaml
import socket
import argparse

yaml.Dumper.ignore_aliases = lambda *args: True

__title__ = "PropelC"
__version__ = "0.2.0"

CWD = os.getcwd()
CWD_PROPEL = "%s/_propelc" % CWD
ANSIBLE_FILE = "%s/_propelc/playbook.yml" % CWD
PROPEL_FILE = "%s/propel.yml" % CWD
HOST_FILE = "%s/_propelc/hosts" % CWD

PROPELC_EXISTS = os.path.isdir(CWD_PROPEL)

ROLES = {

    "setup": [
        {
            "name": "SETUP: Checking Propel existence",
            "stat": "path=/var/propel",
            "register": "propelexists"
        },
        {
            "name": "SETUP: PIP Installing Propel",
            "action": "command pip install propel",
            "when": "propelexists.stat.exists == False"
        },
        {
            "name": "SETUP: Propel",
            "action": "command propel-setup",
            "when": "propelexists.stat.exists == False"
        },
        {
            "name": "SETUP: Checking App existence",
            "stat": "path={{ app_path }}",
            "register": "direxists"
        },
        {
            "name": "SETUP: Create App - Setting up app dir and Propel",
            "command": "propel -c {{ app_path }} --git-push-cmd {{ app_path }} 'echo \"{{ app_path}} has been updated!\" '",
            "when": "direxists.stat.exists == False",
        }
    ],
    "upgrade": [
        {
            "name": "UPDATE DIST",
            "apt": "update_cache=yes"
        },
        {
            "name": "UPGRADE PROPEL",
            "action": "command pip install propel --upgrade",
        }
    ],
    "route53": [
        {
            "name": "ROUTE53: Collecting Host Ips",
            "run_once": True,
            "set_fact": "ips={{ ','.join(play_hosts) }}",
        },
        {
            "name": "ROUTE53: Create Records",
            "run_once": True,
            "local_action": {
                "module": "route53",
                "command": "create",
                "overwrite": True,
                "zone": "{% set zonename = '.'.join(item.split('.')[-2:3]) %}{{ zonename }}.",
                "record": "{{ item }}.",
                "type": "A",
                "value": "{{ ips }}"
            },
            "with_items": "{{ route53 }}"
        }
    ],

    "route53_delete": [
        {
            "name": "ROUTE53: Collecting route53 records",
            "local_action": {
                "module": "route53",
                "command": "get",
                "zone": "{% set zonename = '.'.join(item.split('.')[-2:3]) %}{{ zonename }}.",
                "record": "{{ item }}",
                "type": "A",
                "register": "rec",
            },
            "with_items": "{{ route53_delete }}"
        },
        {
            "name": "ROUTE53: Delete records",
            "local_action": {
                "module": "route53",
                "command": "delete",
                "zone": "{{ rec.results.0.set.zone }}",
                "record": "{{ rec.results.0.set.record }}",
                "ttl": "{{ rec.results.0.set.ttl }}",
                "type": "{{ rec.results.0.set.type }}",
                "value": "{{ rec.results.0.set.value }}",
                "when": "rec.results.0"
            }
        }
    ],

    "s3buckets": [
        {
            "name": "S3BUCKETS: Create buckets",
            "run_once": True,
            "local_action": {
                "module": "s3",
                "bucket": "{{ item }}",
                "mode": "create",
                "validate_certs": "no",
                "region": "us-east-1",
            },
            "with_items": "{{ s3buckets }}"
        }
    ],
    "delete_app": [
        {
            "name": "DELETE: Delete app",
            "shell": "rm -rf {{ app_path }}*"

        }
    ],
    "run_propel": [
        {
            "name": "PROPEL: Run commands",
            "shell": "cd {{ app_path }}; propel {{ propel_vars }}",
        }
    ],
    "git_push": [
        {
            "name": "GIT: Push remote to master",
            "local_action": "command git push -f {{ git_remote}} master"
        }
    ]
}

# This is the template
TEMPLATE = """

################################################################################
# PropelC
################################################################################
# ------------------------------------------------------------------------------
propelc:

  # The full path where the app will reside: /home/domain/domain.com  
  app_path:        
  
  envs:
    # Key of the environments to be used when deploying
    webs:           
    
      # List of all hosts 
      hosts:        
        - 
        
      # List of all domains for route 53, that will point there  
      domains:      
        - 
       
      # dict of propel commands that will be ran: webs|scripts|workers  
      propel:       
      
        # List of all the domains to deploy from
        webs:       
          - 
          
        # List of all the scripts name  
        scripts:    
          -
          
        # List of all the workers name  
        workers:    
          - 
         
      # Misc ansible tasks to run before and after deployment   
      tasks:        
      
        # List of tasks to run before the deploy
        pre:        
            -
            
        # List of tasks to run after
        post:       
            -
            
      # Dict of extra variables       
      vars:         
        key: value
        
  # List of all s3 bucket to create      
  s3buckets:        
    -
    
# ------------------------------------------------------------------------------

"""


# ------------------------------------------------------------------------------


def sh_verbose(line):
    print(line)


def run_playbook(*args, **kwargs):
    playbook = "_propelc/playbook.yml"
    with sh.pushd(CWD):
        sh.ansible_playbook(playbook, "-i", "_propelc/hosts", _out=sh_verbose,
                            *args, **kwargs)


def git_remote_name(name):
    return "propel_%s" % name


def set_git_remotes(name, hosts):
    with sh.pushd(CWD):
        name = git_remote_name(name)
        remote_list = sh.git("remote").strip().split()
        if name in remote_list:
            sh.git("remote", "remove", name)
        sh.git("remote", "add", name, hosts[0])
        if len(hosts) > 1:
            for h in hosts:
                sh.git("remote", "set-url", name, "--push", "--add", h)


def get_propelc_config():
    with open(PROPEL_FILE) as p:
        propel_conf = yaml.load(p)
    return propel_conf.get("propelc")


def gen_playbook():
    plays = []
    propel = get_propelc_config()
    if not propel:
        raise Exception("Missing `propelc` in propel.yml")

    app_path = propel.get("app_path")
    envs = propel.get("envs")
    user = "root"
    upgrade_propel = propel.get("upgrade", False)

    serial = propel.get("serial", 4)
    if not app_path:
        raise Exception("Missing `app_path` in propelc node")
    if "/" not in app_path or "." not in app_path:
        raise Exception(
            "`app_path` must be directory path  with the domain in the format  `/home/site/site.com`")

    hostsd = {k: v.get("hosts") for k, v in envs.items()}

    # CREATE HOST FILE
    with open(HOST_FILE, "w") as h:
        s = "# PropelC: To deploy propel app\n"
        s += "# Generated automatically. All changes must be made in propel.yml\n\n"
        for k, v in hostsd.items():
            s += "[%s]\n" % k
            if v and filter(None, v):
                s += "\n".join(map(get_ip_by_hostname, v))
            s += "\n\n"
        h.write(s)

    # SETUP GIT REMOTE
    for k, v in hostsd.items():
        v = filter(None, v)
        if v:
            git_hosts = ["ssh://%s@%s/%s.git" % (user, h, app_path) for h in v]
            set_git_remotes(k, git_hosts)

    # PROVISION
    vars = {"app_path": app_path}
    if propel.get("delete_app"):
        tasks = [r for r in ROLES["delete_app"]]
    else:
        tasks = ROLES["setup"]

    if upgrade_propel:
        tasks.extend(ROLES["upgrade"])

    # require variables for the items too
    for k in ["s3buckets", "route53_delete"]:
        if k in propel:
            _vars = propel.get(k)
            if _vars and filter(None, _vars):
                vars.update({k: _vars})
                tasks.extend(ROLES[k])

    plays.append([
        {
            "hosts": "*",
            "user": "root",
            "serial": serial,
            "name": "PROVISION HOSTS",
            "tags": ["provision"],
            "vars": vars,
            "tasks": tasks
        }
    ])

    # CONTAINERS
    for name, d in envs.items():
        hosts = d.get("hosts")
        domains = d.get("domains")
        commands = d.get("propel")
        pre_tasks = d.get("tasks", {}).get("pre")
        post_tasks = d.get("tasks", {}).get("post")
        use_git = d.get("use_git", True)

        vars = {"app_path": app_path}
        vars.update(d.get("vars", {}))

        tasks = []

        # Propel variables
        propel_vars = ""
        if commands:
            for k, cmd in {"webs": "-w", "scripts": "-s",
                           "workers": "-k"}.items():
                if k in commands:
                    if not isinstance(commands.get(k), list):
                        raise Exception(
                            "Propel targets `%s.commands.%s` must be a list" % (
                            name, k))
                    if filter(None, commands.get(k)):
                        propel_vars += "%s %s " % (
                        cmd, " ".join(filter(None, commands.get(k))))

        # Route 53
        if domains and filter(None, domains):
            vars.update({"route53": domains})
            tasks.extend(ROLES.get("route53"))

        # pre tasks
        if pre_tasks and isinstance(pre_tasks, list) and filter(None,
                                                                pre_tasks):
            tasks.extend(pre_tasks)

        # Push the data with git
        if use_git:
            tasks.extend(ROLES.get("git_push"))
            vars.update({"git_remote": git_remote_name(name)})

        if propel_vars:
            tasks.extend(ROLES.get("run_propel"))
            vars.update({"propel_vars": propel_vars})

        # post tasks
        if post_tasks and isinstance(post_tasks, list) and filter(None,
                                                                  post_tasks):
            tasks.extend(post_tasks)

        # deploy task
        plays.append([
            {
                "name": "DEPLOYING CONTAINERS: %s" % name,
                "hosts": name,
                "serial": serial,
                "user": "root",
                "tags": [name],
                "vars": vars,
                "tasks": tasks
            }
        ])

    # Create the ansible file
    with open(ANSIBLE_FILE, "w") as a:
        s = yaml.dump(plays, default_flow_style=False, width=1000,
                      explicit_start=True)
        a.write(s.replace("- -", "  -"))


def get_ip_by_hostname(hostname):
    return socket.gethostbyname(hostname.strip())


def get_endpoints():
    with open(PROPEL_FILE) as p:
        propel = yaml.load(p)
    xnodep = propel.get("propelc")
    return xnodep.get("envs").keys()


# ------------------------------------------------------------------------------

def header(msg):
    print("-" * 80)
    print("===== PropelC ======")
    print("-" * 80)
    print("::: %s :::" % msg)
    print("")


def deploy(target="all"):
    header("Deploy to target: %s" % target)
    if target != "all" and target not in get_endpoints():
        print("ERROR: Invalid target: %s" % target)
        print("++++")
        print("* Here are the valid targets:")
        print("\n".join(get_endpoints()))
        print("")
    else:
        gen_playbook()
        cmds = [] if target == "all" else ["--tags", target]
        run_playbook(*cmds)
        print("Done!")


def cmd():
    try:
        parser = argparse.ArgumentParser(
            description="%s %s" % (__title__, __version__))
        parser.add_argument("--init",
                            help="Initialize PropelC in the current directory",
                            action="store_true")
        parser.add_argument("-p", "--provision",
                            help="Provision new application",
                            action="store_true")
        parser.add_argument("-l", "--list",
                            help="List all the environments to deploy",
                            action="store_true")
        parser.add_argument("-d", "--deploy",
                            help="Deploy environments to hosts ie [-d admin network web ...]",
                            nargs='*')
        parser.add_argument("-a", "--all",
                            help="Deploy all ie[-a]",
                            action="store_true")
        parser.add_argument("--restart",
                            help="Restart target ie [-d admin network web ...]",
                            nargs='*')
        parser.add_argument("--undeploy",
                            help="Restart target ie [-d admin network web ...]",
                            nargs='*')
        parser.add_argument("--mkfile",
                            help="With --init, to create the propel.yml file ie[--init --mkfile]",
                            action="store_true")

        arg = parser.parse_args()

        if arg.init:
            header("Init PropelC")
            if not os.path.isfile(PROPEL_FILE):
                if arg.mkfile:
                    with open(PROPEL_FILE, "w") as f:
                        f.write("# Propel.yml - Created by PropelC")
                        f.write("\n\n")
                        f.write(TEMPLATE)
                else:
                    raise Exception(
                        "Missing `propel.yml` file. Type --init --mkfile to automatically create the propel.yml")
            if not os.path.isdir(CWD_PROPEL):
                os.makedirs(CWD_PROPEL)
            if not get_propelc_config():
                with open(PROPEL_FILE, "a") as f:
                    f.write(TEMPLATE)
        else:
            if not PROPELC_EXISTS:
                raise Exception("PropelC is not setup yet. Run `propelc init`")

            gen_playbook()

            # PROVISION
            if arg.provision:
                header("Running provision...")
                run_playbook("--tags", "provision")
                print("Done!")

            # DEPLOY
            elif arg.deploy or arg.all:
                tags = ""
                cmd = ["--skip-tags", "provision"]
                if arg.deploy:
                    tags = ",".join(arg.deploy)
                    cmd.append("--tags")
                    cmd.append(tags)
                else:
                    tags = "ALL"
                header("Deploying Environments: %s" % tags)
                run_playbook(*cmd)
                print("Done!")

            # List Containers
            else:
                header("Environments list")
                for c in get_endpoints():
                    print("- %s" % c)
                print("")

    except Exception as e:
        print("")
        print("")
        print("=" * 80)
        print("ERROR: %s" % e)
        print("=" * 80)

    print("")
    print("-" * 80)
