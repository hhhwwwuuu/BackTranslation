from googletrans import Translator
import nltk
from nltk.tokenize import sent_tokenize
import time
from BackTranslation.languages import LANGUAGES, LANG_CODES
from BackTranslation.translated import Translated
import typing
import httpcore

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class BackTranslation(object):
    """
    Translate the words to other language and translate back
    in order to generate more samples for NLP.
    
    This package built based on googletrans package.
    Thus, you have to create only one instance to translate your words.
    Otherwise, an error will occur from googletrans.

    """

    def __init__(self, url=['translate.google.com'], proxies: typing.Dict[str, httpcore.SyncHTTPTransport] = None):
        self.translator = Translator(service_urls=url, proxies=proxies)
        self.Languages = LANGUAGES
        self.langCodes = LANG_CODES
        self.MAX_LENGTH = 5000

    def translate(self, text, src=None, tmp=None, sleeping=0):

        if not src:
            src = self.translator.detect(text).lang

        if src.lower() not in self.Languages:
            raise ValueError("'{}': INVALID source language.".format(src))

        # if tmp is null, set a default language for tmp.
        if not tmp:
            if src == 'en':
                tmp = 'zh-cn'
            else:
                tmp = 'en'

        if tmp not in self.Languages:
            raise ValueError("'{}': INVALID transited language.".format(tmp))

        if src == tmp:
            raise ValueError("Transited language ({tmp}) should different from srouce language ({src}).".format(
                tmp=self.langCodes[tmp], src=self.langCodes[src]))

        # check the length of text
        if len(text) > self.MAX_LENGTH:
            original_sentences = self._split_segement(sent_tokenize(text))

            t_text = self.translator.translate(original_sentences, src=src, dest=tmp)
            tran_text = ' '.join([t.text for t in t_text])
            time.sleep(sleeping)
            r_text = self.translator.translate([t.text for t in t_text], src=tmp, dest=src)
            back_text = ' '.join([r.text for r in r_text])
            back_text.rstrip()
        else:
            mid_text = self.translator.translate(text, src=src, dest=tmp)
            tran_text = mid_text.text
            time.sleep(sleeping)  # Sleep between translation
            result_text = self.translator.translate(tran_text, src=tmp, dest=src)
            back_text = result_text.text
        result = Translated(src_lang=src, tmp_lang=tmp, text=text, trans_text=tran_text, back_text=back_text)
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

    def searchLanguage(self, language):
        """
        Search a matched language code by language name.

        :param language: the full name of language in english
        :return: return matched language name and their code
        :rtype: dict

        Usage:
            >>> trans = BackTranslation()
            >>> trans.searchLanguage('frenc')
            # {'french': 'fr'}
            >>> trans.searchLanguage('Chinese')
            # {'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw'}
        """
        language = language.lower()
        if language in self.langCodes:
            return {language: self.langCodes[language]}
        else:
            language_list = [key for key in self.langCodes.keys() if language in key]
            if language_list != []:
                return {lan: self.langCodes[lan] for lan in language_list}
            else:
                raise ValueError("{}: No existing language.".format(language))
