

def python_cos(q_vec, b_vec):
    """
    计算余弦相似度
    :param q_vec: 一维数组
    :param b_vec: 一维数组
    :return:
    """
    dot_q_b = 0
    q_vec_length = 0
    b_vec_length = 0
    for q, b in zip(q_vec, b_vec):
        dot_q_b += q * b
        q_vec_length += q * q
        b_vec_length += b * b
    length = (q_vec_length ** (1 / 2)) * (b_vec_length ** (1 / 2))
    cos_sim = dot_q_b / length  # 向量的内积除以向量模长的积
    # print('cos_sim', cos_sim)
    return cos_sim

