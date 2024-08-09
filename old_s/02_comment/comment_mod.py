#!/usr/bin/env python3
import random
import os
import shutil


def get_new_vids():
    with open("./01_get_vids/etc/videos_new.txt", "r") as file:
        new_vids = []
        lines = file.readlines()
        for line in lines:
            new_vids.append(line.replace("\n", ""))
        return new_vids
