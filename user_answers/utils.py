from polls.models import Choice, Question
from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        """
        Переопределение представления поля ChoiceField для вывода
        читаемого названия опций в json ответе.
        """
        return self._choices[obj]


class QuestionChoicesForeignKey(serializers.SlugRelatedField):
    def get_queryset(self):
        question = Question.objects.get(pk=self.context['question_id'])
        return Choice.objects.filter(question=question)
