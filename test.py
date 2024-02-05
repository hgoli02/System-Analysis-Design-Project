#open DB/queue.txt

file = open('./DB/queue.txt', 'r')
file.seek(3)
print(file.read())