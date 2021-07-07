from django.http.response import HttpResponse
from django.shortcuts import redirect, render

import folium
import geocoder
from folium.map import Popup
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method=='POST':
        address=request.POST['search']
        data=Address(address=address)
        data.save()
        # print(address)
        
        # location=geocoder.osm(address)
        # latitude=location.lat
        # longitude=location.lng
        # country=location.country
        return redirect('index')

    else:

        address=Address.objects.all().last()
        location=geocoder.osm(address)
        latitude=location.lat
        longitude=location.lng
        country=location.country
        if latitude == None and longitude == None:
            address.delete()
            messages.error(request, "Entered place is Invalid")
            return redirect(index)

        #create map objects
        map=folium.Map(location=[19,12],zoom_start=2)
        # folium.Marker([5.945,-0.219],tooltip='click',popup='Nigeria').add_to(map)
        folium.Marker([latitude,longitude],tooltip='click',popup=country).add_to(map)

        #html representation of map objects
        map=map._repr_html_()
        context={'map':map}
        return render(request,'index.html',context)
        
