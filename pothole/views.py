from django.shortcuts import render
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from .forms import PotholeForm
from .models import Pothole, pothole_photo_directory
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
from django.contrib.gis.geos import Point
from django.core.serializers import serialize


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class PotholeCreateView(CreateView):
    form_class = PotholeForm
    model = Pothole

    def post(self, request, *args, **kwargs):
        data = dict()


        form = self.form_class(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            geom = json.loads(request.POST['geometry'])
            geom = geom['coordinates']

            last_id = 0 if Pothole.objects.all().first() == None else Pothole.objects.all().first().id

            pothole = Pothole.objects.create(
                id=last_id+1,
                width=request.POST['width'],
                depth=request.POST['depth'],
                response_time_needed=request.POST['response_time_needed'],
                geometry=Point(geom[1],geom[0]),
                photo=None,
                created_by=request.user
            )

            myfile = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(pothole_photo_directory(pothole,myfile.name), myfile)

            pothole.photo = filename
            pothole.save()

            data['success'] = serialize('geojson', [pothole],
                      geometry_field='geometry',
                      fields=('width','depth','response_time_needed','photo'))

            return JsonResponse(data)
        else:
            data['error'] = "form not valid!"
            return JsonResponse(data, status=500)