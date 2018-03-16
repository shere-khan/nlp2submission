import sys, sqlite3, re


def insert(cursor, table_name, column_name, value):
    cursor.execute('''insert into {tn} ({cn}) values ("{wv}")'''
                   .format(tn=table_name, cn=column_name, wv=value))

def insert_word(cursor, word, nextword, tag):
    cursor.execute('''insert into word (word_, tag_, next_word) values ("{wordval}", 
    "{tg}", "{nw}")'''.format(wordval=word, tg=tag, nw=nextword))

def insert_tag_and_prev(cursor, tag, prevtag):
    cursor.execute(
        '''insert into tag (tag_, prev_tag) values ("{tagval}", "{pt}")'''
            .format(tagval=tag, pt=prevtag))

def get_distinct_tags(cursor):
    cursor.execute('''SELECT DISTINCT tag_ FROM tag ORDER BY tag_'''.format())

    return cursor.fetchall()

def get_prob_for_tag(curs, tag):
    curs.execute('''select count(*) from tag where tag_ = "{t}"'''.format(t=tag))
    res = curs.fetchall()[0][0]
    tot = get_tag_total_count(curs)

    return res / tot

def get_tag_count(cursor, tag):
    cursor.execute('''select count(*) from tag where tag_ = "{t}"'''.format(t=tag))

    return cursor.fetchall()[0][0]

def get_tag_total_count(curs):
    curs.execute('''SELECT count(*) FROM tag''')

    return curs.fetchall()[0][0]

def get_distinct_tags_for_word(cursor, word):
    cursor.execute(
        '''select distinct tag_ from word where word_ = "{wd}"'''.format(wd=word))
    res = cursor.fetchall()

    return res

def get_transition_prob(cursor, tag, prevtag):
    cursor.execute('''select count(*) from tag where prev_tag = "{t}"'''.format(
        t=prevtag))
    tagcount = cursor.fetchall()

    cursor.execute('''SELECT count(*) FROM tag WHERE tag_ = "{t}" and prev_tag = "{pt}"'''
                   .format(t=tag, pt=prevtag))
    tag_combo_count = cursor.fetchall()

    return tag_combo_count[0][0] / tagcount[0][0]

def get_transition_prob2(cursor, tag, prevtag):
    cursor.execute('''select count(*) from tag where tag_ = "{pt}"'''.format(pt=prevtag))
    prevtagcount = cursor.fetchall()

    cursor.execute('''SELECT count(*) FROM tag WHERE tag_ = "{t}" and prev_tag = "{pt}"'''
                   .format(t=tag, pt=prevtag))
    tag_combo_count = cursor.fetchall()

    return tag_combo_count[0][0] / prevtagcount[0][0]

def get_word_likelihood(cursor, word, tag):
    res1 = get_count_word_and_tag(cursor, word, tag)
    res2 = get_tag_count(cursor, tag)

    return res1 / res2

def get_distinct_words(curs):
    curs.execute('''SELECT DISTINCT word_ FROM word ORDER BY word_ ASC''')

    return curs.fetchall()

def get_tag_initial_prob(cursor, tag):
    cursor.execute('''select count(*) from tag where prev_tag = "" and tag_ = "{t}"'''
                   .format(t=tag))

    return cursor.fetchall()[0][0]

def insert_sentence_total(curs, count):
    curs.execute('''insert into statistics (tot_sentences) values ({ct})'''
                 .format(ct=count))

def get_sentence_total(curs):
    curs.execute('''SELECT tot_sentences FROM statistics''')

    return curs.fetchall()[0][0]

def get_count_word_and_tag(curs, word, tag):
    curs.execute(
        '''select count(word_) from word where tag_ = "{tg}" and word_ = "{wd}"'''
            .format(tg=tag, wd=word))

    return curs.fetchall()[0][0]

def get_all_distinct_previous_tags_for_tag(curs, tag):
    curs.execute('''select distinct tag_ from tag where prev_tag = "{tg}"'''
                 .format(tg=tag))

    return curs.fetchall()

def get_all_distinct_tags_for_previous_tag(curs, prevtag):
    curs.execute('''select distinct tag_ from tag where prev_tag="{pt}" order by tag_ asc 
    '''.format(
        pt=prevtag))

    return curs.fetchall()

def is_word_in_corpus(curs, word):
    curs.execute('''select * from word where word_ = "{wd}"'''.format(wd=word))
    res = curs.fetchall()

    return False if not res else True

def update_word_set_next_word(curs, word, nextword):
    curs.execute('''update word set next_word = "{nw}" where word_ = "{wd}"'''.format(
        nw=nextword, wd=word))

