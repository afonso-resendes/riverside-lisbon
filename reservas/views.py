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
    AcmeWebhookMessage,
    bundleProvisorio,
    transaction
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
import json
from .tokens import account_activation_token
from Cryptodome.Cipher import AES

import base64




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

@csrf_exempt
def coworkingTanks(request):
    if request.method=="POST":
        payload = request.body
        authTag=request.headers["X-Authentication-Tag"]
        iv=request.headers["X-Initialization-Vector"]
        secretKey="jeGJfbaWQO2zurC2tM7nMuo7ZD9E12dVZZgb+qa3+PA="
        decryptedBody=json.loads(decrypt_AES_GCM(payload, authTag, secretKey, iv).decode('utf8').replace("'", '"'))
        checkWebhook(decryptedBody, request)
        statusMsg = decryptedBody['returnStatus']['statusMsg']
        notificationID = decryptedBody["notificationID"]
        statusCode=decryptedBody['returnStatus']['statusCode']
        data = {
            'statusCode': statusCode,
            'statusMsg': statusMsg,
            'notificationID': notificationID
        }
        return JsonResponse(data)
    else:
        return HttpResponse("ups!")

def decrypt_AES_GCM(encryptedMsg, authTag, secretKey, iv):
    iv = base64.b64decode(iv)
    encryptedMsg = base64.b64decode(encryptedMsg)
    secretKey = base64.b64decode(secretKey)
    authTag = base64.b64decode(authTag)
    aesCipher = AES.new(secretKey, AES.MODE_GCM, iv)
    plaintext = aesCipher.decrypt_and_verify(encryptedMsg, authTag)
    return plaintext

def checkWebhook(payload, request):
    transactions=transaction.objects.get(transactionId=payload['transactionID'])
    print(transactions)
    print(transactions.transactionId)
    transactions.status=payload['paymentStatus']
    transactions.save() 
    try:
        reserva_cow_prov=reservas_Coworking_provisoria.objects.get(transactionId=payload['transactionID'])
        if reserva_cow_prov and payload['paymentStatus']=='Success':
            print("reserva_cow_prov")
            reservas_Coworking.objects.create(
                user=reserva_cow_prov.user,
                nrLugares=get_RealQty(reserva_cow_prov),
                startDate=reserva_cow_prov.startDate,
                endDate=reserva_cow_prov.endDate,
                nrDias=reserva_cow_prov.nrDias,
                cost_price=reserva_cow_prov.cost_price,
                chair1=reserva_cow_prov.chair1,
                chair2=reserva_cow_prov.chair2,
                chair3=reserva_cow_prov.chair3,
                chair4=reserva_cow_prov.chair4,
                chair5=reserva_cow_prov.chair5,
                chair6=reserva_cow_prov.chair6,
                chair7=reserva_cow_prov.chair7,
                chair8=reserva_cow_prov.chair8,
                chair9=reserva_cow_prov.chair9,
                chair10=reserva_cow_prov.chair10,
                chair11=reserva_cow_prov.chair11,
                chair12=reserva_cow_prov.chair12
                )
            confirmPurchase(request, reserva_cow_prov.user, reserva_cow_prov.user.email)
    except:
        try:
            meet_prov=meetingRoomProvisoria.objects.get(transactionId=payload['transactionID'])
            if meet_prov and payload['paymentStatus']=='Success':
                print("meet_prov")
                meetingRoomCalendar.objects.create(
                    user = meet_prov.user,
                    date = meet_prov.date,
                    startTime =meet_prov.startTime,
                    endTime = meet_prov.endTime,
                    cost_price =  meet_prov.cost_price
                )
                confirmPurchase(request, meet_prov.user, reserva_cow_prov.user.email)
        except:
            try:
                bundle_prov=bundleProvisorio.objects.get(transaction_id=payload['transactionID'])
                if bundle_prov and payload['paymentStatus']=='Success':
                    print("bundle_prov")
                    user_wallet=Wallet.objects.get(user=bundle_prov.user)
                    if bundle_prov.bundle_5:
                        user_wallet.mettingRoomHours=user_wallet.mettingRoomHours+5
                        user_wallet.save()
                        confirmPurchase(request, meet_prov.user, reserva_cow_prov.user.email)

                    elif bundle_prov.bundle_10:
                        user_wallet.mettingRoomHours=user_wallet.mettingRoomHours+10
                        user_wallet.save()
                        confirmPurchase(request, meet_prov.user, reserva_cow_prov.user.email)
            except:
                pass

def cancelation(request, transactionID=None):
    if request.user.is_superuser:
        return render(request, "cancelation.html")
    else:
        return redirect('index')
