import csv
import json
from collections import defaultdict

from utils import get_column_attrs
from utils.constants import TEXT_MODE, TextAlign, ALIGN_PRIORITY


class Rect(list):
    def __init__(self, rect):
        super().__init__()
        self.check_is_ok(rect)
        self.extend(rect)

    def check_is_ok(self, rect):
        if not isinstance(rect, list) and not isinstance(rect, tuple):
            raise TypeError('错误的类型')
        if len(rect) != 4:
            raise ValueError('错误的元素数量')

    @property
    def xmin(self):
        return self[0]

    @property
    def ymin(self):
        return self[1]

    @property
    def xmax(self):
        return self[2]

    @property
    def ymax(self):
        return self[3]

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    @property
    def center(self):
        return self.xmin + self.width / 2, self.ymin + self.height / 2


class Frame:
    def __init__(self, data):
        self.frame = self._init(data)
        self.aligns = self._aligns(data)

    def _init(self, data):
        items = dict()
        for k, v in data.items():
            items[k] = Rect([v['left'], v['top'], v['left'] + v['width'], v['top'] + v['height']])
        return items

    def _aligns(self, data):
        text_aligns = {}
        for k, v in data.items():
            # 获取不带编号的属性key
            _k = get_column_attrs(k)
            if _k not in TEXT_MODE:
                continue
            text_aligns[k] = self.cal_layer_align(k)
        return text_aligns

    @staticmethod
    def is_layers_near(base_layer, layer, threshold=4):
        """判断两文本图层的中心点是否在一定范围内"""
        if base_layer.width > base_layer.height:
            return abs(base_layer.center[1] - layer.center[1]) < threshold * base_layer.height
        else:
            return abs(base_layer.center[0] - layer.center[0]) < threshold * base_layer.width

    def cal_layer_align(self, layer, threshold=0.02):
        """
        计算图层和其他T、L图层间对齐关系
        :param layer: 图层
        :param threshold: 对齐允许的位置误差，百分值
        """
        aligns = {}
        layer_name, layer = layer, self.frame.get(layer)

        def _set_align(align_direction, label, base_label):
            """坐标相差在offset范围内认为对齐"""
            if label * (1 - threshold) <= base_label <= label * (1 + threshold):
                aligns.setdefault(align_direction, [])
                aligns[align_direction].append(1)

        for name, contrast_layer in self.frame.items():
            _name = get_column_attrs(name)
            if any([
                _name not in TEXT_MODE,
                layer == name,
                # not self.is_layers_near(layer, contrast_layer)
            ]):
                continue
            _set_align(TextAlign.LEFT, layer.xmin, contrast_layer.xmin)
            # _set_align(TextAlign.X_CENTER, layer.center[0], contrast_layer.center[0])

        # 多个对齐关系优先级：图层重要度>对齐数量>对齐优先级
        aligns = sorted(aligns.items(), key=lambda kv: (min(kv[1]), -len(kv[1]), ALIGN_PRIORITY[kv[0]]))

        # 没有对齐关系时，默认为居中
        align = TextAlign.LEFT if not aligns else aligns[0][0]
        return align


def reformat_generate_data(filepath, savepath):
    index_1 = [29,30,31,32,38,39,40,41,42,48,49,50,51,52]
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        p = []
        for index, row in enumerate(reader):
            if index == 0:
                continue
            objects = json.loads(row[3])
            d = defaultdict(list)
            if index < 16:
                d['background'].append({'top': 0, 'left': 0, 'height': 3000, 'width': 2024})
            elif 16 <= index <= 26:
                d['background'].append({'top': 0, 'left': 0, 'height': 3508, 'width': 2366})
            elif index in index_1:
                d['background'].append({'top': 0, 'left': 0, 'height': 525, 'width': 354})
            else:
                d['background'].append({'top': 0, 'left': 0, 'height': 875, 'width': 591})
            for ob in objects['objects']:
                d[ob['title']].append(ob['bbox'])
            res = dict()
            for key, values in d.items():
                if len(values) == 1:
                    res[key] = values[0]
                else:
                    values = sorted(values, key=lambda x: x['width'] * x['height'], reverse=True)
                    for idx, value in enumerate(values, start=1):
                        _key = '_'.join([key, str(idx)])
                        res[_key] = value
            p.append([row[0], json.dumps(res)])
    with open(savepath, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['image_id', 'labels_message'])
        for line in p:
            spamwriter.writerow(line)


if __name__ == '__main__':
    # p = '../dataset/frames.txt'
    # layout_to_frames_to_file(p)
    p = '../包含多列属性数据.csv'
    s = '../dataset/new_box_1.csv'
    reformat_generate_data(p, s)