def get_distinct_word_next_word_pairs(curs, word):
    curs.execute('''select distinct word_, next_word from word where word_ = "{wd}"'''
                 .format(wd=word));

    return curs.fetchall()

class Rules:
    def __init__(self):
        self.was_rule_applied = False

    def rule_sses(self, s):
        exp = r'(?<=[\w])sses$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_xes(self, s):
        exp = r'(?<=[\w])xes$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_ses(self, s):
        exp = r'(?<=[\w])ses$'
        match = re.search(exp, s)
        if match:
            s = s[:-1]
            self.was_rule_applied = True

        return s

    def rule_zes(self, s):
        exp = r'(?<=[\w])zes$'
        match = re.search(exp, s)
        if match:
            s = s[:-1]
            self.was_rule_applied = True

        return s

    def rule_ches(self, s):
        exp = r'(?<=[\w])ches$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_shes(self, s):
        exp = r'(?<=[\w])shes$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            self.was_rule_applied = True

        return s

    def rule_men(self, s):
        exp = r'(?<=[\w])men$'
        match = re.search(exp, s)
        if match:
            s = s[:-2]
            s += 'an'
            self.was_rule_applied = True

        return s

    def rule_ies(self, s):
        exp = r'(?<=[\w])ies$'
        match = re.search(exp, s)
        if match:
            s = s[:-3]
            s += 'y'
            self.was_rule_applied = True

        return s

    def lemmatize(self, s):
        s = self.rule_ches(s)
        if not self.was_rule_applied:
            s = self.rule_ies(s)
        if not self.was_rule_applied:
            s = self.rule_men(s)
        if not self.was_rule_applied:
            s = self.rule_sses(s)
        if not self.was_rule_applied:
            s = self.rule_ses(s)
        if not self.was_rule_applied:
            s = self.rule_shes(s)
        if not self.was_rule_applied:
            s = self.rule_xes(s)
        if not self.was_rule_applied:
            s = self.rule_zes(s)

        return s

def has_special_char(s):
    exp = r'[\W]'
    match = re.search(exp, s)

    return True if match else False

def parse_line(line):
    entry = line.split()
    word = entry[0].lower()
    r = Rules()
    word = r.lemmatize(word)

    tag = entry[1].split('\n')[0]

    return word, tag

class Stats:
    def __init__(self):
        self.sent_count = 0

def create(c):
    c.execute('''CREATE TABLE word (word_ TEXT, tag_ TEXT, count REAL, next_word TEXT)''')
    c.execute(
        '''CREATE TABLE tag (tag_ TEXT, prev_tag TEXT, next_tag TEXT, count REAL)''')
    c.execute('''CREATE TABLE statistics (tot_sentences REAL)''')

def delete(c):
    c.execute('''DROP TABLE word''')
    c.execute('''DROP TABLE tag''')
    c.execute('''DROP TABLE statistics''')

def createtables(curs):
    curs.execute('''PRAGMA table_info(statistics)''')
    res = curs.fetchall()
    if not res:
        curs.execute(
            '''CREATE TABLE statistics (tot_sentences REAL)''')
    else:
        curs.execute('''DROP TABLE statistics''')
        curs.execute(
            '''CREATE TABLE statistics (tot_sentences REAL)''')

    curs.execute('''PRAGMA table_info(word)''')
    res = curs.fetchall()
    if not res:
        curs.execute(
            '''CREATE TABLE word (word_ TEXT, tag_ TEXT, count REAL, next_word TEXT)''')
    else:
        curs.execute('''DROP TABLE word''')
        curs.execute(
            '''CREATE TABLE word (word_ TEXT, tag_ TEXT, count REAL, next_word TEXT)''')

    curs.execute('''PRAGMA table_info(tag)''')
    res = curs.fetchall()
    if not res:
        curs.execute(
            '''CREATE TABLE tag (tag_ TEXT, prev_tag TEXT, next_tag TEXT, count REAL)''')
    else:
        curs.execute('''DROP TABLE tag''')
        curs.execute(
            '''CREATE TABLE tag (tag_ TEXT, prev_tag TEXT, next_tag TEXT, count REAL)''')

class Vertex:
    __slots__ = 'element'

    def __init__(self, x):
        self.element = x

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return 'element: {0}'.format(self.element)

    def __repr__(self):
        return 'element: {0}'.format(self.element)

class Edge:
    __slots__ = 'origin', 'destination', 'element'

    def __init__(self, u, v, x):
        self.origin = u
        self.destination = v
        self.element = x

    def endpoints(self):
        return self.origin, self.destination

    def opposite(self, v):
        return self.destination if v is self.origin else self.origin

    def __hash__(self):
        return hash((self.origin, self.destination))

