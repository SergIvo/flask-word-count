import re

from pymorphy2 import MorphAnalyzer

#We should have:
#Number of words - check
#Number of sentences - check
#Number of paragraphs - probably
#Paragraphs with direct speech ratio - not quite
#Dialog attribution ratio - probably
#Number of unique words - probably
#Number of non-semantic words - probably
#Ipm number of parts of speech - probably
#Presence in sentences for each part of speech - prbly
#Number of basises in sentences - ?


def merge_dicts(dicts_one, dicts_two, key):
    for i in dicts_one:
            for j in dicts_two:
                if i[key] == j[key]:
                    for kword in j:
                        if kword != key:
                            i[kword] = j[kword]
                    break
    return dicts_one

#Class for better handling all analysis methods and producing more handy data structure
class Text_Analyze():
    def __init__(self, text):
        self.general_data = {'symbols': self.symbols_data(text), 
            'paragraphs': self.paragraphs_data(text), 
            'sentences': self.sentences_data(text), 
            'words': self.words_data(text),
            'punctuation': self.punc_marks(text)}
        self.words_analyzed = self.word_analyze(text)
        self.POS_analyzed = self.POS_analyze(text)
    
    #Methods for general data calculating
    def symbols_data(self, text):
        '''Symbols related information about text'''
        sym_data = {}
        sym_data['total_symbols'] = self.sym_count(text)[0]
        sym_data['without_spaces'] = self.sym_count(text)[1]
        return sym_data
        
    def words_data(self, text):
        '''Words related information about text'''
        words_data = {}
        text_words = self.get_words(text)
        words_data['total'] = len(text_words)
        word_lengths = [len(item) for item in text_words]
        words_data['longest'] = max(word_lengths)
        words_data['shortest'] = min(word_lengths)
        words_data['mean'] = round(sum(word_lengths) / len(word_lengths), 3)
        words_data['autosem'] = self.count_unique(text_words)
        words_data['nonsem'] = self.count_non_semantic(text_words)
        words_data['waste_ratio'] = round(words_data['nonsem'] / words_data['total'], 3)
        return words_data
        
    def paragraphs_data(self, text):
        '''Paragraphs and direct speech related information about text'''
        pargs_data = {}
        text_pars = self.get_paragraphs(text)
        pargs_data['total'] = len(text_pars)
        par_lengths = [len(self.get_words(item)) for item in text_pars]
        pargs_data['shortest'] = min(par_lengths)
        pargs_data['longest'] = max(par_lengths)
        pargs_data['mean'] = round(sum(par_lengths) / len(par_lengths), 3)
        pargs_data['dspeech'] = self.dspeech_ratio(text_pars)
        pars_dspeech = (item for item in text_pars if self.is_dspeech(item))
        pars_dsp_attr_ratio = [self.dspeech_attr_ratio(item) for item in pars_dspeech if self.dspeech_attr_ratio(item)]
        if pars_dsp_attr_ratio:
            pargs_data['dsp_attr'] = sum(pars_dsp_attr_ratio) / len(pars_dsp_attr_ratio)
        return pargs_data
        
    def sentences_data(self, text):
        '''Sentences related information about text'''
        sents_data = {}
        text_sents = self.get_sentences(text)
        sents_data['total'] = len(text_sents)
        sents_lengths = [len(self.get_words(item)) for item in text_sents]
        sents_data['shortest'] = min(sents_lengths)
        sents_data['longest'] = max(sents_lengths)
        sents_data['mean'] = round(sum(sents_lengths) / len(sents_lengths), 3)
        return sents_data
    
    #Method for all frequency characteristics for words
    def word_analyze(self, text):
        '''Word frequencies and other word numerical data'''
        text_words = self.get_words(text)
        word_count = self.word_count(text_words)
        for descript in (self.word_data(item) for item in text_words):
            for word in word_count:
                if descript.normal_form == word['word']:
                    if 'forms' in word.keys():
                        word['forms'].add(descript.word)
                    else:
                        word['forms'] = {descript.word}
                    word['POS'] = descript.tag.POS
        for word in word_count:
            if self.word_rank(word['word']) <= 3:
                word['semantic'] = 'Autosemantic'
            else:
                word['semantic'] = 'Semisemantic'
        text_sents = self.get_sentences(text)
        for sentence in text_sents:
            semantic_part = {word for word in self.get_words(sentence) if self.word_rank(word) <= 3}
            for item in semantic_part:
                for word in word_count:
                    if item in word['forms']:
                        if 'context' in word.keys():
                            word['context'].update(semantic_part)
                        else:
                            word['context'] = semantic_part.copy()
                        word['context'].remove(item)
                        break
        for word in word_count:
            if 'context' in word.keys():
                word['context'] = ', '.join(word['context'])
            else:
                word['context'] = ''
            word['forms'] = ', '.join(word['forms'])
        return word_count
    
    #Method for all frequency characteristics for POSes
    def POS_analyze(self, text):
        text_sents = self.get_sentences(text)
        POS_data = self.POS_presence(text_sents)
        for item in POS_data:
            counted = [word['amount'] for word in filter(lambda x: x['POS'] == item['POS'], self.words_analyzed)]
            item['amount'] = sum(counted)
        return POS_data
    
    #Methods purposed not for standalone usage
    '''MorphAnalyzer used as class attribute since it shell not be changed in any instance of this class.'''
    morph = MorphAnalyzer()
    
    def word_data(self, word):
        '''Raw method for collecting data about word.'''
        all_data = self.morph.parse(word)
        selected = sorted(all_data, key = lambda data: data.score, reverse = True)[0]
        return selected
    
    def word_count(self, words):
        '''Count only normal forms of given words'''
        word_count = {}
        for word in words:
            word_data = self.word_data(word)
            if word_data.normal_form in word_count.keys():
                word_count[word_data.normal_form] += 1
            else:
                word_count[word_data.normal_form] = 1
        counted = [{'word': key, 'amount': word_count[key]} for key in word_count]
        counted.sort(key = lambda pare: pare['amount'], reverse = True)
        total = len(words)
        for item in counted:
            item['ipm'] = round((item['amount'] / total) * 1000000, 2)
        return counted
    
    def count_POS(self, words):
        '''Count just any instances of any part of speech'''
        POS_count = {}
        for word in words:
            word_data = self.word_data(word)
            key = word_data.tag.POS
            if key in POS_count.keys():
                POS_count[key] += 1
            else:
                POS_count[key] = 1
        counted = [{'POS': key, 'amount': POS_count[key]} for key in POS_count]
        counted.sort(key = lambda pare: pare['amount'], reverse = True)
        total = len(words)
        for item in counted:
            item['ipm'] = round((item['amount'] / total) * 1000000, 2)
        return counted
        
    def POS_presence(self, sentences):
        POS_presence ={}
        for sentence in sentences:
            words = [word for word in re.split(r'\W', sentence) if word]
            word_data = [self.word_data(word) for word in words]
            POSes = {data.tag.POS for data in word_data}
            for POS in POSes:
                if POS in POS_presence.keys():
                    POS_presence[POS] += 1
                else:
                    POS_presence[POS] = 1
        counted = [{'POS': key, 'presence': POS_presence[key]} for key in POS_presence]
        counted.sort(key = lambda pare: pare['presence'], reverse = True)
        total = len(sentences)
        for item in counted:
            item['ips'] = round((item['presence'] / total), 3)
        return counted
    
    def word_rank(self, word):
        word_rank = 6
        ranks = [{'rank': 1, 'forms': {'NOUN': 'nomn', 'NPRO': 'nomn', 'VERB': '', 'INFN': ''}},
                {'rank': 2, 'forms': {'NOUN': '', 'NPRO': '', 'PRTF': '', 'PRTS': '', 'GRND': ''}},
                {'rank': 3, 'forms': {'ADJF': '', 'ADJS': '', 'ADVB': '', 'PRED': ''}},
                {'rank': 4, 'forms': {'COMP': '', 'NUMR': ''}},
                {'rank': 5, 'forms': {'PREP': '', 'CONJ': '', 'PRCL': ''}},
                {'rank': 6, 'forms': {'INTJ': ''}}]
        parse_result = self.morph.parse(word)
        description = sorted(parse_result, key = lambda parsed: parsed.score, reverse = True)[0]
        for rank in ranks:
            for key in rank['forms']:
                if key in description.tag and rank['forms'][key] and rank['forms'][key] in description.tag:
                    word_rank = rank['rank']
                    break
                elif key in description.tag and not rank['forms'][key]:
                    word_rank = rank['rank']
                    break
        return word_rank
    
    def count_unique(self, words):
        '''Method for counting autosemantic words'''
        counted = self.word_count(words)
        unique = [x for x in counted if self.word_rank(x['word']) <= 3]
        return len(unique)
        
    def count_non_semantic(self, words):
        '''Method for counting non-semantic words'''
        counted = self.word_count(words)
        non_semantic = [x for x in counted if self.word_rank(x['word']) >= 4]
        return len(non_semantic)
    
    def common_comp(self, sentences):
        '''Method for finding most common POSes components for sentence in given sentences'''
        components = []
        for sentence in sentences:
            words = [word for word in re.split(r'\W', sentence) if word]
            word_data = [self.word_data(word) for word in words]
            POSes = (data.tag.POS for data in word_data)
            components.append(set(POSes))
        return components
    
    #Split given text into sentences
    def get_sentences(self, text):
        sentences = [item for item in re.split(r'[.!?"“”\t\n\r/]', text) if item]
        return sentences
    
    #Split given text into paragraphs
    def get_paragraphs(self, text):
        paragraphs = [item for item in re.split(r'[*\t\n\r/]', text) if item]
        return paragraphs
        
    def get_words(self, text):
        clean_text = ''.join(self.get_paragraphs(text))
        words = [item.lower() for item in re.split(r'\W', clean_text) if item]
        return words
    
        #Calculate text length in symbols with and without spaces
    def sym_count(self, text):
        clean_text = ''.join(self.get_paragraphs(text))
        total = len(clean_text)
        no_space = len(''.join(re.split(r'\s', clean_text)))
        return total, no_space
    
    #Here won't be special methods for calculating length of word, sentence or paragraph sequence
    #since it can be done with just len()
    
    #Counting punctuation marks
    def punc_marks(self, text):
        all_marks = re.findall(r'[.,!?;]{1,3}|(?<=\S):(?=\s\S)|(?<=\S\s)[-―](?=\s\S)', text)
        marks_count = {}
        for mark in set(all_marks):
            marks_count[mark] = all_marks.count(mark)
        return marks_count
    
    #Check if given text contains direct speech
    def is_dspeech(self, text):
        patterns = [r'\s?[-―]{,2}\s.+',
                   r'.+"[.,]?\s[-―]{,2}\s.+',
                   r'.+:\s".+',
                   r'".+\s[-―]{,2}\s.+[.,]\s[-―]{,2}\s.+"']
        for pattern in patterns:
            if re.fullmatch(pattern, text):
                return True
        return False
    
    #Find author's speech in paragraphs with direct speech
    def dspeech_author(self, text):
        patterns = [{'dspeech': r'\s?[-―]{,2}\s.+', 'author': r'\W\s[-―]{,2}\s.+?[,.](\Z|\s[-―])'},
                   {'dspeech': r'.+"[.,]?\s[-―]{,2}\s.+', 'author': r'"[.,]?\s[-―]{,2}\s.+'},
                   {'dspeech': r'.+:\s".+', 'author': r'.+:\s"'},
                   {'dspeech': r'".+\s[-―]{,2}\s.+[.,]\s[-―]{,2}\s.+"', 'author': r'[-―]{,2}\s.+[.,]\s[-―]{,2}'}]
        for pattern in patterns:
            if re.fullmatch(pattern['dspeech'], text) and re.search(pattern['author'], text):
                aspeech_raw = re.search(pattern['author'], text)[0]
                aspeech_clear = [item for item in re.split(r'\A\W+|\W+\Z', aspeech_raw) if item][0]
                return aspeech_clear
        return None
    
    #Calculate direct speech attribution ratio in given text
    def dspeech_attr_ratio(self, par):
        authors = self.dspeech_author(par)
        if authors:
            return len(authors) / len(par)
        else:
            return None
        
    #Calculate paragraphs with direct speech ratio in given text
    def dspeech_ratio(self, paragraphs):
        with_dspeech = 0
        for par in paragraphs:
            if self.is_dspeech(par):
                with_dspeech += 1
        if with_dspeech == 0:
            return 0
        else:
            return with_dspeech / len(paragraphs)

