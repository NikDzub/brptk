#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys

print(f"{sys.argv[0]} is running..")

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

url = "https://www.tiktok.com/@danthonymagic/video/7346973163185622315?_d=ed672222h8l334\u0026_r=1\u0026comment_author_id=6815984445305586694\u0026preview_pb=0\u0026share_comment_id=7361174121373582123\u0026share_item_id=7346973163185622315\u0026sharer_language=en\u0026source=h5_m\u0026u_code=e91bfeg4416bhk"


def start_ui(client):
    d = u2.connect(client.serial)
    print(d.info)
    d.open_url(url)


for client in devices:
    try:
        start_ui(client)
    except:
        pass
