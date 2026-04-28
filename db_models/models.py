from django.db import models
from django.contrib.auth.models import User


class Pacjent(models.Model):
    identyfikator_pacjenta = models.CharField(max_length=100, unique=True)
    rok_urodzenia = models.IntegerField()
    plec = models.CharField(max_length=10)

    lekarz = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pacjenci'
    )

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