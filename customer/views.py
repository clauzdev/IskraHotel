import uuid

from PIL.Image import Image
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import os
from deepface import DeepFace
import cv2
from booking.models import Booking
from customer.forms import UserForm, CustomerForm
from IskraHotel.settings import MEDIA_ROOT, MEDIA_URL
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

# api_key ='xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
# api_secret ='TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'
# image1 = 'https://i.postimg.cc/65gyw833/9cv-H3hr-Ni7g.jpg'
# image2 = 'https://i.postimg.cc/5NY2Pf3M/IQZ9lvio8-Js.jpg'

def register(request):
    registered = False

    next_page = request.GET.get('next', '/')

    print(next_page)

    if request.user.is_authenticated:
        return HttpResponseRedirect(next_page)
    else:
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)

            customer_form = CustomerForm(data=request.POST)

            if user_form.is_valid() and customer_form.is_valid():
                print("valid")
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                customer = customer_form.save(commit=False)
                customer.user = user

                photo_exists = request.POST.get('photo_exists', 0)
                path = request.POST["src"]
                if photo_exists:
                    image = NamedTemporaryFile()
                    image.write(urlopen(path).read())
                    image.flush()
                    image = File(image)
                    name = str(image.name).split('\\')[-1]
                    name += '.jpg'
                    image.name = name
                    customer.photo = image
                customer.save()

                registered = True

                login(request, user)

                return HttpResponseRedirect(next_page)

            else:
                print(user_form.errors, customer_form.errors)

        else:
            user_form = UserForm()
            customer_form = CustomerForm()

    context = {
        'user_form': user_form,
        'customer_form': customer_form,
        'registered': registered,
    }

    return render(request, 'register.html', context)


def user_login(request):
    next_page = request.GET.get('next', '/')

    print(next_page)

    if request.user.is_authenticated:
        return HttpResponseRedirect(next_page)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            photo = request.POST.get('photo')
            
            user = authenticate(username=username, password=password)
            try:
                if user.is_authenticated:

                    if user.is_active:
                        login(request, user)
                        customer = request.user.customer
                        if customer.photo:
                            customerphotopath = MEDIA_ROOT.replace('\\', '/') + '/' + str(customer.photo)
                            uploadedphotopath = MEDIA_ROOT + '/loginpics/'
                            photo_exists = request.POST.get('photo_exists', 0)
                            path = request.POST["src"]

                            tmpData = path.replace('data:image/png;base64,', '')
                            imgdata = base64.b64decode(tmpData)
                            image = NamedTemporaryFile()
                            image.write(urlopen(path).read())
                            image.flush()
                            image = File(image)
                            name = str(image.name).split('\\')[-1]
                            name += '.jpg'
                            image.name = name
                            with open(uploadedphotopath + image.name, 'wb') as f:
                                f.write(imgdata)
                            try:
                                result = DeepFace.verify(customerphotopath, uploadedphotopath + name)
                                print(result)
                                if result['distance'] < 0.25:
                                    return HttpResponseRedirect(next_page)
                                else:
                                    logout(request)
                                    return HttpResponse(
                                        'Лицо не распознано! Попробуйте сделать фото еще раз, при этом убедитесь, что на '
                                        'фотографии Вас отчётливо видно, и фотография не смазана.')
                            except ValueError:
                                logout(request)
                                return HttpResponse(
                                    'Лицо не распознано! Попробуйте сделать фото еще раз, при этом убедитесь, что на '
                                    'фотографии Вас отчётливо видно, и фотография не смазана.')


                        else:
                            return HttpResponseRedirect(next_page)
                    else:
                        return HttpResponse('Аккаунт удален за неактивность. Свяжитесь с нами по телефону')

                else:
                    print('Someone tried to login and failed!')
                    print(f'They used username: {username} and password: {password}')

                    return HttpResponse('Не все поля заполнены!')
            except AttributeError:
                return HttpResponse('Не все поля заполнены!')
        else:
            return render(request, 'login.html', {'next_page': next_page})

def image_upload(request):
    context = dict()
    if request.method == 'POST':
        username = request.POST["username"]
        image_path = request.POST["src"]  # src is the name of input attribute in your html file, this src value is set in javascript code
        print(image_path)
        image = NamedTemporaryFile()
        image.write(urlopen(path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        print(name)
        if image is not None:
            obj = Image.objects.create(username=username, image=image)  # create a object of Image type defined in your model
            obj.save()
            context["path"] = obj.image.url  #url to image stored in my server/local device
            context["username"] = obj.username
        else:
            return redirect('/')
        return redirect('any_url')
    return render(request, 'index.html', context=context)  # context is like respose data we are sending back to user, that will be rendered with specified 'html file'.

@login_required
def user_logout(request):
    logout(request)
    print(request.path)

    return redirect('customer:login')


@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user.customer)
    return render(request, 'dashboard.html', {'bookings': bookings})


