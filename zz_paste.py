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


async def paste():
    try:
        text = pyperclip.paste()
        print(text)

        d.shell(f'input text "{text}"')
        # d(focused=True).set_text(text)

    except Exception as error:
        print(error)


async def main():
    await paste()


asyncio.run(main())
