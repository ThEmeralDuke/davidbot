from subprocess import Popen, PIPE
print("Restart program active")
process = Popen(['swfdump', '/home/ubuntu/python/Bots/test/bot.py', '-d'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
exit()