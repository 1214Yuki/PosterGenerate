import uuid


def random_uuid(with_hyphen=False) -> str:
    """
    生成uuid
    :param with_hyphen: 是否带有-
    :return:
    """
    uid = str(uuid.uuid4())
    return uid if with_hyphen else ''.join(uid.split('-'))


# 文字属性
HEADLINE = 'headline'
SUBTITLE = 'subtitle'
CHART_TITLE = 'chart-title'
CHART_NUMBER = 'chart-number'
TEXT = 'text'
ARTDECO = 'artdeco'

# 行业名称
FOOD = 'food'
SPORT = 'sport'
MAKEUPS = 'makeups'
LIVE = 'live'
COMMON = 'common'


# 行业主色色板
SCENE_COLOR = {
    'food': [],
    'sport': [],
    'makeups': [
        '#F5DEDB',
        '#106F75',
        '#E3A192',
        '#A2B0B3',
        '#E9BEB5',
        '#AA464A',
        '#F0E5E5',
        '#8E8A62',
        '#E18986',
        '#383C31',
        '#F4DCDF',
        '#EC5672',
        '#EA8592',
        '#8C7C7A',
        '#515607',
        '#F7B5CE',
        '#FBE7EC',
        '#CAB39B',
        '#707370',
        '#553631',
        '#F2B2B9',
        '#AD7957',
        '#EDEDEC',
        '#B67C64',
        '#061D9A',
        '#EBC3CA',
        '#7FCDE9',
        '#DAB029',
        '#8D3E49',
        '#3D4E5B',
        '#F76CEF',
        '#ECD5CC',
        '#B508FD',
        '#D26B5C',
        '#332831',
        '#F499B5',
        '#C9EBF2',
        '#A37467',
        '#A66F55',
        '#402A29',
        '#9B393F',
        '#D9A0B5',
        '#2D2E36',
        '#C7B6BB',
        '#4AC2FA',
        '#DD82B8',
        '#4C4FAA',
        '#EADBE9',
        '#8F62BF',
        '#6E71DD',
        '#F04D1E',
        '#E4C7B5',
        '#23F4C1',
        '#1078C6',
        '#181A1F',
        '#C67073',
        '#7BC6EF',
        '#F2EEEE',
        '#B38289',
        '#D7A0A4',
        '#7DA8FA',
        '#475B80',
        '#FABCE0',
        '#AE826B',
        '#F0EFF2',
        '#DFD6BD',
        '#264F48',
        '#7DCC9C',
        '#C34A3C',
        '#6B9484',
        '#53372A',
        '#E9E0DE',
        '#694F3F',
        '#241310',
        '#7F695E',
        '#EED8DD',
        '#D4C319',
        '#A784A9',
        '#BA9C92',
        '#AB95B4',
        '#78273F',
        '#EBDFD1',
        '#C5B389',
        '#262E48',
        '#92695C',
        '#CBAE7C',
        '#EAE6DF',
        '#2A3C1B',
        '#78783D',
        '#6E7D64',
        '#AF4333',
        '#C77A4B',
        '#1C427C',
        '#E6E7D6',
        '#60B9CE',
        '#E6DDDC',
        '#2F2A37',
        '#A0867B',
        '#876E7D',
        '#754A4F',
        '#F9C9C9',
        '#663A34',
        '#9F5149',
        '#DE9949',
        '#CB7A74',
        '#A31D24',
        '#E6C697',
        '#BD6955',
        '#520F13',
        '#B49799',
        '#AC793B',
        '#C6A695',
        '#2C0806',
        '#865850',
        '#572F29',
        '#ECF0EC',
        '#312821',
        '#C35E5A',
        '#CCAA9A',
        '#5CA3A5',
        '#B1D3EE',
        '#E8F2FA',
        '#329FCB',
        '#97BDE1',
        '#7D6053',
        '#97C9B5',
        '#50A18B',
        '#F7F9F9',
        '#F5A644',
        '#201F20',
        '#D1B27E',
        '#243717',
        '#EBE8DF',
        '#7A7B3F',
        '#84955B',
        '#667DC3',
        '#E3BCEF',
        '#8E2AB5',
        '#B26EDD',
        '#E9EAEE',
        '#DBBAA7',
        '#414072',
        '#69453B',
        '#DAD8DB',
        '#6D6E90',
        '#BB9381',
        '#D6B7A4',
        '#684841',
        '#EEDDD5',
        '#F9F5F0',
        '#A17CA4',
        '#FAE1DA',
        '#856D8F',
        '#5C4274',
        '#4C2C21',
    ],
    'live': [],
    'common': []
}


# 文字色彩模型
TEXT_MODE = {
    HEADLINE: 'X',
    SUBTITLE: 'V',
    CHART_TITLE: 'V',
    CHART_NUMBER: 'X',
    TEXT: 'V'
}

# 字体路径
TEXT_FONTS = {
    'headline': 'dataset/text_fonts/{scene}/headline/',
    'subtitle': 'dataset/text_fonts/{scene}/text/'
}

# 特殊文字颜色
GENERATE_FILL_COLOR = [(0, 0, 0), (255, 255, 255)]


class TextAlign:
    """
    文本对齐
    """
    LEFT = 'left'            # 左对齐
    X_CENTER = 'center'      # X方向中心对齐
    RIGHT = 'right'          # 右对齐
    TOP = 'top'              # 上对齐
    Y_CENTER = 'center'      # Y方向中心对齐
    BOTTOM = 'bottom'        # 下对齐


# 对齐关系优先级
ALIGN_PRIORITY = {
    TextAlign.LEFT: 100,
    # TextAlign.X_CENTER: 200,
}


CUSTOM_BG = 'custom_bg'
GENERATE = 'generate'
