# selinux/serializers.py

from rest_framework import serializers
from .models import Selinux, SElinuxEvent, SetroubleshootEntry, message, suggestion


class SElinuxEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SElinuxEvent
        fields = ['digest', 'hostname', 'event', 'date', 'time', 'serial_num', 'event_kind', 'session', 'subj_prime', 'subj_sec', 'subj_kind', 'action', 'result', 'obj_prime', 'obj_sec', 'obj_kind', 'how']

class SelinuxDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selinux
        fields = '__all__'
class SetroubleshootEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SetroubleshootEntry
        fields = '__all__'

class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'
class suggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = suggestion
        fields = '__all__'

class SelinuxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selinux
        fields = '__all__'