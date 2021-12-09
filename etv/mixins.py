from django.utils.http import is_safe_url
from .decorators import ajax_required
from django.utils.decorators import method_decorator

class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class NextUrlMixin(object):
    default_next = "/"
    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return self.default_next


class AjaxRequiredMixin(object):
	@method_decorator(ajax_required)
	def dispatch(self, request, *args, **kwargs):
		return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)