class Graph:
    def __init__(self, directed=False):
        self.outgoing = {}
        self.incoming = {} if directed else self.outgoing

    def is_directed(self):
        return self.incoming is not self.outgoing

    def vertex_count(self):
        return len(self.outgoing)

    def vertices(self):
        return self.outgoing.keys()

    def edge_count(self):
        total = sum(len(self.outgoing[v]) for v in self.outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondary_map in self.outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        return self.outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        adj = self.outgoing if outgoing else self.incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        adj = self.outgoing if outgoing else self.incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        v = Vertex(x)
        self.outgoing[v] = {}
        if self.is_directed():
            self.incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        e = Edge(u, v, x)
        self.outgoing[u][v] = e
        self.incoming[v][u] = e

class WordVertex:
    def __init__(self, word, tag, likelihood):
        self.word = word
        self.tag = tag
        self.likelihood = likelihood
        self.best_prob_so_far = self.likelihood
        self.best_prev = None
        self.prev = None

    def __repr__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag,
                                                           self.likelihood)

    def __str__(self):
        return 'word: {0} tag: {1} likelihood: {2}'.format(self.word, self.tag,
                                                           self.likelihood)

def initializegraph(cursor, sent, exec_columns):
    g = Graph(directed=True)
    start = g.insert_vertex(WordVertex(word="", tag="", likelihood=1))
    prevnodes = [start]

    for w in sent:
        nextnodes = list()

        isword = is_word_in_corpus(curs, w)
        if isword:
            wtags = get_distinct_tags_for_word(cursor, w)
        else:
            wtags = [('NN',)]

        for wtag in wtags:
            wtag = wtag[0]
            if isword:
                likelihood = get_word_likelihood(cursor, w, wtag)
            else:
                likelihood = 1
            v = g.insert_vertex(WordVertex(w, wtag, likelihood))
            nextnodes.append(v)

            for u in prevnodes:
                transprob = get_transition_prob(cursor, wtag, u.element.tag)
                g.insert_edge(u, v, transprob)

        exec_columns.append(nextnodes)
        prevnodes = nextnodes

    return g

def find_tagging(sentence):
    exec_columns = list()
    g = initializegraph(curs, sentence, exec_columns)
    print('Intermediate Values:', end='\n\n')
    viterbi(g, sentence, exec_columns)
    print_best_path(exec_columns)

def print_emission_probs(curs):
    words = get_distinct_words(curs)
    for w in words:
        w = w[0]
        tags = get_distinct_tags_for_word(curs, w)
        for t in tags:
            t = t[0]
            like = get_word_likelihood(curs, w, t)
            print('{:>23}'.format(w), end=' ')
            print('{:>4}'.format(t), end=' ')
            print('{:<.6f}'.format(like), end='\n')
    print()

def print_tags_observed(curs):
    tags = get_distinct_tags(curs)

    print('All tags observed:')
    for i, tag in enumerate(tags):
        print("{0} {1}".format(i, tag[0]))
    print()

def print_tag_dist(curs):
    tags = get_distinct_tags(curs)

    print('Initial Distributions', end='\n\n')
    for tag in tags:
        totsent = get_sentence_total(curs)
        initct = get_tag_initial_prob(curs, tag[0])
        p = initct / totsent
        print('{0} {1:.5f}'.format(tag[0], p))
    print()

def print_best_path(exec_column):
    best = max(exec_column[-1], key=lambda x: x.element.best_prob_so_far)

    print()
    print('Viterbi Tagger Output', end='\n\n')
    printlist = list()
    while best.element.prev:
        printlist.append((best.element.word, best.element.tag))
        best = best.element.prev

    for item in reversed(printlist):
        print('{0} tag: {1}'.format(item[0], item[1]))

def print_transition_probs(curs):
    print('Transition Probabilities:', end='\n\n')
    prevtags = get_distinct_tags(curs)
    for pt in prevtags:
        pt = pt[0]
        resultlist = list()
        tags = get_all_distinct_tags_for_previous_tag(curs, pt)

        totprob = 0
        for t in tags:
            t = t[0]
            prob = get_transition_prob2(curs, t, pt)
            resultlist.append(((t, pt), prob))
            totprob += prob

        print('[{:.6f}]'.format(totprob), end='   ')
        # print('{:<.6f}'.format(like), end='\n')
        for res in resultlist:
            tags = res[0]
            t = tags[0]
            pt = tags[1]
            prob = res[1]
            print('[{0} | {1}] {2:.6f}'.format(t, pt, prob), end=' ')
        print()
    print()

