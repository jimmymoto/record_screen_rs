from django.db import models
from django.contrib.auth.models import User
# Create your models here.
AGENTE = 'AG'
SUPERVISOR = 'SU'
ADMINISTRADOR = 'AD'
TYPE_USER = [
    (AGENTE, 'Agente'),
    (SUPERVISOR, 'Supervisor'),
    (ADMINISTRADOR, 'Administrador'),
]

ASTATUS = [
    ('OK', 'OK'),
    ('FAIL', 'FAIL'),
    ('RUNNING', 'RUNNING')
]


class License(models.Model):
    clientId = models.CharField(max_length=100)
    stateLicense = models.BooleanField(verbose_name="Estado del Usuario")

    class Meta:
        indexes = [
            models.Index(fields=['clientId'])
        ]

    def __str__(self):
        return f"{self.id} | {self.stateLicense}"


class UserGroups(models.Model):
    name = models.CharField(max_length=200)
    users_group = models.ManyToManyField(User)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario plataforma")
    user_groups = models.ManyToManyField(UserGroups, blank=True)
    typeUser = models.CharField(max_length=10, choices=TYPE_USER, verbose_name="Tipo de Usuario")
    licenseUser = models.ForeignKey(License, null=False, on_delete=models.CASCADE, verbose_name="Tipo Licencia")


class Session(models.Model):
    sessionId = models.CharField(max_length=200)
    agente = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Agente con sesion")
    createdAt = models.DateTimeField(
        verbose_name="Creation date", auto_now_add=True, null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['sessionId'])
        ]

    def __str__(self):
        return f"{self.id} | {self.sessionId}"


class Grabaciones(models.Model):
    grabacionesId = models.CharField(max_length=200)
    sessionId = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Sesion asociada")
    name = models.CharField(max_length=200)
    outputMode = models.CharField(max_length=100, blank=True)
    resolution = models.CharField(max_length=20, blank=True, null=True)
    recordingLayout = models.CharField(max_length=20, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    duration = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=4)
    url = models.URLField(blank=True, null=True)
    hasAudio = models.BooleanField(blank=True)
    hasVideo = models.BooleanField(blank=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['grabacionesId'])
        ]

    def __str__(self):
        return f"{self.id} | {self.grabacionesId}"


class GrabAdit(models.Model):
    date = models.DateTimeField(null=False)
    task_name = models.CharField(max_length=200, null=True)
    task_by = models.TextField(max_length=10, null=False)
    value = models.TextField(max_length=10, null=False)
    status = models.CharField(max_length=30, null=True, choices=ASTATUS)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['task_name'])
        ]

    def __str__(self):
        return f"{self.id}"
