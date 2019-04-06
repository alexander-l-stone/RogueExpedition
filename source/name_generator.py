import random

######### Unused simplistic generator begins #########
consonants = [
    'b',
    'd',
    'f',
    'g',
    'h',
    'k',
    'l',
    'm',
    'n',
    'p',
    'r',
    's',
    't',
    'v',
    'z',
    "'",
]

vowels = [
    'a',
    'e',
    'i',
    'o',
    'u',
    'y',
]

def generateSyllable():
    syl = ''
    # onset
    syl += consonants[random.randrange(0,len(consonants))]
    # nucleus (no syllabic consonants for now)
    syl += vowels[random.randrange(0,len(vowels))]
    #possible dipthong
    if(random.random() < 0.2):
        syl += vowels[random.randrange(0,len(vowels))]
    #coda
    if(random.random() < 0.5):
        syl += consonants[random.randrange(0,len(consonants))]
    return syl

def generateWord():
    word = ''
    syl_count = random.randrange(1,3) + random.randrange(2) + random.randrange(2) + random.randrange(2)
    for _ in range(0, syl_count):
        word += generateSyllable()
    return word

######### Unused simplistic generator ends #########

#manner, place, voice
consonantTable = {
    'approximant' : {
        'alveolar' : {
            '+' : 'l'
        },
        'post-alveolar' : {
            '+' : 'r'
        },
        'palatal' : {
            '+' : 'y'
        }
    },
    'fricative' : {
        'labiodental' : {
            '+' : 'v',
            '-' : 'f'
        },
        'alveolar' : {
            '+' : 'z',
            '-' : 's'
        }
    },
    'plosive' : {
        'labial' : {
            '+' : 'b',
            '-' : 'p'
        },
        'alveolar' : {
            '+' : 'd',
            '-' : 't'
        },
        'post-alveolar' : {
#            '+' : 'dj',
            '-' : 'sh'
        },
        'velar' : {
            '+' : 'g',
            '-' : 'k'
        },
        'glottal' : {
            '-' : "'"
        }
    },
    'nasal' : {
        'labial' : {
            '+' : 'm'
        },
        'alveolar' : {
            '+' : 'n'
        }
    },
}

vowelTable = {
    'front' : {
        'high' : 'i',
        'mid' : 'e'
    },
    'mid' : {
        'low' : 'a'
    },
    'back' : {
        'high' : 'u',
        'mid' : 'o'
    }
}

def generatePhoneticConsonant():
    con = {}
    con['consonant'] = True
    con['vowel'] = False
    con['manner'] = random.choice(list(consonantTable.keys()))
    con['place'] = random.choice(list(consonantTable[con['manner']].keys()))
    con['voice'] = random.choice(list(consonantTable[con['manner']][con['place']].keys()))

    return con

def generatePhoneticVowel():
    vow = {}
    vow['consonant'] = False
    vow['vowel'] = True
    vow['backness'] = random.choice(list(vowelTable.keys()))
    vow['height'] = random.choice(list(vowelTable[vow['backness']].keys()))

    return vow

def generatePhoneticSyllable():
    syl = []

    # onset
    syl.append(generatePhoneticConsonant())
    if random.random() < 0.35:
        syl.append(generatePhoneticConsonant())
    # nucleus (no syllabic consonants for now)
    syl.append(generatePhoneticVowel())
    if random.random() < 0.2:
        syl.append(generatePhoneticVowel())
    #coda
    if random.random() < 0.35:
        syl.append(generatePhoneticConsonant())
        if random.random() < 0.2:
            syl.append(generatePhoneticConsonant())

    return syl

def generatePhoneticWord(rules):
    word = []
    syl_count = random.randrange(1,3) + random.randrange(2) + random.randrange(2) + random.randrange(2)
    for _ in range(0, syl_count):
        word.extend(generatePhoneticSyllable())

    last = len(word) - 1
    #print("last = " + str(last))
    #print("word = " + str(word))
    #print("\n")
    i = 0
    while i < last:
        #pre = {}
        #offset = 1
        #while pre == {}:
        #    pre = word[i - 1] if i >= offset else '#'
        #    offset += 1

        pre = word[i - 1] if i <= 0 else '#'
        target = word[i]
        post = word[i + 1] if i < last else '#' 

        restart = False
        for rule in rules:
            word[i] = rule.apply(pre, target, post)
            if word[i] == {}:
                del word[i]
                last -= 1
                break
            #print('new value = ' + str(word[i]))
            #print("")
        if restart:
            continue
        i += 1

    #print("processed word = " + str(word))

    string = ''
    for char in word:
        string += translatePhoneme(char)

    return string