def print_tag_count(curs):
    tags = get_distinct_tags(curs)
    print('Total # tags: {0}'.format(len(tags)))

def print_lexicals(curs):
    words = get_distinct_words(curs)
    print('Total # lexicals: {0}'.format(len(words)))

def print_num_sentences(curs):
    numsent = get_sentence_total(curs)
    print('Total # sentences : {0}'.format(numsent), end='\n\n')

def print_tokens_found_in_corpus(curs, words):
    print('Tokens Found In Corpus:', end='\n\n')
    for i, w in enumerate(words):

        isword = is_word_in_corpus(curs, w)
        if isword:
            tags = get_distinct_tags_for_word(curs, w)
            # print('Iteration {ct}:'.format(ct=i), end='   ')
            print('{0} : '.format(w), end=' ')
            for t in tags:
                t = t[0]
                like = get_word_likelihood(curs, w, t)
                print('{0} ({1:.6f})'.format(t, like), end=' ')
            print()

def print_bigrams(curs):
    words = get_distinct_words(curs)
    tot_bigrams = 0
    for w in words:
        w = w[0]
        bigrams = get_distinct_word_next_word_pairs(curs, w)
        if bigrams:
            tot_bigrams += len(bigrams)

    print('Total # bigrams : {0}'.format(tot_bigrams))

def viterbi(g, sent, exec_columns):
    class Path:
        def __init__(self, edge, prob):
            self.edge = edge
            self.prob = prob

    for word, col in zip(sent, exec_columns):
        print('{0} : '.format(word), end=' ')
        resultlist = list()
        for v in col:
            edges_in = g.incident_edges(v, outgoing=False)
            probs = list()

            # select best transition probability out of all incoming edges to v
            # and stores best path (prev) and prob (maxprob) in v
            for e in edges_in:
                prev = e.opposite(v)
                possible_best = prev.element.best_prob_so_far * e.element \
                                * v.element.likelihood
                probs.append(Path(e, possible_best))

            best_path = max(probs, key=lambda x: x.prob)
            v.element.best_prob_so_far = best_path.prob
            v.element.prev = best_path.edge.opposite(v)

            resultlist.append(((best_path.edge.origin.element.tag, v.element.tag),
                               best_path.prob))
        totprob = 0
        for res in resultlist:
            prob = res[1]
            totprob += prob

        for res in resultlist:
            edges = res[0]
            prob = res[1]
            prev = edges[0]
            cur = edges[1]
            print('{0} ({1:.6f}, {2})'.format(cur, prob / totprob, prev), end=' ')
            sys.stdout.flush()

        print()


def readdata():
    file_name = sys.argv[1]
    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()

    createtables(curs)

    sent_count = 0
    with open(file_name, 'r') as f:
        lines = f.readlines()

        for i in range(0, len(lines)):
            line = lines[i]

            if i >= 1:
                prevline = lines[i - 1]
                if line != '\n':
                    word, tag = parse_line(line)
                    # queries.insert_word(curs, word, tag)

                    prevtag = ""

                    if prevline != '\n':
                        prev = parse_line(prevline)
                        prevtag = prev[1]

                    insert_tag_and_prev(curs, tag, prevtag)

                    nextword = ""
                    if i < len(lines):
                        nextline = lines[i + 1]
                        if nextline != '\n':
                            nextword, nexttag = parse_line(nextline)

                    insert_word(curs, word, nextword, tag)

                else:
                    sent_count += 1
            else:
                if line != '\n':
                    word, tag = parse_line(line)
                    nextword = ""
                    if i < len(lines):
                        nextline = lines[i + 1]
                        if nextline != '\n':
                            nextword, nexttag = parse_line(nextline)
                    insert_word(curs, word, nextword, tag)
                    insert_tag_and_prev(curs, tag, "")

    insert_sentence_total(curs, sent_count)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print('University of Central Florida')
    print('CAP6640 String 2018 - Dr. Glinos')
    print()
    print('Viterbi Algorithm HMM Tagger by Justin Barry', end='\n\n')

    readdata()
    test_file = sys.argv[2]
    emissions_flag = sys.argv[3]

    conn = sqlite3.connect('corpus.db')
    curs = conn.cursor()

    print_tags_observed(curs)
    print_tag_dist(curs)
    if emissions_flag == 'True':
        print_emission_probs(curs)
    print_transition_probs(curs)
    print('Corpus Features: ', end='\n\n')
    print_tag_count(curs)
    print_lexicals(curs)
    print_num_sentences(curs)

    with open(test_file) as f:
        for line in f:
            print()

            line = line.lower()
            sent = line.split()
            print_tokens_found_in_corpus(curs, sent)
            print()

            find_tagging(sent)
