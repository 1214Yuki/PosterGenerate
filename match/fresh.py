import copy
import json

import pandas as pd

from utils import get_column_attrs
from utils.frame import Frame
from match import python_cos

ARRAY = {
    'headline': [0] * 10,
    'subtitle': [0] * 10,
    'text': [0] * 10,
    'artdeco': [0] * 10,
    'chart-number': [0] * 10,
    'chart-title': [0] * 10,
}


def vector_items(items):
    vec = []
    fm = copy.deepcopy(ARRAY)
    for item in items:
        _item = get_column_attrs(item)
        if len(item.split('_')) > 1:
            _index = int(item.split('_')[-1]) - 1
        else:
            _index = 0
        if not fm.get(_item):
            continue
        array = fm[_item]
        array[_index] = 1
        fm[_item] = array

    for k in sorted(fm.keys()):
        vec.extend(fm[k])
    return vec


def filter_data(path):
    """
    过滤数据：没有background的
    """
    df = pd.read_csv(path)
    df = df[df.apply(lambda x: json.loads(x['labels_message']).get('background') is not None, axis=1)]
    data = {}
    for _, d in df.iterrows():
        labels_msg = json.loads(d['labels_message'])
        lm = labels_msg.keys()
        data[d['image_id']] = (vector_items(lm), Frame(labels_msg))
    return data


def match_best_data(path, vc, ratio=0.95):
    datas = filter_data(path)
    match_data = []
    for image_id, data in datas.items():
        percent = python_cos(vc, data[0])
        if percent > ratio:
            match_data.append((image_id, percent, data[1]))
            print(f'match: {image_id}, percent: {percent}')
    return sorted(match_data, key=lambda x: x[1], reverse=True)
