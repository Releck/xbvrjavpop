import requests
import os
import time
from pathlib import Path
import re

XBVR_HOST = 'http://localhost:9999'
CHINESE_CASINOS = [
    'xhd1080.com',
    'hjd2048.com',
    'ses23.com',
    'big2048.com',
    'dioguitar23.net',
    'fengniao151.vip',
    'fbfb.me',
    'bbs2048.org',
    'fun2048.com'
]
DELAY_SCRAPE_SECS = 5


def match_code(title):
    for c in CHINESE_CASINOS:
        if c in title:
            title = title.replace(c, '')
    match = re.search(pattern='([a-zA-Z]{2,6}|3DSVR|AVOPENVR)[-]?([0-9]{2,5})', string=title)
    if match:
        # DSVR-001 = 3DSVR-0001
        pfx = match.group(1).upper()
        serial = match.group(2)
        if pfx == 'DSVR':
            pfx = '3DSVR'
        if pfx == '3DSVR':
            serial = str(int(serial)).zfill(4)
        else:
            serial = str(int(serial)).zfill(3)
        code = f'{pfx}-{serial}'
        return code


def seek_matches():
    unmatched = requests.post(f'{XBVR_HOST}/api/files/list',
                          json={"sort": "created_time_desc", "state": "unmatched", "createdDate": [],
                                "resolutions": [], "framerates": [], "bitrates": [], "limit": 99999}).json()
    already_matched = set()
    for unmatch in unmatched:
        p = Path(os.path.join(unmatch['path'], unmatch['filename']))
        potential_match = match_code(unmatch['filename'])
        if not potential_match:
            potential_match = match_code(p.parent.name)
            if not potential_match:
                print(f'Couldn\'t match {p}')
                continue
        match = match_code(potential_match)
        print(f'Matched {p} to {match}')
        if match not in already_matched:
            qmatch = match
            if match.split('-')[0] == '3DSVR':
                qmatch = match[1:]
            resp = requests.post(f'{XBVR_HOST}/api/task/scrape-javr', json={'q': qmatch})
            if resp.ok:
                already_matched.add(match)
                print(f'Added {match} to XBVR')
            time.sleep(DELAY_SCRAPE_SECS)
        resp = requests.post(f'{XBVR_HOST}/api/files/match', json={'file_id': unmatch['id'], 'scene_id': match})
        if resp.ok:
            print(f'Linked {unmatch["filename"]} to {match}')


def main():
    seek_matches()


if __name__ == '__main__':
    main()
