#!/usr/bin/env python3
# undo proxy

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import subprocess

# serial = input("Enter comment device serial port 127.0.0.1: ")

serial = sys.argv[1]  # 127.0.0.1:6555


def start_ui(serial):
    # atx
    d = u2.connect(serial)  # print(d.info)
    d.uiautomator.start()
    # d.app_start("com.github.uiautomator")
    # d(resourceId="com.github.uiautomator:id/start_uiautomator").click()

    # proxy

    # d.shell("settings put global http_proxy localhost:3333")
    d.shell("settings put global http_proxy :0")
    # subprocess.run(f"adb -s {serial} reverse tcp:3333 tcp:8082", shell=True, check=True)
    subprocess.run(f"adb -s {serial} reverse --remove tcp:3333", shell=True, check=True)


def main():
    try:
        start_ui(serial)
    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":
    main()
