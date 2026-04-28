from django.db import models
from django.contrib.auth.models import User

"""
class User(AbstractUser):
    ROLE_CHOICES = (
        ('lekarz', 'Lekarz'),
        ('admin', 'Administrator'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
"""

class Pacjent(models.Model):
    from django.db import models
from django.utils import timezone

class Pacjent(models.Model):
    identyfikator_pacjenta = models.CharField(max_length=100, blank=True)
    rok_urodzenia = models.IntegerField()
    plec = models.CharField(max_length=20)
    lekarz = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pacjenci')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.identyfikator_pacjenta:
            rok_2_cyfry = str(self.rok_urodzenia)[-2:]
            minuta = timezone.now().strftime('%M')
            self.identyfikator_pacjenta = f"P-{self.id}{rok_2_cyfry}/{minuta}"
            
            super().save(update_fields=['identyfikator_pacjenta'])

    def __str__(self):
        return self.identyfikator_pacjenta


class Badanie(models.Model):
    pacjent = models.ForeignKey(
        Pacjent,
        on_delete=models.CASCADE,
        related_name='badania'
    )
    sciezka_do_pliku = models.TextField()
    data_wgrania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badanie {self.id} - {self.pacjent}"


class WynikAnalizyAI(models.Model):
    badanie = models.OneToOneField(
        Badanie,
        on_delete=models.CASCADE,
        related_name='wynik_ai'
    )
    prawdopodobienstwo_choroby = models.FloatField(help_text="W %")

    def __str__(self):
        return f"Wynik AI dla badania {self.badanie.id}"


class RaportKoncowy(models.Model):
    wynik = models.OneToOneField(
        WynikAnalizyAI,
        on_delete=models.CASCADE,
        related_name='raport'
    )
    notatki_lekarza = models.TextField()
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Raport {self.id}"