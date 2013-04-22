from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class ProtectedMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProtectedMixin, self).dispatch(request, *args, **kwargs)

