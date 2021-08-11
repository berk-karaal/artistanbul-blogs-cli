# Scrape Artistanbul blog titles and links
import os
import requests
from bs4 import BeautifulSoup
from sty import bg, fg, rs, Style, RgbBg, RgbFg, ef
import time

os.system("clear")
print("Yükleniyor...")

URL = "https://www.artistanbul.io/blog/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

titles = soup.find_all("h2", class_="qodef-post-title")

os.system("clear")

fg.title_fg = Style(RgbFg(189, 151, 247))
bg.title_bg = Style(RgbBg(255, 255, 255))
fg.link_fg = Style(RgbFg(6, 69, 173))

n = 1
for x in titles:
    print(
        fg.da_grey
        + bg.title_bg
        + str(n)
        + ") "
        + ef.i
        + ef.b
        + fg.title_fg
        + x.find("a").text
        + "  "
        + fg.rs
        + bg.rs
        + ef.rs
    )
    print(fg.link_fg + x.find("a")["href"] + fg.rs)

    print()
    n += 1
    time.sleep(0.1)
