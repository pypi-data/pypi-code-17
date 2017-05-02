# coding=utf-8
import argparse
import asyncio
import json
import logging
import os
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from cachetools import TTLCache
import aiohttp
from dns.resolver import Resolver
from dnslib import *
from retry import retry

from aiosocks.connector import ProxyConnector, ProxyClientRequest


class GoogleDirectConnector(aiohttp.TCPConnector):
    def __init__(self, google_ip):
        super().__init__()
        self.google_ip = google_ip

    @asyncio.coroutine
    def _resolve_host(self, host, port):
        return [{'hostname': 'dns.google.com', 'host': str(self.google_ip), 'port': 443,
                 'family': self._family, 'proto': 0, 'flags': 0}]


class DNSServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, loop=None, semaphore=None, public_ip=None, proxy_ip=None, google_ip=None, domain_set=None,
                 socks_proxy=None, cache_size=None, cache_ttl=None):
        self.loop = loop
        self.semaphore = semaphore
        self.public_ip = public_ip
        self.proxy_ip = proxy_ip
        self.domain_set = domain_set
        self.google_ip = google_ip
        self.socks_proxy = socks_proxy
        self.cache = TTLCache(maxsize=cache_size, ttl=cache_ttl)
        if self.socks_proxy:
            self.base_url = 'https://{}/resolve?'.format('dns.google.com')
        else:
            self.base_url = 'https://{}/resolve?'.format(google_ip)

        self.headers = {'Host': 'dns.google.com'}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, client):
        try:
            request = DNSRecord.parse(data)
        except DNSError:
            return None
        else:
            asyncio.ensure_future(self.query_and_answer(request=request, client=client))

    def match_client_ip(self, query_name):
        if self.public_ip == self.proxy_ip:
            return self.public_ip
        else:
            if any(str(query_name)[:-1].endswith(x) for x in self.domain_set):
                return self.proxy_ip
            return self.public_ip

    @retry(exceptions=aiohttp.client_exceptions.ClientConnectionError, tries=3)
    async def http_fetch(self, url):
        with await self.semaphore:
            if self.socks_proxy:
                connector = ProxyConnector(remote_resolve=True)
                request_class = ProxyClientRequest

            else:
                connector = GoogleDirectConnector(self.google_ip)
                request_class = aiohttp.client_reqrep.ClientRequest

            with aiohttp.ClientSession(loop=self.loop, connector=connector, request_class=request_class) as session:
                try:
                    async with session.get(url, proxy=self.socks_proxy, headers=self.headers) as resp:
                        result = await resp.read()
                        return result
                except aiohttp.client_exceptions.ClientConnectionError:
                    # FIXME,should we retry in aiohttp or just leave it to client?
                    pass

    @staticmethod
    def build_answer_from_json(request, json_item):
        ans = request.reply()
        ans.header.rcode = json_item['Status']
        if 'Answer' in json_item.keys():
            for answer in json_item['Answer']:
                q_type = QTYPE[answer['type']]
                q_type_class = globals()[q_type]
                ans.add_answer(
                    RR(rname=answer['name'], rtype=answer['type'], ttl=answer['TTL'],
                       rdata=q_type_class(answer['data'])))
        elif 'Authority' in json_item.keys():
            for auth in json_item['Authority']:
                q_type = QTYPE[auth['type']]
                q_type_class = globals()[q_type]
                ans.add_auth(RR(rname=auth['name'], rtype=auth['type'], ttl=auth['TTL'],
                                rdata=q_type_class(auth['data'])))
        packet_resp = ans.pack()
        return packet_resp

    def return_serv_fail(self, request, client):
        ans = request.reply()
        ans.header.rcode = 2
        packet_resp = ans.pack()
        self.transport.sendto(packet_resp, client)

    async def query_and_answer(self, request, client):
        logging.debug('Request name: {}, Request type:{}.'.format(request.q.qname, QTYPE[request.q.qtype]))
        serv_fail = False
        if self.cache.get(request.q.qname) and 'Answer' in self.cache.get(request.q.qname).keys():
            json_resp = self.cache.get(request.q.qname)
            logging.debug('Cached:{}'.format(request.q.qname))
        else:
            logging.debug('Fetch:{}'.format(request.q.qname))
            client_ip = self.match_client_ip(request.q.qname) + '/24'
            url = self.base_url + urlencode(
                {'name': request.q.qname, 'type': request.q.qtype, 'edns_client_subnet': client_ip})
            logging.debug('Querying URL:{}.'.format(url))
            http_resp = await self.http_fetch(url)
            if http_resp:
                json_resp = json.loads(http_resp)
                self.cache[request.q.qname] = json_resp
            else:
                logging.debug('Return Serv Fail!')
                serv_fail = True
        if serv_fail:
            self.return_serv_fail(request, client)
        else:
            packet_resp = self.build_answer_from_json(request, json_resp)
            self.transport.sendto(packet_resp, client)


