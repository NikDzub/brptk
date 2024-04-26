#!/usr/bin/env python3
# pip install packaging==21.3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


serial = sys.argv[1]  # 127.0.0.1:6562


author_id = "6923224065499694085"
aweme_id = "7352165286990171424"
d = "ed672222h8l334"
cid = "7362099827268993800"
uid = "7255177357119161349"

url = f"""
https://www.tiktok.com/@{author_id}/
video/{aweme_id}?
_d={d}&
comment_author_id={uid}&
share_comment_id={cid}&
""".replace(
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
