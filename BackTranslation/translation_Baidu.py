import http.client
import hashlib
import urllib
import random
import json

import nltk
from nltk.tokenize import sent_tokenize
from BackTranslation.translated import Translated

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class BackTranslation_Baidu(object):

    def __init__(self, appid, secretKey):
        if not appid:
            raise ValueError("'{}': INVALID appid, please register in http://api.fanyi.baidu.com/.".format(appid))

        if not secretKey:
            raise ValueError(
                "'{}': INVALID secretKey, please register in http://api.fanyi.baidu.com/.".format(secretKey))

        self.appid = appid
        self.secretKey = secretKey
        self.MAX_LENGTH = 6000
        self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        self.queryURL = '/api/trans/vip/translate'

    def translate(self, text, src='auto', tmp=None):
        if src == 'auto':
            src = self._get_srcLang(self._sendRequest(text, src, 'en'))

        if not tmp:  # if tmp is None, set the default tmp language
            if src == 'en':
                tmp = 'zh'
            else:
                tmp = 'en'

        if src == tmp:
            raise ValueError(
                "Transited language ({tmp}) should different from srouce language ({src}).".format(tmp=tmp, src=src))

        # check the length of sentence
        if len(text.encode('utf-8')) > self.MAX_LENGTH:
            original_sentences = self._split_segement(sent_tokenize(text))

            # translate the sentence one by one
            tran_text = []
            back_text = []
            for sentence in original_sentences:
                if sentence == "":
                    continue
                # language A --> language B
                mid = self._get_translatedText(self._sendRequest(sentence, src, tmp))
                tran_text.append(mid)

                # language B --> language A
                back_text.append(self._get_translatedText(self._sendRequest(mid, tmp, src)))
            tran_text = ' '.join(tran_text)
            back_text = ' '.join(back_text)
        else:
            tran_text = self._get_translatedText(self._sendRequest(text, src, tmp))
            back_text = self._get_translatedText(self._sendRequest(text, tmp, src))
        result = Translated(src_lang=src, tmp_lang=tmp, text=text, trans_text=tran_text, back_text=back_text)
        return result

    def _sendRequest(self, text, src, tmp):
        salt = random.randint(32768, 65536)
        sign = hashlib.md5((self.appid + text + str(salt) + self.secretKey).encode()).hexdigest()
        url = self.queryURL + '?appid=' + self.appid + '&q=' + urllib.parse.quote(
            text) + '&from=' + src + '&to=' + tmp + '&salt=' + str(salt) + '&sign=' + sign

        try:
            self.httpClient.request('GET', url)
            response = self.httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
        except Exception as e:
            print("'{}': Connection error.".format(e))

        return result

    def _split_segement(self, sentences):
        """
        Split the long sentences into multiple sentences whose lengths are less than MAX_LENGTH.

        :param sentences: the list of tokenized sentences from source text
        :return: the list of sentences with proper length
        :rtype: list
        """
        sentences_list = []
        block = ""
        for sentence in sentences:
            if len((block.rstrip() + ' ' + sentence).encode('utf-8')) > self.MAX_LENGTH:
                sentences_list.append(block.rstrip())
                block = sentence
            else:
                block = block + sentence + ' '
        sentences_list.append(block.rstrip())
        return sentences_list

    def closeHTTP(self):
        self.httpClient.close()

    def _get_srcLang(self, result):
        return result['from']

    def _get_translatedText(self, result):
        return result['trans_result'][0]['dst']
