from transformers import pipeline

text = "On Mondays, Wednesdays and Fridays it was Court Hand and Summulae Logicales, while the rest of the week it was the Organon, Repetition and Astrology. The governess was always getting muddled with her astrolabe, and when she got specially muddled she would take it out of the Wart by rapping his knuckles. She did not rap Kay's knuckles, because when Kay grew older he would be Sir Kay, the master of the estate. The Wart was called the Wart because it more or less rhymed with Art, which was short for his real name. Kay had given him the nickname. Kay was not called anything but Kay, as he was too dignified to have a nickname and would have flown into a passion if anybody had tried to give him one. The governess had red hair and some mysterious wound from which she derived a lot of prestige by showing it to all the women of the castle, behind closed doors. It was believed to be where she sat down, and to have been caused by sitting on some armor at a picnic by mistake. Eventually she offered to show it to Sir Ector, who was Kay's father, had hysterics and was sent away. They found out afterwards that she had been in a lunatic hospital for three years."

model = pipeline("summarization")
result = model(text, max_length=100, min_length=30)

print(result[0]['summary_text'])
