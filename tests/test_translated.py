import pytest
from BackTranslation.translated import Translated


def make_result(back_text):
    return Translated(src_lang='en', tmp_lang='zh-cn', text='hello', trans_text='你好', back_text=back_text)


def test_attributes():
    r = make_result('hello there')
    assert r.source_text == 'hello'
    assert r.src == 'en'
    assert r.tmp == 'zh-cn'
    assert r.tran_text == '你好'
    assert r.result_text == 'hello there'


def test_str_short():
    r = make_result('hello there')
    s = str(r)
    assert 'hello there' in s
    assert 'Translated' in s
    assert '...' not in s


def test_str_long():
    long_text = ' '.join(['word'] * 50)
    r = make_result(long_text)
    s = str(r)
    assert '...' in s
    # Should only show first 30 words
    assert s.count('word') == 30


def test_str_exactly_30_words():
    text = ' '.join(['word'] * 30)
    r = make_result(text)
    s = str(r)
    assert '...' not in s
