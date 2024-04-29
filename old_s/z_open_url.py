#!/usr/bin/env python3
# pip install packaging==21.3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


serial = sys.argv[1]  # 127.0.0.1:6562
url = str(sys.argv[2])


def open_url(serial):
    # atx
    print(url)
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
