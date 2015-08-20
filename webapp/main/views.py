from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from world.models import World


def index(request):
    context = {
        'worlds': World.objects.all()
    }
    return render(request, 'main/index.html', context)


@login_required
def wolrd(request, world_id):
    world = get_object_or_404(World, pk=world_id)
    return render(request, 'main/wolrd.html')


@login_required
def world_data(request, world_id):
    world = get_object_or_404(World, pk=world_id)
    return JsonResponse({
        'id': world.pk,
        'name': world.name,
        'points': world.points
    })
