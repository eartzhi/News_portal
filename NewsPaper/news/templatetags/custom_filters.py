from django import template

register = template.Library()


@register.filter()
def censored(text: str, vocabulary=None) -> str:
    if vocabulary is None:
        vocabulary = ['долг', 'Долг', 'дефиц',
                      'Дефиц', 'беда', 'Беда']
    for word in vocabulary:
        text = text.replace(word, word[0] + '*' * (len(word) - 1))
    return text


@register.filter()
def censored_for_16_3_1(text: str, vocabulary=None) -> str:
    if vocabulary is None:
        vocabulary = ['долг', 'Долг', 'дефиц',
                      'Дефиц', 'беда', 'Беда']
    for word in vocabulary:
        text = text.replace(word, word[0] + '*' * (len(word) - 2) + word[-1])
    return text
