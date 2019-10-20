# users/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from garden.models import Garden
from django.http import JsonResponse
from django.conf import settings

from .forms import CustomUserCreationForm, ImageFileUploadForm, DummyGardenLog
from django.http import HttpResponseRedirect

#my_view is here because you can't pass settings links with the data
def my_view(request):
    username = request.user.username
    if request.user.garden_set.all().count() == 1:
        gardenname = Garden.objects.get(user=request.user).name
        return HttpResponseRedirect('/%s/%s' % (username, gardenname))
    else:
        return HttpResponseRedirect('/%s/gardens' %username)

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
def index(request, username=None):
    context = {'MEDIA_URL':settings.MEDIA_URL}
    return render(request,"users/index.html", context)
    
def profile(request,username=None):
    if username == request.user.username:
        if request.method == 'POST':
            form = DummyGardenLog(request.POST, request.FILES)
            if form.is_valid():
                new_log = form.save(commit=False)
                garden = Garden.objects.get(serial='mb00001')
                new_log.garden = garden
                new_log.save()
                return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
            else:
                return JsonResponse({'error': True, 'errors': form.errors})
        else:
            form = ImageFileUploadForm()
            form2 = DummyGardenLog()
            context = {'form': form, 'form2' : form2}
            return render(request, 'users/profile.html', context)
    else: 
        return render(request,'users/no_access.html')
