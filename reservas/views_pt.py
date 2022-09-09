import datetime
from datetime import date, datetime, timedelta
from email import message
from multiprocessing import context
from re import T
from sre_constants import SUCCESS
from time import time

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import (
    Product,
    Wallet,
    meetingRoomCalendar,
    meetingRoomProvisoria,
    reservas_Coworking,
    reservas_Coworking_provisoria,
    Price,
)
from django.db.models import Q
from reservas.models import mensagen

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


def coworkingTanks(request):
    if request.method == "POST":
        if request.POST.get("paymentStatus_input"):
            success = request.POST.get("paymentStatus_input")
            if success:
                user_wallet = Wallet.objects.get(user=request.user)

                reserva_provisoria = reservas_Coworking_provisoria.objects.get(
                    user=request.user)

                multipy_nr = reserva_provisoria.nrDias / 7
                user_wallet.mettingRoomHours = user_wallet.mettingRoomHours+multipy_nr*2
                user_wallet.save()

                nr_Lugares = get_RealQty(reserva_provisoria)
                reservas_Coworking.objects.create(
                    user=request.user,
                    nrLugares=nr_Lugares,
                    startDate=reserva_provisoria.startDate,
                    endDate=reserva_provisoria.endDate,
                    nrDias=reserva_provisoria.nrDias,
                    cost_price=reserva_provisoria.cost_price,
                    chair1=reserva_provisoria.chair1,
                    chair2=reserva_provisoria.chair2,
                    chair3=reserva_provisoria.chair3,
                    chair4=reserva_provisoria.chair4,
                    chair5=reserva_provisoria.chair5,
                    chair6=reserva_provisoria.chair6,
                    chair7=reserva_provisoria.chair7,
                    chair8=reserva_provisoria.chair8,
                    chair9=reserva_provisoria.chair9,
                    chair10=reserva_provisoria.chair10,
                    chair11=reserva_provisoria.chair11,
                    chair12=reserva_provisoria.chair12,
                )
                reserva_provisoria.delete()
            return redirect("wallet")
    return render(request, "tanks_coworking.html")


def m5Thanks(request):
    if request.method == "POST":
        if request.POST.get("paymentStatus_input"):
            success = request.POST.get("paymentStatus_input")
            if success:
                user_wallet = Wallet.objects.get(user=request.user)
                user_wallet.mettingRoomHours = user_wallet.mettingRoomHours+5
                return redirect("wallet")
    return render(request, "m5thanks.html")


