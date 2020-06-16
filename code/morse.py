
class morsecode_V1:
    """ Version 1:
    Every word is divided by '\'
    Every letter is divided by ' '
    """
    def __init__(self):
        self.mtb = dict()
        self.rmtb = dict()
        self.mtb = {
        'A': '·-',
        'B': '-···',
        'C': '-·-·',
        'D': '-··',
        'E': '·',
        'F': '··-·',
        'G': '--·',
        'H': '····',
        'I': '··',
        'J': '·---',
        'K': '-·-',
        'L': '·-··',
        'M': '--',
        'N': '-·',
        'O': '---',
        'P': '·--·',
        'Q': '--·-',
        'R': '·-·',
        'S': '···',
        'T': '-',
        'U': '··-',
        'V': '···-',
        'W': '·--',
        'X': '-··-',
        'Y': '-·--',
        'Z': '--··',
        '1': '·----',
        '2': '··---',
        '3': '···--',
        '4': '····',
        '5': '·····',
        '6': '-····',
        '7': '--···',
        '8': '---··',
        '9': '----·',
        '0': '-----',
        '.': '·-·-·-',
        ':': '---···',
        ',': '--··--',
        ';': '-·-·-·',
        '?': '··--··',
        '=': '-···-',
        '\'': '·----·',
        '/': '-··-·',
        '!': '-·-·--',
        '-': '-····-',
        '_': '··--·-',
        '"': '·-··-·',
        '(': '-·--·',
        ')': '-·--·-',
        '$': '···-··-',
        '&': '·-···',
        '@': '·--·-·',
        '+': '·-·-·',
        }

        self.rmtb = {'·-': 'A',
        '-···': 'B',
        '-·-·': 'C',
        '-··': 'D',
        '·': 'E',
        '··-·': 'F',
        '--·': 'G',
        '····': 'H',
        '··': 'I',
        '·---': 'J',
        '-·-': 'K',
        '·-··': 'L',
        '--': 'M',
        '-·': 'N',
        '---': 'O',
        '·--·': 'P',
        '--·-': 'Q',
        '·-·': 'R',
        '···': 'S',
        '-': 'T',
        '··-': 'U',
        '···-': 'V',
        '·--': 'W',
        '-··-': 'X',
        '-·--': 'Y',
        '--··': 'Z',
        '·----': '1',
        '··---': '2',
        '···--': '3',
        '····-': '4',
        '·····': '5',
        '-····': '6',
        '--···': '7',
        '---··': '8',
        '----·': '9',
        '-----': '0',
        '·-·-·-': '.',
        '---···': ':',
        '--··--': ',',
        '-·-·-·': ';',
        '··--··': '?',
        '-···-': '=',
        '·----·': "'",
        '-··-·': '/',
        '-·-·--': '!',
        '-····-': '-',
        '··--·-': '_',
        '·-··-·': '"',
        '-·--·': '(',
        '-·--·-': ')',
        '···-··-': '$',
        '·-···': '&',
        '·--·-·': '@',
        '·-·-·': '+'
        }
        self.max_n = max(len(k) for k in self.rmtb)

    def encode(self, src_text):
        res = ''
        src_text = src_text.upper()
        for ch in src_text:
            res += self.mtb.get(ch, '\\') + ' '
        return res

    def decode(self, morse_text):
        res = ''
        for seg in morse_text.split():
            res += self.rmtb.get(seg, ' ') + ' '
        return res

    def test(self):
        print(self.encode('i love u!'))
        print(self.decode('·· \\ ·-·· --- ···- · \\ ··- -·-·--'))       
     
class morsecode_V2(morsecode_V1):
    """make my own dict with google-10000-english.txt
    Every word is divided by '\'
    """
    def __init__(self):
        morsecode_V1.__init__(self)
        self.word_dict = {}
        with open('google-10000-english.txt') as f:
            for word in f.read().split():
                self.word_dict[self.encode(word)] = word
    
    def encode(self, src_text):
        res = ''
        src_text = src_text.upper()
        for ch in src_text:
            res += self.mtb.get(ch, '\\')
        return res

    def decode(self, morse_text):
        res = ''
        for word in morse_text.split('\\'):
            if word in self.word_dict:
                res += self.word_dict[word] + ' '
        return res

    def test(self):
        print(self.encode('i love you'))
        print(self.decode('··\\·-··---···-·\\-·-----··-'))   


class morsecode_V3(morsecode_V2):
    """make my own dict with google-10000-english.txt
    There are no divided sign
    """
    def __init__(self):
        morsecode_V1.__init__(self)
        self.word_dict = {}
        with open('google-10000-english.txt') as f:
            for word in f.read().split()[:3000]:
                self.word_dict[self.encode(word)] = word
        self.max_len = max([len(k) for k in self.word_dict])
        self.min_len = min([len(k) for k in self.word_dict])

    def encode(self, src_text):
        res = ''
        src_text = src_text.upper()
        for ch in src_text:
            res += self.mtb.get(ch, '')
        return res

    def decode(self, morse_text):
        res = self.guess_morse(morse_text, '', 0, [], 0)
        result = []
        for item in res:
            result.append((len(item.split()), item))
        result = sorted(result)
        return result[:30]

    def guess_morse(self, seg, cur_morse, cur_start, res, depth):
        for end in range(cur_start + self.min_len, min(cur_start + self.max_len + 1, len(seg) + 1)):
            single_word = self.word_dict.get(seg[cur_start: end], None)
            if single_word:
                if end == len(seg):
                    res.append(cur_morse + ' ' + single_word)
                    break
                elif depth <= 7:
                    self.guess_morse(seg, cur_morse + ' ' + single_word, end, res, depth + 1)
        if cur_start == 0:
            return res

    def test(self):
        print(self.encode('i love you'))
        print(self.decode(self.encode('i love you')))
    
class morsecode_V4(morsecode_V3):
    def decode(self, morse_text):
        return self.guess_morse_reverse_max_len(morse_text)

    def guess_morse_reverse_max_len(self, morse_text):
        if morse_text == '':
            return ''
        else:
            for start in range( max( len(morse_text) - self.max_len, 0 ), len(morse_text)):
                single_word = self.word_dict.get(morse_text[start:], None)
                if single_word:
                    break
            return self.guess_morse_reverse_max_len(morse_text[:start]) + (' ' if morse_text[:start] else '') + single_word

    def test(self):
        print(self.decode(self.encode('i love you')))

mytest = morsecode_V4()
mytest.test()
