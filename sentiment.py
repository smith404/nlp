import pandas as pd

def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
    return final

df = pd.read_csv('temp/Reviews.csv')
print(df.head(8))