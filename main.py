import Data_Processing as DP
import Hotel_Estimation as HE
import Data_Search as DS
import requests


BASE_URL = "https://www.booking.com/hotel/[]/<>.ru.html"
URL = DS.get_URL(BASE_URL)
if (URL == -1) or requests.get(URL).status_code != 200:
    print ("Ошибка получения ссылки")

feedbacks_list = DP.FeedBacks_Processing(URL)
feedbacks_list = DP.translate_text(feedbacks_list)

if len(feedbacks_list) == 0:
    print("Не найдено отзывов об этом отеле")
    exit(0)
print(f"Средняя оценка гостей: {HE.Average_Count(feedbacks_list)}/10")
print(f"Оценка по длине: {HE.Average_Lencount(feedbacks_list)}/10")
print(f"Оценка по словам: {HE.Words_Estimation(feedbacks_list)}/10")
PRED, CM = HE.Model_Classifier(feedbacks_list)
print(f"Оценка модели-классификатора: {PRED.sum() / len(PRED)}")
