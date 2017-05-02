import koji

import fedmsg
import fedmsg.consumers
import robosignatory.utils as utils
from pdc_client import PDCClient

import logging
log = logging.getLogger("robosignatory.tagconsumer")


class TagSignerConsumer(fedmsg.consumers.FedmsgConsumer):
    config_key = 'robosignatory.enabled.tagsigner'

    def __init__(self, hub):
        if hub:
            super(TagSignerConsumer, self).__init__(hub)
            self.config = self.hub.config
        else:
            # No hub, we are in ad-hoc mode
            self.config = fedmsg.config.load_config()
            logging.basicConfig(level=logging.DEBUG)

        prefix = self.config.get('topic_prefix')
        env = self.config.get('environment')
        self.topic = [
            '%s.%s.buildsys.tag' % (prefix, env)
        ]

        self.module_prefixes = \
            tuple(self.config['robosignatory.module_prefixes'])
        self.valid_base_module_names = \
            tuple(self.config['robosignatory.base_module_names'])

        self.pdc_client = PDCClient(
            server=self.config['robosignatory.pdc_url'], develop=True)

        signing_config = self.config['robosignatory.signing']
        self.signer = utils.get_signing_helper(**signing_config)

        self.koji_clients = {}
        for instance in self.config['robosignatory.koji_instances']:
            instance_info = self.config[
                'robosignatory.koji_instances'][instance]
            client = koji.ClientSession(instance_info['url'],
                                        instance_info['options'])

            if instance_info['options']['authmethod'] == 'ssl':
                client.ssl_login(instance_info['options']['cert'],
                                 None,
                                 instance_info['options']['serverca'])
            elif instance_info['options']['authmethod'] == 'kerberos':
                kwargs = {}
                for opt in ('principal', 'keytab', 'ccache'):
                    if opt in instance_info['options']:
                        kwargs[opt] = instance_info['options'][opt]
                client.krb_login(**kwargs)
            else:
                raise Exception('Only SSL and kerberos authmethods supported')

            instance_obj = {'client': client,
                            'tags': {},
                            'module_streams': {}}
            for tag in instance_info['tags']:
                if tag['from'] in instance_obj['tags']:
                    raise Exception('From detected twice: %s' % tag['from'])
                instance_obj['tags'][tag['from']] = {'to': tag['to'],
                                                     'key': tag['key'],
                                                     'keyid': tag['keyid']}

            for stream in instance_info['module_streams']:
                if stream['stream'] in instance_obj['module_streams']:
                    raise Exception('Module stream detected twice: %s'
                                    % stream['stream'])
                instance_obj['module_streams'][stream['stream']] = {
                    'key': stream['key'], 'keyid': stream['keyid']}

            self.koji_clients[instance] = instance_obj

            log.info('TagSignerConsumer ready for service')

    def consume(self, msg):
        topic = msg['topic']
        if topic not in self.topic:
            return

        msg = msg['body']['msg']

        #  {u'build_id': 799208,
        #   u'name': u'python-fmn-rules',
        #   u'tag_id': 374,
        #   u'instance': u'primary',
        #   u'tag': u'epel7-infra',
        #   u'user': u'puiterwijk',
        #   u'version': u'0.9.1',
        #   u'owner': u'sayanchowdhury',
        #   u'release': u'1.el7'}}

        build_nvr = '%(name)s-%(version)s-%(release)s' % msg
        build_id = msg['build_id']
        tag = msg['tag']
        koji_instance = msg['instance']

        log.info('Build %s (%s) tagged into %s on %s',
                 build_nvr, build_id, tag, koji_instance)

        if koji_instance not in self.koji_clients:
            log.info('Koji instance not known, skipping')
            return

        instance = self.koji_clients[koji_instance]
        if tag in instance['tags']:
            self.dowork(build_nvr, build_id, tag, koji_instance,
                        skip_tagging=False)
        elif tag.startswith(self.module_prefixes):
            self.sign_modular_rpms(build_nvr, build_id, tag, koji_instance)


    def verify_base_module_tag(self, tag):
        """
        Verifies that the base module tag is valid. Sets the tag['stream']
        and tag['verified'].
        """
        query = {}
        query["koji_tag"] = tag["name"]
        query["active"] = True
        retval = self.pdc_client.unreleasedvariants(page_size=-1, **query)

        if not retval or len(retval) != 1:
            tag["verified"] = False
            return tag

        if retval[0]["variant_name"] not in self.valid_base_module_names:
            tag["verified"] = False
            return tag

        tag["verified"] = True
        tag["stream"] = retval[0]["variant_version"]
        return tag

    def get_base_module_tag(self, session, info, parent_tags=None):
        """
        Recursively traverse the inheritance hiearchy of tags in Koji to find
        out the base module tag.
        """

        # Handle only tags with modular prefix.
        if not info['name'].startswith(self.module_prefixes):
            return None

        # Find all targets pointing to our current tag, there should be just
        # single target for our tag.
        targets = session.getBuildTargets(destTagID=info['id'])
        if not targets:
            return None

        # TODO: For now skip the -repo target. We are creating these targets
        # for modules only to force kojira to create repo for the modules.
        # We can remove these targets and this code once the composes will be
        # be running, but for that, we need robosignatory to sign packages
        # (chicken and egg)...
        targets = [target for target in targets
                   if target['name'] != info['name'] + "-repo"]

        if len(targets) != 1:
            log.info("Expected exactly 1 target for tag %s, skipping."
                     % info["name"])
            return None

        target = targets[0]

        # Get the build tag of this target.
        build_tag_id = target["build_tag"]
        build_tag_info = session.getTag(build_tag_id)

        # Store the dest_tag as a possible base tag (we don't know yet).
        base_module_tag = {"id": target["dest_tag"],
                           "name": target["dest_tag_name"],
                           "verified": False,
                           "stream": None}

        # Get the inheritance data and filter out tags from parent_tags set.
        # Following those tags would bring us back to the already seen target.
        inheritance_data = session.getInheritanceData(build_tag_info['name'])
        inheritance_data = [data for data in inheritance_data
                            if data['parent_id'] not in parent_tags]

        # Iterate over all the tags this tag inherits from. There may be many of
        # them, because single module can build-require multiple other modules.
        for inherited in inheritance_data:
            # Make a note to ourselves that we have seen this parent_tag.
            parent_tag_id = inherited['parent_id']
            parent_tags.add(parent_tag_id)

            # Get tag info for the parent_tag.
            info = session.getTag(parent_tag_id)
            if info is None:
                return base_module_tag

            # Try to recursively find all the parents of this parent tag.
            maybe_tag = self.get_base_module_tag(session, info, parent_tags)
            if not maybe_tag:
                continue

            # Verify that the found tag is really a valid base module tag.
            maybe_tag = self.verify_base_module_tag(maybe_tag)
            if maybe_tag['verified']:
                # In case we have already found valid tag in the previous subtree
                # and right now we have another one, compare that their streams
                # are matching.
                if (base_module_tag['verified']
                        and maybe_tag['stream'] != base_module_tag['stream']):
                    log.warn("Multiple base module streams found in "
                             "inheritance tree.")
                    return None
                else:
                    base_module_tag = maybe_tag

        return base_module_tag

    def sign_modular_rpms(self, build_nvr, build_id, tag, koji_instance):
        # Skip the -build tag.
        if tag.endswith("-build"):
            log.info("Skipping build tag %s" % tag)
            return

        instance = self.koji_clients[koji_instance]
        session = instance["client"]

        # Get the tag to find out its id.
        info = session.getTag(tag)
        if info is None:
            log.info("Koji tag %s not known, skipping" % tag)
            return

        # Try to find out if the current tag is a base module before traversing
        # the tag inheritance tree.
        maybe_tag = {
            "id": info["id"],
            "name": info['name'],
            "verified": False,
            "stream": None,
        }
        maybe_tag = self.verify_base_module_tag(maybe_tag)
        if maybe_tag["verified"]:
            base_module_tag = maybe_tag
        else:
            # build tag inherits from the main tag, so when we are evaluating
            # which tag is the right one to check when examining tag inheritance
            # we have to know that we do not want to go back to the main tag.
            # Therefore we have to track the set of parent tags.
            parent_tags = set([info['id']])

            # Resulting base module tag according to which we will use the right key.
            base_module_tag = self.get_base_module_tag(
                session, info, parent_tags=parent_tags)

        if not base_module_tag:
            log.info("No base module tag found in inheritance tree for "
                     "%s, skipping" % tag)
            return

        if not base_module_tag["verified"]:
            log.info("No verified base module tag found in inheritance tree for "
                     "%s, skipping. Found tag: %r" % (tag, base_module_tag))
            return

        if base_module_tag["stream"] not in instance['module_streams']:
            log.info("Base module stream %s not allowed for "
                     "auto-sign" % base_module_tag["stream"])
            return

        stream_info = instance['module_streams'][base_module_tag["stream"]]
        # We are not moving to any tag after signing.
        stream_info["to"] = tag

        # Cache the stream_info (which is in the same format as tag_info), so
        # for next package in this tag, we know what key to use without
        # traversing the Koji tag inheritance tree.
        instance["tags"][tag] = stream_info

        self.dowork(build_nvr, build_id, tag, koji_instance,
                    tag_info=stream_info)


    def dowork(self, build_nvr, build_id, tag, koji_instance,
               skip_tagging=False, tag_info=None):
        instance = self.koji_clients[koji_instance]

        if not build_id:
            build_id = instance['client'].findBuildID(build_nvr)

        if not tag_info:
            if tag not in instance['tags']:
                log.info('Tag not autosigned, skipping')
                return

            tag_info = instance['tags'][tag]

        log.info('Going to sign with %s (%s) and move to %s',
                 tag_info['key'], tag_info['keyid'], tag_info['to'])

        rpms = utils.get_rpms(instance['client'],
                              build_nvr=build_nvr,
                              build_id=build_id,
                              sigkey=tag_info['keyid'])
        log.info('RPMs to sign and move: %s',
                 ['%s (%s, signed: %s)' %
                    (key, rpms[key]['id'], rpms[key]['signed'])
                    for key in rpms.keys()])
        if len(rpms) < 1:
            log.info('Build contains no rpms, skipping signing and writing')

        if all([rpms[rpm]['signed'] for rpm in rpms]) or len(rpms) < 1:
            log.debug('All RPMs are already signed')
        else:
            to_sign = [key for key in rpms.keys() if not rpms[key]['signed']]
            log.debug('RPMs needing signing: %s' % to_sign)
            cmdline = self.signer.build_sign_cmdline(tag_info['key'],
                                                     rpms.keys(),
                                                     koji_instance)
            log.debug('Signing command line: %s' % cmdline)

            ret, stdout, stderr = utils.run_command(cmdline)
            if ret != 0:
                log.error('Error signing! Signing output: %s, stdout: '
                          '%s, stderr: %s', ret, stdout, stderr)
                return

        if len(rpms) > 1:
            log.info('Build was succesfully signed, telling koji to write with key'
                     ' %s', tag_info['keyid'])

            for rpm in rpms:
                instance['client'].writeSignedRPM(rpms[rpm]['id'],
                                                  tag_info['keyid'])

            log.info('Signed RPMs written out')

        if skip_tagging:
            log.info('Tagging skipped, done')
        else:
            log.info('Packages correctly signed, moving to %s' %
                     tag_info['to'])
            if tag == tag_info['to']:
                log.info('Non-gated, not moving')
            else:
                instance['client'].tagBuild(tag_info['to'], build_id, False,
                                            tag)
