import datetime
from datetime import datetime
from email import message

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import (
    Product,
    meetingRoomCalendar,
    reservas_Coworking,
    reservas_Coworking_provisoria,
    Price,
)
from django.db.models import Q
from polls.models import mensagens
from dotenv import load_dotenv
from django.views.generic import TemplateView
from django.conf import settings
from .forms import ReservaModelForm, CreateUserForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from .tokens import account_activation_token


load_dotenv()


def get_qty(reserva):
    qty = 0
    if reserva.chair1 == True:
        qty += 1
    if reserva.chair2 == True:
        qty += 1
    if reserva.chair3 == True:
        qty += 1
    if reserva.chair4 == True:
        qty += 1
    if reserva.chair5 == True:
        qty += 1
    if reserva.chair6 == True:
        qty += 1
    if reserva.chair7 == True:
        qty += 1
    if reserva.chair8 == True:
        qty += 1
    if reserva.chair9 == True:
        qty += 1
    if reserva.chair10 == True:
        qty += 1
    if reserva.chair11 == True:
        qty += 1
    if reserva.chair12 == True:
        qty += 1
    if qty == 0:
        qty = 1
    return qty*reserva.nrDias


def get_RealQty(reserva):
    qty = 0
    if reserva.chair1 == True:
        qty += 1
    if reserva.chair2 == True:
        qty += 1
    if reserva.chair3 == True:
        qty += 1
    if reserva.chair4 == True:
        qty += 1
    if reserva.chair5 == True:
        qty += 1
    if reserva.chair6 == True:
        qty += 1
    if reserva.chair7 == True:
        qty += 1
    if reserva.chair8 == True:
        qty += 1
    if reserva.chair9 == True:
        qty += 1
    if reserva.chair10 == True:
        qty += 1
    if reserva.chair11 == True:
        qty += 1
    if reserva.chair12 == True:
        qty += 1

    return qty


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            all_users = get_user_model().objects.all()
            all_reservas = reservas_Coworking.objects.all()
            nrMensagens = mensagens.objects.all()
            if request.method == "POST":
                users_to_delete = request.POST.getlist("users_to_delete")
                for user in users_to_delete:
                    user_to_delete = get_user_model().objects.filter(username=user)
                    user_to_delete.delete()
            context = {
                "nrUsers": len(all_users),
                "all_users": all_users,
                "nrReservas": len(all_reservas),
                "all_reservas": all_reservas,
                "nrMensagens": len(nrMensagens),
            }
            return render(request, "admin.html", context)
        else:
            if request.method == "POST":
                if request.POST.get("message"):
                    name = request.POST.get("name", False)
                    razao = request.POST.get("razao")
                    message = request.POST.get("message", False)
                    mensagens.objects.create(
                        user=request.user,
                        date=datetime.now(),
                        ClientName=name,
                        Reason=razao,
                        ClientEmail=request.user.email,
                        ClientMessage=message,
                    )

                    return redirect("index")
            else:
                MensagensPendentes = mensagens.objects.filter(
                    user=request.user, Pendente=True)
                reservas = reservas_Coworking.objects.filter(user=request.user)

                nrMensagens = 0
                difference = 0
                todayDate = datetime.now()

                if len(reservas) != 0:
                    difference = abs(
                        ((reservas[0].endDate)-todayDate.date()).days)

                for mensagem in MensagensPendentes:
                    nrMensagens = nrMensagens + 1

                context = {
                    "reservas": reservas,
                    "difference": difference,
                    "nrMensagens": nrMensagens,
                    "MensagensPendentes": MensagensPendentes,
                }
                return render(request, "dashboard(resendes).html", context)
    else:
        return render(request, "index.html")


