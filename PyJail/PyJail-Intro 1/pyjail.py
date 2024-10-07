import re

welcome="|Welcome to Echo Bot|"
desc="I have created a bot that echo whatever you said!"
logout="Bot is tired he needs to sleep. Good Bye!"

def seperator(x):
	num=len(x)
	sep=num * "+"
	return sep

def main():
	sep=seperator(welcome)
	print(sep+"\n"+welcome+"\n"+sep+"\n"+desc)
	for i in range(10):
		try:
			user_input=input("Echo >>")
			if re.match("^(_?[A-Za-z0-9])*[A-Za-z](_?[A-Za-z0-9])*$", user_input):
				print("Bot said "+user_input)
			else:
				print(eval(user_input))
		except:
			print('Unexpected Error has occured')

	sep=seperator(logout)
	print(sep+"\n"+logout+"\n"+sep)

if __name__=='__main__':
	main()