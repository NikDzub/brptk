#!/usr/bin/env python3
# pip install packaging==21.3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


print(f"{sys.argv[0]} is running..")

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

cid = "7361472708431151880"
aweme_id = "7359115844732996870"
uid = "7255177357119161349"

url = f"https://www.tiktok.com/@apnatemplate7/video/7359115844732996870?_d=ed672222h8l334\u0026_r=1\u0026comment_author_id={uid}\u0026preview_pb=0\u0026share_comment_id=xw{cid}\u0026share_item_id=7359115844732996870\u0026sharer_language=en\u0026source=h5_m\u0026u_code=e91bfeg4416bhk"

print(url)


def start_ui(client):
    # atx
    d = u2.connect(client.serial)  # print(d.info)
    d.open_url(url)


for client in devices:
    try:
        start_ui(client)
    except Exception as error:
        print(error)
        pass
