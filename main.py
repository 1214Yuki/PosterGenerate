import json
import itertools

import streamlit as st
from PIL import Image
from networkx.algorithms.tree.branchings import random_string
from streamlit.elements.image import image_to_url
from streamlit.commands.page_config import get_random_emoji

from generate import generate_streamlit
from utils.constants import CUSTOM_BG, GENERATE, MAKEUPS, HEADLINE, CHART_TITLE, CHART_NUMBER, TEXT, \
    SUBTITLE

_type_mapper = {
    '自定义背景': CUSTOM_BG,
    '自动生成': GENERATE,
}


_scene_mapper = {
    '美妆': MAKEUPS,
    # '运动': SPORT
}


def sidebar_custom():
    st.sidebar.markdown('''# 数字广告平面图像设计生成 ''')
    st.sidebar.markdown('## **场景选择**')
    st.sidebar.markdown('')
    scene = st.sidebar.selectbox('', ['美妆', '运动'])
    st.sidebar.markdown('## **生成方式**')
    st.sidebar.markdown('')
    _type = st.sidebar.selectbox('', ['自定义背景', '自动生成'])
    st.sidebar.markdown('## 展示数量')
    show_count = st.sidebar.number_input('', min_value=5, max_value=100, key='1', value=10)
    # show_count = random.randint(300, 500)
    st.sidebar.markdown('## 文案填写')
    # st.sidebar.markdown('#### 标题')
    headline = st.sidebar.text_input('标题', value='')
    # st.sidebar.markdown('#### 副标题个数')
    sub_nums = st.sidebar.number_input('副标题个数', min_value=0, max_value=100, key='2', step=1)
    subtitles = []
    for i in range(1, int(sub_nums) + 1):
        subtitle = st.sidebar.text_input(f'副标题{i}', value='')
        subtitles.append(subtitle)

    charts = []
    # st.sidebar.markdown('#### 图表个数')
    chart_nums = st.sidebar.number_input('图表个数', min_value=1, max_value=100, key='3', step=1)
    for i in range(1, int(chart_nums) + 1):
        chart_title = st.sidebar.text_input(f'图表标题{i}', value='')
        chart_number = st.sidebar.text_input(f'图表数据{i}', value='')
        charts.append((chart_title, chart_number))

    texts = []
    # st.sidebar.markdown('#### 说明性文字个数')
    text_nums = st.sidebar.number_input('说明性文字个数', min_value=0, max_value=100, key='4', step=1)
    for i in range(1, int(text_nums) + 1):
        text = st.sidebar.text_input(f'说明性文字{i}', value='')
        texts.append(text)
    if _type_mapper[_type] == CUSTOM_BG:
        st.sidebar.markdown('## 上传图片')
        bg = st.sidebar.file_uploader('', type=['jpg', 'png'])
    else:
        # bg = st.sidebar.color_picker('背景色选取')
        bg = None

    placeholder = st.empty()
    with placeholder.beta_container():
        st.image('page.png', width=950)

    go = st.sidebar.button('海报生成')
    if go:
        placeholder.empty()
        if not headline or (not charts and charts[0][0] and charts[0][1]):
            st.error('标题和图表为必填字段!')

        subtitles.sort(key=lambda k: len(k), reverse=True)
        texts.sort(key=lambda k: len(k), reverse=True)
        charts.sort(key=lambda k: len(k[0]), reverse=True)

        _input = {
            HEADLINE: headline,
        }
        if len(subtitles) > 1:
            _input.update(
                {f'subtitle_{idx}': value for idx, value in enumerate(subtitles, start=1)}
            )
        else:
            _input.update(
                {SUBTITLE: value for idx, value in enumerate(subtitles, start=1)}
            )

        if len(texts) > 1:
            _input.update(
                {f'text_{idx}': value for idx, value in enumerate(texts, start=1)}
            )
        else:
            _input.update(
                {TEXT: value for idx, value in enumerate(texts, start=1)}
            )

        if len(charts) > 1:
            for idx, value in enumerate(charts, start=1):
                chart = {
                    f'chart-title_{idx}': value[0],
                    f'chart-number_{idx}': value[1],
                }
                _input.update(chart)
        else:
            _input.update({
                CHART_TITLE: charts[0][0],
                CHART_NUMBER: charts[0][1]
            })

        print(json.dumps(_input))
        if bg is None and _type_mapper[_type] == CUSTOM_BG:
            st.error('未上传背景图片！请上传背景图片')
        else:
            _type = _type_mapper[_type]
            scene = _scene_mapper[scene]
            file_name = random_string(5) + '.jpg'
            if bg:
                Image.open(bg).convert('RGB').save(f'dataset/upload/{file_name}', format='JPEG')
                bg_pic = f'dataset/upload/{file_name}'
            else:
                bg_pic = None

            # 特殊处理，模版存在2个text情况
            if len(texts) == 2 and scene == MAKEUPS and _type == TEMPLATE:
                scene = MAKEUPS + '2text'
                _input.pop('text_1')
                _input.pop('text_2')
            else:
                scene = MAKEUPS

            results = generate_streamlit(_input, _type, scene, show_count, bg_pic)
            links = []
            for index, res in enumerate(results):
                link = image_to_url(res, res.width, False, 'RGB', 'JPEG', index)
                links.append(link)
            html_image_show(links)


def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.

    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    return itertools.islice(enumerate(items), min_index, max_index)


def html_image_show(links):
    divs = [
        f"""
    <div class="brick">
    <a href="{idx}">
    <img src="{idx}">
    </a>
    </div>
    """
        for idx in links
    ]
    divs = "\n".join(divs)

    with open("statics/labs.css") as FIN:
        css0 = FIN.read()

    with open("statics/masonry.css") as FIN:
        css1 = FIN.read()

    html = """
    <html>
      <base target="_blank" />
      <head>
        <style> %s </style>
        <style> %s </style>
      </head>
      <body>
      <div class="masonry">
      %s
      </div>
      </body>
    </html>
    """ % (
        css0,
        css1,
        divs,
    )

    st.components.v1.html(html, height=3000, scrolling=True)


emoji = get_random_emoji()
app_formal_name = f"{emoji} 战报设计"
st.set_page_config(
    layout="wide", page_title=app_formal_name,
)
sidebar_custom()
