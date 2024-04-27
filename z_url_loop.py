#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


serial = sys.argv[1]  # 127.0.0.1:6562
urls_path = "./urls.txt"
urls = []


def get_urls(path):
    with open(path, "r") as urls_file:
        for line in urls_file:
            urls.append(f"{line}".replace("\n", ""))
    print(urls)


def open_url(serial, url):
    # atx
    print(serial, url)
    d = u2.connect(serial)  # print(d.info)
    d.open_url(url)


def main():
    try:
        get_urls(urls_path)
        open_url(serial)
    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":
    main()
