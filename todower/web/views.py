from django.shortcuts import render
from .models import *
from datetime import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import TaskForm
from django.db import transaction
import collections
# Create your views here.


@transaction.atomic
def main(request):
    last_day = Day.objects.filter(member__user_id=request.user.id).order_by('-date').first()
    if last_day is None or last_day.date < date.today():
        day = Day(date=date.today())
        day.member = request.user.member
        day.save()
        list_todo = List(progress=1, day=day)
        list_todo.save()
        list_progress = List(progress=2, day=day)
        list_progress.save()
        list_done = List(progress=3, day=day)
        list_done.save()
        if last_day is None:
            list_backlog = List(progress=4, day=day)
            list_backlog.save()
            return render(request, 'web/main.html', locals())
        old_todo_list = List.objects.get(day=last_day, progress=1)
        old_progress_list = List.objects.get(day=last_day, progress=2)
        for task in Task.objects.filter(list=old_todo_list):
            task.list = list_todo
            task.priority += 10
            task.save()
        for task in Task.objects.filter(list=old_progress_list):
            task.list = list_progress
            task.priority += 10
            task.save()

    backlog = Task.objects.filter(list__progress=4, list__day__member__user_id=request.user.id).order_by('-priority')
    done = Task.objects.filter(list__day__date=datetime.today(), list__progress=3, list__day__member__user_id=request.user.id)
    progress = Task.objects.filter(list__day__date=datetime.today(), list__progress=2, list__day__member__user_id=request.user.id)
    todo = Task.objects.filter(Q(list__day__date=datetime.today()) & Q(list__progress=1) & Q(list__day__member__user__id=request.user.id)).order_by('-priority')
    return render(request, 'web/main.html', locals())


def change(request, id_task, list_number):
    task = Task.objects.get(id=id_task)
    if list_number == '4':
        task.list = List.objects.get(progress=list_number, day__member__user_id=request.user.id)
    else:
        task.list = List.objects.get(progress=list_number, day__date=datetime.today(), day__member__user_id=request.user.id)
    task.save()
    return HttpResponseRedirect('/main/')


def add_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            if "submit" in request.POST:
                list = List.objects.get(progress=1, day__date=datetime.today(), day__member__user_id=request.user.id)
            else:
                list = List.objects.get(progress=4, day__member__user_id=request.user.id)
            task = task_form.save(commit=False)
            task.list = list
            task.save()
            return HttpResponseRedirect('/main/')
    task_form = TaskForm()
    return render(request, 'web/add_task.html/', locals())


def history(request):
    days = Day.objects.filter(member_id=request.user.member.id).order_by('-date')
    histo = {}
    for day in days:
        histo[str(day.date)] = Task.objects.filter(list__progress=3, list__day__date=day.date, list__day__member_id=request.user.member.id)
    return render(request, 'web/history.html', locals())


def update_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if request.method == 'POST':
        if 'delete' in request.POST:
            task.delete()
            return HttpResponseRedirect('/main/')
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task.save()
            return HttpResponseRedirect('/main/')

    task_form = TaskForm(instance=task)
    return render(request, 'web/update_task.html', locals())
