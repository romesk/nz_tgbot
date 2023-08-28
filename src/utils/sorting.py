
UKRAINIAN_ALNUM = "0123456789АаБбВвГгҐґДдЕеЄєЖжЗзИиІіЇїЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЮюЯя"


def ukrainian_sort_key(word):
    """
    Python doesn't have a built-in sorting key for Ukrainian, so we need to create one to include
    original ukrainian letters such as і, й, ї
    """

    key = []

    for c in word:
        if c in UKRAINIAN_ALNUM:
            key.append(UKRAINIAN_ALNUM.index(c))
        else:
            key.append(1000)  # if not present in alphabet, put it at the end

    return key
