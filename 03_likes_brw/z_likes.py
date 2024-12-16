#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright, Request, Response, Route
import json
from pathlib import Path
import sys
from datetime import datetime
import random
import mod
from colorama import Fore, Style


like_browsers = int(sys.argv[1])

cookies_json = mod.get_cookies(like_browsers)
new_videos = mod.get_new_vids()
eval_file = open("./03_likes_brw/etc/interval.js", "r").read()

# clear
with open("./02_comment_loop/etc/comment_url.txt", "w") as urls_file:
    urls_file.write("")


async def handle_vid(route: Route):
    if (
        "https://v16-webapp-prime.tiktok.com/video/" in route.request.url
        or "https://www.tiktok.com/api/related/item_list/" in route.request.url
    ):
        await route.abort()
    else:
        await route.continue_()


async def browser_l(segment, segment_index):

    async with async_playwright() as p:
        context = await p.firefox.launch(headless=True)
        page = await context.new_page(reduced_motion="reduce")

        await page.route("**/*", handle_vid)

        trash_vid = []
        for cookie_index, cookie in enumerate(segment):
            try:
                print(
                    f"{Fore.LIGHTGREEN_EX}browser [{segment_index}] - {cookie} [{cookie_index}/{len(segment)}]{Style.RESET_ALL} {datetime.now()}"
                )
                await context.contexts[0].add_cookies(
                    json.loads(Path(f"./03_likes_brw/etc/cookies/{cookie}").read_text())
                )

                for vid in new_videos:
                    print(vid)
                    if trash_vid.count(vid) < 3:
                        try:
                            likes = 0
                            await page.goto(vid)

                            main_vid = await page.wait_for_selector("video")
                            await main_vid.evaluate("e => e.remove()")
                            side_nav = await page.wait_for_selector(
                                'div[class*="DivSideNavContainer"]'
                            )
                            await side_nav.evaluate("e => e.remove()")
                            bg_vids = await page.wait_for_selector(
                                'div[class*="DivVideoList"]'
                            )
                            await bg_vids.evaluate("e => e.remove()")
                            await page.evaluate(eval_file)
                            await page.wait_for_selector(
                                ".target", timeout=random.randrange(30000, 50000)
                            )
                            hearts = await page.query_selector_all(".heart_box svg")

                            for heart in hearts:
                                if await heart.get_attribute("fill") == "currentColor":
                                    await heart.click()
                                    likes += 1
                                    await page.wait_for_timeout(1000)

                            print(
                                f"{vid} {Fore.RED}({likes} x <3) {Fore.LIGHTGREEN_EX}({cookie}){Style.RESET_ALL}"
                            )

                        except Exception as error:
                            # print(error)
                            trash_vid.append(vid)
                            # print(f"{vid} appended to trash")
                            pass

            except Exception as error:
                # print(error)
                pass

        await page.close()
        await context.close()


async def main():
    print(f"{Fore.BLUE}\n{sys.argv[0]} is running.. {datetime.now()}{Style.RESET_ALL}")

    await asyncio.gather(
        *[
            browser_l(segment, segment_index)
            for segment_index, segment in enumerate(cookies_json)
        ]
    )


asyncio.run(main())
