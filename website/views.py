import requests
import logging

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.http import (require_http_methods, require_GET,
    require_POST)
from django.views.decorators.csrf import csrf_exempt

from website.auth import login_required
from website.utils import (get_api_server_url)
from website.communicate import Communicator
from website.auth import is_authenticated
from website.forms import (LoginForm, RegistryForm, ProjectForm)

logger = logging.getLogger("website")


def index(request):
    """
    Return the home page before login in.
    """
    if is_authenticated(request)[0]:
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'website/index.html', locals(),
        RequestContext(request))


@require_POST
def registry(request):
    """
    User registry view, should post username, password1, password2, email.
    """
    form = RegistryForm(request.POST)
    if form.is_valid() and form.password_varify():
        data = {
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password1'],
            'email': form.cleaned_data['email'],
            'is_staff': False,
            'is_active': True
        }
        client = Communicator()
        cookies = client.registry(data)

        if 'sessionid' in cookies:
            response = HttpResponseRedirect(reverse('home'))
            response.set_cookie('sessionid', cookies['sessionid'])
            return response

    return HttpResponseRedirect(reverse('index'))


@require_POST
def login(request):
    """
    Login view.
    """
    form = LoginForm(data=request.POST)

    if form.is_valid():
        data = {
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password']
        }
        client = Communicator()
        cookies = client.login(data)

        if 'sessionid' in cookies:
            response = HttpResponseRedirect(reverse('home'))
            response.set_cookie('sessionid', cookies['sessionid'])
            return response

        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))


def logout(request):
    """
    Logout view.
    """
    client = Communicator(cookies=request.COOKIES)
    client.logout()
    return HttpResponseRedirect(reverse('index'))


@login_required()
def home(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }

    client = Communicator(cookies=request.COOKIES)

    # Get project lists
    projects = client.project_lists()
    context['projects'] = projects

    return render(request, 'website/home.html', context,
        RequestContext(request))


@login_required()
@csrf_exempt
@require_POST
def create_project(request, *args, **kwargs):
    form = ProjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(reverse('home'))

    client = Communicator(cookies=request.COOKIES)
    data = {
        'name': form.cleaned_data['name'],
        'desc': form.cleaned_data['desc'],
        'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken']
    }

    ok = client.create_project(data)
    logger.debug(ok)
    return HttpResponseRedirect(reverse('home'))


@login_required()
def delete_project(request, *args, **kwargs):
    project_id = kwargs['pid']

    client = Communicator(cookies=request.COOKIES)
    ok = client.delete_project(project_id)
    if ok:
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


@login_required()
def list_images(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }

    project_id = kwargs.get('pid')
    client = Communicator(cookies=request.COOKIES)
    context['images'] = client.image_lists(project_id=project_id)

    return render(request, 'website/images.html', context,
        RequestContext(request))


@login_required()
def delete_image(request, *args, **kwargs):
    project_id = kwargs['pid']
    image_id = kwargs['iid']

    client = Communicator(cookies=request.COOKIES)
    ok = client.delete_image(project_id=project_id, image_id=image_id)
    if ok:
        return HttpResponseRedirect(reverse('list-images',
            kwargs={'pid': project_id}))
    return HttpResponseRedirect(reverse('list-images',
        kwargs={'pid': project_id}))


@login_required()
def project_intro(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/project_intro.html', context,
        RequestContext(request))


@login_required()
def list_applications(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/applications.html', context,
        RequestContext(request))


@login_required()
def list_volumes(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/volumes.html', context,
        RequestContext(request))


@login_required()
def list_publics(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/public_images.html', context,
        RequestContext(request))


@login_required()
def show_image_detail(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/image_detail.html', context,
        RequestContext(request))


@login_required()
def show_application_detail(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/application_detail.html', context,
        RequestContext(request))


@login_required()
def show_volume_detail(request, *args, **kwargs):
    context = {
        'username': kwargs.get('username')
    }
    return render(request, 'website/volume_detail.html', context,
        RequestContext(request))
