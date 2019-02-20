import threading


class Thread(threading.Thread):
	def __init__(self,i):
		self.i = i
		

	def start(self):
		print(self.i)


def function(i):
	print(i)




threads = [Thread(i) for i in range(10)]

for thread in threads:
	thread.start()


