import exceptions
import random
class Algorithm:
	
	def __init__(self, N):
		# Here paste your initializing code
		self.l = [];
		
		for i in range(N):
			self.l.append(i)
			
		random.shuffle(self.l);
		
	def Execute(self):
		# Here paste your algorithm's code instead exception
		raise exceptions.NotImplementedException()
		
		''' Example 1 '''
		'''
		sorted = False  # We haven't started sorting yet

		while not sorted:
			sorted = True  # Assume the list is now sorted
			for element in range(0, len(self.l)-1):
				if self.l[element] > self.l[element + 1]:
					sorted = False  # We found two elements in the wrong order
					hold = self.l[element + 1]
					self.l[element + 1] = self.l[element]
					self.l[element] = hold
					
		'''
		
		''' Example 2 '''
		'''
		l.sort()
		'''
		
	def Clean(self):
		# Here paste your cleaning code, if needed
		pass