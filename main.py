import random
from nltk.corpus import wordnet
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

book_file = open('theonceandfutureking.txt', 'r')
heroic_words = open("heroicwords.txt", 'r')
common_words = open("commonwords.txt", 'r')
reading_log_file = open("readinglogs.txt", "w")

text = book_file.read()

heroic_text = heroic_words.read().split()
common_text = common_words.read().split()

book_file.close()
heroic_words.close()
common_words.close()

common_word_found = False
cleaned_book = []
chapter_count = 97
page_count = 677
pages_per_chapter = 7
chapter = 1
page = 1
adjs = ["great", "complex", "fascinating", "interesting", "engaging"]

def main(chapter, page, text, chapter_count, pages_per_chapter):
  print_or_export = input("Do you want to Print the reading logs, or Export them to txt?: ")
  generate_chapter_info(chapter, page, chapter_count, pages_per_chapter, print_or_export)

def generate_chapter_info(chapter, page, chapter_count, pages_per_chapter, print_or_export):
    words = generate_words()
    significant_statements = generate_significant_statements()
    reading_log_file.truncate(0)

    # Make reading log
    for i in range(1, chapter_count):
      locative_info = generate_locative_info(chapter, page, pages_per_chapter)
      word, definition = generate_word_def(words)
      connotation = find_sentence(word, split_book(keep_periods=True, return_string=False, keep_caps=False, keep_punctuation=False))
      vocab = generate_vocab(page, pages_per_chapter, word, definition)
      significant_statement, significant_word = random.choice(list(significant_statements.items()))
      rationale = generate_rationale(i%3, significant_word)
      main_idea, sentence1, sentence2 = cut_sentence(generate_main_idea(split_on_chapters(split_book(True, True, True, False))[i]))
      reflection = generate_reflection(i%4, sentence1, sentence2, adjs[i%4])
      
      out_reading_log(print_or_export, locative_info, vocab, connotation, significant_statement, rationale, main_idea, reflection, page, pages_per_chapter)
      
      chapter += 1
      page += pages_per_chapter
    reading_log_file.close()

def out_reading_log(print_or_export, locative_info, vocab, connotation, significant_statement, rationale, main_idea, reflection, page, pages_per_chapter):
  if print_or_export.lower() == "print":
    print(locative_info)
    print(vocab)
    print("Connotation: " + "\"" + connotation + "\"")
    print("Page " + str(random.randint(page, page+pages_per_chapter-1)) + ", Significant Statement: " + significant_statement)
    print("Rationale: " + rationale)
    print(main_idea)
    print("Reflection: " + reflection + "\n")
  if print_or_export.lower() == "export":
    print("Exporting...")
    reading_log_file.write(locative_info + "\n")
    reading_log_file.write(vocab + "\n")
    reading_log_file.write("Connotation: " + "\"" + connotation + "\"" + "\n")
    reading_log_file.write("Page " + str(random.randint(page, page+pages_per_chapter-1)) + ", Significant Statement: " + significant_statement + "\n")
    reading_log_file.write("Rationale: " + rationale + "\n")
    reading_log_file.write(main_idea + "\n")
    reading_log_file.write("Reflection: " + reflection + "\n" + "\n")

def cut_sentence(sentence):
  sentences = sentence.split(".")
  first_two_sentences = ". ".join(sentences[:2]) + "."
  return first_two_sentences, sentences[0][11:], sentences[1]

def generate_rationale(version, significant_word):
  versions = [f"This quote from the book is significant. They use the word {significant_word}. It shows the heroism in the statement.",
  f"I thought the use of the word {significant_word} showed the heroism in the actions. It definitely stands out as a powerful statement.", f"When the author uses the word {significant_word}, it shows heroism."]

  return versions[version]

def generate_reflection(version, sentence1, sentence2, adj):
  versions = [f"I thought that {sentence1} was an interesting part and made it a memorable chapter. {sentence2} was an intriguing moment.", f"I liked this chapter because of {sentence1}. I thought it was a really {adj} chapter.", f"I’m looking forward to seeing how this story turns out. It’s really engaging so far. I thought {sentence1} was a really interesting part.", f"I look forward to learning more about {sentence1}. This chapter set up a lot of stuff and it was great."]

  return versions[version]

def split_on_chapters(text):
  start = 0
  chapters = []
  
  while True:
    start = text.find("Chapter", start)
    if start == -1:
      break
    end = text.find("Chapter", start + 1)
    if end == -1:
      end = len(text)
    chapters.append(text[start:end])
    start = end

  return chapters

def generate_significant_statements():
  statements = {}
  for word in heroic_text:
    statement = find_sentence(word, split_book(keep_periods=True, return_string=False, keep_caps=True, keep_punctuation=False))
    if statement:
      statements[statement] = word
  return statements

def generate_main_idea(text):
  parser = PlaintextParser.from_string(text, Tokenizer("english"))
  summarizer = LexRankSummarizer()

  summary = summarizer(parser.document, 1)
  joined_summary = " ".join([str(sent) for sent in summary])

  return "Main Idea: " + joined_summary

def generate_locative_info(chapter, page, pages_per_chapter):
  return f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"

def generate_word_def(words):
  return random.choice(list(words.items()))

def generate_vocab(page, pages_per_chapter, word, definition):
  return f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"

def find_sentence(word, text):
  split_sentence_book = text
  for sentence in split_sentence_book:
    if word in sentence:
      end_char = sentence.find(word) + (len(word) - 1)
      return sentence[:end_char + 20]
  
def get_definition(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    return definition

def word_exists(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    if definition:
      return True
    else:
      return False

def split_book(keep_periods, return_string, keep_caps, keep_punctuation):
  text_to_clean = text
  if not keep_punctuation:
    text_to_clean = text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace("\n", "")
  if not keep_punctuation and not keep_periods:
    text_to_clean = text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace(".", "").replace("\n", "")
  if not keep_caps:
    text_to_clean = text_to_clean.lower()
  if return_string:
    return text_to_clean
  else:
    if keep_periods:
      return text_to_clean.split(".")
    else: 
      return text_to_clean.split()

def generate_words():
  words = {}

  unpunctuated_book = split_book(keep_periods=False, return_string=False, keep_caps=False, keep_punctuation=False)

  for word in unpunctuated_book:
      for common_word in common_text:
          if word != common_word:
            common_word_found = False
          if word == common_word or len(word) < 9:
            common_word_found = True
            break
      if common_word_found == False and word_exists(word):
        words[word] = get_definition(word)
        cleaned_book.append(word)
      common_word_found = False
  return words

if __name__ == "__main__":
    main(chapter, page, text, chapter_count, pages_per_chapter)

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()