def translatePhoneme(p):
    #print('translating phoneme = ' + str(p))
    if p.get('consonant', False):
            tc = consonantTable.get(p['manner'], {}).get(p['place'], {}).get(p['voice'], '')
            #print("appending char = " + str(tc))
            return tc
    if p.get('vowel', False):
        tv = vowelTable.get(p['backness'], {}).get(p['height'], '')
        #print("appending char = " + str(tv))
        return tv
    print('ERROR: Phoneme parse failed')
    return ''

class PhoneticRule:
    def __init__(self, pre, target, post, changes):
        self.pre = pre
        self.target = target
        self.post = post
        self.changes = changes

    def __repr__(self):
        return 'pre = ' + str(self.pre) + ' target = ' + str(self.target) + ' post = ' + str(self.post) + ' changes = ' + str(self.changes)

    def apply(self, pre, target, post):
        #print("applying rule\t" + str(self) + "\nto arguments\tpre = " + str(pre) + " target = " + str(target) + " post = " + str(post))

        if self.pre != '*':
            if pre == '#':
                if self.pre != '#':
                    return target
            elif self.pre == '#':
                return target
            else:
                for k,v in self.pre.items():
                    if pre.get(k) != v:
                        return target

        if self.target != '*':
            for k,v in self.target.items():
                #print('comparing (k,v) = (' + str(k) + ',' + str(v) + ") to target.get(k) = " + str(target.get(k)))
                if target.get(k) != v:
                    return target

       # print('matched')

        if self.post != '*':
            if post == '#':
                if self.post != '#':
                    return target
            elif self.post == '#':
                return target
            else:
                for k,v in self.post.items():
                    if post.get(k) != v:
                        return target
        
        if self.changes == '':
            return {}
        
        target.update(self.changes)
        return target

defaultRules = {
    # limit consonant cluster size
    PhoneticRule({'consonant' : True}, {'consonant' : True}, {'consonant' : True}, ''),
    # consonant clusters much match voicing
    # TODO fix so that there is no coda/onset bleed
    PhoneticRule({'voice' : '+'}, {'voice' : '-'}, '*', ''),
    PhoneticRule({'voice' : '-'}, {'voice' : '+'}, '*', ''),
    # prevent lr cluster
    PhoneticRule({'manner' : 'approximant', 'place' : 'alveolar'}, {'manner' : 'approximant', 'place' : 'post-alveolar'}, '*', ''),
    # prevent coda nasal cluster
    PhoneticRule({'manner' : 'nasal'}, {'consonant' : True}, {'vowel' : True}, ''),
    PhoneticRule({'consonant' : True}, {'manner' : 'nasal'}, {'vowel' : True}, ''),
    # no clusters with glottal stops
    PhoneticRule({'manner' : 'plosive', 'place' : 'glottal'}, {'consonant' : True}, '*', ''),
    PhoneticRule({'consonant' : True}, {'manner' : 'plosive', 'place' : 'glottal'}, '*', ''),
    # no word initial or final glottals
    PhoneticRule('#', {'manner' : 'plosive', 'place' : 'glottal'}, '*', ''),
    PhoneticRule('*', {'manner' : 'plosive', 'place' : 'glottal'}, '#', ''),
}

# TEST BLOCK bc idk how to write real python tests

#seen = {}
#for i in range(0,100):
    #val = random.randrange(1,3) + random.randrange(2) + random.randrange(2) + random.randrange(2)
    #seen.update({val : seen.get(val, 0) + 1})
#    print(generatePhoneticWord(defaultRules))
    #print(generateWord())
#print(str(seen))

#p = PhoneticRule({'consonant' : True}, {'manner' : 'nasal'}, {'vowel' : True}, '').apply({'consonant': True, 'manner' : 'nasal'},
#    {'consonant' : True, 'manner' : 'nasal', 'place' : 'labial', 'voice' : 'voiced'}, {'vowel' : True})

#p['consonant'] = True
#print(str(p))
#print(translatePhoneme(p))
