from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的as_view
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs) # 这句相当于user_center_info.as_view即再调一次as_view!(第一次调用其第一次父类的as_view,这次调用第二个父类的as_view) cls指向的是user_center_info
        return login_required(view)