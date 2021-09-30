from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from .forms import PlayerForm
from .forms import ScannerForm
from .models import Player
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import base64

def home(request):
    form = PlayerForm()

    if request.method == "POST":
        print(request.POST)
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                player = form.save()
                factory = qrcode.image.svg.SvgImage
                profile_pic =  "https://ici-community.herokuapp.com/static/images/{}".format(player.profile_picture)
                # qr_text = "{},{},{},{}".format(player.id, player.first_name, player.last_name, profile_pic)
                qr_text = "{}".format(player.id)
                img = qrcode.make(qr_text, image_factory=factory, box_size=20)
                stream = BytesIO()
                img.save(stream)

                base64_image = base64.b64encode(stream.getvalue()).decode()
                qr = 'data:image/svg+xml;utf8;base64,' + base64_image
                messages.success(request, 'Registration completed successfully!')
                return render(request, 'result.html', {'qr': qr})
                # return render(request, 'result.html', {'qr': stream.getvalue().decode()})
            except BadHeaderError:
                messages.error(request, 'Registration failed! Please try again later.')
        else:
            messages.error(request, 'Registration failed! Please try again later.')
    
    context = {'form': form}
    return render(request, 'registration.html', context)


def scanner(request):
    scannerForm = ScannerForm()
    obj = None
    print('Scanner In Progress :::::::::::::::::::')
    if request.method == "POST":
        scannerForm = ScannerForm(request.POST)
        if scannerForm.is_valid():
            try:
                playerId = request.POST['ID']
                print(" Scanned ID ::::::::::: {}".format(playerId))
                obj = Player.objects.get(id=playerId)
                print(obj)
            except Exception as e:
                    print('ERROR  :::::::: {}'.format(e))
                    messages.error(request, 'User not found :( ! ')
        else:
            messages.error(request, 'User not found :( ! ')
    
    if obj is None:
        profile_image = "profile_icon.png"
    else:
        profile_image = '{}{}'.format(settings.MEDIA_URL, obj.profile_picture)

    context = {
        'player' : obj,
        'scannerForm' : scannerForm,
        'profile_image' : profile_image
    }
    return render(request, 'scanner.html', context)


# def result(request):
#     return render(request, 'result.html', context)

# #sending email
#  email_to = form.cleaned_data['email']
# subject = "Website Inquiry" 
# message = "Registration completed successfully!"
# email_from = settings.EMAIL_HOST_USER
# try:
#     send_mail(subject, message, email_from, [email_to]) 
#     messages.success(request, 'Registration completed successfully!')
# except BadHeaderError:
#     messages.error(request, 'Registration failed! Please try again later.')
# else:
# messages.error(request, 'Registration failed! Please try again later.')