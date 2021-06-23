from __future__ import unicode_literals

import colorsys
import math
import os
import random
import re
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from itertools import zip_longest
from multiprocessing import cpu_count
from concurrent.futures import as_completed

import textwrap
from PIL import ImageDraw, Image, ImageFont, ImageColor
from colorthief import ColorThief
from networkx.algorithms.tree.branchings import random_string

from match.fresh import match_best_data, vector_items
from utils import get_column_attrs
from utils.color import color_match_harmony
from utils.constants import *

tp_executor = ThreadPoolExecutor(max_workers=cpu_count() * 3)


NO_WRAP_TYPE = [
    CHART_NUMBER,
    CHART_TITLE,
    # TEXT
]

COLOR_SV = {
    'makeups': (0.6, 0.8),
}

COLOR_MODE = {
    'makeups': {
        HEADLINE: 'X',
        SUBTITLE: 'X'
    }
}


FONT_WEIGHT = {
    'makeups': {
        HEADLINE: ['华康勘亭流 Std W9.otf', '华康新综艺 Std W7.ttf', '江西拙楷2.0.ttf']
    }
}


class Generate:
    def __init__(self, scene, frame, fill_data, bg_pic=None, save_dir=None):
        self.im = None
        self.scene = scene
        self.frame = frame
        self.fill_data = fill_data
        self.bg_pic = bg_pic
        self.bg_color = self.get_bg_color()
        self.canvas = self.get_bg_pic()
        self.fonts = self.distribute_text_font()
        self.colors = self.distribute_text_color()
        self.save_dir = save_dir
        self.base_dir = self._base_dir()

    def distribute_text_font(self):
        main_path = TEXT_FONTS.get(HEADLINE).format(scene=self.scene)
        sub_path = TEXT_FONTS.get(SUBTITLE).format(scene=self.scene)
        main_fonts = []
        for font in os.listdir(main_path):
            if font.startswith('.'):
                continue
            if font in FONT_WEIGHT.get(self.scene)[HEADLINE]:
                main_fonts.extend([os.path.join(main_path, font)] * 3)
            else:
                main_fonts.extend([os.path.join(main_path, font)])
        # main_fonts = [os.path.join(main_path, font) for font in os.listdir(main_path) if not font.startswith('.')]
        sub_fonts = [os.path.join(sub_path, font) for font in os.listdir(sub_path) if not font.startswith('.')]
        headline = chart_number = random.choice(main_fonts)
        subtitle = chart_title = text = random.choice(sub_fonts)

        d = dict()
        for text_type in self.frame.frame:
            _text_type = get_column_attrs(text_type)
            if _text_type in [HEADLINE, CHART_NUMBER]:
                d[text_type] = headline
            else:
                d[text_type] = text

        return d

    def get_text_type_crop_bg_color(self, text_type):
        # text_rect = self.frame.frame.get(text_type)
        if self.bg_pic:
            # b = io.BytesIO()
            # bg = self.im.crop(text_rect).convert('RGB')
            # bg.save(b, 'JPEG')
            # color_thief = ColorThief(b)
            # color = color_thief.get_color(quality=10)
            color = self.bg_color
        else:
            color = self.bg_color
        return color

    def get_color_mode(self):
        return COLOR_MODE.get(self.scene, {
            HEADLINE: 'X',
            SUBTITLE: 'X'
        })

    def distribute_text_color(self):
        color_mode = self.get_color_mode()
        main_colors = self.get_text_color(
            HEADLINE, color_mode=color_mode[HEADLINE], number=30, fill_colors=GENERATE_FILL_COLOR)
        headline = chart_number = subtitle = chart_title = text = random.choice(main_colors[0:17] + main_colors[22:])
        # 随机挑选30以内的数，若能被4整除则选结果2
        if random.choice(range(10)) % 2 == 0:
            subtitle = chart_title = text = random.choice(self.get_text_color(
                SUBTITLE, color_mode=TEXT_MODE[SUBTITLE], number=30)[:17])

        d = dict()
        for text_type in self.frame.frame:
            _text_type = get_column_attrs(text_type)
            if _text_type in [HEADLINE, CHART_NUMBER]:
                d[text_type] = headline
            else:
                d[text_type] = text

        return d

    def get_bg_color(self):
        if self.bg_pic:
            color_thief = ColorThief(self.bg_pic)
            color = color_thief.get_color(quality=10)
        else:
            scene_colors = SCENE_COLOR.get(self.scene)[::5]
            color = random.choice(scene_colors)
            color = ImageColor.getrgb(color)
            # todo: 尝试获取颜色明度，饱和度选择背景色
        return color

    def get_bg_pic(self):
        bg_rect = self.frame.frame.get('background')
        if bg_rect:
            bg_size = bg_rect.width, bg_rect.height
        else:
            bg_size = (2024, 3000)

        if self.bg_pic:
            img = Image.open(self.bg_pic) if isinstance(self.bg_pic, str) else self.bg_pic
            im = img.resize(bg_size, Image.ANTIALIAS)
            canvas = ImageDraw.Draw(im)
        else:
            im = Image.new("RGB", bg_size, self.bg_color)
            canvas = ImageDraw.Draw(im)
        self.im = im
        return canvas

    @staticmethod
    def _get_reduce_size_count(ratio):
        if ratio < 1:
            reduce = 0
        elif 1 < ratio < 2:
            reduce = 1
        elif ratio < 3:
            reduce = 3
        elif ratio < 5:
            reduce = 5
        else:
            reduce = 8
        return reduce

    def get_text_font_size(self, text_type, font_path):
        origin_text = text = self.fill_data.get(text_type)
        text_rect = self.frame.frame.get(text_type)
        olfs = int(text_rect.height)
        f = ImageFont.truetype(font_path, olfs)
        w, h = f.getsize_multiline(text)
        w_ratio, h_ratio = w / text_rect.width, h / text_rect.height
        scale_olfs = olfs
        lines_spacing = scale_olfs * 0.1
        text_list = re.split(r'(；|;\s|，|,\s|！|!\s|。)', origin_text)
        text_list = list(zip_longest(text_list[::2], text_list[1::2], fillvalue=''))
        text_list = [''.join(i) for i in text_list]
        while w_ratio > 1 or h_ratio > 1:
            reduce = self._get_reduce_size_count(max(w_ratio, h_ratio))
            scale_olfs = scale_olfs - reduce
            _text_type = get_column_attrs(text_type)
            if _text_type not in NO_WRAP_TYPE:
                div, off = olfs // scale_olfs, olfs % scale_olfs
                div = div if div else div + 1
                _div = math.ceil(len(text_list) / div)
                if len(text_list) <= 1:
                    _text_list = textwrap.wrap(textwrap.dedent(origin_text), width=math.ceil(len(origin_text) / div))
                else:
                    _text_list = []
                    for i in range(div):
                        _text_list.append(''.join(text_list[i*_div:(i+1)*_div]))

                lines_spacing = scale_olfs * 0.1
                text = '\n'.join(_text_list)
            f = ImageFont.truetype(font_path, scale_olfs)
            w, h = f.getsize_multiline(text, spacing=lines_spacing)
            w_ratio, h_ratio = w / text_rect.width, h / text_rect.height
        print(text)
        return text, scale_olfs, lines_spacing, w, h

    def get_color_hsv(self, color_rgb):
        color_hsv = list(colorsys.rgb_to_hsv(color_rgb[0], color_rgb[1], color_rgb[2]))
        color_hsv[2] = color_hsv[2] / 255.
        s, v = COLOR_SV.get(self.scene)
        return color_hsv[0], s or color_hsv[1], v or color_hsv[2]

    def get_text_color(self, text_type, color_mode, number, fill_colors=None):
        fill_colors = fill_colors or GENERATE_FILL_COLOR
        color_rgb = self.get_text_type_crop_bg_color(text_type)
        color_rgb = self.get_color_hsv(color_rgb)
        colors = color_match_harmony(color_rgb, mode=color_mode, number=number)
        return colors + fill_colors

    def get_text_font(self, text_type):
        font_path = self.fonts.get(text_type)
        multi_text, font_size, lines_spacing, w, h = self.get_text_font_size(text_type, font_path)
        return multi_text, ImageFont.truetype(font_path, font_size, encoding='unic'), font_size, lines_spacing, w, h

    def get_text_attrs(self, text_type):
        color = self.colors.get(text_type)
        text, font, font_size, lines_spacing, w, h = self.get_text_font(text_type)
        return {
            'color': color,
            'font': font,
            'text': text,
            'font_size': font_size,
            'lines_spacing': lines_spacing,
            'box_size': (w, h)
        }

    def render(self, is_show=True):
        try:
            for text_type, data in self.fill_data.items():
                text_rect = self.frame.frame.get(text_type)
                _text_type = get_column_attrs(text_type)
                if _text_type in TEXT_MODE:
                    attrs = self.get_text_attrs(text_type)
                    xy = text_rect.xmin, text_rect.ymin + (text_rect.height - attrs['box_size'][1]) / 2
                    align = self.frame.aligns.get(text_type)
                    self.canvas.multiline_text(
                        xy=xy, text=attrs['text'], align=align,
                        fill=tuple(attrs['color']),
                        font=attrs['font'], spacing=attrs['lines_spacing'])
                else:
                    w_s, h_s = text_rect.width / data.size[0], text_rect.height / data.size[1]
                    size = (int(text_rect.width * h_s), int(text_rect.height)) \
                        if w_s > h_s else (int(text_rect.width), int(text_rect.height * w_s))
                    data = data.resize(size, Image.ANTIALIAS)
                    xmin = int((text_rect.width - size[0]) / 2 + text_rect.xmin)
                    ymin = int((text_rect.height - size[1]) / 2 + text_rect.ymin)
                    self.im.paste(data, (xmin, ymin, xmin + size[0], ymin + size[1]))

                # self.canvas.rectangle(xy=text_rect, outline="red", width=4)
            if is_show:
                self.show()
            return self.im
        except Exception as e:
            print(f'catch error: {e}')
            print(traceback.print_exc())
            return None

    def _base_dir(self):
        if self.save_dir:
            if self.bg_pic:
                _dir = os.path.splitext(self.bg_pic)[0].split('/')[-1]
            else:
                _dir = 'pure_bg_color'
            base_dir = os.path.join(self.save_dir, _dir)
            os.makedirs(base_dir, exist_ok=True)
            return base_dir

    def show(self):
        if self.base_dir:
            path = os.path.join(self.base_dir, random_string(6) + '.jpg')
            self.im.convert('RGB').save(path, format='JPEG')
        else:
            self.im.show()


def exec_generate_posters(frames_path, input_data, scene, match_ratio, most_count,
                          bg_pic=None, is_show=False, thread=True, save_dir=None):
    vc = vector_items(input_data.keys())
    match_frames = match_best_data(frames_path, vc, match_ratio)[:most_count]
    random.shuffle(match_frames)

    if most_count > len(match_frames):
        div = most_count / match_frames
        match_frames = match_frames * math.ceil(div)
        match_frames = match_frames[:most_count]

    results = []
    if thread:
        print('enter threading ....')
        futures = []
        for _id, precent, frame in match_frames:
            gen = Generate(scene, frame, input_data, bg_pic=bg_pic, save_dir=save_dir)
            future = tp_executor.submit(gen.render, is_show)
            futures.append(future)

        for future in as_completed(futures):
            if future.result() is None:
                continue
            results.append(future.result())
        results = results * 2
        return results[:most_count]

    print('enter signle runing ...')
    for _id, precent, frame in match_frames:
        gen = Generate(scene, frame, input_data, bg_pic=bg_pic, save_dir=save_dir)
        res = gen.render(is_show)
        if res is None:
            continue
        results.append(res)
    return results
