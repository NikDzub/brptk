#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import asyncio
import re
import random
import get_vids_mod


users = get_vids_mod.get_all_users()
used_vids = get_vids_mod.get_used_vids()
new_vids = get_vids_mod.get_new_vids()

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()
device_id = sys.argv[1]


def loop(serial):
    d = u2.connect(serial)  # print(d.info)

    d.open_url(f"https://www.tiktok.com/@ihptto")
    d(text="Message").exists(timeout=10)

    try:

        for user in users:

            d.open_url(f"https://www.tiktok.com/@{user}")
            d(descriptionContains="profile").exists(timeout=10)

            for new_video in new_vids:
                d.open_url(new_video)
                d(descriptionContains="profile").exists(timeout=10)
                d(descriptionContains="Read or add comments").exists(timeout=10)
                d.press(62)
                d(descriptionContains="Read or add comments").click()

                # comment -----------------------------------------------------------------
                comments_list = []
                for i in range(2):

                    for com in d(className="android.widget.TextView", focusable="True"):
                        try:
                            comment_text = com.get_text()
                            if comment_text not in comments_list:
                                comments_list.append(com.get_text())
                        except:
                            pass

                    d.swipe_ext("up", scale=0.8)

                comments_list = [
                    "Google This H2X7A.NL",
                    "Guys Dont google H2X7A.NL",
                    "Hey Just Google H2X7A.NL",
                    "Check this out! Google the code H2X7A.NL",
                ]
                random.shuffle(comments_list)
                for comment_index, comment in enumerate(comments_list):

                    if comment_index < 1:
                        # print(f"comment : {comment}")
                        d(textContains="Add comment...").click(10)
                        d(textContains="Add comment...").set_text(f"{comment}")

                        # tag
                        # try:
                        #     d.send_keys("@")
                        #     d(descriptionContains="Mention someone in a comment").click()
                        #     d(textContains="Amber").click(timeout=5000)
                        # except:
                        #     pass

                        d(descriptionContains="Post comment").click(timeout=10)

    except Exception as error:
        print(error)


def main():
    for device in devices:
        if device_id in device.serial:
            try:
                loop(device.serial)
            except Exception as error:
                print(error)
                pass


if __name__ == "__main__":
    main()
