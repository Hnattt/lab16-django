from django.shortcuts import get_object_or_404,render
from django.views.decorators.http import require_safe
from .models import Device
@require_safe
def index(request):
 q=request.GET.get('q','').strip(); devices=Device.objects.order_by('serial')
 if q: devices=devices.filter(name__icontains=q)
 return render(request,'monitoring/index.html',{'devices':devices,'q':q})
@require_safe
def device_detail(request,pk):
 return render(request,'monitoring/detail.html',{'device':get_object_or_404(Device,pk=pk)})
