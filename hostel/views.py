from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Hostel, Room, Application, Allocation
from .forms import ApplicationForm

# List all hostels
def hostels_list(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostel/hostels_list.html', {'hostels': hostels})


# Hostel details page (shows rooms and availability)
def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = hostel.rooms.filter(is_active=True)
    return render(request, 'hostel/hostel_detail.html', {
        'hostel': hostel,
        'rooms': rooms
    })


# Step 1: Select hostel page
@login_required
def select_hostel(request):
    hostels = Hostel.objects.all()
    if request.method == 'POST':
        hostel_id = request.POST.get('hostel_id')
        if hostel_id:
            return redirect('apply_hostel_form', hostel_id=hostel_id)
        messages.error(request, "Please select a hostel.")
    return render(request, 'hostel/select_hostel.html', {'hostels': hostels})


# Step 2: Application form for selected hostel
@login_required
def apply_hostel_form(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)

    # Prevent multiple applications to same hostel
    if Application.objects.filter(student=request.user, preferred_hostel=hostel).exists():
        messages.warning(request, f"You have already applied for {hostel.name}.")
        return redirect('hostels_list')

    # POST request
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        # filter to rooms inside this hostel only
        form.fields['preferred_room'].queryset = Room.objects.filter(
            hostel=hostel,
            is_active=True
        )

        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.preferred_hostel = hostel
            application.save()

            messages.success(request, f"Application for {hostel.name} submitted successfully.")
            return redirect('hostels_list')

    else:
        # GET request
        form = ApplicationForm()
        form.fields['preferred_room'].queryset = Room.objects.filter(
            hostel=hostel,
            is_active=True
        )

    return render(request, 'hostel/apply_hostel_form.html', {
        'form': form,
        'hostel': hostel
    })


# Staff: Pending applications
@login_required
def allocations_pending(request):
    apps = Application.objects.filter(status='pending')
    return render(request, 'hostel/applications_list.html', {'applications': apps})


# Staff: Allocate student to a room
@login_required
@transaction.atomic
def allocate(request, app_pk, room_pk):
    app = get_object_or_404(Application, pk=app_pk)
    room = get_object_or_404(Room, pk=room_pk)

    if room.occupied + 1 > room.capacity:
        messages.error(request, 'Room is full')
        return redirect('allocations_pending')

    # Create Allocation, update room, and mark application approved
    Allocation.objects.create(student=app.student, room=room)
    room.occupied += 1
    room.save()

    app.status = 'approved'
    app.preferred_room = room
    app.save()

    messages.success(request, 'Student allocated successfully')
    return redirect('allocations_pending')
