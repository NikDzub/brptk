#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import comment_mod
import asyncio
import re
import random


serial = sys.argv[1]  # 127.0.0.1:6555
new_vids_arr = comment_mod.get_new_vids()


def loop(serial):
    d = u2.connect(serial)  # print(d.info)

    d.open_url(f"https://www.tiktok.com/@ihptto")
    d(text="Message").exists(timeout=10)

    for vid_url in new_vids_arr:
        try:
            print(vid_url)
            d.open_url(vid_url)

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

            random.shuffle(comments_list)
            for comment_index, comment in enumerate(comments_list):

                if comment_index < 1:
                    # print(f"comment : {comment}")
                    d(textContains="Add comment...").click(10)
                    d(textContains="Add comment...").set_text(comment)
                    d(descriptionContains="Post comment").click(timeout=10)

        except Exception as error:
            print(error)

        except Exception as error:
            print(error)


def main():
    try:
        loop(serial)
    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":
    main()
