#!/usr/bin/env python3
# pip install packaging==21.3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess


# print(f"{sys.argv[0]} is running..")

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


def start_ui(client):
    # atx
    d = u2.connect(client.serial)  # print(d.info)
    d.uiautomator.start()
    print(d.info)
    d.app_start("com.github.uiautomator")
    d(resourceId="com.github.uiautomator:id/start_uiautomator").click()


for client in devices:
    print(client.serial)
    try:
        start_ui(client)
    except Exception as error:
        print(error)
        pass
