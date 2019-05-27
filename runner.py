
import plex


# ... συμπληρώστε τον κώδικά σας για τον συντακτικό αναλυτή - διερμηνευτή της γλώσσας ...
class ParseError(Exception):
	pass

class ParseRun(Exception):
	pass

class MyParser:
	def __init__(self):
		space = plex.Any(" \n\t")
		par = plex.Str('(',')')
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		name = letter+plex.Rep(letter|digit)
		bit = plex.Range('01')
		bits = plex.Rep1(bit)
		keyword = plex.Str('print','PRINT')
		space = plex.Any(" \n\t")
		operator=plex.Str('^','&','|','=')
		self.st = {}
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(bits,'BIT_TOKEN'),
			(keyword,'PRINT'),
			(par,plex.TEXT),
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
			raise ParseError("perimenw (")

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
			varname= self.text
			self.match('IDENTIFIER')
			self.match('=')
			e=self.expr()
			self.st[varname]= e
		elif self.la=='PRINT':
			self.match('PRINT')
			e=self.expr()
			print(e)
		else:
			raise ParseError("perimenw IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='FLOAT_TOKEN':	
			f=self.term()
			t=self.term_tail()
			if t is None:
				return f
			if t[0]=='+':
				return f+t[1]
			return f-t[1]
		else:
			raise ParseError("perimenw ( or IDENTIFIER or FLOAT or )")
	def term_tail(self):
		if self.la=='+' or self.la=='-':
			op=self.addop()
			f=self.term()
			t=self.term_tail()
			if t is None:
				return op,f
			if t[0]=='+':
				return op,f+t[1]
			return op,f-t[1]
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw + or -")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='FLOAT_TOKEN' or self.la==')':	
			f=self.factor()
			t=self.factor_tail()
			if t is None:
				return f
			if t[0]=='*':
				return f*t[1]
			return f/t[1]
		else:
			raise ParseError("perimenw ( or IDENTIFIER or FLOAT or )")
	def factor_tail(self):
		if self.la=='*' or self.la=='/':
			op=self.multop()
			f=self.factor()
			t=self.factor_tail()
			if t is None:
				return op,f
			if t[0]=='*':
				return op,f*t[1]
			return op,f/t[1]
		elif self.la=='+' or self.la=='-' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw * or /")
	def factor(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
			raise ParseRun("perimenw id poy exei arxikopoih8h")
		elif self.la=='FLOAT_TOKEN':
			value=float(self.text)
			self.match('FLOAT_TOKEN')
			return value
		else:
			raise ParseError("perimenw id float or (")
	def addop(self):
		if self.la=='+':
			self.match('+')
			return('+')
		elif self.la=='-':
			self.match('-')
			return('-')
		else:
			raise ParseError("perimenw + or -")
	def multop(self):
		if self.la=='*':
			self.match('*')
			return('*')
		elif self.la=='/':
			self.match('/')
			return('/')
		else:
			raise ParseError("perimenei * or /")

parser = MyParser()
with open('test.txt','r') as fp:
	parser.parse(fp)