def index(request, price=None, payment_Method=None, payment_status=None, transactionID=None):
    if price and payment_Method and payment_status and transactionID:
        try:
            transaction.objects.get(transactionId=transactionID)
        except:
            transaction.objects.create(
                            user=request.user,
                            transactionId=transactionID,
                            status = payment_status,
                            payment_Method = payment_Method,
                            price = float(price),
                        )
        return render(request, "dashboard(resendes).html")

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
                    return redirect("index")
            else:
                context = {
                    "user": request.user,
                }
                return render(request, "dashboard(resendes).html", context)
    else:
        return render(request, "index.html")


def coworkingSimulation(request, spgContext=None, transactionID=None, transactionSignature=None):
    r_form = ReservaModelForm()
    reservaprovisoria = reservas_Coworking_provisoria.objects.filter(
        user=request.user.id)
    reservas = reservas_Coworking.objects.all()
    viewChairs = False
    if transactionID:
        print(transactionID)
        reserva_prov=reservas_Coworking_provisoria.objects.get(user=request.user.id)
        reserva_prov.transactionId=transactionID
        reserva_prov.save()
        context = {
            "dates": str(reserva_prov.startDate)+" / "+str(reserva_prov.endDate),
            "nrChairs": get_RealQty(reserva_prov),
            "reservaprovisoria": reserva_prov,
            "provPrice": round(reserva_prov.cost_price, 2),
        }
        return render(request, "coworkingSimulation.html", context)
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
                try:
                    freeChair.remove(1)
                except:
                    pass
            if reserva.chair2 == True:
                try:
                    freeChair.remove(2)
                except:
                    pass
            if reserva.chair3 == True:
                try:
                    freeChair.remove(3)
                except:
                    pass
            if reserva.chair4 == True:
                try:
                    freeChair.remove(4)
                except:
                    pass
            if reserva.chair5 == True:
                try:
                    freeChair.remove(5)
                except:
                    pass
            if reserva.chair6 == True:
                try:
                    freeChair.remove(6)
                except:
                    pass
            if reserva.chair7 == True:
                try:
                    freeChair.remove(7)
                except:
                    pass
            if reserva.chair8 == True:
                try:
                    freeChair.remove(8)
                except:
                    pass
            if reserva.chair9 == True:
                try:
                    freeChair.remove(9)
                except:
                    pass
            if reserva.chair10 == True:
                try:
                    freeChair.remove(10)
                except:
                    pass
            if reserva.chair11 == True:
                try:
                    freeChair.remove(11)
                except:
                    pass
            if reserva.chair12 == True:
                try:
                    freeChair.remove(12)
                except:
                    pass

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
            "provPrice": round(standPrice*quantaty, 2),
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


