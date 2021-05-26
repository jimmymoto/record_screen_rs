from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .forms import *
from datetime import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from grabaciones.tasks import record_init, stop_init
# Create your views here.


#@basicauth
def inicio(request):
    form = ""
    sessiones = ""
    if request.user.is_anonymous != True:
        try:
            usuario = UserProfile.objects.get(user=request.user)
            if usuario.licenseUser.stateLicense:
                if request.method == "POST":
                    form = FormSession(data=request.POST)
                    if form.is_valid():
                        sesion = Session.objects.create(sessionId=form.data['sessionId'], agente=request.user)
                        if request.user.userprofile.licenseUser.stateLicense:
                            sessionId = sesion.sessionId
                            clientId = request.user.userprofile.licenseUser.clientId
                            datesession = datetime.strftime(datetime.strptime(str(sesion.createdAt)[:19],
                                                                              '%Y-%m-%d %H:%M:%S'),  "%Y_%m_%d_%H_%M_%S")
                            name_session = sessionId + '_' + clientId + '_' + datesession
                            datasession = '{"mediaMode": "ROUTED","recordingMode": "MANUAL","customSessionId": "' + \
                                          name_session + '","defaultOutputMode": "COMPOSED"}'
                            headers = {'Content-Type': 'application/json'}
                            url_api = settings.SECRETS['URL_APP'] + '/api/sessions'
                            response = requests.post(url_api, headers=headers, auth=(settings.SECRETS['URL_USER'],
                                                                                     settings.SECRETS['URL_PASS']),
                                                     data=str(datasession))
                            if response.status_code == 200:
                                return HttpResponseRedirect('grabaciones/inicio.html?sessionId=' + str(sesion.id))
                            else:
                                messages.info(request, f"No se pudo redirigir la sessión.")
                    else:
                        messages.info(request, f"No se pudo crear la sessión.")
                    return redirect('/')
                else:
                    try:
                        form = FormSession()
                        sessiones = Session.objects.filter(agente=request.user)
                    except ObjectDoesNotExist:
                        messages.warning(request, f"El usuario no ha creado sessiones.")
                        pass
        except ObjectDoesNotExist:
            messages.warning(request, f"El usuario no esta autorizado.")
            pass

    context = {'form': form, 'sessiones': sessiones}
    return render(request, "sessiones/inicio.html", context)


def grabaciones(request):
    name_session = ''
    idsession = ''
    status = False
    if request.method == "POST":
        if request.POST['namesession'] is not None and request.POST['idsession'] is not None:
            namesession = request.POST['namesession']
            idsession = Session.objects.get(id=request.POST['idsession'])
            if request.POST.get('stop_grab'):
                stop_record = stop_init(grabacionesId=request.POST['namesession'])
                if stop_record:
                    return HttpResponseRedirect('inicio.html?sessionId=' + str(idsession.id))
                else:
                    return HttpResponse("No Data Valid")
            else:
                graba = Grabaciones.objects.update_or_create(grabacionesId=namesession, sessionId=idsession,
                                                   name=namesession, outputMode="COMPOSED",
                                                   hasAudio=True, hasVideo=True, status="ready")

                record = record_init.delay(grabacionesId=request.POST['namesession'], max_retries=0)
                return HttpResponseRedirect('inicio.html?sessionId=' + str(idsession.id) + '&status_grab=true')
    if request.method == "GET":
        if request.GET.get('sessionId') is not None:
            sessionid = Session.objects.get(id=request.GET['sessionId'])
            idsession = sessionid.sessionId
            idcreated = sessionid.createdAt
            clientId = request.user.userprofile.licenseUser.clientId
            datesession = datetime.strftime(datetime.strptime(str(idcreated)[:19],
                                                              '%Y-%m-%d %H:%M:%S'), "%Y_%m_%d_%H_%M_%S")
            name_session = str(idsession) + '_' + clientId + '_' + datesession
            grabaciones = Grabaciones.objects.filter(sessionId=sessionid.id)
        else:
            idsession = ''
            name_session = ''
            grabaciones = Grabaciones.objects.all()
    status_grab = True if request.GET.get('status_grab', None) else False
    grab_real = True if len(grabaciones) > 0 else False
    form = FormGrabacion()
    context = {'form': form, 'grabaciones': grabaciones,
               'namesession': name_session, 'idsession': sessionid.id, 'url_api': settings.SECRETS['URL_APP'],
               'status_grab': status_grab, 'grab_real': grab_real}
    return render(request, "grabaciones/inicio.html", context)


def editar_session(request, pk):
    session = Session.objects.get(sessionId=pk)
    form = FormSession(instance=session)
    context = {'form': form, 'url_api': settings.SECRETS['URL_APP']}
    return render(request, 'sessiones/editar_session.html', context)


def editar_grabacion(request, pk):
    grabacion = Grabaciones.objects.get(sessionId=pk)
    form = FormSession(instance=grabacion)
    context = {'form': form, 'url_api': settings.SECRETS['URL_APP']}
    return render(request, 'grabaciones/editar_grabacion.html', context)


def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            nombre_usuario = form.cleaned_data.get('username')
            messages.success(request, f"Nueva cuenta creada: {nombre_usuario}")
            login(request, usuario)
            messages.info(request, f"Usuario logueado: {nombre_usuario}")
            return redirect("grabaciones:inicio")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = UserCreationForm
    return render(request, "principal/registro.html", {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Usuario deslogueado")
    return redirect("grabaciones:inicio")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasena = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contrasena)
            if user is not None:
                login(request, user)
                messages.info(request, f"Usuario {usuario} logueado")
                return redirect("grabaciones:inicio")
            else:
                messages.error(request, "Usuario o contraseña equivocada")
        else:
            messages.error(request, "Usuario o contraseña equivocada")

    form = AuthenticationForm()
    return render(request, "principal/login.html", {"form": form})
