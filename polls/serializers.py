from django.utils import timezone
from rest_framework import serializers

from .models import Choice, Poll, Question


class PollSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if self.instance:
            if (data.get('end_date') and
                    data['end_date'] < self.instance.start_date):

                raise serializers.ValidationError(
                    'Дата окончания не может быть раньше даты начала')
        else:
            if (data.get('end_date') and
               data['end_date'] < timezone.now().date()):

                raise serializers.ValidationError(
                    'Дата окончания не может быть раньше текущей даты')
        return data

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    poll = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = Choice
        fields = '__all__'