def coworkingSimulation(request):
    r_form = ReservaModelForm()
    reservaprovisoria = reservas_Coworking_provisoria.objects.filter(
        user=request.user)
    reservas = reservas_Coworking.objects.all()
    viewChairs = False
    if request.method == "POST":

        reservaprovisoria.delete()
        standPrice = 0

        dates = request.POST.get("daterange")
        datesTrim = request.POST.get("daterange").replace(" ", "")
        dateSplit = datesTrim.split("-")
        startDateSplit = dateSplit[0].split("/")
        endDateSplit = dateSplit[1].split("/")
        instance = r_form.save(commit=False)
        startdate = datetime(int(startDateSplit[2]), int(
            startDateSplit[0]), int(startDateSplit[1]))
        enddate = datetime(int(endDateSplit[2]), int(
            endDateSplit[0]), int(endDateSplit[1]), 0, 0, 0)
        cadeirasSelecionadas = request.POST.getlist('cadeiras_escolhidas')
        print(cadeirasSelecionadas)
        if '1' in cadeirasSelecionadas:
            instance.chair1 = True
        if '2' in cadeirasSelecionadas:
            instance.chair2 = True
        if '3' in cadeirasSelecionadas:
            instance.chair3 = True
        if '4' in cadeirasSelecionadas:
            instance.chair4 = True
        if '5' in cadeirasSelecionadas:
            instance.chair5 = True
        if '6' in cadeirasSelecionadas:
            instance.chair6 = True
        if '7' in cadeirasSelecionadas:
            instance.chair7 = True
        if '8' in cadeirasSelecionadas:
            instance.chair8 = True
        if '9' in cadeirasSelecionadas:
            instance.chair9 = True
        if '10' in cadeirasSelecionadas:
            instance.chair10 = True
        if '11' in cadeirasSelecionadas:
            instance.chair11 = True
        if '12' in cadeirasSelecionadas:
            instance.chair12 = True

        instance.startDate = startdate
        instance.endDate = enddate
        instance.user = request.user
        nrDias = (datetime(int(endDateSplit[2]), int(endDateSplit[0]), int(
            endDateSplit[1]))-datetime(int(startDateSplit[2]), int(startDateSplit[0]), int(startDateSplit[1]))).days
        if nrDias == 0:
            nrDias = 1
        instance.nrDias = nrDias

        instance.save()

        if nrDias < 30:
            standPrice = 7.14
        if nrDias >= 30 and nrDias <= 90:
            standPrice = 5.33
        if nrDias > 90:
            standPrice = 5

        freeChair = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        reservas = reservas_Coworking.objects.filter(Q(endDate__range=[startdate, enddate]) | Q(
            startDate__range=[startdate, enddate]) | Q(startDate=startdate, endDate=enddate))
        for reserva in reservas:
            if reserva.chair1 == True:
                freeChair.remove(1)
            if reserva.chair2 == True:
                freeChair.remove(2)
            if reserva.chair3 == True:
                freeChair.remove(3)
            if reserva.chair4 == True:
                freeChair.remove(4)
            if reserva.chair5 == True:
                freeChair.remove(5)
            if reserva.chair6 == True:
                freeChair.remove(6)
            if reserva.chair7 == True:
                freeChair.remove(7)
            if reserva.chair8 == True:
                freeChair.remove(8)
            if reserva.chair9 == True:
                freeChair.remove(9)
            if reserva.chair10 == True:
                freeChair.remove(10)

        reservasProv = reservas_Coworking_provisoria.objects.get(
            user=request.user)
        quantaty = get_qty(reservasProv)
        print(get_RealQty(reservasProv))
        if get_RealQty(reservasProv) == 0:
            reservasProv.second_step = False
        else:
            reservasProv.second_step = True

        instance.cost_price = standPrice*quantaty

        instance.save()
        viewChairs = True
        context = {
            "r_form": r_form,
            "dates": dates,
            "startdate": startdate.strftime("%m/%d/%Y"),
            "enddate": enddate.strftime("%m/%d/%Y"),
            "reservaprovisoria": reservaprovisoria,
            "freeChair": freeChair,
            "provPrice": standPrice*quantaty,
            "viewChairs": viewChairs,
            "cadeirasSubmit": reservasProv.second_step,
        }
        return render(request, "coworkingSimulation.html", context)
    startdate = datetime.now().strftime("%m/%d/%Y")
    enddate = datetime.now().strftime("%m/%d/%Y")
    context = {
        "r_form": r_form,
        "startdate": startdate,
        "enddate": enddate,
        "reservaprovisoria": reservaprovisoria,
        "reservas": reservas,
        "viewChairs": viewChairs,
    }

    return render(request, "coworkingSimulation.html", context)


class SuccessView(TemplateView):
    template_name = "success.html"


def meetingRoomPersonalizada(request):
    if request.method == "POST":
        meetingdate = request.POST.get("daterange1", False)
        print(meetingdate)
        starttime = request.POST.get("starttime", False)
        endtime = request.POST.get("endtime", False)
        tempo1 = datetime.strptime(starttime, "%H:%M")
        tempo2 = datetime.strptime(endtime, "%H:%M")
        salasOcupadas = meetingRoomCalendar.objects.filter(
            Q(date=(meetingdate), startTimerange=[tempo1, tempo2])
            | Q(date=(meetingdate), endTimerange=[tempo1, tempo2])
            | Q(date=(meetingdate), startTimelt=starttime, endTimegt=endtime)
        )

        numeroDeSalas = 0
        for sala in salasOcupadas:
            numeroDeSalas = numeroDeSalas + 1

        if numeroDeSalas < 2:
            messages.success(request, str(numeroDeSalas))
        else:
            messages.error(request, str(numeroDeSalas))
        context = {"salasOcupadas": salasOcupadas}
        return render(request, "meetingRoomPersonalizada.html", context)

    else:
        return render(request, "meetingRoomPersonalizada.html")


def gallery(request):

    return render(request, "gallery.html")


def wallet(request):
    reservas = reservas_Coworking.objects.filter(user=request.user)
    reservasMeeting = meetingRoomCalendar.objects.filter(user=request.user)

    nrReservas = len(reservas)
    nrReservasMeeting = len(reservasMeeting)
    context = {
        "nrReservas": nrReservas,
        "reservas": reservas,
        "nrReservasMeeting": nrReservasMeeting,
        "reservasMeeting": reservasMeeting
    }
    return render(request, "wallet.html", context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "caralgo")
        return redirect('signin')
    else:
        messages.error(request, "sdfsf")


def activateEmail(request, user, to_email):
    print("ativar mail")
    mail_subject = "Activate your user account"
    message = render_to_string("activate.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'

    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print("enviou")
        messages.success(
            request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on')
    else:
        print("não enviou")
        messages.error(request, )


def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        print('1')
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print('2')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            ola = form.cleaned_data.get('email')
            print(ola)

            messages.success(
                request, 'Conta criada com sucesso. Entre já!', extra_tags='reg')
            return redirect("signin")
    context = {'form': form}
    return render(request, 'signup.html', context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username", False)
        pass1 = request.POST.get("pass1", False)

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(
                request, "Your username or password are wrong or your mail is not verified. User not authenticate!"
            )
            return redirect("signin")

    else:
        return render(request, "signin.html")


def signout(request):
    logout(request)
    return redirect("index")
