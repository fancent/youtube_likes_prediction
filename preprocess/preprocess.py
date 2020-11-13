import json
import pandas as pd
import os
import langdetect
from time import time
from io import StringIO
import csv
import numpy as np

os.chdir(os.path.dirname(__file__))
print('Working Directory:', os.path.abspath('.'))


def detect_language(x):
    try:
        return langdetect.detect(x)
    except:
        return ''


def line_by_line_parse(txt: str):
    """
    Read the csv file line by line
    remove the lines that are not properly formatted
    :param txt:
    :return: (data, number of record removed)
    """
    lines = txt.split('\n')
    ok_lines = []
    ok_line_indexs = []
    fail_lines = []
    fail_line_indexs = []
    for i, line in enumerate(lines):
        f = StringIO(line)
        c = list(csv.reader(f))
        if len(c) > 1:
            raise ValueError('Number of lines of a line > 1')
        elif len(c) <= 0:
            fail_lines.append(c)
            fail_line_indexs.append(i)
            continue
        c = c[0]
        if len(c) == 16:
            ok_lines.append(c)
            ok_line_indexs.append(i)
        else:
            fail_lines.append(c)
            fail_line_indexs.append(i)
    fail_line_indexs = np.array(fail_line_indexs)
    invalid_line_indexs = [i[0] - 1 for i in
                           np.split(fail_line_indexs, np.where(np.diff(fail_line_indexs) != 1)[0] + 1)]
    for _ind in invalid_line_indexs:
        ind = ok_line_indexs.index(_ind)
        ok_line_indexs.pop(ind)
        ok_lines.pop(ind)
    data = pd.DataFrame(ok_lines[1:], columns=ok_lines[0])
    return data, len(invalid_line_indexs)


def drop_invalid_byte(buf, offset=0, calls=0) -> tuple:
    """

    :param buf:
    :param offset:
    :param calls:
    :return: text, number of byte removed,
    """
    start = 0
    end = len(buf)
    try:
        # print(f"Extracting from {start+offset}:{end+offset}")
        temp = buf[start:end].decode('utf-8-sig')
        return temp, calls
    except UnicodeDecodeError as err:
        ERR = err
        # print(ERR)
        if ERR.reason == 'invalid continuation byte':
            tailstr, tail_calls = drop_invalid_byte(buf[ERR.end + 1: end], ERR.end + 1)
            return buf[start:ERR.start].decode('utf-8-sig') + tailstr, calls + 1 + tail_calls
        elif ERR.reason == 'invalid start byte':
            return buf[start + 1: end], calls + 1
        elif ERR.reason == 'unexpected end of data':
            return buf[start: end - 1], calls + 1
    except Exception as err:
        raise err


def safe_read_csv(csv_name: str) -> pd.DataFrame:
    try:
        return pd.read_csv(csv_name, encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open(csv_name, 'rb')
        raw_buffer = f.read()
        f.close()
        txt, nbytes = drop_invalid_byte(raw_buffer)
        print(f"Removed {nbytes} invalid bytes")
        f = StringIO(txt)
        try:
            return pd.read_csv(f)
        except:
            data, num_of_invalid_lines = line_by_line_parse(txt)
            print(f"Removed {num_of_invalid_lines} records in {csv_name}")
            return data


if __name__ == '__main__':
    """
            1. removed nan in the features
            2. removed unknown category
            3. added region in the dataframe
            4. added language detection
        """
    features = ['video_id', 'title', 'category_id', 'tags', 'views', 'likes', 'dislikes', 'comment_count',
                'description']
    regions = ['CA', 'DE', 'FR', 'GB', 'IN', 'JP', 'KR', 'MX', 'RU', 'US']
    count = 0

    global_start_time = time()
    for region in regions:
        try:
            print(f"Start process {region}")
            start_time = time()
            csv_name = f'../data/raw/{region}videos.csv'
            json_name = f'../data/raw/{region}_category_id.json'
            data = safe_read_csv(csv_name)[features].astype(
                {'video_id': str, 'title': str, 'category_id': int, 'tags': str, 'views': int, 'likes': int,
                 'dislikes': int, 'comment_count': int, 'description': str})
            category_data = pd.DataFrame(list(
                map(lambda x: {'category_id': int(x['id']), 'category_title': x['snippet']['title']},
                    json.load(open(json_name, 'r'))['items'])))
            data = data.merge(category_data, on='category_id')
            data['region'] = region
            detect_lang_time = time()
            data['lang'] = data['title'].apply(lambda x: detect_language(x))
            print(f"Detect language: {time() - detect_lang_time}s")
            data.to_csv(f'../data/processed/{region}.csv', index=False)
            print(f"Finished process {region} (with {len(data)} records) in {time() - start_time:.2f}s")
            count += len(data)
        except UnicodeDecodeError as e:
            print("Cannot Decode Language", region)
            print(e)
    print()
    print(f"Finished all process (with {count} records) in {time() - global_start_time:.2f}s")
