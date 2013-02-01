import mimetypes
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from notes.models import Note, Attachment, Tag, Version

class NoteForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 
        'style': 'width:100%;height:100%'}))
    shared = forms.BooleanField()
    attachment = forms.FileField(required=False)

def edit(request, note_id=None):

    note = Note(user_id=1)
    
    if note_id:
        note = Note.objects.get(pk=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, 'edit.html', {'form': form, 'note': note})

        note.title = form.cleaned_data.get('title')
        note.save()

        if request.FILES.get('attachment'):
            a = Attachment(note=note)
            a.content = request.FILES['attachment']
            a.save()

        version = Version(note=note, user_id=1)
        version.content = form.cleaned_data.get('content')
        version.shared = form.cleaned_data.get('shared')
        version.save()

        return redirect(note)

    form = NoteForm(initial={
        'content': note.content, 
        'shared': note.shared, 
        'title': note.title
        })

    return render(request, 'edit.html', {'form': form, 'note': note})

def index(request, tag_id=None):
    notes = Note.objects.filter(user_id=1)

    if tag_id:
        notes = notes.filter(tags__pk=tag_id)

    tags = Tag.objects.distinct()
    return render(request, 'index.html', {'notes': notes, 'tags': tags})

def view(request, note_id):
    note = Note.objects.get(pk=note_id)
    version = note.version_set.latest()
    return render(request, 'view.html', {'note': note, 'version': version})

def view_file(request, note_id, file_id):
    note = Note.objects.get(pk=note_id)
    f = note.attachment_set.get(pk=file_id)

    mimetypes.init()
    t, e = mimetypes.guess_type(f.content.name)

    return HttpResponse(f.content.read(), content_type=t)

def delete_file(request, note_id, file_id):
    note = Note.objects.get(pk=note_id)
    f = Attachment.objects.get(pk=file_id)
    f.delete()
    return HttpResponse('File deleted')
