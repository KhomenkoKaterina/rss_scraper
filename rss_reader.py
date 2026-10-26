# You shouldn't change  name of function or their arguments
# but you can change content of the initial functions.
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import html
import json as json_lib


class UnhandledException(Exception):
    pass

def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """
    result =[]

    root = ET.fromstring(xml)

    channel = root.find('channel')

    if channel is None:
        return []



    channel_title = channel.find('title')
    channel_link = channel.find('link')
    channel_lastBuildDate = channel.find('lastBuildDate')
    channel_pubDate = channel.find('pubDate')
    channel_language = channel.find('language')
    channel_managinEditor = channel.find('managingEditor')
    channel_des = channel.find('description')

    
    channel_categ = [
        html.unescape(cat.text.strip()) 
        for cat in channel.findall('category') 
        if cat.text and cat.text.strip()
    ]
    items = channel.findall('item')
    if limit is not None and limit >= 0:
        items = items[:limit]

    if json:
        feed = {}

        if channel_title is not None and channel_title.text and channel_title.text.strip():
            feed['title'] = channel_title.text.strip()
        if channel_link is not None and channel_link.text and channel_link.text.strip():
            feed['link'] = channel_link.text.strip()
        if channel_lastBuildDate is not None and channel_lastBuildDate.text and channel_lastBuildDate.text.strip():
            feed['lastBuildDate'] = channel_lastBuildDate.text.strip()
        if channel_pubDate is not None and channel_pubDate.text and channel_pubDate.text.strip():
            feed['publishDate'] = channel_pubDate.text.strip()
        if channel_language is not None and channel_language.text and channel_language.text.strip():
            feed['language'] = channel_language.text.strip()
        if channel_categ:
            feed['categories'] = channel_categ
        if channel_managinEditor is not None and channel_managinEditor.text and channel_managinEditor.text.strip():
            feed['editor'] = channel_managinEditor.text.strip()
        if channel_des is not None and channel_des.text and channel_des.text.strip():
            feed['description'] = channel_des.text.strip()

        feed['items'] = []

        for item in items:
            i_title = item.find("title")
            i_author = item.find("author")
            i_pubDate = item.find("pubDate")
            i_link = item.find("link")
            i_des = item.find("description")
            i_categ = [
                html.unescape(cat.text.strip())
                for cat in item.findall('category')
                if cat.text and cat.text.strip()
            ]

            entry = {}
            if i_title is not None and i_title.text and i_title.text.strip():
                entry['title'] = i_title.text.strip()
            if i_author is not None and i_author.text and i_author.text.strip():
                entry['author'] = i_author.text.strip()
            if i_pubDate is not None and i_pubDate.text and i_pubDate.text.strip():
                entry['pubDate'] = i_pubDate.text.strip()
            if i_link is not None and i_link.text and i_link.text.strip():
                entry['link'] = i_link.text.strip()
            if i_categ:
                entry['categories'] = i_categ
            if i_des is not None and i_des.text and i_des.text.strip():
                entry['description'] = i_des.text.strip()

            feed['items'].append(entry)
        return [json_lib.dumps(feed, indent=2, ensure_ascii=False)]

  
    channel_fields = [
        ('Feed', channel_title),
        ('Link', channel_link),
        ('Last Build Date', channel_lastBuildDate),
        ('Publish Date', channel_pubDate),
        ('Language', channel_language),
        ('Editor', channel_managinEditor),
        ('Description', channel_des),
    ]

    for label, element in channel_fields:
        if element is not None and element.text is not None and element.text.strip():
            result.append(f'{label}: {element.text.strip()}')
        if label == 'Language' and channel_categ:
            result.append(f'Categories: {" ,".join(channel_categ)}')
    result.append(' ')


    for item in items: 
        i_title = item.find("title")
        i_author = item.find("author")
        i_pubDate = item.find("pubDate")
        i_link = item.find("link")
        i_categ = [
            html.unescape(cat.text.strip())
            for cat in item.findall('category')
            if cat.text and cat.text.strip()
        ]
        i_des = item.find("description")

        item_filds = [
            ('Title', i_title ),
            ('Author', i_author),
            ('Published', i_pubDate),
            ('Link', i_link),
            ('Description', i_des),
        ]
        for lable, el in item_filds:
            if el is not None and el.text is not None and el.text.strip():
                result.append(f'{lable}: {el.text.strip()}')
            if lable == i_categ:
                result.append(f"Categories: {' ,'.join(i_categ)}")
        result.append(' ')
            

    return result 

def main(argv: Optional[Sequence] = None):
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)

    args = parser.parse_args(argv)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(args.source, headers=headers)
    response.raise_for_status()  # сразу упадёт с понятной ошибкой, если код ответа не 200
    xml = response.text

    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)

    
if __name__ == "__main__":
    main()
