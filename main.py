import os
import re
import requests
import urllib.request

LESSON_DIR = "Video"
USER_AGENT = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
HEADERS = {'user-agent': USER_AGENT, 'accept': '*/*'}
URLS = [input('Введите URL до плейлиста с расширением .m3u8: ').strip()]
FILE_NAME = input('Введите желаемое имя файла: ').strip()

try:
    os.makedirs(LESSON_DIR)
except Exception:
    pass
finally:
    os.chdir(LESSON_DIR)


def get_m3u8(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text


def parse_m3u8(m3u8):
    pattern = r'\S+\Wts'
    return re.findall(pattern, m3u8)


def download_lesson(url, file_name, parts_list):
    pattern = r'/\w+\Wm3u8'
    file_name += '.mp4'
    f = open(file_name, 'ab')
    for part in parts_list:
        link = re.sub(pattern, f'/{part}', url)
        try:
            rsp = urllib.request.urlopen(link)
        except Exception:
            break
        print(f'Downloading part {part}: {link}')
        f.write(rsp.read())
    f.close()
    print('Done, Good Luck !!!')


def main():
    m3u8 = get_m3u8(URLS[0])
    parts_list = parse_m3u8(m3u8)
    download_lesson(URLS[0], FILE_NAME, parts_list)


if __name__ == '__main__':
    main()
