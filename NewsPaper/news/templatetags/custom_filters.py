from django import template

register = template.Library()


@register.filter()
def censored(text, vocabulary = ['долг', 'Долг', 'дефиц',
                                 'Дефиц', 'беда',  'Беда']):
    for word in vocabulary:
        text = text.replace(word, '*' * len(word))
    return text
