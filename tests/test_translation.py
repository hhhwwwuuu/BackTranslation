import pytest
from unittest.mock import MagicMock, patch
from BackTranslation.translation import BackTranslation
import httpcore


def _make_translate_result(text):
    m = MagicMock()
    m.text = text
    return m


@pytest.fixture
def trans():
    with patch('BackTranslation.translation.Translator') as MockTranslator:
        instance = MockTranslator.return_value
        instance.translate.side_effect = lambda text, src, dest: (
            _make_translate_result('你好') if dest != 'en' else _make_translate_result('Hello there')
        )
        instance.detect.return_value = MagicMock(lang='en')
        yield BackTranslation.__new__(BackTranslation), instance, MockTranslator


def _build_trans(mock_translate_fn=None):
    with patch('BackTranslation.translation.Translator') as MockTranslator:
        instance = MockTranslator.return_value
        if mock_translate_fn:
            instance.translate.side_effect = mock_translate_fn
        instance.detect.return_value = MagicMock(lang='en')
        t = BackTranslation()
        t.translator = instance
        return t, instance


def test_basic_translation():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = [
        _make_translate_result('你好'),
        _make_translate_result('Hello there'),
    ]
    result = trans.translate('hello', src='en', tmp='zh-cn')
    assert result.src == 'en'
    assert result.tmp == 'zh-cn'
    assert result.source_text == 'hello'
    assert result.tran_text == '你好'
    assert result.result_text == 'Hello there'


def test_auto_detect_src():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = [
        _make_translate_result('你好'),
        _make_translate_result('Hello there'),
    ]
    result = trans.translate('hello', tmp='zh-cn')
    assert result.src == 'en'


def test_default_tmp_when_src_en():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = [
        _make_translate_result('你好'),
        _make_translate_result('Hello there'),
    ]
    result = trans.translate('hello', src='en')
    assert result.tmp == 'zh-cn'


def test_default_tmp_when_src_not_en():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = [
        _make_translate_result('hello'),
        _make_translate_result('你好'),
    ]
    result = trans.translate('你好', src='zh-cn')
    assert result.tmp == 'en'


def test_invalid_src_raises():
    trans, _ = _build_trans()
    with pytest.raises(ValueError, match='INVALID source language'):
        trans.translate('hello', src='xx')


def test_invalid_tmp_raises():
    trans, _ = _build_trans()
    with pytest.raises(ValueError, match='INVALID transited language'):
        trans.translate('hello', src='en', tmp='xx')


def test_same_src_tmp_raises():
    trans, _ = _build_trans()
    with pytest.raises(ValueError, match='should different'):
        trans.translate('hello', src='en', tmp='en')


def test_sleeping_is_called(mocker):
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = [
        _make_translate_result('你好'),
        _make_translate_result('Hello there'),
    ]
    mock_sleep = mocker.patch('BackTranslation.translation.time.sleep')
    trans.translate('hello', src='en', tmp='zh-cn', sleeping=2)
    mock_sleep.assert_called_once_with(2)


def test_connect_timeout_raises_friendly_message():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = httpcore.ConnectTimeout()
    with pytest.raises(httpcore.ConnectTimeout, match='proxies'):
        trans.translate('hello', src='en', tmp='zh-cn')


def test_general_exception_raises_with_hint():
    trans, mock_translator = _build_trans()
    mock_translator.translate.side_effect = Exception('some googletrans error')
    with pytest.raises(Exception, match="sleeping"):
        trans.translate('hello', src='en', tmp='zh-cn')


def test_search_language():
    trans, _ = _build_trans()
    result = trans.searchLanguage('Chinese')
    assert 'zh-cn' in result.values()


def test_search_language_not_found():
    trans, _ = _build_trans()
    with pytest.raises(ValueError):
        trans.searchLanguage('notareallanguage')


def test_long_text_split(mocker):
    trans, mock_translator = _build_trans()
    long_text = 'Hello world. ' * 500

    tran_mock = _make_translate_result('你好')
    back_mock = _make_translate_result('Hello there')
    mock_translator.translate.side_effect = [
        [tran_mock],       # first call: list of sentences → list of results
        [back_mock],       # second call: back-translate list
    ]
    mocker.patch('BackTranslation.translation.sent_tokenize', return_value=['Hello world. ' * 250, 'Hello world. ' * 250])
    mock_sleep = mocker.patch('BackTranslation.translation.time.sleep')
    result = trans.translate(long_text, src='en', tmp='zh-cn')
    assert result.src == 'en'
    assert mock_sleep.called
