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
import pytz
from django.utils import timezone
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q, FilteredRelation
from django.db.models.functions import Lower

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
                
            except Exception as e:
                print('ERROR  :::::::: {}'.format(e))
                messages.error(request, 'Registration failed! Please try again later.')
        else:
            print('Form is not valid ::::::: {}'.format(form.is_valid()))
            messages.error(request, 'Registration failed! Please try again later.')
    
    context = {'form': form}
    return render(request, 'registration.html', context)


def scanner(request):
    if not request.user.is_authenticated:
        return redirect('/login')
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
                

def scanmenow(request, id=None):
    try:
        print('Scanining Player  ID :::::  {}'.format(id))
        player = Player.objects.get(id=id)
        # Create and save player in daliy_scan table
        # scan_timestamp = models.DateTimeField(default=datetime.now(pytz.timezone('US/Central')))
        # scan_timestamp = datetime.now(pytz.timezone('US/Central')) #pytz.timezone("US/Central")
        # scan_timestamp = datetime.utcnow().replace(tzinfo=pytz.timezone('US/Central')) #(tzinfo=pytz.utc)        
        # u = datetime.utcnow()
        # u = u.replace(tzinfo=pytz.utc)
        # tz = pytz.timezone('US/Central')
        # dt_cst = u.astimezone(tz)
        # scan_timestamp = models.DateTimeField(default=timezone.now)

        daily_scan = Daily_Scan.objects.create(player=player)
        print('Player scanned successfully ############## ')
        messages.success(request, 'Player {} scanned successfully!'.format(player.first_name))
    except Exception as e:
        print('ERROR  :::::::: {}'.format(e))

    return redirect(request.META['HTTP_REFERER'])
    # return render(request)


# def players_filter(request):
#     try:
#         # global players_filter_data
#         players_filter_data = request.GET.get('value', None)
#         request.session['players_filter_data'] = players_filter_data
#         print('players_filter value :::::  {}'.format(request.session.get('players_filter_data')))
#         context = {
#         'players_filter_data' : players_filter_data
#         }
#         # render(request, 'player_list.html', context)
#         return HttpResponse('success')
#     except Exception as e:
#         print('ERROR  :::::::: {}'.format(e))


# def test_filter(request):
#     try:
#         value  = request.session.get('players_filter_data')
#         return HttpResponse(f'players_filter_data : {value}')
#     except Exception as e:
#         print('ERROR  :::::::: {}'.format(e))

# def daily_scan_filter(request, date=None):
#     try:
#         print('daily_scan_filter date :::::  {}'.format(date))
#         global daily_scan_filter_date
#         daily_scan_filter_date = date
#     except Exception as e:
#         print('ERROR  :::::::: {}'.format(e))


def get_cst_date():
    date_format = "%Y-%m-%d"
    # Current time in UTC
    now_utc = datetime.now(timezone('UTC'))
    # Convert to central America/Chicago time zone
    now_central_date = now_utc.astimezone(timezone('America/Chicago'))
    db_date = now_central_date.strftime(date_format) 
    print(f"view daily scan date: {db_date}")
    return db_date


class PlayerList(ListView):
    model = Player
    
    def get_context_data(self, **kwargs):
        context = super(PlayerList, self).get_context_data(**kwargs)
        value = self.request.GET.get('value', None)
        object_list = None
        if value is not None:
            print(f"Filter using session value ::: {value}")
            object_list = Player.objects.filter(Q(first_name__istartswith=value) \
                | Q(last_name__istartswith=value) | Q(mobile__istartswith=value))
        else:
            value = ''
            print('No filter yet, getting first 20 record')
            object_list = Player.objects.all()[:20]

        player_total_count = Player.objects.count()
        context.update({'value': value})
        context.update({'player_total_count': player_total_count})
        context.update({'object_list': object_list})
        return context

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, *args, **kwargs):
        return super(PlayerList, self).dispatch(*args, **kwargs)


class Daily_ScanList(ListView):
    model = Daily_Scan

    def get_context_data(self, **kwargs):
        context = super(Daily_ScanList, self).get_context_data(**kwargs)
        value = self.request.GET.get('value', None)
        object_list = None
        count = ''
        if value is not None:
            if value is '' or value is ' ':
                print('Filter is empty, getting first 15 record')
                object_list = Daily_Scan.objects.order_by('-scan_date')[:15]
                count = len(object_list)
            else:
                print(f"Filter using session value ::: {value}")
                object_list = Daily_Scan.objects.filter(Q(scan_date__istartswith=value))
                count = len(object_list)
        else:
            value = ''
            print('No filter yet, getting first 15 record')
            object_list = Daily_Scan.objects.order_by('-scan_date')[:15]
            count = len(object_list)

        context.update({'filter_date': value})
        context.update({'count': count})
        context.update({'object_list': object_list})
        return context

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, *args, **kwargs):
        return super(Daily_ScanList, self).dispatch(*args, **kwargs)  



# plus21 = request.POST.get('plus21', False)
# print('plus21 :::::: {}'.format(plus21))
# print('birth date  :::::: {}'.format(request.POST['date_of_birth']))

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