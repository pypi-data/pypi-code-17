# Copyright 2017 Nokia
# Copyright 2016 Pierre-Yves David <pierre-yves.david@ens-lyon.org>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""monitor and enforce client configuration from a server (EXPERIMENTAL)

This extension allows a server to recommend or enforce some configuration values
to a client during push and pull operation. The server can also detect clients
not using the extension and take appropriate actions.


Basic Setup
===========

This extension will not work with old clients using bundle1 (older than hg-3.5), we recommend
blocking old clients from your server using this config::

  [server]
  bundle1 = False


By default, the server will issue a warning to clients pushing and pulling without
the extension. This behavior can be controlled with the following option::

  [configexpress]
  # Behavior for clients with the extension. Possible values:
  # * ignore:  do not do anything
  # * warning: print a warning to the client (default)
  # * abort:   refuse to interract with the client
  enforce=ignore


Server to Client
================

The server can recommend configuration to the client during ``pull`` and ``clone``.
Recommended config values are put into a dedicated file referenced in the
``configexpress:server2client`` section::

  [configexpress:server2client]
  # path is relative to the config file it is defined in.
  config-key=path/to/config/file.rc

When values specified in the file differ from the user configuration, a prompt
will offer to update that configuration::

  server suggests the following config changes:
    [section_a]
    entry-one=Babar
    entry-two=Celeste
    [section_b]
    other.entry=Other/Text
    some.entry=some text
  apply these changes to your repository config file (yn)

If the new config shadows some of the existing user config, the user will be
informed with the following message::

  this will overwrite these current user configurations:
    [section_a]
    entry2=barbar

Multiple entries can be specified, they will be evaluated independently and the
user will be able to accept or reject them independently.


Client to Server
================

Enabling this extension results in sending the Mercurial version to the server.
Additional information about local configuration can be sent using the
``configexpress:client2server`` section.

Example::

  [configexpress:client2server]
  somelist = ui.verbose ui.username diff.git
  otherlist = extensions.rebase extensions.histedit

On the server side, the value sent by the client will be available to
transaction hooks through environment variables. environment variable are in the
form: ``CLIENTCONFIG_<SECTION>__<NAME>``.

(This only applies for push.)

Config
======

Detailed config help

``configexpress``
-----------------

Control generic behavior of the extension.

``enforce``
    level of enforcement to clients without the extension. Possible values:
    * ignore:  do not do anything
    * warning: print a warning to the client (default)
    * abort:   refuse to interact with the client

``enforcewarningmsg`
  custom warning message (optional). used when ``enforce=warning``

``enforceabortmsg`
  custom abort message (optional). used when ``enforce=abort``

``configexpress:server2client``
-------------------------------

``some-name``
    Configurations to be offered to the user. Value is a path to a config file.
    If the path is relative, it is interpreted relative to the file that
    defines it.

    Each individual entry will result in an independant check and prompt to the
    user.

``configexpress:client2server``
-------------------------------

Control what local config value are sent to the server on pull/push. Entries
have an arbitrary name, values is a list of config option to be send::

Example::

  [configexpress:client2server]
  somelist = ui.verbose ui.username diff.git
  otherlist = extensions.rebase extensions.histedit
