class Translated(object):
    """
    Save the translated result
    """
    def __init__(self, src_lang, tmp_lang, text, trans_text, back_text):
        self.source_text = text
        self.src = src_lang
        self.tmp = tmp_lang
        self.tran_text = trans_text
        self.result_text = back_text


    def __str__(self):
        return self.__unicode__()



    def __unicode__(self):
        if len(self.result_text) > 30 :
            show_text = ' '.join(self.result_text.split(' ')[:30])
            show_text += '...'
        return u'Trabslated(src={src}, tmp={tmp}, result_text={text})'.format(src=self.src, tmp=self.tmp, text = self.result_text)