def meetingRoomPersonalizada(request, spgContext=None, transactionID=None, transactionSignature=None, bundleType=None):
    if transactionID:
        if bundleType:
            if bundleType=="5":
                bundleProvisorio.objects.create(
                    user=request.user,
                    bundle_5=True,
                    bundle_10=False,
                    transaction_id=transactionID
                )
                price=50
                context={
                    "price": price,
                }
                return render(request, "meetingRoomPersonalizada.html", context)
            elif bundleType=="10":
                bundleProvisorio.objects.create(
                    user=request.user,
                    bundle_5=False,
                    bundle_10=True,
                    transaction_id=transactionID
                )
                price=90
                context={
                    "price": price,
                }
                return render(request, "meetingRoomPersonalizada.html", context)


        print(transactionID)
        user_wallet = Wallet.objects.get(user=request.user)
        meet_prov=meetingRoomProvisoria.objects.get(user=request.user.id)
        meet_prov.transactionId=transactionID
        meet_prov.save()
        context = {
            "price": meet_prov.cost_price,
            "startdate": meet_prov.date,
            "startTime": meet_prov.startTime,
            "endTime": meet_prov.endTime,
            "price":meet_prov.cost_price,
            "walletHours": str(user_wallet.mettingRoomHours)+":"+str(user_wallet.mettingRoomMinutes),
        }
        return render(request, "meetingRoomPersonalizada.html", context)
    if request.method == "POST":
        user_wallet = Wallet.objects.get(user=request.user)
        try:
            meetingRoomProv = meetingRoomProvisoria.objects.get(user=request.user)
        except:
            pass
        if request.POST.get("daterange1"):
            try:
                meetingRoomProv.delete()
            except:
                pass
            meetingdate = request.POST.get("daterange1", False)
            startHour = int(request.POST.get("startHour"))
            startMinute = int(request.POST.get("startMinute"))
            startAm_PM = request.POST.get("startAm_PM")
            endHour = int(request.POST.get("endHour"))
            endMinute = int(request.POST.get("endMinute"))
            endAm_PM = request.POST.get("endAm_PM")
            meetingdate.replace(" ", "")
            disponibilidade = True
            dateSplit = meetingdate.split("/")
            meetingDate_Format = datetime(
                int(dateSplit[2]), int(dateSplit[0]), int(dateSplit[1]))
            
            if startAm_PM == "PM":
                if startHour == 12:
                    startHour = 0
                else:
                    startHour += 12
            if endAm_PM == "PM":
                if endHour == 12:
                    endHour = 0
                else:
                    endHour += 12
            s_date = str(startHour)+':'+str(startMinute)
            e_date = str(endHour)+':'+str(endMinute)

                

            startTime = datetime.strptime(s_date, '%H:%M').time()
            endTime = datetime.strptime(e_date, '%H:%M').time()

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


            payWallet = False
            reservationTime = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
            splitRT = str(reservationTime).split(":")
            reservationHour = int(splitRT[0])
            reservationMinute = int(splitRT[1])

            userHours = user_wallet.mettingRoomHours
            userMinutes = user_wallet.mettingRoomMinutes
    

            if userHours > reservationHour:
                left_user_hour = userHours - reservationHour
                if userMinutes > reservationMinute:
                    left_user_minute = userMinutes - reservationMinute
                else:
                    left_user_hour -= 1
                    left_user_minute = 60 - reservationMinute + userMinutes
                    if left_user_minute == 60:
                        left_user_minute = 0
                        left_user_hour += 1
            

            if left_user_hour * 60 + left_user_minute >= (reservationTime.seconds/60):
                payWallet = True

            price = 10*reservationTime.seconds/60/60

            if reservationTime.seconds/60/60 > 5:
                price = 8*reservationTime.seconds/60/60
            elif reservationTime.seconds/60/60 > 10:
                price = 7*reservationTime.seconds/60/60

            price = round(price, 2)

            second_step = True

            meetingRoomProvisoria.objects.create(
                user=request.user,
                date=meetingDate_Format,
                startTime=startTime,
                endTime=endTime,
                cost_price=price
            )
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
                "endValeu": request.POST.get("endtime"),
                "customer_name": request.user.username,
                "customer_mail":request.user.email
            }

            return render(request, "meetingRoomPersonalizada.html", context)

        if request.POST.get("useWallet"):
            startTime = meetingRoomProv.startTime
            endTime = meetingRoomProv.endTime
            reservationTime = datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)

            userHours = user_wallet.mettingRoomHours
            userMinutes = user_wallet.mettingRoomMinutes
            
            
            splitRT = str(reservationTime).split(":")
            reservationHour = int(splitRT[0])
            reservationMinute = int(splitRT[1])
            userHours = user_wallet.mettingRoomHours
            userMinutes = user_wallet.mettingRoomMinutes
            if userHours > reservationHour:
                left_user_hour = userHours - reservationHour
                if userMinutes > reservationMinute:
                    left_user_minute = userMinutes - reservationMinute
                else:
                    left_user_hour -= 1
                    left_user_minute = 60 - reservationMinute + userMinutes
                    if left_user_minute == 60:
                        left_user_minute = 0
                        left_user_hour += 1
            

            user_wallet.mettingRoomHours=left_user_hour
            user_wallet.mettingRoomMinutes=left_user_minute
            user_wallet.save()

            meetingRoomCalendar.objects.create(user=meetingRoomProv.user,
                                               date=meetingRoomProv.date,
                                               startTime=meetingRoomProv.startTime,
                                               endTime=meetingRoomProv.endTime)

            return redirect('wallet')

    else:
        context = {
            "startdate": '08/11/2022',
        }
        return render(request, "meetingRoomPersonalizada.html", context)


def gallery(request):

    return render(request, "gallery.html")


def wallet(request):
    reservas = reservas_Coworking.objects.filter(user=request.user.id)
    reservasMeeting = meetingRoomCalendar.objects.filter(user=request.user)
    user_wallet = Wallet.objects.get(user=request.user)
    userHours = user_wallet.mettingRoomHours
    userMinutes = user_wallet.mettingRoomMinutes
    
    print(request.user)
    print(request.user.email)







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

        messages.success(request, "success")
        return redirect('signin')
    else:
        messages.error(request, "error")


def activateEmail(request, user, to_email):
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
        messages.success(
            request, f'Dear {user}, please go to your emai x{to_email} inbox and click on')
    else:
        messages.error(request, )

def confirmPurchase(request, user, to_email):
    mail_subject = "Activate your user account"
    message = render_to_string("confirmPurchase.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http'

    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on')
    else:
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