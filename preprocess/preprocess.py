import json
import pandas as pd
import os
import langdetect
from time import time

os.chdir(os.path.dirname(__file__))
print('Working Directory:', os.path.abspath('.'))


def detect_language(x):
    try:
        return langdetect.detect(x)
    except:
        return ''


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
            data = pd.read_csv(csv_name, encoding='utf-8-sig')[features]
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
