from translate import Translator
from langdetect import detect, DetectorFactory
import Data_Search
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')



def translate_en_to_ru(text):
    translator = Translator(from_lang='en', to_lang='ru')
    result = translator.translate(text)
    return result


def translate_text(feedbacks_list):
    DetectorFactory.seed = 0
    for i in feedbacks_list:
        if detect(i[1]) == "en":
            i[1] = translate_en_to_ru(i[1])
            i[2] = translate_en_to_ru(i[2])
    return feedbacks_list


def FeedBacks_Processing(URL):
    pattern = re.compile(r'\{.*?"averageScore":.*?}')
    matches = pattern.findall(Data_Search.get_Feedbacks(URL))
    data_list = []

    for match in matches:
        try:
            clean_match = match.replace('&quot;', '"').replace('\\n', '').replace('\\', '')

            data = json.loads(clean_match)
            average_score = data.get('averageScore', None)
            positive_text = data.get('positiveText', '')
            negative_text = data.get('negativeText', '')

            if average_score is not None:
                data_list.append([average_score, positive_text, negative_text])
        except json.JSONDecodeError:
            continue
    return data_list


def Preprocess_Text(text):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review
              if not word in set(stopwords.words('russian'))]
    review = ' '.join(review)

    return review


