from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.http import Http404

from .models import CustomUser, Car, Rental
from .forms import CarForm, RentCarForm



def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        
        # Create and save the user
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password
        )
        login(request, user)  # Log the user in after registration
        return redirect('home')  # Redirect to home page or dashboard

    return render(request, "register.html")



def login_view(request):    
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]

        user = authenticate(request, phone_number=phone_number, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home page
        else:
            messages.error(request, "Invalid phone number or password")
            return redirect("login")

    return render(request, "login.html")



def home(request):
    cars = Car.objects.all()

    
    city_filter = request.GET.get('city')
    if city_filter:
        cars = cars.filter(city__iexact=city_filter)

    
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    if year_from and year_to:
        cars = cars.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        cars = cars.filter(year__gte=year_from)
    elif year_to:
        cars = cars.filter(year__lte=year_to)


    capacity_filter = request.GET.get('capacity')
    if capacity_filter:
        cars = cars.filter(capacity__gte=capacity_filter)

    
    most_liked_cars = Car.objects.annotate(likes_count=Count('liked_by')).order_by('-likes_count')[:5]


    return render(request, 'home.html', {
        'most_liked_cars': most_liked_cars,
        'cars': cars,
    })



@login_required
def user_profile(request):
    user = request.user
    rented_cars = Rental.objects.filter(renter=user)  
    liked_cars = user.liked_cars.all()  
    owned_cars = Car.objects.filter(owner=user)  

    total_spent = sum(rental.total_price for rental in rented_cars)  
    
    context = {
        'user': user,
        'rented_cars': rented_cars,
        'liked_cars': liked_cars,
        'owned_cars': owned_cars,
        'total_spent': total_spent,
    }
    return render(request, 'user_profile.html', context)



@login_required
def add_car(request):
    if request.method == "POST":
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        daily_rental_price = request.POST.get('daily_rental_price')
        capacity = request.POST.get('capacity')
        transmission = request.POST.get('transmission')
        city = request.POST.get('city')
        fuel_tank = request.POST.get('fuel_tank')


        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')


        car = Car(
            brand=brand,
            model=model,
            year=year,
            daily_rental_price=daily_rental_price,
            capacity=capacity,
            transmission=transmission,
            city=city,
            fuel_tank=fuel_tank,
            image1=image1,
            image2=image2,
            image3=image3,
            owner=request.user  
        )

        try:
            car.save()  
            return redirect('home')  
        except ValidationError as e:
            return render(request, 'add_car.html', {'error': str(e)})
    
    return render(request, 'add_car.html')



def view_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'view_car.html', {'car': car})



@login_required
def like_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    user = request.user

    if car in user.liked_cars.all():
        user.liked_cars.remove(car) 
    else:
        user.liked_cars.add(car)

    return redirect(request.META.get('HTTP_REFERER', 'home'))



def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    car = get_object_or_404(Car, id=car_id)
    
    
    if car.owner != request.user:
        return redirect('user_profile')


    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)  
        if form.is_valid():
            form.save()  
            return redirect('user_profile') 
        else:
            print(form.errors)
    else:
        form = CarForm(instance=car)

    return render(request, 'update_car.html', {'form': form, 'car': car})


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return redirect('user_profile')

   
    if request.method == 'POST':
        car.delete() 
        return redirect('user_profile')  

    return render(request, 'delete_car.html', {'car': car})



@login_required
def rent_car(request, car_id):
    car = Car.objects.get(id=car_id)

    if car.owner == request.user:
        return redirect('home')  # Prevent the owner from renting their own car

    if request.method == 'POST':
        form = RentCarForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Calculate the total price using the selected dates
            total_price = (end_date - start_date).days * car.daily_rental_price

            rental = Rental(
                renter=request.user,
                car=car,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price
            )
            rental.save()
            return redirect('user_profile') 
    else:
        form = RentCarForm()

    return render(request, 'rent_car.html', {'form': form, 'car': car})



