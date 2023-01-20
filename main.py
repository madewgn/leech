import requests
#import cloudscraper
from cfscrape import create_scraper
from os import path as ospath
from math import pow, floor
#from http.cookiejar import MozillaCookieJar
from requests import get as rget, head as rhead, post as rpost, Session as rsession
from re import findall as re_findall, sub as re_sub, match as re_match, search as re_search, compile as re_compile, DOTALL
from time import sleep, time
from urllib.parse import urlparse, unquote
# from json import loads as jsonloads
# from lk21 import Bypass
# from lxml import etree
# from cfscrape import create_scraper
from bs4 import BeautifulSoup
# from base64 import standard_b64encode, b64decode
#from playwright.sync_api import Playwright, sync_playwright, expect
#from lk21 import Bypass



def get_link(link: str):
    if 'zippyshare.com' in link:
        return zippy_share(link)
    # elif "racaty.io" in link:
    #     return racaty(link)
    # elif "anonfiles.com" in link:
    #     return anonfiles(link)
    elif "mediafire.com":
        return mediafire(link)
    else:
        return


# def anonfiles(url: str) -> str:
#     """ Anonfiles direct link generator
#     Based on https://github.com/zevtyardt/lk21
#     """
#     return Bypass().bypass_anonfiles(url)



def mediafire(url: str) -> str:
    """ MediaFire direct link generator """
    try:
        link = re_findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        return "No MediaFire links found"
    page = BeautifulSoup(rget(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    return info.get('href')



# def racaty(url: str) -> str:
#     """ Racaty direct link generator
#     based on https://github.com/SlamDevs/slam-mirrorbot"""
#     dl_url = ''
#     try:
#         re_findall(r'\bhttps?://.*racaty\.net\S+', url)[0]
#     except IndexError:
#         return "No Racaty links found"
#     scraper = create_scraper()
#     r = scraper.get(url)
#     soup = BeautifulSoup(r.text, "lxml")
#     op = soup.find("input", {"name": "op"})["value"]
#     ids = soup.find("input", {"name": "id"})["value"]
#     rpost = scraper.post(url, data={"op": op, "id": ids})
#     rsoup = BeautifulSoup(rpost.text, "lxml")
#     dl_url = rsoup.find("a", {"id": "uniqueExpirylink"})[
#         "href"].replace(" ", "%20")
#     return dl_url


def zippy_share(url: str) -> str:
    base_url = re_search('http.+.zippyshare.com', url).group()
    response = rget(url)
    pages = BeautifulSoup(response.text, "html.parser")
    js_script = pages.find(
        "div", style="margin-left: 24px; margin-top: 20px; text-align: center; width: 303px; height: 105px;")
    if js_script is None:
        js_script = pages.find(
            "div", style="margin-left: -22px; margin-top: -5px; text-align: center;width: 303px;")
    js_script = str(js_script)

    try:
        var_a = re_findall(r"var.a.=.(\d+)", js_script)[0]
        mtk = int(pow(int(var_a), 3) + 3)
        uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
        uri2 = re_findall(r"\+\"/(.*?)\"", js_script)[0]
    except:
        try:
            a, b = re_findall(r"var.[ab].=.(\d+)", js_script)
            mtk = eval(f"{floor(int(a)/3) + int(a) % int(b)}")
            uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
            uri2 = re_findall(r"\)\+\"/(.*?)\"", js_script)[0]
        except:
            try:
                mtk = eval(re_findall(r"\+\((.*?).\+", js_script)[0] + "+ 11")
                uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                uri2 = re_findall(r"\)\+\"/(.*?)\"", js_script)[0]
            except:
                try:
                    mtk = eval(re_findall(r"\+.\((.*?)\).\+", js_script)[0])
                    uri1 = re_findall(r"\.href.=.\"/(.*?)/\"", js_script)[0]
                    uri2 = re_findall(r"\+.\"/(.*?)\"", js_script)[0]
                except Exception as err:
                    # LOGGER.error(err)
                    # raise DirectDownloadLinkException(
                    return "ERROR: Failed to Get Direct Link"
    dl_url = f"{base_url}/{uri1}/{int(mtk)}/{uri2}"
    return dl_url



def with_moviepy(filename):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(filename)
    duration       = clip.duration
    fps            = clip.fps
    width, height  = clip.size
    return duration, fps, width, height


import ffmpeg
import subprocess
import os

def create_thumbnail(input_video):
    base, _ = os.path.splitext(input_video)
    output_image = base + '.jpg'

    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', 'thumbnail',
        '-vframes', '1',
        output_image
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(result.stderr)
    else:
        return output_image

#create_thumbnail('input.mp4')


#print(zippy_share("https://www105.zippyshare.com/v/QLSc8fI2/file.html"))
if __name__ == "__main__":
    print(zippy_share("https://www105.zippyshare.com/v/QLSc8fI2/file.html"))