class AsyncDNS(object):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', default=5454, nargs='?', help='Port For Async DNS Server To Listen')
        parser.add_argument('-i', '--ip', nargs='?',
                            help='IP Of Proxy Server To Bypass GFW')
        parser.add_argument('-f', '--file', default='BlockedDomains.dat', nargs='?',
                            help='File That Contains Blocked Domains')
        parser.add_argument('-d', '--debug', action='store_true',
                            help='Enable Debug Logging')
        parser.add_argument('-s', '--socks', nargs='?', help='Socks Proxy IP:Port In Format Like: 127.0.0.1:1086')
        parser.add_argument('-c', '--cache', default=1000, nargs='?', help='DNS Cache Size In Items')
        parser.add_argument('-t', '--ttl', default=1800, nargs='?', help='DNS Cache Time To Live In Seconds')

        args = parser.parse_args()
        parser.set_defaults(debug=False)

        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        if args.file == 'BlockedDomains.dat':
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cur_dir, args.file)
        else:
            file_path = 'BlockedDomains.dat'
        if args.socks:
            socks_proxy = 'socks5://' + args.socks
        else:
            socks_proxy = None

        self.server_loop(args.port, args.ip, file_path, socks_proxy, args.cache, args.ttl)

    @staticmethod
    def resolve_ip(domain):
        resolver = Resolver()
        resolver.nameservers = ['114.114.114.114', '119.29.29.29']
        ip = resolver.query(domain).rrset.items[0]
        return ip

    def get_public_ip(self):
        headers = {'Host': 'ip.taobao.com'}
        req = Request(url='http://{}/service/getIpInfo.php?ip=myip'.format(self.resolve_ip('ip.taobao.com')),
                      headers=headers)
        response = urlopen(req)
        public_ip = json.loads(response.read())['data']['ip']
        logging.info('Your Public IP:{}'.format(public_ip))
        return public_ip

    @staticmethod
    def read_domain_file(file_name):
        domain_set = set()
        with open(file_name) as fp:
            for line in fp:
                domain_set.add(line.strip())
        return domain_set

    def server_loop(self, port, proxy_ip, domain_file, socks_proxy, cache_size, cache_ttl):

        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(20)
        google_ip = self.resolve_ip('dns.google.com')
        logging.debug('Google IP:{}'.format(google_ip))
        public_ip = self.get_public_ip()
        if not proxy_ip:
            proxy_ip = public_ip
        listen = loop.create_datagram_endpoint(
            lambda: DNSServerProtocol(loop=loop, semaphore=semaphore, public_ip=public_ip,
                                      proxy_ip=proxy_ip, google_ip=google_ip,
                                      domain_set=self.read_domain_file(domain_file), socks_proxy=socks_proxy,
                                      cache_size=cache_size, cache_ttl=cache_ttl),
            local_addr=('0.0.0.0', port))
        transport, protocol = loop.run_until_complete(listen)
        logging.info("Running Local DNS Server At Address: {}:{} ...".format(transport.get_extra_info('sockname')[0],
                                                                             transport.get_extra_info('sockname')[1]))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logging.info('Shutting down DNS Server!')

        transport.close()
        loop.close()


def main():
    server = AsyncDNS()
    server.run()


if __name__ == '__main__':
    main()
