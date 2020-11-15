from django.db import models
from polls.models import Choice, Poll, Question


class UserAnswer(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='id пользователя')

    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='user_answer',
        verbose_name='Опрос')

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='user_answer',
        verbose_name='Вопрос')

    text_answer = models.CharField(
        max_length=500, verbose_name='Ответ', null=True)

    one_choice_answer = models.ForeignKey(
        Choice, on_delete=models.CASCADE,
        related_name='user_answer_one_choice',
        verbose_name='Выбранный вариант ответа', null=True)

    multi_choice_answer = models.ManyToManyField(
        Choice, related_name='user_answer_multi_choice')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'question'], name='unique answer')
        ]
