
from generate.generate import exec_generate_posters
from utils.constants import CUSTOM_BG, GENERATE

frame_path = 'dataset/new_box_1.csv'
gen_save_dir = '../result/generate_v1/'
tep_save_dir = '../result/template'


def generate_streamlit(_input, _type, scene, show_counts, bg_pic=None):
    if _type == CUSTOM_BG:
        res = exec_generate_posters(frame_path, _input, scene, match_ratio=0.8, most_count=show_counts,
                                    bg_pic=bg_pic, is_show=False, thread=True)
    elif _type == GENERATE:
        res = exec_generate_posters(frame_path, _input, scene, match_ratio=0.8, most_count=show_counts,
                                    bg_pic=None, is_show=False, thread=True)
    else:
        res = []
    return res
