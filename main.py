f = open('theonceandfutureking.txt', 'r')
cw = open("commonwords.txt", 'r')
book = f.read().split()
common_words = cw.read().split()
common_word_found = False

cleaned_book = []

for word in book:
    for common_word in common_words:
        if word != common_word:
          common_word_found = False
        if word == common_word:
          common_word_found = True
    if common_word_found == False:
      cleaned_book.append(word)
    common_word_found = False


print(len(book))
print(len(cleaned_book))

f.close()