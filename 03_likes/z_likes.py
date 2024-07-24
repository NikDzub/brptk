#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import re
import subprocess


serial = sys.argv[1]  # 127.0.0.1:6562
urls_path = "02_comment/etc/comment_url.txt"


d = u2.connect(serial)  # print(d.info)
d_users_output, exit_code = d.shell("pm list users")
d_users = re.findall(r"UserInfo{(\d+):", d_users_output)


def get_urls(path):
    urls = []
    with open(path, "r") as urls_file:
        for line in urls_file:
            urls.append(f"{line}".replace("\n", ""))
    return urls


def delete_urls(path, urls_to_delete):
    maybe_new_urls = get_urls(urls_path)

    print("maybe new urls:")
    print(maybe_new_urls)

    for url_to_delete in urls_to_delete:
        print(f"url to delete: {url_to_delete}")
        if url_to_delete in maybe_new_urls:
            maybe_new_urls.remove(url_to_delete)
            print(f"delete: {url_to_delete}")

    with open(path, "w") as urls_file:
        for url in maybe_new_urls:
            urls_file.write(url + "\n")


async def open_urls(user_id, urls):
    try:
        print(f"user_id: {user_id}")
        d.shell(f"am switch-user {user_id}")
        await asyncio.sleep(2)
        d(resourceId="com.android.systemui:id/clock").exists(timeout=20)

        d.open_url("https://www.tiktok.com/@ihptto")
        d(text="Message").exists(timeout=20)

        for url in urls:
            d.open_url(url)
            d(descriptionContains="Like or undo like").exists(timeout=20)
            d(descriptionContains="Like or undo like").click()

        # d.shell("pm clear com.zhiliaoapp.musically")
        # d.shell("am force-stop com.zhiliaoapp.musically")
    except:
        print("error")


async def reboot(serial):
    subprocess.run(f"adb -s {serial} reboot", shell=True, check=True)
    asyncio.sleep(20)


async def main():
    while True:
        try:
            urls = get_urls(urls_path)
            if len(urls) > 2:
                for user_id in d_users:
                    await open_urls(user_id, urls)
                delete_urls(urls_path, urls)
                await reboot(serial)

        except Exception as error:
            print(error)
            pass


if __name__ == "__main__":
    asyncio.run(main())
