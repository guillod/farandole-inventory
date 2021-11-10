from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.views.generic import ListView
from django_filters.views import FilterView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.conf import settings

from .models import Object
from .forms import ObjectForm
from .filters import ObjectFilter


def dummylogin(request):
    token = settings.DUMMY_LOGIN['token']
    password = settings.DUMMY_LOGIN['password']
    if 'uid' in request.GET and 'email' in request.GET and 'dn' in request.GET and request.GET.get('token',None) == settings.TOKEN:
        username = request.GET['uid']
        email = request.GET['email']
        displayname = request.GET['dn']
        displayname = displayname.split(" \u200b")[0]
        # get or create user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password, last_name=displayname, is_staff=True)
        # add group
        group = Group.objects.get(name='group')
        user.groups.add(group)
        # authenticate and login
        user = authenticate(request, username=username, password=password)
        if user is not None: login(request, user)
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
    # redirect to nextcloud login (then nextcloud redirect to)
    if not request.user.is_authenticated:
        return redirect("https://cloud.crechefarandole.com/apps/external/1")

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
