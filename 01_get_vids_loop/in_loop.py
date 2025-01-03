#!/usr/bin/env python3

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
print(f"open browsers: {search_browsers}")


users = get_vids_mod.get_users(segments=search_browsers)
used_vids = get_vids_mod.get_used_vids()


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
                try:
                    sys.stdout.flush()
                    async with page.expect_request(
                        "**/api/post/item_list/**",
                        timeout=10000,
                    ) as first:
                        # print(user)
                        await page.goto(
                            f"https://www.tiktok.com/@{user}",
                            timeout=10000,
                            # wait_until="load",
                        )
                        # await page.wait_for_selector("video", timeout=5000)
                    first_request = await first.value
                    response = await first_request.response()
                    response_body = await response.body()

                    if json.loads(response_body)["itemList"]:
                        print(f")", end="")
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
                            if vid.valid() and used == False:

                                url = vid.video_url()
                                used_vids.append(url)
                                vid.display_info()

                                with open(
                                    "./01_get_vids_loop/etc/videos_new.txt", "a"
                                ) as file:
                                    file.write(str(url) + "\n")

                                with open(
                                    "./01_get_vids_loop/etc/videos_used.txt", "w"
                                ) as outfile:
                                    for index, row in enumerate(used_vids):
                                        outfile.write(str(row) + "\n")

                except Exception as error:
                    # print(error)
                    print(f"{Fore.RED}({Style.RESET_ALL}", end="")
                    sys.stdout.flush()
                    pass
            await page.close()

        await asyncio.gather(
            *[browser_l(segment) for index, segment in enumerate(users)]
        )

        await context.close()
        print("")


async def main():
    # print(
    #     f"{Fore.BLUE}\n{sys.argv[0]} started {Fore.LIGHTBLACK_EX}{datetime.now().strftime(f'%H:%M:%S')}{Style.RESET_ALL}"
    # )

    try:
        # Set a timeout of 60 seconds for the main function
        await asyncio.wait_for(get_vids(), timeout=360.0)
    except asyncio.TimeoutError:
        sys.exit(1)

    # await asyncio.gather(*[get_vids()])


asyncio.run(main())
