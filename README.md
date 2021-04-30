# BackTranslation
[![version](https://img.shields.io/badge/version-0.3.1-blue)](https://pypi.org/project/BackTranslation/#description)
[![Downloads](https://pepy.tech/badge/backtranslation)](https://pepy.tech/project/backtranslation)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/hhhwwwuuu/BackTranslation/blob/main/LICENSE)

BackTranslation is a python library that implemented to back translate the words among any two languages. This utilizes [googletrans](https://py-googletrans.readthedocs.io/en/latest/) library and [Baidu Translation API](http://api.fanyi.baidu.com/) to translate the words.

Since there is an error in current verison of googletrans, you have to create only one instance to do back-translation for your work. Otherwise, it is easy to cause a bug from multi-requests. We will keep implementing this library with other translator libraries soon.

If you face any bug, you can open a issue in Github.

### Installation
You can install it from [PyPI](https://pypi.org/project/BackTranslation/#description):

```bash
$ pip install BackTranslation
```


## Usage
### Backtranslation with googletrans
Translate the original text to other language and translate back to augment the diversity of data in NLP research.

Parameters:
* **url**: option. provide a list of services urls for translation if need. Default url is _translate.google.com_.
* **proxies**: Optional. Proxies configuration. Dictionary mapping protocol or protocol and host to the URL of the proxy.
  i.e. proxies = {'http': '127.0.0.1:1234', 'http://host.name': '127.0.0.1:4012'}
* **text**: required. Original text that need to do back translation.
* **src**: option. Source language code of original text. If this parameter is None, the method will detect the language of text automatically. (Default: None)
* **tmp**: option. Middle language code. If this parameter is None, the method will pick one of two languages which is different from src.
* **sleeping**: option. It is a timer to limite the speed of back-translation to avoid the limitation of Google.  (Default: 0)

Return parameter: object _Translated_.

Attributes:
* source_text: original sentence.
* src: the language of original sentence
* tmp: the target language as middle man
* trans_text: intermediate result
* back_text: back-tranlsated result

```python
from BackTranslation import BackTranslation
trans = BackTranslation(url=[
      'translate.google.com',
      'translate.google.co.kr',
    ], proxies={'http': '127.0.0.1:1234', 'http://host.name': '127.0.0.1:4012'})
result = trans.translate('hello', src='en', tmp = 'zh-cn')
print(result.result_text)
# 'Hello there'
```


Note: You just need to create one instance of _BackTranslation_ in order to avoid [the issue in current version of googletrans](https://github.com/ssut/py-googletrans/issues/234#issuecomment-726067552). 

#### Search the language code
You may find out your language code with full language name by using this method.

Parameters:
* **language**: required. A language name in english.

```python
from BackTranslation import BackTranslation
trans = BackTranslation()
trans.searchLanguage('Chinese')
# {'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw'}
```
### Backtranslation_Baidu with Baidu Translation API
To use this stable translation, you are required to register in [Baidu Translation API]((http://api.fanyi.baidu.com/)) for getting your own appID.
It supports 2 million chacters per day for free.
_Note: Currently, they only support Chinese phone number to register the accout._
````python
from BackTranslation import BackTranslation_Baidu
trans = BackTranslation_Baidu(appid='YOUR APPID', secretKey='YOUR SECRETKEY')
result = trans.translate('hello', src='auto', tmp='zh')
print(result.result_text)
# 'hello'
trans.closeHTTP()
```` 
#### Seach language code
Since Baidu provides the different language code, it will be updated soon.


## Version Information
**Version 0.3.1: fix some bugs for Baidu translator.**

Version 0.2.2: fix the services url for Google Translator.

Version 0.2.1: fix the small bug. From this version, the library googletrans version is [4.0.0rc1](https://pypi.org/project/googletrans/4.0.0rc1/).

Version 0.2.0: support back-translation with Baidu API, and fix bugs

Version 0.1.0: support back-translation with googletrans library

## Contribution
Welcome to contribute BackTranslation library!

## reference
- [googletrans](https://py-googletrans.readthedocs.io/en/latest/)
- [Baidu Translation API](http://api.fanyi.baidu.com/)