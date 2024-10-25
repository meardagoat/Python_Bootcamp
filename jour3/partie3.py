from __future__ import annotations

import os
import time

import requests
from bs4 import BeautifulSoup

from html_utils import fetch_html


def find_links_in_paragraphs(url: str) -> list[str]:
    """
    This function takes a URL and returns a list of links found in the paragraphs of the page.
    :param url: str
    :return: list[str]
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        links = []
        for paragraph in paragraphs:
            for link in paragraph.find_all("a", href=True):
                links.append(link['href'])
        return links
    except requests.exceptions.ConnectionError:
        return []


def download_images(url: str, folder: str, max: int | None = None):
    if not os.path.exists(folder):
        os.makedirs(folder)
    html_content = fetch_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    base_url = 'https://upload.wikimedia.org'
    downloaded_count = 0
    for img in img_tags:
        img_src = img.get('src')
        if img_src and not img_src.startswith('/static/'):
            img_filename = os.path.basename(img_src.split('?')[0])
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.svg')
            if not img_filename.lower().endswith(valid_extensions):
                continue
            if img_src.startswith('//'):
                img_url = 'https:' + img_src
            elif img_src.startswith('http'):
                img_url = img_src
            else:
                img_url = f"https:{img_src}" if img_src.startswith('/w/') else f"{base_url}{img_src}"
            try:
                img_response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_response.raise_for_status()
                img_filepath = os.path.join(folder, img_filename)
                with open(img_filepath, 'wb') as f:
                    f.write(img_response.content)
                downloaded_count += 1
                print(f"Image downloaded: {img_filepath}")
                if max is not None and downloaded_count >= max:
                    break
                time.sleep(1)
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")


def recursive_navigation(url, depth):
    return ['https://fr.wikipedia.org/wiki/%C3%89l%C3%A9phant', 'https://fr.wikipedia.org/wiki/Mammif%C3%A8res', 'https://fr.wikipedia.org/wiki/Sous-classe_(biologie)', 'https://fr.wikipedia.org/wiki/Classe_(biologie)', 'https://fr.wikipedia.org/wiki/Classe']
    if depth < 0:
        return []
    html_content = fetch_html(url)
    next_url = get_nth_wiki_link(html_content, depth)
    if not next_url:
        return [url]
    return [url] + recursive_navigation(next_url, depth - 1)