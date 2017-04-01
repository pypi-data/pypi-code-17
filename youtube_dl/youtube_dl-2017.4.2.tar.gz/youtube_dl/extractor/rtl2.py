# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import int_or_none


class RTL2IE(InfoExtractor):
    _VALID_URL = r'http?://(?:www\.)?rtl2\.de/[^?#]*?/(?P<id>[^?#/]*?)(?:$|/(?:$|[?#]))'
    _TESTS = [{
        'url': 'http://www.rtl2.de/sendung/grip-das-motormagazin/folge/folge-203-0',
        'info_dict': {
            'id': 'folge-203-0',
            'ext': 'f4v',
            'title': 'GRIP sucht den Sommerkönig',
            'description': 'md5:e3adbb940fd3c6e76fa341b8748b562f'
        },
        'params': {
            # rtmp download
            'skip_download': True,
        },
    }, {
        'url': 'http://www.rtl2.de/sendung/koeln-50667/video/5512-anna/21040-anna-erwischt-alex/',
        'info_dict': {
            'id': '21040-anna-erwischt-alex',
            'ext': 'mp4',
            'title': 'Anna erwischt Alex!',
            'description': 'Anna nimmt ihrem Vater nicht ab, dass er nicht spielt. Und tatsächlich erwischt sie ihn auf frischer Tat.'
        },
        'params': {
            # rtmp download
            'skip_download': True,
        },
    }]

    def _real_extract(self, url):
        # Some rtl2 urls have no slash at the end, so append it.
        if not url.endswith('/'):
            url += '/'

        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        mobj = re.search(
            r'<div[^>]+data-collection="(?P<vico_id>\d+)"[^>]+data-video="(?P<vivi_id>\d+)"',
            webpage)
        if mobj:
            vico_id = mobj.group('vico_id')
            vivi_id = mobj.group('vivi_id')
        else:
            vico_id = self._html_search_regex(
                r'vico_id\s*:\s*([0-9]+)', webpage, 'vico_id')
            vivi_id = self._html_search_regex(
                r'vivi_id\s*:\s*([0-9]+)', webpage, 'vivi_id')

        info = self._download_json(
            'http://www.rtl2.de/sites/default/modules/rtl2/mediathek/php/get_video_jw.php',
            video_id, query={
                'vico_id': vico_id,
                'vivi_id': vivi_id,
            })
        video_info = info['video']
        title = video_info['titel']

        formats = []

        rtmp_url = video_info.get('streamurl')
        if rtmp_url:
            rtmp_url = rtmp_url.replace('\\', '')
            stream_url = 'mp4:' + self._html_search_regex(r'/ondemand/(.+)', rtmp_url, 'stream URL')
            rtmp_conn = ['S:connect', 'O:1', 'NS:pageUrl:' + url, 'NB:fpad:0', 'NN:videoFunction:1', 'O:0']

            formats.append({
                'format_id': 'rtmp',
                'url': rtmp_url,
                'play_path': stream_url,
                'player_url': 'http://www.rtl2.de/flashplayer/vipo_player.swf',
                'page_url': url,
                'flash_version': 'LNX 11,2,202,429',
                'rtmp_conn': rtmp_conn,
                'no_resume': True,
                'preference': 1,
            })

        m3u8_url = video_info.get('streamurl_hls')
        if m3u8_url:
            formats.extend(self._extract_akamai_formats(m3u8_url, video_id))

        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': title,
            'thumbnail': video_info.get('image'),
            'description': video_info.get('beschreibung'),
            'duration': int_or_none(video_info.get('duration')),
            'formats': formats,
        }
