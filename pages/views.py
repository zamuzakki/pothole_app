from django.views.generic import TemplateView,ListView
from pothole.models import Pothole, PotholeRepair
from pothole.forms import PotholeForm, PotholeSearchForm

class HomePageView(ListView):
    template_name = 'pages/home.html'
    model = Pothole

    extra_context = {
        'POTHOLE_WIDTH': Pothole.WIDTH,
        'POTHOLE_DEPTH': Pothole.DEPTH,
        'POTHOLE_RESPONSE': Pothole.RESPONSE_TIME_NEEDED,
        'form': PotholeForm(),
    }


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'