from rest_framework import serializers
from .models import Feedback
class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = Feedback
        fields = ('screenshot','timestamp')
