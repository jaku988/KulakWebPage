from django.db import models
from django.utils.crypto import get_random_string


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    time = models.DateTimeField()
    cancel_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.cancel_code:  # Generowanie kodu tylko, gdy nie istnieje
            while True:
                new_code = get_random_string(10)
                if not Reservation.objects.filter(cancel_code=new_code).exists():
                    self.cancel_code = new_code
                    break
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.surname} {self.phone} --- {self.time}'
