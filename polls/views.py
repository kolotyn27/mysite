"""Описываем представления для моделей"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


"""Блок представлений прописанных вручную
def index(request):
    Представление списка опубликованных вопросов
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    Представление выбранного вопроса с варианта ответа
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    Представление результатов опроса
    # описание пока аналогично представлению вопроса. Допилю позже
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
"""


class IndexView(generic.ListView):
    """Встроеное представление списока опубликованных вопросов"""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Возвращает последние 5 опубликованных вопросов.
        За исключением вопросов опубликованных в будущем.
        """

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    """Встроеное представление выбранного вопроса"""

    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """Встроеное представление результатов опроса"""

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """Представление результатов голосования с обработкой исключения,
    когда не выбран вариант ответа"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
