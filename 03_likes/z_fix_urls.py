#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
import sys
import re
import subprocess

urls_path = "02_comment_loop/etc/comment_url.txt"


def fix_urls(path):
    # Read the URLs from the file
    with open(path, "r") as urls_file:
        urls = {line.strip() for line in urls_file if line.strip()}

    # Write unique URLs back to the file
    with open(path, "w") as urls_file:
        for url in sorted(urls):
            urls_file.write(f"{url}\n")

    return urls


def main():
    unique_urls = fix_urls(urls_path)
    print(
        f"Unique URLs: {len(unique_urls)}"
    )  # Print number of unique URLs for confirmation


if __name__ == "__main__":
    main()
