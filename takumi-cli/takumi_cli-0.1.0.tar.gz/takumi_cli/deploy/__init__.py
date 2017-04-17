# -*- coding: utf-8 -*-

"""
takumi_cli.deploy
~~~~~~~~~~~~~~~~~

Implement deploy command using ansible.
"""

import json
import os
import tempfile

PLAYBOOK_PATH = os.path.join(
    os.path.dirname(__file__), 'playbook', 'playbook.yml')


def _find_hosts(cwd):
    hosts = os.path.join(cwd, 'hosts')
    if os.path.exists(hosts):
        return hosts


def _vars(d):
    return ['{}={}'.format(k, v) for k, v in sorted(d.items())]


def _convert_section(name, data):
    hosts = data.get('hosts', {})
    group_vars = data.get('vars', {})

    # Set env variable
    group_vars['env'] = name

    items = ['[{}]'.format(name)]
    for host_name, host_vars in sorted(hosts.items()):
        item = [host_name]
        item.extend(_vars(host_vars))
        items.append(' '.join(item))

    section = '\n'.join(items)

    var_section = ''
    if group_vars:
        var_items = '\n'.join(_vars(group_vars))
        var_section = '[{}:vars]\n{}'.format(name, var_items)
    return [section, var_section]


def _convert_hosts(hosts):
    section_names = []
    sections = []
    for k, v in sorted(hosts.items()):
        converted = {}
        if not isinstance(v, dict):
            v = {'hosts': v}
        hs = v.get('hosts', [])
        if isinstance(hs, str):
            hs = [hs]
        for item in hs:
            if not isinstance(item, dict):
                item = {item: {}}
            converted.update(item)
        v['hosts'] = converted
        sections.extend(_convert_section(k, v))
        section_names.append(k)
    return sections, section_names


def _convert_crontab(data, app_name):
    working_dir = '/srv/{}'.format(app_name)
    items = []
    for item in data:
        sched = item.get('schedule')
        if isinstance(sched, str):
            minute, hour, day, month, weekday = sched.split()
            sched = {
                'minute': minute,
                'hour': hour,
                'day': day,
                'month': month,
                'weekday': weekday
            }
        item.update(sched)
        item['work_job'] = 'cd {} && {}'.format(working_dir, item['job'])
        items.append(item)
    return items


def _gen_hosts(deploy_config, app_name):
    hosts = deploy_config.get('targets', {})
    sections, section_names = _convert_hosts(hosts)

    crontab = _convert_crontab(deploy_config.get('crontab', []), app_name)
    deploy_vars = deploy_config.get('vars', {})
    deploy_vars.update({
        'app_name': app_name,
        'app_repo': os.getcwd(),
        'crontabs': json.dumps(crontab)
    })

    main_section = ['[service-deploy:children]']
    main_section.extend(section_names)
    sections.append('\n'.join(main_section))

    main_vars = ['[service-deploy:vars]']
    main_vars.extend(_vars(deploy_vars))
    sections.append('\n'.join(main_vars))

    hosts_file = tempfile.mktemp()
    with open(hosts_file, 'w') as f:
        f.write('\n'.join(sections))
    return hosts_file


def _compose_args(args):
    ansible_args = args['<ansible_args>']
    target = args['<target>']
    tags = args['--tags']

    if target:
        ansible_args.extend(['--limit', target])
    if tags:
        ansible_args.extend(['--tags', tags])

    def _has_inventory():
        return bool(set(('-i', '--inventory-file')).intersection(ansible_args))

    if target and not _has_inventory():
        from takumi_config import config
        hosts = _find_hosts(os.getcwd())
        if not hosts and config.deploy:
            hosts = _gen_hosts(config.deploy, config.app_name)
        if hosts:
            ansible_args.extend(['--inventory-file', hosts])

    if target:
        ansible_args.append(args['--play'] or PLAYBOOK_PATH)
    return ansible_args


def start(args):
    """Start deployment powered by ansible.

    :param args: arguments passed to ansible
    """
    args = _compose_args(args)
    args.insert(0, 'ansible-playbook')
    from ansible.cli.playbook import PlaybookCLI
    cli = PlaybookCLI(args)
    cli.parse()
    cli.run()
