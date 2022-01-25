from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Mebel, Panels, Contours

import json

from django.core import serializers


def post_list(request):
    posts = Mebel.objects.all
    return render(request, 'bazis/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Mebel, pk=pk)
    mebelView={}
    meb = Mebel.objects.get(id=pk)   
    mebelView['depth']=meb.depth
    mebelView['height']=meb.height
    mebelView['width']=meb.width
    pan=Panels.objects.filter(mebel=meb)
    d=[]
    for p in pan:
        pc=[]
        cont=Contours.objects.filter(panel=p)
        for c in cont:
            pc.append({
                        'type'        :c.type,
                        'pos1x'       :c.pos1x,
                        'pos2x'       :c.pos2x,
                        'pos1y'       :c.pos1y,
                        'pos2y'       :c.pos2y,
                        'centerx'     :c.centerx,
                        'centery'     :c.centery,
                        'radius'      :c.radius,
                        'startangle'  :c.start_angle,
                        'endangle'    :c.end_angle,
                        'arcdir'      :c.arc_dir
                        })
        d.append({
                        'title':p.title,
                        'material'     :p.material,  
                        'thickness'    :p.thickness,
                        'posx'         :p.posx,
                        'posy'         :p.posy,
                        'posz'         :p.posz,
                        'rotx'         :p.rotx,
                        'roty'         :p.roty,
                        'rotz'         :p.rotz,
                        'rotw'         :p.rotw,
                        'texture'      :p.texture,
                        'contour'      :pc
            })
    mebelView['panels']=d
    return render(request, 'bazis/post_detail.html', {'post': post, 'mebelView':json.dumps(mebelView)})

def about(request):
    return render(request, 'bazis/about.html')