def m10Thanks(request):
    if request.method == "POST":
        if request.POST.get("paymentStatus_input"):
            success = request.POST.get("paymentStatus_input")
            if success:
                user_wallet = Wallet.objects.get(user=request.user)
                user_wallet.mettingRoomHours += 10
                return redirect("wallet")
    return render(request, "m5thanks.html")


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            all_users = get_user_model().objects.all()
            all_reservas = reservas_Coworking.objects.all()
            nrMensagens = mensagen.objects.all()
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
            if not Wallet.objects.filter(user=request.user):
                Wallet.objects.create(user=request.user, mettingRoomHours=0, mettingRoomMinutes=0)
            if request.method == "POST":
                if request.POST.get("Industry"):
                    name = request.POST.get("name", False)
                    Industry = request.POST.get("Industry")
                    employees = request.POST.get("employees", False)
                    description = request.POST.get("description")
                    mensagen.objects.create(
                        user=request.user,
                        date=datetime.now(),
                        ClientName=name,
                        Reason=Industry,
                        ClientEmail=request.user.email,
                        ClientMessage=description,
                    )

                    return redirect("index_pt")
                if request.POST.get("paymentStatus_input"):
                    success = request.POST.get("paymentStatus_input")
                    if success:
                        reserva_provisoria = reservas_Coworking_provisoria.objects.get(
                            user=request.user)
                        nr_Lugares = get_RealQty(reserva_provisoria)
                        reservas_Coworking.objects.create(
                            user=request.user,
                            nrLugares=nr_Lugares,
                            startDate=reserva_provisoria.startDate,
                            endDate=reserva_provisoria.endDate,
                            nrDias=reserva_provisoria.nrDias,
                            cost_price=reserva_provisoria.cost_price,
                            chair1=reserva_provisoria.chair1,
                            chair2=reserva_provisoria.chair2,
                            chair3=reserva_provisoria.chair3,
                            chair4=reserva_provisoria.chair4,
                            chair5=reserva_provisoria.chair5,
                            chair6=reserva_provisoria.chair6,
                            chair7=reserva_provisoria.chair7,
                            chair8=reserva_provisoria.chair8,
                            chair9=reserva_provisoria.chair9,
                            chair10=reserva_provisoria.chair10,
                            chair11=reserva_provisoria.chair11,
                            chair12=reserva_provisoria.chair12,
                        )
                        reserva_provisoria.delete()
                    return redirect("index_pt")
            else:
                context = {
                    "user": request.user,
                }
                return render(request, "templates_pt/dashboard(resendes).html", context)
    else:
        return render(request, "templates_pt/index.html")


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
        reservas = []
        for r in reservas_Coworking.objects.all():
            if startdate.date() == r.startDate or enddate.date() == r.endDate:
                reservas.append(r)
            elif startdate.date() < r.startDate < enddate.date():
                reservas.append(r)
            elif startdate.date() < r.endDate < enddate.date():
                reservas.append(r)
            elif startdate.date() > r.startDate and enddate.date() < r.endDate:
                reservas.append(r)

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
        nrChairs = get_RealQty(reservasProv)
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
            "nrChairs": nrChairs,
            "reservaprovisoria": reservasProv,
            "freeChair": freeChair,
            "provPrice": standPrice*quantaty,
            "viewChairs": viewChairs,
            "cadeirasSubmit": reservasProv.second_step,
        }
        return render(request, "templates_pt/coworkingSimulation.html", context)
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

    return render(request, "templates_pt/coworkingSimulation.html", context)


class SuccessView(TemplateView):
    template_name = "success.html"


def meetingRoomPersonalizada(request):
    if request.method == "POST":
        user_wallet = Wallet.objects.get(user=request.user)
        meetingRoomProv = meetingRoomProvisoria.objects.get(user=request.user)

        if request.POST.get("daterange1"):
            print("ENTROU dateRange")
            meetingRoomProv.delete()
            meetingdate = request.POST.get("daterange1", False)
            startTime = request.POST.get("starttime")
            endTime = request.POST.get("endtime")
            meetingdate.replace(" ", "")
            disponibilidade = True
            dateSplit = meetingdate.split("/")
            meetingDate_Format = datetime(
                int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1]))

            startTime = datetime.strptime(startTime, '%H:%M').time()
            endTime = datetime.strptime(endTime, '%H:%M').time()

            salasDisponiveis = []
            z = 0
            meetingRoom_bydate = meetingRoomCalendar.objects.filter(
                date=meetingDate_Format)

            for reservaMeeting in meetingRoom_bydate:
                if reservaMeeting.startTime == startTime or reservaMeeting.endTime == endTime:
                    salasDisponiveis.append(z)

                elif reservaMeeting.startTime < startTime < reservaMeeting.endTime:
                    salasDisponiveis.append(z)

                elif reservaMeeting.startTime < endTime < reservaMeeting.endTime:
                    salasDisponiveis.append(z)

                elif reservaMeeting.startTime > startTime and reservaMeeting.endTime < endTime:
                    salasDisponiveis.append(z)

                elif reservaMeeting.startTime < startTime and reservaMeeting.endTime > endTime:
                    salasDisponiveis.append(z)

                z += 1

            if len(salasDisponiveis) > 1:
                disponibilidade = False

            meetingRoomProvisoria.objects.create(
                user=request.user,
                date=meetingDate_Format,
                startTime=startTime,
                endTime=endTime
            )

            payWallet = False
            reservationTime = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
            
            print("reservation time")
            print(reservationTime)

            userHours = user_wallet.mettingRoomHours
            userMinutes = user_wallet.mettingRoomMinutes
            date_test = str(userHours)+':'+str(userMinutes)
            datem = datetime.strptime(date_test, "%H:%M")
            
            if datem.hour * 60 + datem.minute >= (reservationTime.seconds/60):
                payWallet = True

            price = 10*reservationTime.seconds/60/60

            if reservationTime.seconds/60/60 > 5:
                price = 8*reservationTime.seconds/60/60
            elif reservationTime.seconds/60/60 > 10:
                price = 7*reservationTime.seconds/60/60

            price = round(price, 2)

            second_step = True

            context = {
                "second_step": second_step,
                "price": price,
                "startdate": meetingdate,
                "startTime": startTime,
                "endTime": endTime,
                "walletHours": str(user_wallet.mettingRoomHours)+":"+str(user_wallet.mettingRoomMinutes),
                "disponibilidade": disponibilidade,
                "payWallet": payWallet,
                "startValeu": request.POST.get("starttime"),
                "endValeu": request.POST.get("endtime")
            }

            return render(request, "meetingRoomPersonalizada.html", context)
        
        if request.POST.get("useWallet"):
            print("ENTROU wallet")
            startTime = meetingRoomProv.startTime
            endTime = meetingRoomProv.endTime
            reservationTime = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
            
            userHours = user_wallet.mettingRoomHours
            userMinutes = user_wallet.mettingRoomMinutes
            date_test = str(userHours)+':'+str(userMinutes)
            datem = datetime.strptime(date_test, "%H:%M")
            userTime=datem-reservationTime

            user_wallet.mettingRoomHours=userTime.hour
            user_wallet.mettingRoomMinutes=userTime.minute
            user_wallet.save()
            
            meetingRoomCalendar.objects.create(user=meetingRoomProv.user,
                                               date=meetingRoomProv.date,
                                               startTime=meetingRoomProv.startTime,
                                               endTime=meetingRoomProv.endTime)
            print("-------")
            print(user_wallet.mettingRoomHours)
            print("-------")
            return redirect('wallet')

    else:
        context = {
            "startdate": '08/11/2022',
        }
        return render(request, "meetingRoomPersonalizada.html", context)


