#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import re
import pyperclip
import sys


serial = sys.argv[1]  # 127.0.0.1:6555

d = u2.connect(serial)
users_output, exit_code = d.shell("pm list users")
device_profiles = re.findall(r"UserInfo{(\d+):", users_output)


async def open_url():
    try:
        text = pyperclip.paste()
        print(text)
        d.open_url(text)

    except Exception as error:
        print(error)


async def main():
    await open_url()


asyncio.run(main())
