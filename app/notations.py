class Notations():
    def make(self, lang, *dicts):
        notations = {}
        for dictionary in dicts:
            chosen = self.__getattribute__(dictionary)
            notations.update(chosen[lang])
        return notations
    
    def translate_keys(self, lang, data_dict):
        old_keys = list(data_dict.keys())
        for key in old_keys:
            if key in self.data_keys.keys():
                data_dict[self.data_keys[key][lang]] = data_dict.pop(key)
        return data_dict
    
    def translate(self, lang, data):
        if isinstance(data, dict):
            data = self.translate_keys(lang, data)
            for key in data:
                data[key] = self.translate(lang, data[key])
        elif isinstance(data, str):
            if data in self.data_strings.keys():
                data = self.data_strings[data][lang]
        elif isinstance(data, list):
            for item in data:
                item = self.translate(lang, item)
        return data
    
    base = {'ENG': {'start': 'Start', 
            'past': 'Past text', 
            'count': 'Results', 
            'xlsx': 'Results in .xlsx', 
            'language': 'Сменить язык'}, 
        'RU': {'start': 'Старт', 
            'past': 'Вставить текст', 
            'count': 'Результаты', 
            'xlsx': 'Результаты в .xlsx', 
            'language': 'Switch language'}}
            
    index = {'ENG':{'title': 'Word counter', 
            'from_file': 'Or load file', 
            'load_file': 'Load text file', 
            'upload': 'Upload'}, 
        'RU': {'title': 'Счетчик слов', 
            'from_file': 'Или открыть из файла', 
            'load_file': 'Загрузить текстовый файл', 
            'upload': 'Загрузить'}}
            
    past = {'ENG': {'text_form': 'Past text from buffer', 
            'text_area': 'Past your text here.', 
            'analyze': 'Analyze'}, 
        'RU': {'text_form': 'Вставить текст из буфера', 
            'text_area': 'Вставьте текст сюда.', 
            'analyze': 'Анализировать'}}
    
    count = {'ENG':{'title': 'Analysis results', 
            'download': 'Download in .xlsx', 
            'general_data': 'General data', 
            'word_frequency': 'Word frequency', 
            'pos_frequency': 'POS frequency'}, 
        'RU': {'title': 'Результаты анализа', 
            'download': 'Скачать в формате .xlsx', 
            'general_data': 'Общие данные', 
            'word_frequency': 'Частотность слов', 
            'pos_frequency': 'Частотность частей речи'}}
    
    data_keys = {'total_symbols': {'RU': 'Количество символов',  'ENG': 'Number of symbols'}, 
        'without_spaces': {'RU': 'Количество символов без проблелов',  'ENG': 'Number of symbols without spaces'}, 
        'total': {'RU': 'Общее количество',  'ENG': 'Total number'}, 
        'shortest': {'RU': 'Наименьшая длина',  'ENG': 'Minimal length'}, 
        'longest': {'RU': 'Наибольшая длина',  'ENG': 'Maximal length'}, 
        'mean': {'RU': 'Средняя длина',  'ENG': 'Mean length'}, 
        'autosem': {'RU': 'Автосемантических слов',  'ENG': 'Number of autosemantic words'}, 
        'nonsem': {'RU': 'Синсемантических слов',  'ENG': 'Number of semisemantic words'}, 
        'waste_ratio': {'RU': 'Водность',  'ENG': 'Semisemantic words ratio'}, 
        'dspeech': {'RU': 'Абзацев с прямой речью',  'ENG': 'Number of paragraphs with direct speech'}, 
        'dsp_attr': {'RU': 'Доля авторской речи в прямой',  'ENG': 'Dialog attribution ratio'}, 
        'word': {'RU': 'Слово',  'ENG': 'Word'}, 
        'forms': {'RU': 'Формы слова',  'ENG': 'Word forms'}, 
        'POS': {'RU': 'Часть речи',  'ENG': 'Part of speech'}, 
        'semantic': {'RU': 'Семантическая роль',  'ENG': 'Semantic role'}, 
        'context': {'RU': 'Контекстные слова',  'ENG': 'Context words'}, 
        'ipm': {'RU': 'Частотность (ipm)',  'ENG': 'Frequency (ipm)'}, 
        'amount': {'RU': 'Количество',  'ENG': 'Amount'},
        'presence': {'RU': 'Предложений, содержащих',  'ENG': 'Sentences containing'}, 
        'ips': {'RU': 'Доля содержащих предложений',  'ENG': 'Ratio of sentences containing'}, 
        'symbols': {'RU': 'Символы',  'ENG': 'Symbols'}, 
        'paragraphs': {'RU': 'Абзацы',  'ENG': 'Paragraphs'}, 
        'sentences': {'RU': 'Предложения',  'ENG': 'Sentences'}, 
        'words': {'RU': 'Слова',  'ENG': 'Words'}, 
        'punctuation': {'RU': 'Знаки препинания',  'ENG': 'Punctuation'}}
    
    data_strings = {'Autosemantic': {'RU': 'Автосемантическое',  'ENG': 'Autosemantic'}, 
        'Semisemantic': {'RU': 'Синсемантическое',  'ENG': 'Semisemantic'}, 
        'NOUN': {'RU': 'Существительное', 'ENG': 'Noun'},
        'ADJF': {'RU': 'Прилагательное', 'ENG': 'Adjective'},
        'ADJS': {'RU': 'Краткое прилагательное', 'ENG': 'Adjective (short)'},
        'COMP': {'RU': 'Компаратив', 'ENG': 'Comparative'},
        'VERB': {'RU': 'Глагол', 'ENG': 'Verb'},
        'INFN': {'RU': 'Глагол (инфинитив)', 'ENG': 'Verb infinitive'},
        'PRTF': {'RU': 'Причастие', 'ENG': 'Participle'},
        'PRTS': {'RU': 'Краткое причастие', 'ENG': 'Participle short'},
        'GRND': {'RU': 'Деепричастие', 'ENG': 'Gerunds'},
        'NUMR': {'RU': 'Числительное', 'ENG': 'Numeral'},
        'ADVB': {'RU': 'Наречие', 'ENG': 'Adverb'},
        'NPRO': {'RU': 'Местоимение', 'ENG': 'Pronoun'},
        'PRED': {'RU': 'Предикатив', 'ENG': 'Predicative'},
        'PREP': {'RU': 'Предлог', 'ENG': 'Preposition'},
        'CONJ': {'RU': 'Союз', 'ENG': 'Conjunction'},
        'PRCL': {'RU': 'Частица', 'ENG': 'Particle'},
        'INTJ': {'RU': 'Междометие', 'ENG': 'Interjection'}, 
        'header': {'RU': 'Подсчет слов',  'ENG': 'Word count'}, 
        'info': {'RU': 'Небольшое веб-приложение для частотного анализа текста. Загрузка текста из файла пока возможна только для формата .txt.',
            'ENG': 'A small web-app for word frequency analysis. Loading text from file now supporting only .txt format.'}, 
        'good_file': {'RU': 'Файл загружен.',  'ENG': 'File loaded.'}, 
        'bad_file': {'RU': 'Нет файла, либо его формат не поддерживается.',  'ENG': 'No file or unsupported format.'}, 
        'no_text': {'RU': 'Нет текста для анализа.',  'ENG': 'No text provided.'}, 
        'big_download': {'RU': 'Файл с результатами слишком большой для скачки.',  'ENG': 'Result file is too big for download.'}
        }
