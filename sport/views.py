from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import CreateView
from .forms import PlayerForm
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
                # form.save()
                factory = qrcode.image.svg.SvgImage
                first_name = form.cleaned_data['first_name'] 
                last_name = form.cleaned_data['last_name']
                profile_pic =  "https://ici-community/static/images/".format(form.cleaned_data['profile_picture'])
                qr_text = "{},{},{}".format(first_name, last_name, profile_pic)
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