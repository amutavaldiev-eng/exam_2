from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


def register(request):
    if request.method == 'POST':
        data = request.POST
        User.objects.create_user(
            username=data.get('username'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            phone=data.get('phone'),
            position=data.get('position'),
            photo=request.FILES.get('photo')
        )
        return redirect('loginn')
    return render(request, 'registration.html')

def home(request):
    return render(request, "home.html")



def loginn(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(
            request,
            username=data.get('username'),
            password=data.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')
    
    
    
@login_required
def logout_user(request):
    logout(request)
    return redirect('loginn')


@login_required
def fields(request):
    field = Field.objects.all()
    category = Category.objects.all()
    search = request.GET.get("search")
    cat = request.GET.get("category")
    if search:
        field = field.filter(Q(name__icontains=search) | Q(address__icontains=search))
    if cat:
        field = field.filter(category_id=cat)
    return render(request, "fields.html", {"fields": field ,"categories": category})



@login_required
def show_fields(request, id):
    field = get_object_or_404(Field, id=id)
    book = Booking.objects.filter( field=field, status='active').first()
    return render(request, 'field_detail.html', {'field': field,'book': book})

@login_required
def book_field(request, id):
    field = get_object_or_404(Field, pk=id)
    if request.method == 'POST':
        if not field.is_free:
            return redirect('fields')
        Booking.objects.create(
            user=request.user,
            field=field,
            has_team=request.POST.get('has_team') == 'yes',
            players_needed=request.POST.get('players_needed') or 0)
        field.is_free = False
        field.save()
        return redirect('my_fields')

    return render(request, 'book_field.html', {'field': field})


@login_required
def my_fields(request):
    books = Booking.objects.filter(user=request.user)
    return render(request, 'my_fields.html', {'books': books})



@login_required
def booking_detail(request, id):
    book = get_object_or_404(Booking, pk=id, user=request.user)
    return render(request, 'booking_detail.html',{'book': book})



@login_required
def cancel_booking(request, id):
    book = get_object_or_404(Booking, pk=id, user=request.user)
    book.status = 'cancelled'
    book.save()
    book.field.is_free = True
    book.field.save()
    return redirect('my_fields')



@login_required
def finish_booking(request, id):
    book = get_object_or_404(Booking, pk=id, user=request.user)
    book.status = 'completed'
    book.save()
    book.field.is_free = True
    book.field.save()

    return redirect('my_fields')


@login_required
def play_together(request):
    books = Booking.objects.filter(has_team=False, status='active',)
    return render(request, 'play_together.html', {'books': books})





@login_required
def join_team(request, id):
    book = get_object_or_404(Booking, pk=id)
    if book.user == request.user:
        return redirect('play_together')
    participants = Participant.objects.filter(booking=book,user=request.user)
    if participants:
        return redirect('play_together')
    Participant.objects.create(booking=book, user=request.user)
    return redirect('play_together')



@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.about = request.POST.get('about')
        request.user.save()
        return redirect('profile')
    return render(request, 'update_profile.html')



@login_required
def leave_team(request, id):
    participant = get_object_or_404(Participant,booking_id=id,user=request.user)
    participant.delete()
    return redirect('play_together')