"""
from __future__ import absolute_import
import cStringIO as io
import os
import tempfile

from mercurial.i18n import _
from mercurial import (
    bundle2,
    config,
    error,
    exchange,
    extensions,
    scmutil,
    ui as uimod,
    util
)

__version__ = '0.1.0'
testedwith = '4.1.2'
minimumhgversion = '4.1.1'
buglink = 'https://bitbucket.org/Mathiasdm/hg-configexpress/issues'

CLIENT2SERVER_SECTION = 'configexpress:client2server'
SERVER2CLIENT_SECTION = 'configexpress:server2client'

def getconfigstr(configitems, ui=None):
    '''Given a set of configuration entries of the form (section, item, value),
       a string in the hgrc format is generated.
       Giving the 'ui' argument makes sure values are taken from that argument,
       ignoring the 'value' entries in configitems.'''
    data = []
    configitems.sort()
    previoussection = None
    for (section, item, value) in configitems:
        if ui and not ui.hasconfig(section, item):
            continue
        if not previoussection or section != previoussection:
            data.append("[%s]" % section)
        previoussection = section
        if ui:
            value = ui.config(section, item)
        if value is None:
            value = ""
        data.append("%s=%s" % (item, value))
    if not data:
        return ''
    data.append('') # final \n
    return '\n'.join(data)

def calculateconfigdiff(first, second, onlyfirst=True):
    '''Calculate differences in configuration between 2 configurations.

       onlyfirst -- only check configuration entries that occur in the first config'''
    add = [] # config items present in first, not in second
    diff1 = [] # config items in first that are different in second
    diff2 = [] # config items in second that are different in first
    remove = [] # config items present in second, not in first
    for (section, item, value) in first.walkconfig():
        if not second.hasconfig(section, item):
            add.append((section, item, value))
        elif second.config(section, item) != value:
            diff1.append((section, item, value))
    if not onlyfirst:
        for(section, item, value) in second.walkconfig():
            if not first.hasconfig(section, item):
                remove.append((section, item, value))
            elif first.config(section, item) != value:
                diff2.append((section, item, value))
    return (add, diff1, diff2, remove)

@exchange.b2partsgenerator('configexpress:clientinfo', idx=0)
def _getbundlesendisaminfo(pushop, bundler):
    '''Send an additional (optional) clientinfo bundle part to the server.
       This bundle part is optional to make sure the server doesn't error out.
    '''
    if 'clientinfo' in pushop.stepsdone:
        return
    pushop.stepsdone.add('clientinfo')

    configitems = []
    for key, _ in pushop.ui.configitems(CLIENT2SERVER_SECTION):
        for entry in pushop.ui.configlist(CLIENT2SERVER_SECTION, key):
            (section, element) = entry.split('.', 1)
            configitems.append((section, element, None))
    data = getconfigstr(configitems, pushop.ui)

    part = bundler.newpart('configexpress:clientinfo', mandatory=False, data=data)
    part.addparam('hgversion', str(util.version()), mandatory=False)

    def handlereply(op):
        pass

    return handlereply

@bundle2.parthandler('configexpress:clientinfo', ())
def bundle2getisaminfo(op, part):
    '''Retrieve a clientinfo part and store parameters as hook arguments'''
    tr = op.gettransaction()
    for key, value in part.advisoryparams:
        tr.hookargs["CLIENTCONFIG_%s" % key] = value
    data = part.read() #TODO: not very safe
    fp = io.StringIO(data)
    cfg = config.config()
    cfg.read(path="", fp=fp)

    for section in cfg.sections():
        for (item, value) in cfg.items(section):
            key = "CLIENTCONFIG_%s__%s" % (section, item)
            tr.hookargs[key] = value

@exchange.getbundle2partsgenerator('configexpress:proposedconfig')
def _getbundleproposedconfig(bundler, repo, source, **kwargs):
    '''Send an additional (optional) proposedconfig bundle to the client.'''
    if not repo.ui.has_section(SERVER2CLIENT_SECTION):
        return

    items = sorted(repo.ui.configitems(SERVER2CLIENT_SECTION, ignoresub=True))
    for (item, configfile) in items:
        if os.path.isabs(configfile):
            configpath = configfile
        else:
            source = repo.ui.configsource(SERVER2CLIENT_SECTION, item)
            sourcebase = repo.vfs.dirname(source)
            configpath = os.path.join(sourcebase, configfile)
        if not os.path.exists(configpath):
            repo.ui.warn("configexpress: proposedconfig not found: %s\n" % configpath)
            return
        (option, suboptions) = repo.ui.configsuboptions(SERVER2CLIENT_SECTION, item)

        data = util.readfile(configpath)

        part = bundler.newpart('configexpress:proposedconfig', mandatory=False, data=data)
        part.addparam('name', item, mandatory=False)

_serverproposal = _("server suggests the following config changes:")
_outdatedconfig = _("this will overwrite these current user configurations:")

_hgrcdirname = 'hgrc-ext-config-express'
_hgrcdispatchname = 'hgrc-ext-config-express.rc'

_hgrccomment = ('# This "%include" enables config from the configexpress extension.'
                ' keep at end of file\n')
_hgrcinclude = '%%include ./%s\n' % _hgrcdispatchname


@bundle2.parthandler('configexpress:proposedconfig', ())
def bundle2getproposedconfig(op, part):
    '''Retrieve a proposed configuration, calculate the difference
       to our own configuration and apply the difference.'''
    serverdata = part.read()
    name = "%s.rc" % part.params.get('name', 'untitled-%s' % part.id)

    #TODO: just use StringIO (needs ui.readconfig support for fp)
    with tempfile.NamedTemporaryFile() as f:
        f.write(serverdata)
        f.seek(0)
        serverui = uimod.ui()
        serverui.readconfig(f.name)
    # 1. Calculate the differences between client and server
    (add, diff1, diff2, remove) = calculateconfigdiff(serverui, op.ui, onlyfirst=False)
    if not add and not diff1:
        # no proposed changes to the configuration
        # XXX handle location
        op.records.add('configexpress.enabled-config',
                       {'file': name})
        return
    proposedconfig = getconfigstr(add + diff1)
    # 2. Propose applying differences to client
    op.ui.warn(_serverproposal + "\n")
    for line in proposedconfig.splitlines(True):
        op.ui.warn('  ' + line)
    if diff2:
        op.ui.warn(_outdatedconfig + "\n")
        for line in getconfigstr(diff2).splitlines(True):
            op.ui.warn('  ' + line)
    res = op.ui.promptchoice("apply these changes to your repository config file (yn)? $$ &Yes $$ &No")
    if res != 0:
        return

    # XXX move to a dedicated lock instead
    with op.repo.wlock():
        op.repo.vfs.makedirs(_hgrcdirname)
        with op.repo.vfs('%s/%s' % (_hgrcdirname, name), 'w', atomictemp=True) as partrc:
            _writeboilerplate(partrc)
            partrc.write(serverdata)
        op.records.add('configexpress.enabled-config', {'file': name})

def _writeboilerplate(f):
    f.write('# this file is managed by the configexpress extension\n')
    f.write('# /!\\ do not edit /!\\\n')

def _finalizeconfig(orig, *args, **kwargs):
    # XXX if not config changed, we should avoid rewriting everything
    op = orig(*args, **kwargs)
    entries = op.records['configexpress.enabled-config']
    if not entries:
        return op
    # XXX move to a dedicated lock instead
    with op.repo.wlock():
        with op.repo.vfs(_hgrcdispatchname, 'w', atomictemp=True) as sharedrc:
            _writeboilerplate(sharedrc)
            for entry in sorted(entries):
                sharedrc.write('%%include ./%s/%s\n' % (_hgrcdirname, entry['file']))

        commentidx = []
        includeidx = []
        rclines = op.repo.vfs.tryread('hgrc').splitlines(True)
        idx = 0
        for idx, line in enumerate(rclines):
            if line == _hgrccomment:
                commentidx.append(idx)
            elif line == _hgrcinclude:
                includeidx.append(idx)
        finalidx = idx

        if not commentidx + includeidx:
            # simple: no existing data
            with op.repo.vfs('hgrc', 'a') as mainrc:
                mainrc.write(_hgrccomment)
                mainrc.write(_hgrcinclude)
        elif commentidx != [finalidx -1] or includeidx != [finalidx]:
            # some data exist at the wrong spot, drop them
            dropped = set(commentidx + includeidx)
            with op.repo.vfs('hgrc', 'w', atomictemp=True) as mainrc:
                for idx, line in enumerate(rclines):
                    if idx not in dropped:
                        mainrc.write(line)
                mainrc.write(_hgrccomment)
                mainrc.write(_hgrcinclude)
    return op

_capability = 'ext-configexpress'
_enforcemsgwarn = _("this server recommends using the 'configexpress'"
                    " extension\n")
_enforcemsgabort = _("this server requires the 'configexpress' extension")


def checkreplycaps(orig, op, inpart):
    orig(op, inpart)
    if op.reply is not None:
        _enforceext(op.ui, op.reply)

_maxabortlength = 80

def _enforceext(ui, bundler):
    if _capability not in bundler.capabilities:
        # client does not have the extension enabled
        policy = ui.config('configexpress', 'enforce', 'warning')
        if policy == 'ignore':
            pass
        elif policy == 'warning':
            msgwarn = ui.config('configexpress', 'enforcewarningmsg', _enforcemsgwarn)
            ui.warn(msgwarn)
        elif policy == 'abort':
            msgabort = ui.config('configexpress', 'enforceabortmsg', _enforcemsgabort)
            if len(msgabort) > _maxabortlength:
                ui.warn(msgabort)
                ui.warn('\n')
                ui.warn('    - - -\n')
                msgabort = msgabort[:_maxabortlength] + "..."
            raise error.Abort(msgabort)
        else:
            msg = _("unknown value for 'configexpress.enforce': %s" % policy)
            ui.warn(msg)

@exchange.getbundle2partsgenerator('enforceconfigexpress', idx=0)
def _getbundlechangegrouppart(bundler, repo, source, bundlecaps=None,
                              b2caps=None, heads=None, common=None, **kwargs):
    _enforceext(repo.ui, bundler)

def uisetup(ui):
    replycapshandler = bundle2.parthandlermapping['replycaps']
    def wrapper(op, inpart):
        return checkreplycaps(replycapshandler, op, inpart)
    wrapper.params = replycapshandler.params
    bundle2.parthandlermapping['replycaps'] = wrapper
    bundle2.capabilities[_capability] = ()
    extensions.wrapfunction(bundle2, 'processbundle', _finalizeconfig)
