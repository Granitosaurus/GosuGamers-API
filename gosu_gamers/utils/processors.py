import collections


def first(iterator):
    if not isinstance(iterator, collections.Iterable):
        raise TypeError('Iterator "{}" not iterable')
    for el in iterator:
        if el is None:
            continue
        if el == '':
            continue
        return el
    return None

if __name__ == '__main__':
    print(first('1234'))
    print(first([1,2,3]))
    print(first(['', '100']))