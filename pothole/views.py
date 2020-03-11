from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
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
    template_name = 'pothole/modal_form.html'
    extra_context = {}

    def get_context_data(self, *args, **kwargs):
        self.extra_context['action'] = self.request.path

        kwargs.update(self.extra_context)
        return super().get_context_data(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = dict()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            geom = json.loads(request.POST['geometry'])
            geom = geom['coordinates']

            last_id = 0 if Pothole.objects.all().first() == None else Pothole.objects.all().first().id

            pothole = Pothole.objects.create(
                pk=last_id+1,
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

            string_json = serialize('geojson', [pothole],
                      geometry_field='geometry',
                      fields=('id','width','depth','response_time_needed','photo'))
            geojson = json.loads(string_json)
            geojson['features'][0]['properties']['id'] = str(pothole.id)
            geojson['features'][0]['properties']['get_width_display'] = pothole.get_width_display()
            geojson['features'][0]['properties']['get_depth_display'] = pothole.get_depth_display()
            geojson['features'][0]['properties']['get_response_time_needed_display'] = pothole.get_response_time_needed_display()
            geojson['features'][0]['properties']['photo'] = pothole.photo.url

            data['success'] = geojson

            print(data['success'])

            return JsonResponse(data)
        else:
            data['error'] = "form not valid!"
            return JsonResponse(data, status=500)

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data(*args, **kwargs))

class PotholeDetailView(DetailView):
    model = Pothole
    queryset = Pothole.objects.all()

    def get_object(self, queryset=None):
        id = int(self.request.GET.get('id',0))
        print(id)
        if not id == 0:
            return self.queryset.get(id=id)

    def render_to_response(self, context, **response_kwargs):
        data = dict()
        pothole = self.get_object()
        string_json = serialize('geojson', [pothole],
                                geometry_field='geometry',
                                fields=('id', 'width', 'depth', 'response_time_needed', 'photo'))
        geojson = json.loads(string_json)
        geojson['features'][0]['properties']['id'] = str(pothole.id)
        geojson['features'][0]['properties']['get_width_display'] = pothole.get_width_display()
        geojson['features'][0]['properties']['get_depth_display'] = pothole.get_depth_display()
        geojson['features'][0]['properties']['get_response_time_needed_display'] = pothole.get_response_time_needed_display()
        geojson['features'][0]['properties']['photo'] = pothole.photo.url

        data['success'] = geojson
        return JsonResponse(data)

class PotholeListView(ListView):
    model = Pothole
    queryset = Pothole.objects.all()

    def get_object(self, queryset=None):
        width = self.request.GET.get('width', 'all')
        depth = self.request.GET.get('depth', 'all')
        response = self.request.GET.get('response', 'all')

        print(width, depth, response)

        criteria = dict()

        if not width == 'all':
            criteria['width'] = width
        if not depth == 'all':
            criteria['depth'] = depth
        if not response == 'all':
            criteria['response_time_needed'] = response
        return self.queryset.filter(**criteria)

    def render_to_response(self, context, **response_kwargs):
        data = dict()
        pothole = self.get_object()
        pothole = list(pothole)
        string_json = serialize('geojson', pothole,
                                geometry_field='geometry',
                                fields=('id', 'width', 'width_display', 'depth', 'response_time_needed', 'photo'))
        geojson = json.loads(string_json)

        for index,item in enumerate(geojson['features']):
            # print(index,item)
            item['properties']['id'] = str(pothole[index].id)
            item['properties']['get_width_display'] = pothole[index].get_width_display()
            item['properties']['get_depth_display'] = pothole[index].get_depth_display()
            item['properties']['get_response_time_needed_display'] = pothole[index].get_response_time_needed_display()
            item['properties']['photo'] = pothole[index].photo.url

        data['success'] = geojson
        return JsonResponse(data)