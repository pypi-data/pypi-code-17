# coding=utf-8
from dnslib import *
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from dns.resolver import Resolver
from aiosocks.connector import ProxyConnector, ProxyClientRequest
import os
import json
import logging
import argparse
import asyncio
import aiohttp


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
                 socks_proxy=None):
        self.loop = loop
        self.semaphore = semaphore
        self.public_ip = public_ip
        self.proxy_ip = proxy_ip
        self.domain_set = domain_set
        self.google_ip = google_ip
        self.socks_proxy = socks_proxy
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

    async def http_fetch(self, url):
        with await self.semaphore:
            if self.socks_proxy:
                with aiohttp.ClientSession(loop=self.loop, connector=ProxyConnector(remote_resolve=True),
                                           request_class=ProxyClientRequest) as session:
                    async with session.get(url, proxy=self.socks_proxy, headers=self.headers) as resp:
                        result = await resp.read()
                        return result

            else:
                with aiohttp.ClientSession(loop=self.loop, connector=GoogleDirectConnector(self.google_ip)) as session:
                    async with session.get(url, headers=self.headers) as resp:
                        result = await resp.read()
                        return result

    async def query_and_answer(self, request, client):
        logging.debug(request.q.qname)
        client_ip = self.match_client_ip(request.q.qname) + '/24'
        url = self.base_url + urlencode(
            {'name': request.q.qname, 'type': request.q.qtype, 'edns_client_subnet': client_ip})
        logging.debug(url)
        resp = json.loads(await self.http_fetch(url))
        ans = request.reply()
        ans.header.rcode = resp['Status']
        if 'Answer' in resp.keys():
            for answer in resp['Answer']:
                q_type = QTYPE[answer['type']]
                q_type_class = globals()[q_type]
                ans.add_answer(
                    RR(rname=answer['name'], rtype=answer['type'], ttl=answer['TTL'],
                       rdata=q_type_class(answer['data'])))
        elif 'Authority' in resp.keys():
            for auth in resp['Authority']:
                q_type = QTYPE[auth['type']]
            q_type_class = globals()[q_type]
            ans.add_auth(RR(rname=auth['name'], rtype=auth['type'], ttl=auth['TTL'],
                            rdata=q_type_class(auth['data'])))
        packet_resp = ans.pack()
        self.transport.sendto(packet_resp, client)


class AsyncDNS(object):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--port', default=5454, nargs='?', help='Port for async dns server to listen')
        parser.add_argument('-i', '--ip', nargs='?',
                            help='IP of proxy server to bypass gfw')
        parser.add_argument('-f', '--file', default='BlockedDomains.dat', nargs='?',
                            help='file that contains blocked domains')
        parser.add_argument('-d', '--debug', default=False, nargs='?',
                            help='enable debug logging')
        parser.add_argument('-s', '--socks', nargs='?', help='socks proxy IP:Port in format like: 127.0.0.1:1086')

        args = parser.parse_args()

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

        self.server_loop(args.port, args.ip, file_path, socks_proxy)

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

    def server_loop(self, port, proxy_ip, domain_file, socks_proxy):

        loop = asyncio.get_event_loop()
        semaphore = asyncio.Semaphore(10)
        google_ip = self.resolve_ip('dns.google.com')
        logging.debug('Google IP:{}'.format(google_ip))
        public_ip = self.get_public_ip()
        if not proxy_ip:
            proxy_ip = public_ip
        listen = loop.create_datagram_endpoint(
            lambda: DNSServerProtocol(loop=loop, semaphore=semaphore, public_ip=public_ip,
                                      proxy_ip=proxy_ip, google_ip=google_ip,
                                      domain_set=self.read_domain_file(domain_file), socks_proxy=socks_proxy),
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
