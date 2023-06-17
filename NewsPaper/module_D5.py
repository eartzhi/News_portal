from news.models import *

# пишем статьи
NEWS1_HEADER ='Дефицит бюджета'
NEWS1_TEXT = 'Дефицит бюджета РФ достиг максимальных показателей: он уже больше,' \
             ' чем дефицит за весь прошлый год'

NEWS2_HEADER = 'Долги россиян'
NEWS2_TEXT = 'Россияне задолжали по кредитам 2 трлн рублей. «Проблема не то что' \
             ' актуальна, она суперкрайне актуальна», — заявил директор' \
             ' Федеральной службы судебных приставов. Сейчас у ведомства' \
             ' в работе 12 млн документов с просрочками по оплате.'

ARTICLE1_HEADER = 'Информационная служба Хабра посетила первый день ' \
                  'конференция «Тема Еды»'
ARTICLE1_TEXT = 'На конференции выступал руководитель аналитики «Яндекс Еды» ' \
                'и Delivery Club Роман Халкечев. В своём докладе он рассказал,' \
                ' как локдаун ускорил развитие доставки готовой еды и продуктов,' \
                ' что снятия ограничений не уменьшило популярность доставки. ' \
                'По словам Халчкевича, количество заказов из ресторанов в ' \
                '«Яндекс Еде» среди пользователей из Москвы с 2019 выросло в ' \
                '2,5, Санкт‑Петербурга — в 5,5 раз. Остальные регионы по ' \
                'доставке из ресторанов растут с того же периода значительно ' \
                'больше — в 16 раз. Больше половины заказов готовой еды в ' \
                '«Яндекс Еде» приходятся на регионы, в 2019 году этот показатель' \
                ' составлял 20%. По данным компании, треть жителей Москвы, ' \
                'Санкт‑Петербурга и Казани хотя бы раз заказывал еду из ' \
                'ресторанов с доставкой в прошлом году. Сейчас в сервисах ' \
                '«Яндекс Еда» и Delivery Clu используются технологии машинного ' \
                'обучения. С их помощью популярные сочетания позиций и на ' \
                'стадии оформления заказа предлагают пользователю дополнить' \
                ' заказ. В некоторых регионах идёт тест улучшения изображений' \
                ' блюд с помощью генеративных нейросетей. Кроме того, компания' \
                ' представила топ-3 фактора, влияющих на выбор ресторана среди' \
                ' пользователей — это скорость доставки в 66%, стоимость' \
                ' доставки в 65% и рейтинг заведения в 57%.'

ARTICLE2_HEADER = 'Memo (FMX)'
ARTICLE2_TEXT = 'Модифицировал штатный Memo (FMX) для добавления возможности' \
                ' форматирования текста. А также, ускорил его работу в разных' \
                ' аспектах (прокрутка, выделение, вставка строк и т.д.)' \
                ' Актуально для Delphi 11.3 (на более ранних, скорее всего,' \
                ' работать не будет, т.к. внесены изменения в штатный модуль' \
                ' FMX.Memo.Style.pas, который может быть несовместим между' \
                ' версиями. Модуль находится рядом с проектом).'

# вводим данные
User.objects.create_user('Bасильев Василий')
User.objects.create_user('Иванов Иван')
User.objects.create_user('Петров Петр')
User.objects.create_user('Просто Федя')
User.objects.create_user('Пушкин')

Author.objects.create(user=User.objects.get(pk=1), nick_name='Черный плащ')
Author.objects.create(user=User.objects.get(pk=2), nick_name='Чип не Дейл')
Author.objects.create(user=User.objects.get(username='Пушкин'), nick_name='Много пишу')
Author.objects.create(user=User.objects.get(username='Просто Федя'))

Category.objects.create(category='Политика')
Category.objects.create(category='Философия')
Category.objects.create(category='Экономика')
Category.objects.create(category='Как я провел лето')

Post.objects.create(author=Author.objects.get(nick_name='Черный плащ'),
                    post_type=Post.NEWS,
                    header=NEWS1_HEADER, text=NEWS1_TEXT)
Post.objects.create(author=Author.objects.get(nick_name='Чип не Дейл'),
                     post_type=Post.NEWS,
                     header=NEWS2_HEADER, text=NEWS2_TEXT)
