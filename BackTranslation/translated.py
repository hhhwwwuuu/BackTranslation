class Translated(object):
    """
    Save the translated result
    """
    def __init__(self, src_lang, tmp_lang, text, trans_text, back_text, dst_lang=None, mode='back_translation'):
        self.source_text = text
        self.src = src_lang
        self.tmp = tmp_lang
        self.dst = dst_lang if dst_lang is not None else tmp_lang
        self.mode = mode
        self.tran_text = trans_text
        self.result_text = back_text

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        if len(self.result_text.split(' ')) > 30:
            show_text = ' '.join(self.result_text.split(' ')[:30])
            show_text += '...'
        else:
            show_text = self.result_text
        return u'Translated(src={src}, tmp={tmp}, result_text={text})'.format(src=self.src, tmp=self.tmp, text=show_text)
