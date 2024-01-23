from django.shortcuts import render
from .models import Selinux, SElinuxEvent, SetroubleshootEntry
from rest_framework import viewsets, generics
from .models import SElinuxEvent, message, suggestion, SetroubleshootEntry
from .serializers import SElinuxEventSerializer, SelinuxDataSerializer, SetroubleshootEntrySerializer, messageSerializer, suggestionSerializer
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import pprint
from .models import Selinux, SElinuxEvent

from .forms import suggestionForm



@csrf_exempt
def host_message_sugestion(request, hostname, message):
    # Get the message for the specified host
    host_message = get_object_or_404(suggestion, hostname=hostname, message=message)

    context = {
        'host_message': host_message,
    }

    return render(request, 'host_message_suggestion_template.html', context)


@csrf_exempt
def selinux_list(request):
    try:
        selinux_entries = Selinux.objects.all()
    except Selinux.DoesNotExist:
        selinux_entries = {}
    return render(request, 'selinux_list.html', {'selinux_entries': selinux_entries})

@csrf_exempt
def message_list(request, pk=None):
    if pk:
        messages = message.objects.filter(hostname=pk)
    else:
        messages = message.objects.all()
    return render(request, 'message_list.html', {'messages': messages})

@csrf_exempt
def suggestion_list(request, pk=None, message=None):
    suggestions = suggestion.objects.all()
    return render(request, 'suggestion_list.html', {'suggestions': suggestions})



@csrf_exempt
def SetroubleshootEntry_list_full(request):
    events = SetroubleshootEntry.objects.all()
    return render(request, 'SetroubleshootEntry_list_full.html', {'events': events})

@csrf_exempt
def SetroubleshootEntry_list(request):
    events = SetroubleshootEntry.objects.all()
    return render(request, 'SetroubleshootEntry_list.html', {'events': events})

@csrf_exempt
def SetroubleshootEntry_host(request, hostname):
    entries = SetroubleshootEntry.objects.filter(HOSTNAME=hostname).order_by('realtime_timestamp')
    context = {'entries': entries, 'hostname': hostname}
    return render(request, 'SetroubleshootEntry_list.html', context)

@csrf_exempt
class selinuxAPIview(generics.CreateAPIView):
    queryset = Selinux.objects.all()
    serializer_class = SelinuxDataSerializer

@csrf_exempt
class SetroubleshootEntryAPIview(generics.CreateAPIView):
    queryset = SetroubleshootEntry.objects.all()
    serializer_class = SetroubleshootEntrySerializer

@csrf_exempt
class messageAPIview(generics.CreateAPIView):
    queryset = message.objects.all()
    serializer_class = messageSerializer

@csrf_exempt
class suggestionAPIview(generics.CreateAPIView):
    queryset = suggestion.objects.all()
    serializer_class =suggestionSerializer

@method_decorator(csrf_exempt, name='dispatch')
@csrf_exempt
class UploadSelinuxDataView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Assuming 'hostname' is a unique key
            hostname = data.get('hostname')

            selinux_instance, created = Selinux.objects.update_or_create(
                hostname=hostname,
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {hostname} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {hostname} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    
@csrf_exempt
def selinux_event_list(request):
    selinux_event_entries = SElinuxEvent.objects.all()
    pprint.pprint(selinux_event_entries)

    return render(request, 'selinux_event_list.html', {'selinux_event_entries': selinux_event_entries})


@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class UploadSElinuxEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            digest = data.get('digest')

            SElinuxEvent_instance, created = SElinuxEvent.objects.update_or_create(
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {digest} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {digest} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        

@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class SetroubleshootEntryView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            cursor = data.get('cursor')

            SetroubleshootEntry_instance, created = SetroubleshootEntry.objects.update_or_create(
                defaults=data
            )

            if created:
                return JsonResponse({'message': f'Data for {cursor} created successfully.'}, status=201)
            else:
                return JsonResponse({'message': f'Data for {cursor} updated successfully.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        
# views.py
@csrf_exempt
def host_message(request, pk=None):
    # Get the message for the specified host
    host_message = get_object_or_404(message, digest=pk)
    suggestions = suggestion.objects.filter(messagedigest=pk)
    if request.method == 'POST':
        form = suggestionForm (request.POST)
        if form.is_valid():
            form.save()
    else:
        form = suggestionForm()

    context = {
        'host_message': host_message,
        'suggestions': suggestions,
        'form': form,
    }

    return render(request, 'host_message_template.html', context)
