("Hello, humanities!")
2+2
2 + 2
name = "humanities"
print(name.upper())
help(len) #built-in help
message = "Welcome to the humanities!"
print(message)
name = "Ada" 
if name == "Ada":
# print a greeting only if the name matches "Ada"
    print("Hello, Ada!")
    print("Welcome to Coding the Humanities.")
    year = 2026
    title = "Coding the Humanities"
    is_class_today = True
print(type(year)) #<class 'int'>
print(type(title)) #<class 'str'>
print(type(is_class_today)) #<class 'bool'>
#Stretch make title uppercase
print(title.upper())
tokens = 123
documents = 10
avg_tokens = tokens / documents
leftover = tokens % documents
print("Average:", avg_tokens)
print("Leftover:", leftover)
text = "Coding the Humanities"
first_word = text [0:6]
last_10_chars = text [-10:]
print(first_word)
print(last_10_chars)
line = " Hello, Humanities! "
clean = line.strip() #remove surrounding spaces
clean = clean.lower() #convert to lowercase
clean = clean.replace("!", " ") #remoce exclamation mark

tokens = clean. split() #split into tokens
print(clean)
print(tokens)

author = "Austen"
tokens = 12345
docs = 12
avg_tokens = tokens / docs

line= f"{author} corpus: {docs} documnents, {round(avg, 1)} tokens on average." #f-string with variables and rounding
print(line) #Austen has an average of 1028.75 tokens per document.