def gallery(request):

    return render(request, "templates_pt/gallery.html")


def wallet(request):
    reservas = reservas_Coworking.objects.filter(user=request.user)
    reservasMeeting = meetingRoomCalendar.objects.filter(user=request.user)
    user_wallet = Wallet.objects.get(user=request.user)
    userHours = user_wallet.mettingRoomHours
    userMinutes = user_wallet.mettingRoomMinutes
    date = str(userHours)+':'+str(userMinutes)
    datem = datetime.strptime(date, "%H:%M")
    print(datem.hour) # 11.
    print(datem.minute) # 22.
   
   
   
    #zeroHours = datetime.combine(date.today(
    #), user_wallet.mettingRoomHours) - datetime.combine(date.today(
    #), user_wallet.mettingRoomHours)
    #mettingRoomHours = timedelta(user_wallet.mettingRoomHours)
   
    
    nrReservas = len(reservas)
    nrReservasMeeting = len(reservasMeeting)
    context = {
        "nrReservas": nrReservas,
        "reservas": reservas,
        "meetingRoomHours": userHours,
         "meetingRoomMinutes": userMinutes,
        "nrReservasMeeting": nrReservasMeeting,
        "reservasMeeting": reservasMeeting,
        
    }
    return render(request, "templates_pt/wallet.html", context)


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
    accounts = User.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            for user in accounts:
                if form.cleaned_data.get('email') == user.email:
                    messages.warning(request, 'email already exists.')
                    context = {'form': form}
                    return render(request, 'signup.html', context)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            messages.success(
                request, 'Conta criada com sucesso. Entre já!', extra_tags='reg')
            return redirect("signin")
    context = {'form': form}
    return render(request, 'templates_pt/signup.html', context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username", False)
        pass1 = request.POST.get("pass1", False)

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect("index_pt")
        else:
            messages.error(
                request, "Your username or password are wrong or your mail is not verified. User not authenticate!"
            )
            return redirect("signin_pt")

    else:
        return render(request, "templates_pt/signin.html")


def signout(request):
    logout(request)
    return redirect("index_pt")
