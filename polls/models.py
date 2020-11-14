from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название опроса')
    start_date = models.DateField('Дата начала опроса', auto_now_add=True)
    end_date = models.DateField('Дата окончания опроса')
    description = models.TextField('Описание')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-start_date', '-end_date', )


class Question(models.Model):
    TEXT_ANSWER = 'TA'
    ONE_CHOICE = 'OC'
    MULTI_CHOICE = 'MC'
    CHOICES_TYPE = [
        (TEXT_ANSWER, 'Ответ текстом'),
        (ONE_CHOICE, 'Ответ с выбором одного варианта'),
        (MULTI_CHOICE, 'Ответ с выбором нескольких вариантов')
    ]
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE,
        related_name='questions', verbose_name='Опрос')

    text = models.TextField('Текст вопроса')
    choice_type = models.CharField(
        max_length=100, choices=CHOICES_TYPE, verbose_name='Тип вопроса')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id', )


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name='Вопрос',
        related_name='choices')

    text = models.CharField(max_length=255, verbose_name='Вариант ответа')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id', )
