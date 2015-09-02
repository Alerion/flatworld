from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from world.models import World


def index(request):
    context = {
        'worlds': World.objects.all()
    }
    return render(request, 'main/index.html', context)


@login_required
def worlds(request):
    context = {
        'worlds': World.objects.all()
    }
    return render(request, 'main/worlds.html', context)


@login_required
def world(request, world_id):
    try:
        world_obj = World.objects.get(pk=world_id)
    except World.DoesNotExist:
        return redirect('main:worlds')

    world_obj.create_city_for_user(request.user)

    context = {
        'TILE_SERVER': settings.TILE_SERVER,
        'FRONTEND_ADDR': settings.FRONTEND_ADDR,
        'FRONTEND_PORT': settings.FRONTEND_PORT,
        'STATIC_URL': settings.STATIC_URL,
        'world': world_obj
    }
    return render(request, 'main/wolrd.html', context)
