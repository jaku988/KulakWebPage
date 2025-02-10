from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from KulakWebPage import settings
from .forms import ReservationForm
from .models import Reservation

def home(request):


    return render(request, 'base/home.html')

def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            cancel_link = request.build_absolute_uri("")

            user_subject = "Rezerwacja"
            user_message = (f'Rezerwacja na dane\n'
                            f'{reservation.name} {reservation.surname}\n'
                            f'{reservation.time.strftime('%H:%M')} {reservation.time.strftime('%d.%m.%Y')}\n'
                            f'potwierdzona.\n'
                            f'Kod anulowania rezerwacji: {reservation.cancel_code}\n')
            send_mail(user_subject, user_message, settings.EMAIL_HOST_USER, [reservation.email], fail_silently=False)

            admin_subject = "Nowa rezerwacja"
            admin_message = (f'Nowa rezerwacja na dane:\n'
                             f'Imie: {reservation.name}\n'
                             f'Nazwisko: {reservation.surname}\n'
                             f'Data: {reservation.time.strftime('%d.%m.%Y')}\n'
                             f'Godzina: {reservation.time.strftime('%H:%M')}\n'
                             f'Kontakt: {reservation.phone} {reservation.email}\n')
            send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, ['mineface98@gmail.com'], fail_silently=False)

            return HttpResponse('Success!')
    else:
        form = ReservationForm()

    context = {
        "form": form
    }

    return render(request, 'base/reservation_page.html', context)