f = open('GalaxyThree.txt', 'r')
cw = open("commonwords.txt", 'r')
book = f.read().split()
common_words = cw.readlines()

for word in book:
    for common_word in common_words:
        if word == common_word:
            book.remove(word)
            print("word removed")

print(len(book))

f.close()