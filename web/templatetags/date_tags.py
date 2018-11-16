from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='nb_days')
def nb_days(date):
    if date == "" or date is None:
        return ""
    delta = datetime.combine(date, datetime.min.time()) - datetime.today()
    return "(" + str(delta.days) + ")"
