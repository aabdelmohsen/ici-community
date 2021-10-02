from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from django.views.generic import ListView
from .forms import PlayerForm
from .forms import ScannerForm
from .models import Player
from .models import Daily_Scan
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import base64
import time

def home(request):
    form = PlayerForm()

    if request.method == "POST":
        print(request.POST)
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                player = form.save()
                factory = qrcode.image.svg.SvgImage
                qr_text = "{}".format(player.id)
                img = qrcode.make(qr_text, image_factory=factory, box_size=20)
                stream = BytesIO()
                img.save(stream)
                base64_image = base64.b64encode(stream.getvalue()).decode()
                qr = 'data:image/svg+xml;utf8;base64,' + base64_image
                messages.success(request, 'Registration completed successfully!')
                return render(request, 'result.html', {'qr': qr})
                
            except BadHeaderError:
                messages.error(request, 'Registration failed! Please try again later.')
        else:
            messages.error(request, 'Registration failed! Please try again later.')
    
    context = {'form': form}
    return render(request, 'registration.html', context)


def scanner(request):
    scannerForm = ScannerForm()
    player = None
    print('Scanner In Progress :::::::::::::::::::')
    if request.method == "POST":
        scannerForm = ScannerForm(request.POST)
        if scannerForm.is_valid():
            try:
                
                playerId = request.POST['ID']
                print(" Scanned ID ::::::::::: {}".format(playerId))
                player = Player.objects.get(id=playerId)
                
                # Create and save player in daliy_scan table
                daily_scan = Daily_Scan.objects.create(player=player)
                print('daily_scan saved successfully ############## ')

            except Exception as e:
                    print('ERROR  :::::::: {}'.format(e))
                    messages.error(request, 'Something went wrong, please make sure Player Id is correct :( ! ', extra_tags='scanner')
        else:
            messages.error(request, 'Value is invalid! ', extra_tags='scanner')
    
    if player is None:
        profile_image = '{}{}'.format(settings.MEDIA_URL, "profile_icon.png")
    else:
        profile_image = '{}{}'.format(settings.MEDIA_URL, player.profile_picture)

    context = {
        'player' : player,
        'scannerForm' : scannerForm,
        'profile_image' : profile_image
    }
    return render(request, 'scanner.html', context)


def getqrcode(request, id=None):
    try:
        print('Generating QR Code for Player  ID :::::  {}'.format(id))
        factory = qrcode.image.svg.SvgImage
        qr_text = "{}".format(id)
        img = qrcode.make(qr_text, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        base64_image = base64.b64encode(stream.getvalue()).decode()
        qr_code = 'data:image/svg+xml;utf8;base64,' + base64_image
        messages.success(request, 'QR code generated successfully!')
    except Exception as e:
        print('ERROR  :::::::: {}'.format(e))

    context = {
        'qr_code' : qr_code
    }
    return render(request, 'getqrcode.html', context)
                




class PlayerList(ListView):
    model = Player




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


# from django.core.files import File
# from django.core.files.images import ImageFile
# import pyqrcode
# # player.qr_code = File(stream)
# # player.qr_code = ImageFile(open(File(stream), "rb"))
# img_name = '{}-{}.png'.format(player.id, player.first_name)


# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=20,
#     border=4,
# )
# qr.add_data(qr_text)
# qr.make(fit=True)
# filename = img_name
# img_test = qr.make_image()
# img_test.save(settings.MEDIA_URL)
# player.qr_code.save(img_name, img_test, save=False)

# # player.qr_code.save(img_name,  File(base64_image) , save=False)  
# player.save()