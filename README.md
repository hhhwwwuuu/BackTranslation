# BackTranslation
[![version](https://img.shields.io/badge/version-0.1-blue)]()
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/hhhwwwuuu/BackTranslation/blob/main/LICENSE)
Back translation for NLP using Google Translator.

### Installation
```bash
$ pip install BackTranslation
```

## Usage
### Backtranslation
```python
from BackTranslation import BackTranslation
trans = BackTranslation()
result = trans.translate('hello', src='en', tmp = 'zh-cn')
print(result.result_text)
# 'Hello there'
```

### Search the language code

```python
from BackTranslation import BackTranslation
trans = BackTranslation()
trans.searchLanguage('Chinese')
# {'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw'}
```


## reference
- [googletrans](https://py-googletrans.readthedocs.io/en/latest/)