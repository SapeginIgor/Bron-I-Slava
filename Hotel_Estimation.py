from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import Data_Processing as DP




bad_words = ["Грязн", "шумн", "устаревш", "неустойчив", "переполнен", "невежлив", "неухожен", "скучн", "темн", "протекающ", "заплесневел", "неудобн", "плох", "утомительн", "дорог", "опасн", "мерзк", "устал", "неприемлем", "необслуживаем", "холодн", "неудовлетворительн", "тесн", "неаккуратн", "затхл", "неприятн", "убог", "ненадежн", "неперсонализированн", "пыльн", "неприветлив", "хлипк", "непрофессиональн", "ужасн", "отталкивающ", "неподходящ", "непривлекательн", "непостоян", "тосклив", "негостеприимн", "мрачны", "сомнител", "неухоженн", "потерян", "нагл", "неинтересн", "бесполезн", "вредн"]
good_words = ["Роскошн", "Уютн", "Современ", "Изыскан", "Прекрасн", "Романтичн", "Элегантн", "Атмосферн", "Удобн", "Безупречн", "Чист", "Просторн", "Стройн", "Светл", "Дружелюб", "Стильн", "Лаконич", "Комфорт", "Прият", "Нежн", "Утончен", "Отличн", "Модн", "Изящн", "Интимн", "Аккуратн", "Благоустроен", "Блестящ", "Цветаст", "Бесподоб", "Гармонич", "Умиротворен", "Манящ", "Безмятеж", "Натуральн", "Радостн", "Пленительн", "Ненавязчив", "Цельн", "Опрят", "Уравновешен", "Сказочн", "Богат", "Восхитительн", "Пикантн", "Строг", "Благородн", "Щедр", "Фешенебельн", "Мил"]


def Average_Count(feedbacks_list):
    s = 0
    for i in range(len(feedbacks_list)):
        s += feedbacks_list[i][0]

    return round(s / len(feedbacks_list), 2)


def Average_Lencount(feedbacks_list):
    s = 0.0
    for i in range(len(feedbacks_list)):
        s += len(feedbacks_list[i][1]) / (len(feedbacks_list[i][1]) + len(feedbacks_list[i][2]))
    return round(s * 10 / len(feedbacks_list), 2)


def Words_Estimation(feedback_list):
    good_count = 0
    for i in range(len(feedback_list)):
        for word in good_words:
            if word in feedback_list[i][1]:
                good_count += 1
    bad_count = 0
    for i in range(len(feedback_list)):
        for word in bad_words:
            if word in feedback_list[i][2]:
                bad_count += 1
    if good_count + bad_count == 0:
        return -1
    return round(10 * good_count / (good_count + bad_count), 2)


def Model_Classifier(feedbacks_list):
    reviews = []
    ratings = []
    for i in range(len(feedbacks_list)):
        reviews.append(feedbacks_list[i][1] + " " + feedbacks_list[i][2])
        ratings.append(feedbacks_list[i][0])

    for i in range(len(reviews)):
        reviews[i] = DP.Preprocess_Text(reviews[i])
    for i in reviews:
        if i == [" "]:
            reviews.remove(i)
    cv = CountVectorizer(max_features=5000)
    reviews = cv.fit_transform(reviews).toarray()
    X_train, X_test, Y_train, Y_test = train_test_split(reviews, ratings, test_size=0.25)
    model = RandomForestClassifier(n_estimators=1000, criterion='entropy')

    model.fit(X_train, Y_train)
    PRED = model.predict(X_test)
    CM = confusion_matrix(Y_test, PRED)
    return PRED, CM