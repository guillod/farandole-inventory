from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.views.generic import ListView
from django_filters.views import FilterView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.utils.crypto import get_random_string
import requests

from .models import Object
from .forms import ObjectForm
from .filters import ObjectFilter


def login_oauth(request):
    state = get_random_string(length=12)
    request.session['state'] = state
    return redirect(f"{settings.OAUTH['authorize_url']}?response_type=code&client_id={settings.OAUTH['client_id']}&state={state}")

def authorize(request):
    # parse parameters
    code = request.GET.get('code', False)
    state = request.GET.get('state', False)
    # validate state
    if request.session['state'] != state: redirect('home')
    # get access token
    r = requests.post(settings.OAUTH['access_token_url'], data={'grant_type':'authorization_code', 'code':code, 'state':state, 'client_id':settings.OAUTH['client_id'], 'client_secret': settings.OAUTH['client_secret']})
    if r.status_code != 200:
        return render(request, "error.html", {'error': "Impossible d'obtenir une authentification"})
    access_token = r.json().get('access_token', None)
    # get user data
    r = requests.get(settings.OAUTH['user_info_url'], headers={'authorization': f"Bearer {access_token}"})
    if r.status_code != 200:
        return render(request, "error.html", {'error': "Authentification invalide"})
    try:
        username = r.json()['ocs']['data']['id']
        email = r.json()['ocs']['data']['email']
        displayname = r.json()['ocs']['data']['display-name']
        displayname = displayname.split(" \u200b")[0]
    except:
        return render(request, "error.html", {'error': "Impossible d'importer les données"})
    # get or create user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username, email, last_name=displayname, is_staff=True)
    # add group
    group = Group.objects.get(name='group')
    user.groups.add(group)
    # login and redirect
    login(request, user)
    return redirect('home')

class ObjectListView(LoginRequiredMixin,FilterView):
    model = Object
    filterset_fields = {'description':['icontains'], 'group':['exact'], 'location':['exact'], 'state':['exact']}
    #filterset_class = ObjectFilter
    paginate_by = 50

    # delete grid session if present
    def get(self, request, *args, **kwargs):
        if request.session.get('grid', False): del request.session['grid']
        return super().get(request, *args, **kwargs)

    #def photo_thumbnail(self):
    #    return format_html('<a href="{0}"><img src="{0}" style="max-height:50px;max-width:100px;" /></a>', obj.photo.url)

class ObjectGridView(LoginRequiredMixin,FilterView):
    model = Object
    filterset_fields = {'description':['icontains'], 'group':['exact'], 'location':['exact'], 'state':['exact']}
    template_name = "inventory/object_grid.html"
    #filterset_class = ObjectFilter
    paginate_by = 50

    # add grid session
    def get(self, request, *args, **kwargs):
        request.session['grid'] = True
        return super().get(request, *args, **kwargs)

def home(request):
    # get corresponding view (grid or list)
    if request.session.get('grid', False):
        return ObjectGridView.as_view()(request)
    else:
        return ObjectListView.as_view()(request)

@login_required
def object_form(request, object_id=None):

    # get instance on modification
    instance = get_object_or_404(Object, pk=object_id) if object_id else None

    # on form post
    if request.method == 'POST':
        # instanciate form
        form = ObjectForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            # add user fields and save data
            form_data = form.save(commit=False)
            if not form_data.created_by_id:
                form_data.created_by_id = request.user.id
            form_data.updated_by_id = request.user.id
            form_data.save()
            messages.success(request, f"{form.cleaned_data['description']} bien enregistré.")
            if "addanother" in request.POST:
                initial = { key: form.cleaned_data[key] for key in ['group','location'] }
                form = ObjectForm(initial=initial)
            else:
                return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'enregistrement.")
    else:
        form = ObjectForm(instance=instance)

    return render(request, 'inventory/object_form.html', { 'form': form, 'instance': instance })