Post.objects.create(author=Author.objects.get(nick_name='Много пишу'),
                     post_type=Post.NEWS,
                     header=ARTICLE1_HEADER, text=ARTICLE1_TEXT)
Post.objects.create(author=Author.objects.get(nick_name='Много пишу'),
                     post_type=Post.NEWS,
                     header=ARTICLE2_HEADER, text=ARTICLE2_TEXT)

Post.objects.get(pk=1).category.add(Category.objects.get(pk=2))
Post.objects.get(pk=1).category.add(Category.objects.get(pk=3))
Post.objects.get(pk=1).category.add(Category.objects.get(pk=1))
Post.objects.get(pk=2).category.add(Category.objects.get(pk=2))
Post.objects.get(pk=2).category.add(Category.objects.get(pk=3))
Post.objects.get(pk=3).category.add(Category.objects.get(pk=4))
Post.objects.get(pk=4).category.add(Category.objects.get(pk=4))

Comment.objects.create(post=Post.objects.get(pk=1),
                       user=User.objects.get(username='Просто Федя'),
                       comment_text='Первый')
Comment.objects.create(post=Post.objects.get(pk=2),
                       user=User.objects.get(username='Просто Федя'),
                       comment_text='Первый')
Comment.objects.create(post=Post.objects.get(pk=3),
                       user=User.objects.get(username='Просто Федя'),
                       comment_text='Первый')
Comment.objects.create(post=Post.objects.get(pk=4),
                       user=User.objects.get(username='Просто Федя'),
                       comment_text='Первый')
Comment.objects.create(post=Post.objects.get(pk=3),
                       user=User.objects.get(username='Пушкин'),
                       comment_text='Мало русского языка')
Comment.objects.create(post=Post.objects.get(pk=4),
                       user=User.objects.get(username='Пушкин'),
                       comment_text='Мало русского языка')
Comment.objects.create(post=Post.objects.get(pk=1),
                       user=User.objects.get(username='Иванов Иван'),
                       comment_text='Фу...не интересно')
Comment.objects.create(post=Post.objects.get(pk=2),
                       user=User.objects.get(username='Васильев Василий'),
                       comment_text='Актуальненько')
Comment.objects.create(post=Post.objects.get(pk=3),
                       user=User.objects.get(username='Васильев Василий'),
                       comment_text='Скучно')
Comment.objects.create(post=Post.objects.get(pk=4),
                       user=User.objects.get(username='Bасильев Василий'),
                       comment_text='Еще скучнее')
Comment.objects.create(post=Post.objects.get(pk=1),
                       user=User.objects.get(username='Иванов Иван'),
                       comment_text='Еще раз фуу')
Comment.objects.create(post=Post.objects.get(pk=2),
                       user=User.objects.get(username='Иванов Иван'),
                       comment_text='Ну не очень')

Comment.objects.get(pk=1).like()
for i in range(100):
    Comment.objects.get(pk=2).like()
Comment.objects.get(pk=1).like()
for i in Comment.objects.filter(user=User.objects.get(username='Пушкин')):
    for j in range(1356):
        i.like()
for i in range(21):
    Comment.objects.get(pk=3).like()
for i in range(9):
    Comment.objects.get(pk=11).like()
for i in range(12):
    Comment.objects.get(pk=12).dislike()
for i in Comment.objects.filter(user=User.objects.get(username='Иванов Иван')):
    for j in range(17):
        i.dislike()

for i in range(1000):
     Post.objects.get(pk=1).like()
for i in range(1340):
     Post.objects.get(pk=2).dislike()
for i in range(643):
     Post.objects.get(pk=3).like()
for i in range(643):
     Post.objects.get(pk=4).like()

# обновляем рейтинг всех авторов
for auth in  Author.objects.all():
    auth.update_rating()

# Вывести username и рейтинг лучшего пользователя
# (применяя сортировку и возвращая поля первого объекта).
Author.objects.order_by('-rating').values_list('user__username', 'rating')\
    .first()

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей
# статьи, основываясь на лайках/дислайках к этой статье.
Post.objects.order_by('-rating').values('creation_time__date',
                                        'author__user__username', 'rating',
                                        'header').first()

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=Post.objects.order_by('-rating')
                       .first()).values_list('creation_time__date',
                                             'user__username', 'rating',
                                             'comment_text')
