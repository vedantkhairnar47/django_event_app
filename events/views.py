from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'events/register.html', {'form': form})



@login_required
def dashboard(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'events/dashboard.html', {'events': events})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)   # ❗ stop DB save
            event.user = request.user         # 🔗 assign user
            event.save()                      # ✅ save to DB
            return redirect('dashboard')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, id):
    event = Event.objects.get(id=id, user=request.user)
   

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form})

@login_required
def delete_event(request, id):
    event = Event.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        event.delete()
        return redirect('dashboard')

    return render(request, 'events/delete_event.html', {'event': event})



@login_required
def event_detail(request, id):
    event = Event.objects.get(id=id, user=request.user)
    return render(request, 'events/event_detail.html', {'event': event})
