# This file is part of caucase
# Copyright (C) 2017  Nexedi
#     Alain Takoudjou <alain.takoudjou@nexedi.com>
#     Vincent Pelletier <vincent@nexedi.com>
#
# caucase is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# caucase is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with caucase.  If not, see <http://www.gnu.org/licenses/>.

import os, errno
import time
import ConfigParser
import logging
import requests
import argparse
import traceback
import pem
import json
from OpenSSL import crypto
from caucase import utils
from datetime import datetime

CSR_KEY_FILE = 'csr.key.txt'
RENEW_CSR_KEY_FILE = 'renew_csr.key.txt'

def parseArguments():
  """
  Parse arguments for Certificate Authority Request.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('--ca-url',
                      required=True,
                      help='Certificate Authority URL')
  parser.add_argument('-c', '--ca-crt-file',
                      default='ca.crt.pem',
                      help='Path for CA Cert file. default: %(default)s')
  parser.add_argument('-x', '--crt-file',
                      default='crt.pem',
                      help='Path for Certificate file. default: %(default)s')
  parser.add_argument('-k', '--key-file',
                      default='key.pem',
                      help='Path of key file. default: %(default)s')
  parser.add_argument('-s', '--csr-file',
                      default='csr.pem',
                      help='Path where to store csr file. default: %(default)s')
  parser.add_argument('--digest',
                      default="sha256",
                      help='Digest used to sign data. default: %(default)s')
  parser.add_argument('--cn',
                      help='Common name to use for request new certificate')
  parser.add_argument('--no-check-certificate',
                      action='store_false', default=True, dest='verify_certificate',
                      help='When connecting to CA on HTTPS, disable certificate verification.')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('--request', action='store_true',
                      help='Request a new Certificate')
  group.add_argument('--revoke', action='store_true',
                      help='Revoke existing certificate')
  group.add_argument('--renew', action='store_true',
                      help='Renew current certificate and and replace with existing files')

  return parser



def requestCertificate(config):

  ca_request = CertificateAuthorityRequest(config.key_file, config.crt_file,
          config.ca_crt_file, config.ca_url, digest=config.digest,
          verify_certificate=config.verify_certificate)

  # download or update ca crt file
  ca_request.getCACertificateChain()

  if os.path.exists(config.crt_file):
    return

  if not os.path.exists(config.csr_file):
      csr = ca_request.generateCertificateRequest(config.key_file,
          cn=config.cn, csr_file=config.csr_file)
  else:
    csr = open(config.csr_file).read()

  ca_request.signCertificate(csr)


def revokeCertificate(config):

  os.close(os.open(config.key_file, os.O_RDONLY))
  os.close(os.open(config.crt_file, os.O_RDONLY))

  ca_revoke = CertificateAuthorityRequest(config.key_file, config.crt_file,
          config.ca_crt_file, config.ca_url, digest=config.digest,
          verify_certificate=config.verify_certificate)

  # download or update ca crt file
  ca_revoke.getCACertificateChain()

  ca_revoke.revokeCertificate()

def renewCertificate(config, backup_dir):

  os.close(os.open(config.key_file, os.O_RDONLY))
  os.close(os.open(config.crt_file, os.O_RDONLY))

  ca_renew = CertificateAuthorityRequest(config.key_file, config.crt_file,
          config.ca_crt_file, config.ca_url, digest=config.digest,
          verify_certificate=config.verify_certificate)

  # download or update ca crt file
  ca_renew.getCACertificateChain()

  ca_renew.renewCertificate(config.csr_file, backup_dir)

def main():
  parser = parseArguments()
  config = parser.parse_args()

  base_dir = os.path.dirname(config.crt_file)
  os.chdir(os.path.abspath(base_dir))

  if config.request:
    if not config.cn or not config.ca_url:
      parser.print_help()
      exit(1)

    requestCertificate(config)

  elif config.revoke:
    if not config.ca_url:
      parser.print_help()
      exit(1)

    revokeCertificate(config)
  
  elif config.renew:
    backup_dir = os.path.join('.', 'old-%s' % datetime.now().strftime('%Y%m%d%H%M%S'))

    os.mkdir(backup_dir)
    if os.path.exists(CSR_KEY_FILE):
      os.rename(CSR_KEY_FILE, os.path.join(backup_dir, CSR_KEY_FILE))
    if os.path.exists(config.csr_file):
      base_name = os.path.basename(config.csr_file)
      os.rename(config.csr_file, os.path.join(backup_dir, base_name))

    renewCertificate(config, backup_dir)
  else:
    parser.print_help()
    exit(1)

class CertificateAuthorityRequest(object):

  def __init__(self, key, certificate, cacertificate, ca_url,
               max_retry=10, digest="sha256",
               verify_certificate=False, logger=None):

    self.key = key
    self.certificate = certificate
    self.cacertificate = cacertificate
    self.ca_url = ca_url
    self.logger = logger
    self.max_retry = max_retry
    self.digest = digest
    self.extension_manager = utils.X509Extension()
    self.ca_certificate_list = []
    self.verify_certificate = verify_certificate

    while self.ca_url.endswith('/'):
      # remove all / at end or ca_url
      self.ca_url = self.ca_url[:-1]

    if os.path.exists(self.cacertificate):
      self.ca_certificate_list = [
          crypto.load_certificate(crypto.FILETYPE_PEM, x._pem_bytes) for x in
          pem.parse_file(self.cacertificate)
        ]
      

    if self.logger is None:
      self.logger = logging.getLogger('Certificate Request')
      self.logger.setLevel(logging.DEBUG)
      handler = logging.StreamHandler()
      handler.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
      handler.setFormatter(formatter)

      self.logger.addHandler(handler)

    self.generatePrivatekey(self.key)

  def _request(self, method, url, data={}):
    try:
      req = getattr(requests, method)
      kw = {}
      if data:
        kw['data'] = data
      kw['verify'] = self.verify_certificate
      return req(url, **kw)
    except requests.ConnectionError, e:
      self.logger.error("Got ConnectionError while sending request to CA. Url is %s\n%s" % (
          url, str(e)))
      return None

  def _checkCertEquals(self, first_cert, second_cert):
    """
      Say if two certificate PEM object are the same
      
      XXX - more checks should be done ?
    """

    return first_cert.set_subject().CN == second_cert.get_subject().CN and \
              first_cert.get_serial_number() == second_cert.get_serial_number()

  def _writeNewFile(self, file_path, content, mode=0644):
    fd = os.open(file_path,
                  os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_TRUNC, mode)
    try:
      os.write(fd, content)
    finally:
      os.close(fd)

  def generateCertificateRequest(self, key_file, cn,
      country='', state='', locality='', email='', organization='',
      organization_unit='', csr_file=None):

    with open(key_file) as fkey:
      key = crypto.load_privatekey(crypto.FILETYPE_PEM, fkey.read())

    req = crypto.X509Req()
    subject = req.get_subject()
    subject.CN = cn
    if country:
      subject.C = country
    if state:
      subject.ST = state
    if locality:
      subject.L = locality
    if organization:
      subject.O = organization
    if organization_unit:
      subject.OU = organization_unit
    if email:
      subject.emailAddress = email
    req.set_pubkey(key)
    self.extension_manager.setDefaultCsrExtensions(req)
    req.sign(key, self.digest)

    csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)

    if csr_file is not None:
      with open(csr_file, 'w') as req_file:
        req_file.write(csr)
    
      os.chmod(csr_file, 0640)

    return csr

  def generatePrivatekey(self, output_file, size=2048):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, size)

    try:
      key_fd = os.open(output_file,
                       os.O_CREAT|os.O_WRONLY|os.O_EXCL|os.O_TRUNC,
                       0600)
    except OSError, e:
      if e.errno != errno.EEXIST:
        raise
    else:
      os.write(key_fd, crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
      os.close(key_fd)

  def checkCertificateValidity(self, cert):
    cert_pem = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    pkey = open(self.key).read()
    key_pem = crypto.load_privatekey(crypto.FILETYPE_PEM, pkey)

    return utils.checkCertificateValidity(
              self.ca_certificate_list,
              cert_pem,
              key_pem)

  def getValidCACertificateChain(self):
    ca_cert_url = '%s/crt/ca.crt.json' % self.ca_url
    self.logger.info("Updating CA certificate file from %s" % ca_cert_url)
    cert_list = response_json = []
    cert_list_chain = ""
    response = self._request('get', ca_cert_url)
    while not response or response.status_code != 200:
      # sleep a bit then try again until  ca cert is ready
      time.sleep(10)
      response = self._request('get', ca_cert_url)

    response_json = json.loads(response.text)

    if len(response_json) > 0:
      iter_ca_cert = iter(response_json)
      is_valid = False
      payload = utils.unwrap(iter_ca_cert.next(), lambda x: x['old'], [self.digest])
      # check that old certificate is known
      old_x509 = crypto.load_certificate(crypto.FILETYPE_PEM, payload['old'])
      for x509 in self.ca_certificate_list:
        if self._checkCertEquals(x509, old_x509):
          is_valid = True

      if not is_valid:
        # no local certificate matches
        raise CertificateVerificationError("Updated CA Certificate chain could " \
            "not be validated using local CA Certificate at %r. \nYou can " \
            "try removing your local ca file if it was not updated for more " \
            "that a year." % self.cacertificate)

      # if not old_x509.has_expired():
      cert_list.append(old_x509)
      cert_list.append(
          crypto.load_certificate(crypto.FILETYPE_PEM, payload['new'])
        )
      cert_list_chain = "%s\n%s" % (payload['old'], payload['new'])

      for next_itmen in iter_ca_cert:
        payload = utils.unwrap(next_itmen, lambda x: x['old'], [self.digest])
        old_x509 = crypto.load_certificate(crypto.FILETYPE_PEM, payload['old'])
        if self._checkCertEquals(cert_list[-1], old_x509):
          cert_list.append(
              crypto.load_certificate(crypto.FILETYPE_PEM, payload['new'])
            )
          cert_list_chain += "\n%s" % payload['new']
        else:
          raise CertificateVerificationError("Get updated CA Certificate " \
              "retourned %s but validation of data failed" % response_json)

    # dump into file
    if not cert_list_chain or not cert_list:
      return
    self.ca_certificate_list = cert_list
    fd = os.open(self.cacertificate, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0640)
    try:
      for cert in cert_list:
        os.write(fd, cert_list_chain)
    finally:
      os.close(fd)

  def getCACertificateChain(self):

    # If cert file exists exist
    if os.path.exists(self.cacertificate) and os.stat(self.cacertificate).st_size > 0:
      # Get all valids CA certificate
      return self.getValidCACertificateChain()

    ca_cert_url = '%s/crt/ca.crt.pem' % self.ca_url
    self.logger.info("getting CA certificate file %s" % ca_cert_url)
    response = None
    while not response or response.status_code != 200:
      response = self._request('get', ca_cert_url)
      if response is not None:
        try:
          x509 = crypto.load_certificate(crypto.FILETYPE_PEM, response.text)
        except crypto.Error, e:
          traceback.print_exc()
          response = None
        else:
          self.ca_certificate_list = [x509]
          break
      # sleep a bit then try again until  ca cert is ready
      time.sleep(10)

    fd = os.open(self.cacertificate,
                  os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_TRUNC, 0640)
    try:
      os.write(fd, response.text)
    finally:
      os.close(fd)

  def signCertificate(self, csr):

    if os.path.exists(self.certificate) and os.stat(self.certificate).st_size > 0:
      return

    data = {'csr': csr}
    retry = 0
    sleep_time = 10
    request_url = '%s/csr' % self.ca_url
    csr_key = ""

    self.logger.info("Request signed certificate from CA...")
    if os.path.exists(CSR_KEY_FILE):
      with open(CSR_KEY_FILE) as fkey:
        csr_key = fkey.read()

    if csr_key:
      self.logger.info("Csr was already sent to CA, using csr : %s" % csr_key)
    else:
      response = self._request('put', request_url, data=data)

      while (not response or response.status_code != 201) and retry < self.max_retry:

        self.logger.error("%s: Failed to sent CSR. \n%s" % (
            response.status_code, response.text))
        self.logger.info("will retry in %s seconds..." % sleep_time)
        time.sleep(sleep_time)
        retry += 1
        response = self._request('put', request_url, data=data)

      if response.status_code != 201:
        raise Exception("ERROR: failed to put CSR after % retry. Exiting..." % retry)

      self.logger.info("CSR succefully sent.")
      # Get csr Location from request header: http://xxx.com/csr/key
      self.logger.debug("Csr location is: %s" % response.headers['Location'])

      csr_key = response.headers['Location'].split('/')[-1]
      with open(CSR_KEY_FILE, 'w') as fkey:
        fkey.write(csr_key)

      # csr is xxx.csr.pem so cert is xxx.cert.pem
    self.logger.info("Waiting for signed certificate...")

    reply_url = '%s/crt/%s.crt.pem' % (self.ca_url, csr_key[:-8])
    response = self._request('get', reply_url)

    while not response or response.status_code != 200:
      time.sleep(sleep_time)
      response = self._request('get', reply_url)

    self.logger.info("Validating signed certificate...")
    if not self.checkCertificateValidity(response.text):
      # certificate verification failed, should raise ?
      self.logger.warn("Certificate validation failed.\n" \
        "Please double check the signed certificate before use. Also consider" \
        "revoke it and request a new signed certificate.")

    fd = os.open(self.certificate,
                  os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_TRUNC, 0644)
    try:
      os.write(fd, response.text)
    finally:
      os.close(fd)
    self.logger.info("Certificate correctly saved at %s." % self.certificate)

  def revokeCertificate(self, message=""):
    """
    Send a revocation request for the givent certificate to the master.
    """
    sleep_time = 10
    retry = 1

    pkey = open(self.key).read()
    cert = open(self.certificate).read()
    cert_pem = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

    payload = dict(
      reason=message,
      revoke_crt=cert)

    wrapped = utils.wrap(payload, pkey, [self.digest])
    request_url = '%s/crt/revoke' % self.ca_url
    data = {'payload': json.dumps(wrapped)}

    self.logger.info("Sent Certificate revocation request for CN: %s." % (
                      cert_pem.get_subject().CN))

    response = self._request('put', request_url, data=data)
    break_code = [201, 404, 500, 404]

    while response is None or response.status_code not in break_code:
      self.logger.error("%s: Failed to send revoke request. \n%s" % (
          response.status_code, response.text))

      self.logger.info("will retry in %s seconds..." % sleep_time)
      time.sleep(sleep_time)

      response = self._request('put', request_url, data=data)
      retry += 1
      if retry < self.max_retry:
        break

    if response.status_code != 201:
      raise Exception("ERROR: failed to put revoke certificate after %s retry. Exiting..." % retry)

    self.logger.info("Certificate %s was successfully revoked." % (
                      self.certificate))

  def renewCertificate(self, csr_file, backup_dir, backup_key=True):
    """
    Renew the current certificate. Regenerate private key if backup_key is `True`
    """
    sleep_time = 10
    retry = 1
    new_key_path = '%s.renew' % self.key
    new_cert_path = '%s.renew' % self.certificate
    key_file = self.key
    cert = open(self.certificate).read()
    cert_pem = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    csr_key = ""

    try:
      if backup_key:
        self.generatePrivatekey(new_key_path)
        key_file = new_key_path

      if not os.path.exists(csr_file):
        csr = self.generateCertificateRequest(key_file,
                                                  cn=cert_pem.get_subject().CN,
                                                  csr_file=csr_file)
      else:
        csr = open(csr_file).read()

      if os.path.exists(RENEW_CSR_KEY_FILE):
        csr_key = open(RENEW_CSR_KEY_FILE).read()

      if not csr_key:
        payload = dict(
          renew_csr=csr,
          crt=cert)

        pkey = open(self.key).read()
        wrapped = utils.wrap(payload, pkey, [self.digest])
        request_url = '%s/crt/renew' % self.ca_url
        data = {'payload': json.dumps(wrapped)}

        self.logger.info("Send Certificate Renewal request for CN: %s." % (
                          cert_pem.get_subject().CN))

        response = self._request('put', request_url, data=data)
        break_code = [201, 404, 500, 404]

        while response is None or response.status_code not in break_code:
          self.logger.error("%s: Failed to send renewal request. \n%s" % (
              response.status_code, response.text))
          self.logger.info("will retry in %s seconds..." % sleep_time)
          time.sleep(sleep_time)

          response = self._request('put', request_url, data=data)
          retry += 1
          if retry < self.max_retry:
            break

        if response.status_code != 201:
          raise Exception("ERROR: failed to put certificate renewal request after %s retry. Exiting...\n%s" % (
                            retry, response.text))

        csr_key = response.headers['Location'].split('/')[-1]
        with open(RENEW_CSR_KEY_FILE, 'w') as fkey:
          fkey.write(csr_key)

      self.logger.info("Waiting for signed certificate...")

      reply_url = '%s/crt/%s.crt.pem' % (self.ca_url, csr_key[:-8])
      response = self._request('get', reply_url)

      while not response or response.status_code != 200:
        time.sleep(sleep_time)
        response = self._request('get', reply_url)

      self.logger.info("Validating signed certificate...")

      self._writeNewFile(new_cert_path, response.text)
      # change location of files
      if backup_key:
        os.rename(self.key,
                  os.path.join(backup_dir, os.path.basename(self.key)))
        os.rename(new_key_path, self.key)
        self.logger.info("Private correctly renewed at %s." % self.key)

      os.rename(self.certificate,
                os.path.join(backup_dir, os.path.basename(self.certificate)))
      os.rename(new_cert_path, self.certificate)


      if not self.checkCertificateValidity(response.text):
        # certificate verification failed, should raise ?
        self.logger.warn("Certificate validation failed.\n" \
          "Please double check the signed certificate before use. Also consider" \
          "revoke it and request a new signed certificate.")
      else:
        self.logger.info("Certificate correctly renewed at %s." % self.certificate)
    except:
      raise
    else:
      for path in [csr_file, RENEW_CSR_KEY_FILE]:
        if os.path.exists(path):
          os.unlink(path)
    finally:
      for path in [new_cert_path, new_key_path]:
        if os.path.exists(path):
          os.unlink(path)

