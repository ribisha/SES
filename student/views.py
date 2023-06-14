
from django.shortcuts import render,HttpResponsePermanentRedirect,redirect
from . models import *
from .form import StudentApplicationForm
from django.views import View
from django.utils import timezone
from background_task import background
from datetime import timedelta
from datetime import datetime




def delete_expired_notifications():
    expired_notifications = Notification.objects.filter(time__lte=timezone.now() - timedelta(minutes=2880))
    expired_notifications.delete()


def student_register(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            new_student = form.save()

            # Create a notification for the new student
            current_time = timezone.now()
            notification = Notification.objects.create(student=new_student, time=current_time)
            notification.save()

            Notification.delete_expired_notifications()  # Manually call the function to delete expired notifications
            return HttpResponsePermanentRedirect('/')
        else:
            return render(request, 'application.html', {'form': form})
    else:
        form = StudentApplicationForm()
        return render(request, 'application.html', {'form': form})
    
    
def student_login(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None and user.is_superuser:
    #         login(request, user)
    #         return redirect('dashboard')
    #     else:
    #         return render(request, 'profile/st_profile.html',{'error_message': 'Invalid credentials!'})
    # else:
    return render(request, 'profile/st_profile.html')


class RegisterForm:
    pass


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

def student_profile(request):
    return render(request, 'student_profile.html')