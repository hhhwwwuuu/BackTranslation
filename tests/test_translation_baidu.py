import pytest
import json
from unittest.mock import MagicMock, patch, call
from BackTranslation.translation_Baidu import BackTranslation_Baidu


def _mock_response(src_lang, translated_text):
    return {
        'from': src_lang,
        'to': 'en',
        'trans_result': [{'dst': translated_text, 'src': 'original'}]
    }


@pytest.fixture
def trans():
    with patch('BackTranslation.translation_Baidu.http.client.HTTPConnection'):
        t = BackTranslation_Baidu(appid='test_appid', secretKey='test_secret')
        t._sendRequest = MagicMock()
        return t


def test_basic_translation(trans):
    trans._sendRequest.side_effect = [
        _mock_response('en', '你好'),
        _mock_response('zh', 'Hello there'),
    ]
    result = trans.translate('hello', src='en', tmp='zh')
    assert result.src == 'en'
    assert result.tmp == 'zh'
    assert result.tran_text == '你好'
    assert result.result_text == 'Hello there'


def test_back_translation_uses_tran_text_not_original(trans):
    """Issue #6: back-translation must use tran_text, not the original text."""
    calls = []

    def side_effect(text, src, tmp):
        calls.append((text, src, tmp))
        if src == 'en':
            return _mock_response('en', '你好')
        return _mock_response('zh', 'Hello there')

    trans._sendRequest.side_effect = side_effect
    trans.translate('hello', src='en', tmp='zh')

    assert calls[0] == ('hello', 'en', 'zh')
    assert calls[1][0] == '你好', "Back-translation must use intermediate text, not original"


def test_auto_detect_src(trans):
    trans._sendRequest.side_effect = [
        _mock_response('en', 'detected'),
        _mock_response('en', '你好'),
        _mock_response('zh', 'Hello there'),
    ]
    result = trans.translate('hello', src='auto', tmp='zh')
    assert result.src == 'en'


def test_default_tmp_when_src_en(trans):
    trans._sendRequest.side_effect = [
        _mock_response('en', '你好'),
        _mock_response('zh', 'Hello there'),
    ]
    result = trans.translate('hello', src='en')
    assert result.tmp == 'zh'


def test_default_tmp_when_src_not_en(trans):
    trans._sendRequest.side_effect = [
        _mock_response('zh', 'hello'),
        _mock_response('en', '你好'),
    ]
    result = trans.translate('你好', src='zh')
    assert result.tmp == 'en'


def test_same_src_tmp_raises(trans):
    with pytest.raises(ValueError, match='should different'):
        trans.translate('hello', src='en', tmp='en')


def test_invalid_appid():
    with patch('BackTranslation.translation_Baidu.http.client.HTTPConnection'):
        with pytest.raises(ValueError, match='INVALID appid'):
            BackTranslation_Baidu(appid='', secretKey='secret')


def test_invalid_secretkey():
    with patch('BackTranslation.translation_Baidu.http.client.HTTPConnection'):
        with pytest.raises(ValueError, match='INVALID secretKey'):
            BackTranslation_Baidu(appid='appid', secretKey='')


def test_sleeping_is_called(trans, mocker):
    """Issue #6: sleeping parameter must throttle requests to respect Baidu 1 QPS."""
    trans._sendRequest.side_effect = [
        _mock_response('en', '你好'),
        _mock_response('zh', 'Hello there'),
    ]
    mock_sleep = mocker.patch('BackTranslation.translation_Baidu.time.sleep')
    trans.translate('hello', src='en', tmp='zh', sleeping=1)
    mock_sleep.assert_called_with(1)


def test_default_sleeping_is_one(trans, mocker):
    trans._sendRequest.side_effect = [
        _mock_response('en', '你好'),
        _mock_response('zh', 'Hello there'),
    ]
    mock_sleep = mocker.patch('BackTranslation.translation_Baidu.time.sleep')
    trans.translate('hello', src='en', tmp='zh')
    mock_sleep.assert_called_with(1)
