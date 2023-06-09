import feedparser
import urllib.parse

def parse_oge_feeds(feed_url, file_name):
    feed = feedparser.parse(feed_url)
    with open(f'{file_name}.txt', 'w') as f:
        for entry in feed.entries:
            url = entry.file
            parsed = urllib.parse.urlparse(url)
            parsed_path = urllib.parse.quote(parsed.path)
            parsed = parsed._replace(path=parsed_path)
            final_url= parsed.geturl()
            f.write(f'{final_url}\n')

parse_oge_feeds('https://www.oge.gov/Web/OGERSSFe.nsf/rss?openagent&uid=9B8916B9CD41203C852585F400745620', 'oge_a')
parse_oge_feeds('https://www.oge.gov/Web/OGERSSFe.nsf/rss?openagent&uid=6E2066517D9D3FD2852585F40076B07E', 'oge_b')