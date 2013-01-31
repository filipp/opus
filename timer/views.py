import json
from datetime import datetime, timedelta

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render

from timer.models import Event, Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'duration': forms.HiddenInput()
        }

def go(request):
    return render(request, 'timer.html')

def events(request, label, event_id=None):

    fmt = '%Y%m%d'
    label = Label.objects.get(pk=label)

    if request.method == 'POST':
        event = Event(user_id=1)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
        else:
            print form.errors
    
    start = datetime.now()
    events = Event.objects.filter(labels=label)

    if request.GET.get('start'):
        start = datetime.strptime(request.GET.get('start'), fmt)
        events = events.filter(started_at__lte=start)
    
    delta = timedelta(days=1)

    if request.GET.get('group') == 'week':
        delta = timedelta(days=7)
    
    if request.GET.get('group') == 'month':
        delta = timedelta(days=30) # BULLSHIT!

    try:
        now = events[0].started_at
    except IndexError, e:
        now = start

    next = now + delta
    previous = now - delta

    form = EventForm(initial={'labels': [label]})

    if request.GET.get('view') == 'report':
        return render(request, 'event_grid.html', {'events': events})

    return render(request, 'timer.html', {
        'events': events,
        'label': label,
        'form': form,
        'title': start,
        'previous': previous.strftime(fmt),
        'next': next.strftime(fmt),
        })

def delete_event(request, event_id):
    Event.objects.filter(pk=event_id).delete()
    return HttpResponse('OK')

def labels(request):
    labels = Label.objects.filter(user_id=1)
    return render(request, 'labels.html', {'labels': labels})

def alarm(request):
    return render(request, 'alarm.html')

def edit_label(request, label_id=None):

    label = Label(user_id=1)

    if label_id:
        label = Label.objects.get(pk=label_id)

    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            label = form.save()
        else:
            print form.errors

    return redirect(label)

def view_event(request, event_id):
    return render(request, 'event_detail.html')
