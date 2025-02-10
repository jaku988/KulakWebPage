from django import forms
from .models import Reservation
from .widgets import DateTimePickerInput
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'surname', 'phone', 'email', 'time']
        widgets = {
            'time': DateTimePickerInput(attrs={'type': 'datetime-local'}),
        }

    def clean_time(self):
        time = self.cleaned_data.get('time')
        now = timezone.now()

        # Sprawdzenie, czy data jest w przeszłości lub po 2100 roku
        if time < now:
            raise ValidationError("Nie możesz dokonać rezerwacji na przeszłą datę.")
        if time.year > 2100:
            raise ValidationError("Nie możesz dokonać rezerwacji na datę po 2100 roku.")

        # Sprawdzenie, czy data jest w dni powszednie i w godzinach 9:00-17:00
        if time.weekday() >= 5:
            raise ValidationError("Rezerwacji można dokonywać tylko w dni powszednie (pn-pt).")
        if not (9 <= time.hour < 17):
            raise ValidationError("Rezerwacji można dokonywać tylko w godzinach 9:00-17:00.")

        # Pobranie wszystkich istniejących rezerwacji z wyjątkiem obecnej
        reservations = Reservation.objects.exclude(id=self.instance.id).order_by('time')

        # Minimalny odstęp czasu między rezerwacjami
        min_gap = timedelta(hours=1, minutes=30)

        # Znalezienie najbliższego możliwego terminu
        next_available_time = time
        for reservation in reservations:
            reserved_time = reservation.time

            # Jeśli obecny termin koliduje z istniejącą rezerwacją
            if reserved_time - min_gap < next_available_time < reserved_time + min_gap:
                next_available_time = reserved_time + min_gap

        # Ustawienie najbliższego dostępnego terminu na 9:00 w przypadku przekroczenia godzin pracy
        if next_available_time.hour >= 17:
            next_available_time += timedelta(days=1)
            next_available_time = next_available_time.replace(hour=9, minute=0)

        # Ustawienie najbliższego dostępnego terminu na kolejny dzień roboczy w przypadku weekendu
        while next_available_time.weekday() >= 5:  # 5 = sobota, 6 = niedziela
            next_available_time += timedelta(days=1)
            next_available_time = next_available_time.replace(hour=9, minute=0)

        # Jeśli pierwotny czas wybrany przez użytkownika jest niedozwolony, zwracamy błąd
        if next_available_time != time:
            raise ValidationError(
                f"Musi być co najmniej 1,5 godziny odstępu między rezerwacjami. "
                f"Najwcześniejszy możliwy termin rezerwacji to {next_available_time.strftime('%Y-%m-%d %H:%M')}."
            )

        return time
