"""Online CA Service WSGI middleware - exposes issue certificate and get trust
roots as web service methods

Contrail Project
"""
__author__ = "P J Kershaw"
__date__ = "24/05/10"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = "$Id$"
import logging
log = logging.getLogger(__name__)

import os
import base64
import string

from webob import Request
from paste.httpexceptions import (HTTPException, HTTPMethodNotAllowed,
                                  HTTPBadRequest)
from OpenSSL import crypto

import six

from contrail.security.onlineca.server import _string2bytes
from contrail.security.onlineca.server.interfaces import OnlineCaInterface
from contrail.security.onlineca.server.factory import call_module_object
from contrail.security.onlineca.server.openssl_utils import X509SubjectName


class OnlineCaMiddlewareError(Exception):
    """Errors related to the Online CA Service middleware"""


class OnlineCaMiddlewareConfigError(Exception):
    """Errors related to the configuration for the Online CA Service middleware
    """


class OnlineCaMiddleware(object):
    """Web service interface for issuing certificates and providing CA trust
    roots

    @cvar CA_CLASS_FACTORY_OPTNAME: config file option name for Python path to
    function or class constructor to make a CA instance.  CA instance must
    implement CA interface class as defined in the interfaces module -
    onlineca.server.interfaces import OnlineCaInterface
    @type CA_CLASS_FACTORY_OPTNAME: string

    @cvar DEFAULT_CA_CLASS_FACTORY: default value for the key name in
    WSGI environ dict to assign to the Logon function created by this
    middleware
    @type DEFAULT_CA_CLASS_FACTORY: string

    @cvar CERT_REQ_POST_PARAM_KEYNAME: HTTP POST field name for the
    certificate request posted in logon calls
    @type CERT_REQ_POST_PARAM_KEYNAME: string

    @ivar ISSUE_CERT_URIPATH_OPTNAME: ini file option name for issue cert URI
    path parameter
    @type ISSUE_CERT_URIPATH_OPTNAME: string

    @ivar DEFAULT_ISSUE_CERT_URIPATH: URI sub-path for issue cert call
    @type DEFAULT_ISSUE_CERT_URIPATH: string

    @ivar TRUSTROOTS_URIPATH_OPTNAME: ini file option name for trustroots URI
    path parameter
    @type TRUSTROOTS_URIPATH_OPTNAME: string

    @ivar DEFAULT_TRUSTROOTS_URIPATH: URI sub-path for get trustroots call
    @type DEFAULT_TRUSTROOTS_URIPATH: string

    @cvar DEFAULT_PARAM_PREFIX: prefix for ini file option names
    @type DEFAULT_PARAM_PREFIX: string
    """

    # Options for ini file
    CA_CLASS_FACTORY_OPTNAME = 'ca_class_factory_path'

    # Default environ key names
    DEFAULT_CA_CLASS_FACTORY = 'onlineca.server.impl.CertificateAuthorityImpl'

    ISSUE_CERT_URIPATH_OPTNAME = 'issue_cert_uripath'
    DEFAULT_ISSUE_CERT_URIPATH = '/certificate/'

    CERT_SUBJECT_NAME_TEMPLATE_OPTNAME = 'cert_subject_name_template'

    TRUSTROOTS_URIPATH_OPTNAME = 'trustroots_uripath'
    DEFAULT_TRUSTROOTS_URIPATH = '/trustroots/'

    TRUSTROOTS_DIR_OPTNAME = 'trustroots_dir'
    DEFAULT_TRUSTROOTS_DIR = None

    CERT_CHAIN_FILEPATHS_OPTNAME = "cacert_chain_filepaths"
    CERT_CHAIN_FILEPATHS_OPT_DELIM = ','

    CERT_REQ_POST_PARAM_KEYNAME = 'certificate_request'

    __slots__ = (
        '_app',
        '__ca',
        '__ca_class_factory_path',
        '__issue_cert_uripath',
        '__cert_subject_name_template',
        '__trustroots_uripath',
        '__trustroots_dir',
        '__cacert_chain'
    )
    DEFAULT_PARAM_PREFIX = 'onlineca.server.'
    CA_DEFAULT_PARAM_PREFIX = 'ca_class.'

    def __init__(self, app):
        '''Create attributes

        @type app: function
        @param app: WSGI callable for next application in stack
        '''
        self._app = app
        self.__ca_class_factory_path = None
        self.__issue_cert_uripath = None
        self.__cert_subject_name_template = None
        self.__trustroots_uripath = None
        self.__trustroots_dir = None
        self.__cacert_chain = []
        self.__ca = None

    @classmethod
    def filter_app_factory(cls, app, global_conf, prefix=DEFAULT_PARAM_PREFIX,
                           **app_conf):
        obj = cls(app)
        obj.parse_config(prefix=prefix, **app_conf)

        return obj

    def parse_cacert_chain_files(self, *cacert_chain_filepaths):
        """Read in CA certificate files corresponding to chain of trust from
        this CA to a CA root.  These files can be set optionally to form part
        of the response back from issue_certificate call.  They don't apply
        in cases where this CA is a root CA or this CA is only when step down
        from a root CA.

        e.g. 1) Intermediate CA 1 and Intermediate CA 2 form a chain between
        this CA and a root CA: they *MAY* be set in *cacert_chain_filepaths so
        that a caller of issue_certificate gets them and can use them to make up
        the chain of trust to the root CA

        Root CA
            |_ Intermediate CA 1
                            |_ Intermediate CA 2
                                            |_ This CA

        Alternatively, in the above, the caller may be able to derive the
        intermediate CAs from another source - a separate CA trust bundle.  In
        this case there is no need to set the intermediate CAs here.

        e.g. 2)

        Root CA
            |_ This CA

        There are no intermediate CAs, there is no need to use this method

        e.g. 3)

        Root CA (= this CA)

        Again no intermediate CAs, no need to use this method
        """
        cacert_chain = []
        for cacert_chain_filepath in cacert_chain_filepaths:
            with open(cacert_chain_filepath, "r") as cacert_chainfile:
                pem_cert = cacert_chainfile.read()

            cacert_chain += [pem_cert]

        self.cacert_chain = cacert_chain

    def parse_config(self,
                     prefix=DEFAULT_PARAM_PREFIX,
                     ca_prefix=CA_DEFAULT_PARAM_PREFIX,
                     **app_conf):
        """Parse dictionary of configuration items updating the relevant
        attributes of this instance

        @type prefix: string
        @param prefix: prefix for configuration items
        @type ca_prefix: string
        @param ca_prefix: explicit prefix for CA class
        specific configuration items - ignored in this derived method
        @type app_conf: dict
        @param app_conf: PasteDeploy application specific configuration
        dictionary
        """

        # Extract parameters
        cls = self.__class__
        ca_class_factory_path_optname = prefix + cls.CA_CLASS_FACTORY_OPTNAME

        self.ca_class_factory_path = app_conf.get(ca_class_factory_path_optname,
                                                  cls.DEFAULT_CA_CLASS_FACTORY)

        issuecert_uripath_optname = prefix + cls.ISSUE_CERT_URIPATH_OPTNAME
        self.__issue_cert_uripath = app_conf.get(issuecert_uripath_optname,
                                                 cls.DEFAULT_ISSUE_CERT_URIPATH)

        cert_subj_name_optname = prefix + cls.CERT_SUBJECT_NAME_TEMPLATE_OPTNAME
        self.__cert_subject_name_template = app_conf.get(cert_subj_name_optname)
        if self.__cert_subject_name_template is None:
            raise OnlineCaMiddlewareConfigError('Error no certificate subject '
                                                'name template set (config '
                                                'option %r)' %
                                                cert_subj_name_optname)

        trustroot_uripath_optname = prefix + cls.TRUSTROOTS_URIPATH_OPTNAME
        self.__trustroots_uripath = app_conf.get(trustroot_uripath_optname,
                                                 cls.DEFAULT_TRUSTROOTS_URIPATH)

        trustroot_dir_optname = prefix + cls.TRUSTROOTS_DIR_OPTNAME
        self.__trustroots_dir = app_conf.get(trustroot_dir_optname,
                                             cls.DEFAULT_TRUSTROOTS_DIR)

        cacert_chain_filepaths_opt = prefix + cls.CERT_CHAIN_FILEPATHS_OPTNAME

        # Certificate chain to be returned with certificate issuing call
        # This is optional
        cacert_chain_filepaths_s = app_conf.get(cacert_chain_filepaths_opt)
        if cacert_chain_filepaths_s is not None:
            cacert_chain_filepaths = [
                filepath.strip() for filepath in cacert_chain_filepaths_s.split(
                                            cls.CERT_CHAIN_FILEPATHS_OPT_DELIM)
                ]
            self.parse_cacert_chain_files(*cacert_chain_filepaths)

        ca_opt_prefix = prefix + ca_prefix
        ca_opt_offset = len(ca_opt_prefix)
        ca_opt = {}
        for optname, optval in app_conf.items():
            if optname.startswith(ca_opt_prefix):
                ca_optname = optname[ca_opt_offset:]
                ca_opt[ca_optname] = optval

        self.instantiate_ca(**ca_opt)

    def instantiate_ca(self, **ca_object_kwargs):
        '''Create CA class instance
        @param ca_object_kwargs: keywords to CA class constructor
        '''
        self.__ca = call_module_object(self.ca_class_factory_path,
                                       object_properties=ca_object_kwargs)
        if not isinstance(self.__ca, OnlineCaInterface):
            raise TypeError('%r CA class factory must return a %r derived '
                            'type' % (self.ca_class_factory_path,
                                      type(OnlineCaInterface)))

    @property
    def ca_class_factory_path(self):
        return self.__ca_class_factory_path

    @ca_class_factory_path.setter
    def ca_class_factory_path(self, value):
        if not isinstance(value, six.string_types):
            raise TypeError('Expecting string type for "ca_class_factory_path"'
                            '; got %r type' % type(value))

        self.__ca_class_factory_path = value

    @property
    def issue_cert_uripath(self):
        """Get URI path for get trust roots method
        @rtype: string
        @return: path for get trust roots method
        """
        return self.__issue_cert_uripath

    @issue_cert_uripath.setter
    def issue_cert_uripath(self, value):
        """Set URI path for get trust roots method
        @type value: string
        @param value: path for get trust roots method
        """
        if not isinstance(value, six.string_types):
            raise TypeError('Expecting string type for '
                            '"issue_cert_uripath"; got %r' %
                            type(value))

        self.__issue_cert_uripath = value

    @property
    def cert_subject_name_template(self):
        return self.__cert_subject_name_template

    @cert_subject_name_template.setter
    def cert_subject_name_template(self, value):
        if not isinstance(value, six.string_types):
            raise TypeError('Expecting string type for '
                            '"cert_subject_name_template"; got %r' %
                            type(value))

        self.__cert_subject_name_template = value

    @property
    def trustroots_uripath(self):
        """Get URI path for get trust roots method
        @rtype: string
        @return: path for get trust roots method
        """
        return self.__trustroots_uripath

    @trustroots_uripath.setter
    def trustroots_uripath(self, value):
        """trust roots path
        """
        if not isinstance(value, six.string_types):
            raise TypeError('Expecting string type for "path"; got %r' %
                            type(value))

        self.__trustroots_uripath = value

    @property
    def trustroots_dir(self):
        """Get trust roots dir
        """
        return self.__trustroots_dir

    @trustroots_dir.setter
    def trustroots_dir(self, value):
        """trust roots dir
        """
        if not isinstance(value, six.string_types):
            raise TypeError('Expecting string type for "path"; got %r' %
                            type(value))

        self.__trustroots_dir = value

    @property
    def cacert_chain(self):
        """Optional property for cases where the certificate for this CA is an
        intermediate one.  Set the remaining intermediate CA certificates in
        the chain up to but not include the root

        These files can be set optionally to form part
        of the response back from issue_certificate call.  They don't apply
        in cases where this CA is a root CA or this CA is only when step down
        from a root CA.

        e.g. 1) Intermediate CA 1 and Intermediate CA 2 form a chain between
        this CA and a root CA: they *MAY* be set in *cacert_chain_filepaths so
        that a caller of issue_certificate gets them and can use them to make up
        the chain of trust to the root CA

        Root CA
            |_ Intermediate CA 1
                            |_ Intermediate CA 2
                                            |_ This CA

        Alternatively, in the above, the caller may be able to derive the
        intermediate CAs from another source - a separate CA trust bundle.  In
        this case there is no need to set the intermediate CAs here.

        e.g. 2)

        Root CA
            |_ This CA

        There are no intermediate CAs, there is no need to use this method

        e.g. 3)

        Root CA (= this CA)

        Again no intermediate CAs, no need to use this method

        :rtype: tuple
        """
        return tuple(self.__cacert_chain)

    @cacert_chain.setter
    def cacert_chain(self, value):
        """Optional property for cases where the certificate for this CA is an
        intermediate one.  Set this CA's cert and any remaining intermediate CA
        certificates in the chain up to but not including the root

        These files can be set optionally to form part
        of the response back from issue_certificate call.  They don't apply
        in cases where this CA is a root CA.

        e.g. 1) Intermediate CA 1 and Intermediate CA 2 and this CA form a chain
        between a certificate issued from this authority and a root CA: they
        *MAY* be set in *cacert_chain_filepaths so that a caller of
        issue_certificate gets them and can use them to make up the chain of
        trust to the root CA

        Root CA
            |_ Intermediate CA 1
                    |_ Intermediate CA 2
                            |_ This CA
                                    |_ new cert issued from this CA

        Alternatively, in the above, the caller may be able to derive the
        intermediate CAs from another source - a separate CA trust bundle.  In
        this case there is no need to set the intermediate CAs here.

        e.g. 2)

        Root CA
            |_ This CA
                    |_ new cert issued from this CA

        This CA is the single intermediate CA between newly issued certs and
        the root.  Set this CA's cert in the cacert_chain

        e.g. 3)

        Root CA (= this CA)

        There are no intermediate CAs, no need to use this method

        :param value: list of CA certificates in chain of trust from this CA
        to root CA
        :type value: any iterable of string PEM formatted certificates
        """
        for pem_cert in value:
            try:
                crypto.load_certificate(crypto.FILETYPE_PEM, pem_cert)
            except Exception as exc:
                raise TypeError('Expecting PEM format string for '
                                '"cacert_chain" elements got error: '
                                '{}'.format(exc))

        # Keep internally as a list
        self.__cacert_chain = list(value)

    def __call__(self, environ, start_response):
        '''Match request and call appropriate callback method

        @type environ: dict
        @param environ: WSGI environment variables dictionary
        @type start_response: function
        @param start_response: standard WSGI start response function
        '''
        log.debug("OnlineCaMiddleware.__call__ ...")
        request = Request(environ)

        try:
            response = self._process_request(request)

        except HTTPException as e:
            return e(environ, start_response)

        if response is None:
            return self._app(environ, start_response)
        else:
            start_response('200 OK',
                           [('Content-length', str(len(response))),
                            ('Content-type', 'text/plain')])
            return [response]

    def _process_request(self, request):
        if request.path_info == self.__issue_cert_uripath:
            response = self._issue_certificate(request)

        elif request.path_info == self.__trustroots_uripath:
            response = self._get_trustroots(request)
        else:
            response = None

        return response

    def _issue_certificate(self, request):
        '''Issue a new certificate from the Certificate Signing Request passed
        in the POST'd request

        @param request: HTTP request
        @type request: webob.Request
        @return: new certificate together with an intermediate CA certificates
        set in cacert_chain attribute
        @rtype: string
        '''

        if request.method != 'POST':
            response = "HTTP Request method not recognised"
            log.error("HTTP Request method %r not recognised", request.method)
            raise HTTPMethodNotAllowed(response, headers=[('Allow', 'POST')])

        # Extract cert request and convert to standard string - SSL library
        # will not accept unicode
        cert_req_key = self.__class__.CERT_REQ_POST_PARAM_KEYNAME
        str_cert_req = str(request.POST.get(cert_req_key))
        if str_cert_req is None:
            response = ("No %r form variable set in POST message" %
                        cert_req_key)
            log.error(response)
            raise HTTPBadRequest(response)

        log.debug("certificate request = %r", str_cert_req)

        # TODO: Deprecate PEM cert request support.
        # Support decoding based on PEM encoded request or similar, base64
        # encoded request.  The latter is a better approach, support both forms
        # for now until clients can be updated
        try:
            cert_req = crypto.load_certificate_request(crypto.FILETYPE_PEM,
                                                       str_cert_req)
        except crypto.Error:
            # Re-try, this time interpreting the text as a base64 encoded value
            try:
                der_cert_req = base64.b64decode(str_cert_req)
                cert_req = crypto.load_certificate_request(crypto.FILETYPE_ASN1,
                                                           der_cert_req)
            except crypto.Error:
                log.error("Error loading input certificate request: %r",
                          str_cert_req)
                raise HTTPBadRequest("Error loading input certificate request")

        subject_name_tmpl = string.Template(self.cert_subject_name_template)
        subject_name_str = subject_name_tmpl.substitute(**request.environ)

        subject_name = X509SubjectName.from_string(subject_name_str)
        subject_name_ = subject_name.as_openssl_x509_subject_name()

        cert = self.__ca.issue_certificate(cert_req, subject_name_,
                                           request.environ)

        cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

        # Return certificate and any additional CA certificates in the trust
        # chain
        return cert_pem + ''.join(self.__cacert_chain)

    def _get_trustroots(self, request):
        """Retrieve the set of trust roots (CA certificates and associated
        signing policy files) needed to trust this service.

        @param request: HTTP request
        @type request: webob.Request
        @rtype: string
        @return: trust roots base64 encoded and concatenated together
        """
        if request.method != 'GET':
            response = "HTTP Request method not recognised"
            log.error("HTTP Request method %r not recognised", request.method)
            raise HTTPMethodNotAllowed(response, headers=[('Allow', 'GET')])

        trust_roots = b''
        for filename in os.listdir(self.trustroots_dir):
            filepath = os.path.join(self.trustroots_dir, filename)
            if os.path.isdir(filepath):
                continue

            with open(filepath, 'rb') as trustroot_file:
                file_content = trustroot_file.read()

            trust_roots += b"%s=%s\n" % (_string2bytes(filename),
                                         base64.b64encode(file_content))

        return trust_roots
