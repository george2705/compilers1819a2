
import plex


# ... συμπληρώστε τον κώδικά σας για τον συντακτικό αναλυτή - αναγνωριστή της γλώσσας ...
class ParseError(Exception):
	pass

class MyParser:
	def __init__(self):
		space = plex.Any(" \n\t")
		string = plex.Str('"') + plex.Rep(plex.AnyBut('"')) + plex.Str('"')
		dong = plex.Str('!','?','(',')')
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		name = letter+plex.Rep(letter|digit)
		keyword = plex.Str('print','PRINT')
		space = plex.Any(" \n\t")
		operator=plex.Str('+','-','*','/','=')
		floater = plex.Rep(digit)+plex.Str('.')+plex.Rep1(digit)
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(floater,'FLOAT_TOKEN'),
			(keyword,'PRINT'),
			(string,'STRING_TOKEN'),
			(dong,plex.TEXT),
			(name,'IDENTIFIER'),
			(space,plex.IGNORE)
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("perimenw ! ? (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la=='IDENTIFIER' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("perimenw IDENTIFIER or Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("perimenw IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='FLOAT_TOKEN':	
			self.term()
			self.term_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or FLOAT or )")
	def term_tail(self):
		if self.la=='+' or self.la=='-':
			self.addop()
			self.term()
			self.term_tail()
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw + or -")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='FLOAT_TOKEN' or self.la==')':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or FLOAT or )")
	def factor_tail(self):
		if self.la=='*' or self.la=='/':
			self.multop()
			self.factor()
			self.factor_tail()
		elif self.la=='+' or self.la=='-' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw * or /")
	def factor(self):
		if self.la=='(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la=='FLOAT_TOKEN':
			self.match('FLOAT_TOKEN')
		else:
			raise ParseError("perimenw id float or (")
	def addop(self):
		if self.la=='+':
			self.match('+')
		elif self.la=='-':
			self.match('-')
		else:
			raise ParseError("perimenw + or -")
	def multop(self):
		if self.la=='*':
			self.match('*')
		elif self.la=='/':
			self.match('/')
		else:
			raise ParseError("perimenei * or /")

parser = MyParser()
with open('test.txt','r') as fp:
	parser.parse(fp)

