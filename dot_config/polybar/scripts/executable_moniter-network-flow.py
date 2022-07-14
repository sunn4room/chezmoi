#!/usr/bin/env python3

import sys
import os
import time

units = ['B', 'K', 'M', 'G', 'T', 'P']

def get_speed(diff):
    united_diff = diff
    unit_idx = 0
    while unit_idx != 5 and united_diff >= 1024:
        united_diff >>= 10
        unit_idx += 1
    return f"{united_diff}{units[unit_idx]}"

def readbytes(file):
    with open(file, "r") as f:
        return int(f.read()[:-1])

def diff_func(file):
    prev = readbytes(file)
    def diff():
        nonlocal prev
        cur = readbytes(file)
        res = cur - prev
        prev = cur
        return res
    return diff

mode = sys.argv[1]
net_cards = []
for card in os.listdir("/sys/class/net"):
    if card != "lo" and (not card.startswith("docker")):
        net_cards.append(card)
diffs = []
for card in net_cards:
    diffs.append(diff_func(f"/sys/class/net/{card}/statistics/{mode}x_bytes"))

def get_diff():
    global diffs
    sum = 0
    for diff in diffs:
        sum += diff()
    return sum

interval = int(sys.argv[2])

while True:
    time.sleep(interval)
    print(get_speed(get_diff() // interval), flush=True)
