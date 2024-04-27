#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import mod
import asyncio
import re
import random


serial = sys.argv[1]  # 127.0.0.1:6555
fam_users = mod.get_users()


def loop(serial):
    d = u2.connect(serial)  # print(d.info)

    d.open_url(f"https://www.tiktok.com/@ihptto")
    d(text="Message").exists(timeout=10)

    for user in fam_users:
        try:
            # go 2 usr -----------------------------------------------------------------
            d.open_url(f"https://www.tiktok.com/@{user}")
            d(text="Message").exists(timeout=10)
            # await asyncio.sleep(1)
            d.swipe_ext("up", scale=0.8)
            # print(f"{user} loaded")

            # get n pins -----------------------------------------------------------------
            d(resourceId="com.zhiliaoapp.musically:id/cover").exists(timeout=10)
            n_pins = d(text="Pinned").count
            # print(f"pins : {n_pins}")

            # go latest vid -----------------------------------------------------------------
            d(resourceId="com.zhiliaoapp.musically:id/cover")[n_pins].click()
            d(resourceId="com.zhiliaoapp.musically:id/title").exists(timeout=10)
            # await asyncio.sleep(1)
            d.press(62)

            # check n of comments -----------------------------------------------------------------
            d(descriptionContains="Read or add comments").exists(timeout=10)
            n_comments_desc = d(descriptionContains="Read or add comments").info[
                "contentDescription"
            ]
            n_comments_filtered = re.sub("[^0-9]", "", n_comments_desc)

            if (
                "K" in n_comments_desc
                or int(n_comments_filtered) > 20
                # or "ago" in n_ago
                # or "m ago" in n_ago
            ):

                # go2 comments -----------------------------------------------------------------
                d(descriptionContains="Read or add comments").click(timeout=10)
                d(descriptionContains="Like or undo like").exists(timeout=10)

                new = False

                # (-h/m ago ??? ) -----------------------------------------------------------------
                # d(text="Reply").left(className="android.widget.TextView").get_text()
                for i in range(24):
                    if len(d(text=f"{i}h")) or len(d(text=f"{i}m")):
                        new = True

                if new:

                    # comment -----------------------------------------------------------------
                    comments_list = []
                    for i in range(2):

                        for com in d(
                            className="android.widget.TextView", focusable="True"
                        ):
                            try:
                                comment_text = com.get_text()
                                if comment_text not in comments_list:
                                    comments_list.append(com.get_text())
                            except:
                                pass

                        d.swipe_ext("up", scale=0.8)

                    random.shuffle(comments_list)
                    for comment_index, comment in enumerate(comments_list):
                        if comment_index < 2:
                            # print(f"comment : {comment}")
                            d(textContains="Add comment...").click(10)
                            d(textContains="Add comment...").set_text(comment)
                            d(descriptionContains="Post comment").click(timeout=10)

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
