# BackTranslation
[![version](https://img.shields.io/badge/version-0.1-blue)](https://pypi.org/project/BackTranslation/#description)
[![Downloads](https://pepy.tech/badge/backtranslation)](https://pepy.tech/project/backtranslation)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/hhhwwwuuu/BackTranslation/blob/main/LICENSE)

BackTranslation is a python library that implemented to back translate the words among any two languages. This utilizes [googletrans](https://py-googletrans.readthedocs.io/en/latest/) library to translate the words.

Since there is an error in current verison of googletrans, you have to create only one instance to do back-translation for your work. Otherwise, it is easy to cause a bug from multi-requests. We will keep implementing this library with other translator libraries soon.

If you face any bug, you can open a issue in Github.

### Installation
You can install it from [PyPI](https://pypi.org/project/BackTranslation/#description):

```bash
$ pip install BackTranslation
```


## Usage
### Backtranslation
Translate the original text to other language and translate back to augment the diversity of data in NLP research.
Parameters:
* **text**: required. Original text that need to do back translation.
* **src**: option. Source language code of original text. If this parameter is None, the method will detect the language of text automatically. (Default: None)
* **tmp**: option. Middle language code. If this parameter is None, the method will pick one of two languages which is different from src.
* **sleeping**: option. It is a timer to limite the speed of back-translation to avoid the limitation of Google.  (Default: 0)

```python
from BackTranslation import BackTranslation
trans = BackTranslation()
result = trans.translate('hello', src='en', tmp = 'zh-cn')
print(result.result_text)
# 'Hello there'
```

### Search the language code
You may find out your language code with full language name by using this method.
Parameters:
* **language**: required. A language name in english.

```python
from BackTranslation import BackTranslation
trans = BackTranslation()
trans.searchLanguage('Chinese')
# {'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw'}
```


## reference
- [googletrans](https://py-googletrans.readthedocs.io/en/latest/)