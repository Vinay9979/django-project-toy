from django.db.models import Func

class SubstringBefore(Func):
    function = 'SUBSTRING'
    template = "%(function)s(%(expressions)s FROM 1 FOR LOCATE('.', %(expressions)s) - 1)"
