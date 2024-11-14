#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import re
import subprocess
from datetime import datetime
import random


serial = sys.argv[1]  # 127.0.0.1:6562
urls_path = "02_comment_loop/etc/comment_url.txt"


d = u2.connect(serial)  # print(d.info)
d_users_output, exit_code = d.shell("pm list users")
d_users = re.findall(r"UserInfo{(\d+):", d_users_output)


def get_urls(path):
    urls = []
    with open(path, "r") as urls_file:
        for line in urls_file:
            urls.append(f"{line}".replace("\n", ""))

    # clear
    with open(path, "w") as urls_file:
        urls_file.write("")

    return urls


async def open_urls(user_id, urls):
    try:
        print(f"user_id: {user_id}")
        d.shell(f"am switch-user {user_id}")
        await asyncio.sleep(5)
        d.shell(f"input keyevent KEYCODE_WAKEUP")
        await asyncio.sleep(2)
        d.shell(f"input keyevent KEYCODE_WAKEUP")
        await asyncio.sleep(1)
        d.shell(f"input keyevent KEYCODE_MENU")
        # d(resourceId="com.android.systemui:id/clock").exists(timeout=20)

        d.open_url("https://www.tiktok.com/@ihptto")
        d(text="Message").exists(timeout=20)

        for index, url in enumerate(urls):
            d.open_url(url)
            current_timestamp = datetime.now().strftime("%H:%M:%S")

            print(f"{index}/{len(urls)} {url} {current_timestamp}")
            comment_found = d(textContains="Ella").exists(timeout=20)

            if comment_found:
                d(descriptionContains="Like or undo like").exists(timeout=20)
                d(descriptionContains="Like or undo like").click()
                try:
                    # reply
                    d(textContains="Reply").click()
                    random_replies = [
                        "I downloaded the app its so fun, thank you!!!",
                        "Lol go to her bio 😮",
                        "what are you guys talking about?",
                        "thanks for the cash app, i just earned 50$",
                        "This Game app is crazyyy🥹",
                        "DAMN go see the bio link i just got $220",
                        "OMG this is actualy legit",
                        "yep its real guys",
                        "Thank you",
                        "🥹 Wow Thanks for the link",
                        "Looking good hey",
                        "Thanks for the app download🥹",
                        "Did you guys tried the thing in her bio? its kinda crazy",
                        "Wow thanks for the app",
                        "Damn this bio link saved me 😮",
                        "Looking good hey",
                        "Damn Thank you",
                        "Thanks so much!! ily, guys go check the link in her bio",
                    ]
                    d(focused=True).set_text(random.choice(random_replies))
                    d(descriptionContains="Post comment").click()
                except:
                    pass

            else:
                urls.remove(url)
                print(f"remove: {url}")

        # d.shell("pm clear com.zhiliaoapp.musically")
        d.shell("am force-stop com.zhiliaoapp.musically")
    except Exception as error:
        print(error)
        pass


async def reboot(serial):
    subprocess.run(f"adb -s {serial} reboot", shell=True, check=True)
    asyncio.sleep(20)


async def main():

    try:
        urls = get_urls(urls_path)

        for user_id in d_users:
            await open_urls(user_id, urls)
        d.shell(f"am switch-user 0")
        await asyncio.sleep(3)
        # await reboot(serial)

    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":
    asyncio.run(main())
