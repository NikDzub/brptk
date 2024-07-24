#!/usr/bin/env python3

# python3 (# brwsrs) (# new vids)

import asyncio
from playwright.async_api import async_playwright
import sys
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import get_vids_mod
from datetime import datetime
import json
from colorama import Fore, Style

search_browsers = int(sys.argv[1])
n_new = int(sys.argv[2])


users = get_vids_mod.get_users(segments=search_browsers)
used_vids = get_vids_mod.get_used_vids()
new_vids = []


async def get_vids():
    global new_vids

    async with async_playwright() as p:
        # context = await p.firefox.launch(
        #     headless=False,
        #     # proxy={
        #     #     "server": "181.177.87.173:9291",
        #     #     "username": "3jFvwU",
        #     #     "password": "qF5DWZ",
        #     # },
        # )
        get_vids_mod.clean_firefox()
        context = await p.firefox.launch_persistent_context(
            user_data_dir="./firefox", headless=True
        )

        async def browser_l(segment):

            page = await context.new_page(
                # user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
            )
            await page.goto("https://www.tiktok.com/", wait_until="load")
            # await page.wait_for_timeout(546546456)

            for user in segment:
                if len(new_vids) < n_new:
                    try:
                        sys.stdout.flush()
                        async with page.expect_request(
                            "**/api/post/item_list/**",
                            timeout=10000,
                        ) as first:
                            await page.wait_for_timeout(2000)
                            await page.goto(
                                f"https://www.tiktok.com/@{user}",
                                timeout=10000,
                                wait_until="domcontentloaded",
                            )

                        # await page.wait_for_timeout(134000)
                        first_request = await first.value
                        response = await first_request.response()
                        response_body = await response.body()

                        if json.loads(response_body)["itemList"]:
                            print(f"|", end="")
                            videos_json = json.loads(response_body)["itemList"]
                            current_timestamp = datetime.now().timestamp()
                            for vid in videos_json:
                                vid = get_vids_mod.Video(
                                    vid["author"]["uniqueId"],
                                    vid["author"]["verified"],
                                    vid["id"],
                                    ((current_timestamp - vid["createTime"]) / 3600),
                                    vid["stats"]["commentCount"],
                                    vid["stats"]["diggCount"],
                                    vid["stats"]["playCount"],
                                    vid["stats"]["collectCount"],
                                    vid["stats"]["shareCount"],
                                )
                                used = vid.video_url() in used_vids

                                if (
                                    vid.valid()
                                    and used == False
                                    # and len(new_vids) < n_new
                                ):
                                    new_vids.append(vid.video_url())
                                    used_vids.append(vid.video_url())
                                    vid.display_info()

                    except Exception as error:
                        # print(error)
                        print(f"{Fore.RED}|{Style.RESET_ALL}", end="")
                        sys.stdout.flush()
                        pass

                else:
                    break

        await asyncio.gather(
            *[browser_l(segment) for index, segment in enumerate(users)]
        )

        with open("./etc/videos_new.txt", "w") as outfile:
            for index, row in enumerate(new_vids):
                outfile.write(str(row) + "\n")

        with open("./etc/videos_used.txt", "w") as outfile:
            for index, row in enumerate(used_vids):
                outfile.write(str(row) + "\n")

        await context.close()
        print("")


async def main():
    print(
        f"{Fore.BLUE}\n{sys.argv[0]} started {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
    )
    await asyncio.gather(*[get_vids()])


asyncio.run(main())
