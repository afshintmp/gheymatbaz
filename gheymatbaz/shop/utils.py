from itertools import chain


def get_child_id_func(ch):
    for cat in ch:
        if cat.child_category_list is None:
            ne = cat.child_category_list
            o = list(chain(ne, get_child_id_func(ne)))
