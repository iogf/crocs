"""
"""

from crocs.yacc import Lexer, Yacc, LexMap, LexNode, Rule, Grammar, TokVal
from crocs.token import Token

class Blank(Token):
    pass

class WordTokens:
    lexmap  = LexMap()
    LexNode(lexmap, r'[a-zA-Z]+', type=Token)
    LexNode(lexmap, r' +', type=Blank)

class WordGrammar:
    grammar  = Grammar()
    r_phrase = Rule(grammar, TokVal('alpha'), Blank, TokVal('beta'))

class WordParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(WordTokens.lexmap)
        super(WordParser, self).__init__(WordGrammar.grammar)
    
        self.add_handle(WordGrammar.r_phrase, self.handle_phrase)

    def run(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        ptree  = self.build(tokens)
        return ptree

    def handle_phrase(self, ptree):
        pass

data = 'alpha beta gamma zeta'
parse = WordParser()
ptree = parse.run(data)
print(list(ptree))
