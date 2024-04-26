#!/usr/bin/env python3
# pip install packaging==21.3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


serial = sys.argv[1]  # 127.0.0.1:6562


cid = "7361472708431151880"
aweme_id = "7359115844732996870"
uid = "7255177357119161349"

url = f"""https://www.tiktok.com/@lior__glam/video/7357731497970912519
?_d=ed672222h8l334\u0026
_r=1\u0026
comment_author_id=6812321935420310533\u0026
preview_pb=0\u0026
share_comment_id=7358144608507085586\u0026
share_item_id=7357731497970912519\u0026
sharer_language=en\u0026
source=h5_m\u0026
u_code=e91bfeg4416bhk""".replace(
    "\n", ""
)

print(url)


def open_url(serial):
    # atx
    d = u2.connect(serial)  # print(d.info)
    d.open_url(url)


def main():
    try:
        open_url(serial)
    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":
    main()
