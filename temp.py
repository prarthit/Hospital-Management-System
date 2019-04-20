class A():
	def hi(self, j):
		j.f = 5;

class C():
	def __init__(self):
		self.f = 1;
		
	def prin(self):
		print(self.f);

class B():
	def __init__(self):
		self.kk();
	
	def kk(self):
		p = C();
		s = A();
		s.hi(p);
		p.prin();

g = B()
