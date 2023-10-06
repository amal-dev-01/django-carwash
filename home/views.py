from django.shortcuts import render,HttpResponse,get_object_or_404
from userview.models import UserDetails
from datetime import datetime
from datetime import date,timedelta
import holidays
from django.contrib.auth.decorators import login_required
from userview.forms import EditUserForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import Category, Package,VechileType,Variation,Slot,Booking
from .forms import BikeForm
from .forms import CarForm,SlotForm
from django.utils import timezone
from threading import Thread
from time import sleep
# import razorpay


# Create your views here.

@login_required(login_url=('login','loginwithotp'))
def home(request):
    current_time = datetime.now().time()
    print(current_time)
    opening_time = datetime.strptime("09:00:00", "%H:%M:%S").time()
    closing_time = datetime.strptime("19:00:00", "%H:%M:%S").time()
    
    current_year = date.today().year
    indian_holidays = holidays.India(years=current_year)
    current_date = date.today() 
    print(current_date)
    
    # all_holidays = indian_holidays.items()
    # for date, name in all_holidays:
    #     print(f"{date}: {name}")

    
    if current_date in indian_holidays:
        holiday_message = f"{current_date} is not available : {indian_holidays[current_date]}"
        status = holiday_message
    else:
        is_sunday = datetime.now().weekday() == 6
        
        if is_sunday:
            status = "Closed (Sunday)"
        else:
            status = "Open"
    
    context = {"status": status, "holiday_message": holiday_message if "holiday_message" in locals() else ""}
    
    package=Package.objects.all()

    print(package)
    return render(request, 'hometemplates/home.html',context)
 


def dashboard(request):
    user_email=request.user.email
    try:
        user = UserDetails.objects.get(email=user_email)
    except User.DoesNotExist:
        user = None
    if user:
        first_name=user.first_name
        last_name=user.last_name
        email=user.email
        phone_number=user.phone_number
        context = {
            'first_name': first_name,   
            'last_name': last_name,
            'email':email,
            'phone_number':phone_number,
            'id':user.id,
        }
    else:
       
        context = {
            'error_message': 'User not found'
        }

    return render(request, 'hometemplates/dash.html',context )

def service(request):
    return render(request, 'hometemplates/service.html')

def myorder(request):
    orders = Booking.objects.filter(user=request.user, is_ordered=True )
    context ={
        'orders':orders
    }
    return render(request, 'hometemplates/order.html',context)

def orderdetails(request, id):
    order = get_object_or_404(Booking, user=request.user, id=id)
    variation = order.variation
    vechile_type = variation.vechile_type
    print(vechile_type)
    slot = order.slot
    context = {
        'booking_id': order.id,
        'vechile_type': vechile_type,
        'variation':variation,
        'package': variation.package,
        'price': variation.price,
        'is_canceled':order.is_canceled,
    }

    return render(request, 'hometemplates/orderdetails.html', context)

def cancel_order(request, order_id):
    order = get_object_or_404(Booking, id=order_id, user=request.user)
    order.is_canceled = True
    slott = Slot.objects.get(id = order.slot.id)
    slott.is_available = True
    slott.date=None
    slott.timeslot=None
    slott.save()
    order.save()
    return redirect('myorder')

def editprofile(request, id):
    if request.method == 'POST':
        user_details = UserDetails.objects.get(pk=id)
        form = EditUserForm(request.POST, instance=user_details)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            # Check if the new email already exists
            existing_user = UserDetails.objects.filter(email=new_email).exclude(id=id).first()

            if existing_user:
                messages.error(request, 'Email already exists. Please use a different email address.')
            else:
                form.save()
                return redirect('/home/dashboard')
    else:
        user_details = UserDetails.objects.get(pk=id)
        form = EditUserForm(instance=user_details)

    return render(request, 'edit.html', {'form': form})
    

def category(request, vehicle):
    form = None
    packages = None
    formPackage = None  # Initialize formPackage outside the if block

    if vehicle == 'car':
        form = CarForm(request.GET)
    else:
        form = BikeForm(request.GET)
        
    if form and form.is_valid():
        vehicle_name = form.cleaned_data['name']
        vehicle_type = VechileType.objects.filter(vechile_type=vehicle_name).first()

        if vehicle_type:
            packages = Variation.objects.filter(vechile_type=vehicle_type)

    return render(request, 'hometemplates/category.html', {'form': form, 'packages': packages})


def select(request,id):
    print(id)
    try:
        select_pack = Variation.objects.get(id=id)
        today = timezone.now().date()
        # context={
        #     'id':select_pack.id,
        #     'vechile_type':select_pack.vechile_type,
        #     'package':select_pack.package,
        #     'price':select_pack.price,
        # }
        user = request.user
        # if user.has_used_coupon == False:
        #      context={
        #     'id':select_pack.id,
        #     'vechile_type':select_pack.vechile_type,
        #     'package':select_pack.package,
        #     'price':select_pack.price,
        #     'coupon':fisrt_login,
        #      }
        # else:
        #      context={
        #     'id':select_pack.id,
        #     'vechile_type':select_pack.vechile_type,
        #     'package':select_pack.package,
        #     'price':select_pack.price,
        #      }
        has_used_coupon = user.has_used_coupon
        context = {
            'id': select_pack.id,
            'vechile_type': select_pack.vechile_type,
            'package': select_pack.package,
            'price': select_pack.price,
        }

        
        if not has_used_coupon:
            coupon_code = "first_login"  
            context['coupon'] = coupon_code
        
    except Variation.DoesNotExist:
        pass
        
    return render(request, 'hometemplates/select.html',context )





def slotbook(request,id=None,dates=None):
    print(id,'nnnnnnnnnn')
    formatted_date = None
    if dates is not None:
        try:
            date_obj = datetime.strptime(dates, "%Y, %m, %d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return HttpResponse("Invalid date format")

    today = date.today()
    booked_dates = Slot.objects.filter(date__gt=today).values_list("date", "timeslot")
    date_list = [{"timeslot": timeslot, "date": (date.year, date.month, date.day)} for date, timeslot in booked_dates]
    fd = [today + timedelta(days=i) for i in range(1, 6)]
    five_date = [date.strftime('%Y, %m, %d') for date in fd]
    booked_slot = Slot.objects.filter(date = formatted_date,is_available=False).values_list("timeslot",flat=True)

    
    
    if request.method == 'POST':
        form = SlotForm(request.POST)
        
        if form.is_valid():            
            slot = form.save(commit=False)
            print(slot)
            # date_obj = datetime.strptime(dates, "%Y, %m, %d")
            # formatted_date = date_obj.strftime("%Y-%m-%d")
            slot.date = formatted_date
            print(slot.date)
            slot.variation = Variation.objects.get(id=id)
            print(slot.variation)
        
            slot.save()
            print(slot.id)
            return redirect('booking', slot_id=slot.id) 
    else:
        form = SlotForm()

    return render(request, 'hometemplates/slotbook.html', {'id':id,'form': form,"date_list":date_list,"five_date":five_date,'booked_slot':booked_slot})


# def book(request, slot_id):
#     user=request.user
#     print(user)
#     if not user.has_used_coupon:
#         # Render the coupon form
#         coupon_form = CouponForm()
#         return render(request, 'hometemplates/coupon.html', {'coupon_form': coupon_form ,'slot_id':slot_id})
#     else:
        
#         print(slot_id,'hloooooooooooooooooo')
#         slot = Slot.objects.get(id=slot_id)
#         variation=slot.variation
#         price=variation.price
#         vechile_type=variation.vechile_type
#         package=variation.package
#         # print(package)
#         time_ranges = {
#         0: '9:00 - 9:30',
#         1: '10:00 - 10:30',
#         2: '11:00 - 11:30',
#         3: '12:00 - 12:30',
#         4: '13:00 - 13:30',
#         5: '14:00 - 14:30',
#         6: '15:00 - 15:30',
#         7: '16:00 - 16:30',
#         }
#         time=slot.timeslot
        
#         booking=Booking( 
#             user=user,
#             slot=slot,
#             variation=variation,
#         )
#         booking.save()
        
#         print(booking.id,'booookin')
#         formatted_time = time_ranges.get(time, 'Unknown Time Range')
#         print(formatted_time)
#         context={
#             'id':booking.id,
#             'first_name':user.first_name,
#             'last_name':user.last_name,
#             'package':package,
#             'vechile_type':vechile_type,
#             'price':price,
#             'date':slot.date,
#             'time':formatted_time,

#         }
#         return render(request, 'hometemplates/booking.html',context)

# Define time_ranges here so that it's accessible in the entire view function
time_ranges = {
    0: '9:00 - 9:30',
    1: '10:00 - 10:30',
    2: '11:00 - 11:30',
    3: '12:00 - 12:30',
    4: '13:00 - 13:30',
    5: '14:00 - 14:30',
    6: '15:00 - 15:30',
    7: '16:00 - 16:30',
}

def book(request, slot_id,coupon=None):
    user = request.user
    print(user)

    if not user.has_used_coupon:
        # coupon_code = request.session['coupon_code']
        # print(coupon_code)

        # Render the coupon form
        coupon_form = CouponForm()
        return render(request, 'hometemplates/coupon.html', {'coupon_form': coupon_form, 'slot_id': slot_id})
    # elif :
    #     coupon_code = request.session['coupon_code']
    #     print(coupon_code,'.............')

    #     try:
    #         coupon = Coupon.objects.get(code=coupon_code)

    #         # Check if the coupon has already been used by the user
    #         if not coupon.used:
    #             # Mark the coupon as used by the user
    #             coupon.used.add(user)

    #             # Calculate the discounted price
    #             slot = get_object_or_404(Slot, id=slot_id)
    #             variation = slot.variation
    #             package = variation.package
    #             discounted_price = variation.price - (variation.price * (coupon.discount_percentage / 100))
    #             if discounted_price < 0:
    #                 discounted_price = 0  # Ensure the price is not negative

    #             # Create a booking with the discounted price
    #             time = slot.timeslot

    #             booking = Booking(
    #                 user=user,
    #                 slot=slot,
    #                 variation=variation,
    #                 discounted_price=discounted_price,
    #             )
    #             booking.save()

    #             print(booking.id, 'booookin')
    #             formatted_time = time_ranges.get(time, 'Unknown Time Range')
    #             print(formatted_time)
                
    #             context = {
    #                 'id': booking.id,
    #                 'first_name': user.first_name,
    #                 'last_name': user.last_name,
    #                 'package': package,
    #                 'vechile_type': variation.vechile_type,
    #                 'price': discounted_price,
    #                 'date': slot.date,
    #                 'time': formatted_time,
    #             }
    #             return render(request, 'hometemplates/booking.html', context)
    #         else:
    #             # Coupon has already been used by the user
    #             return redirect('booking', slot_id=slot_id)
    #     except Coupon.DoesNotExist:
    #         # Coupon code is invalid
    #         return redirect('booking')
    else:
        slot = get_object_or_404(Slot, id=slot_id)
        variation = slot.variation
        package = variation.package
        
        price = variation.price
        booking = Booking(
            user=user,
            slot=slot,
            variation=variation,
            price=price,  
        )
        booking.save()
        time = slot.timeslot
        formatted_time = time_ranges.get(time, 'Unknown Time Range')
        print(coupon, 'coupon code')

        if coupon:
            try:
                print('hi')
                coupon = Coupon.objects.get(code=coupon)
                discount_percentage = 100
                discounted_price = (int(price) - int(discount_percentage))
                price = discounted_price
                booking.price = price
                booking.save()  
            except Coupon.DoesNotExist:
                # Handle the case where the coupon code does not exist
                pass



        context = {
            'id': booking.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'package': package,
            'vechile_type': variation.vechile_type,
            'price': price,
            'date': slot.date,
            'time': formatted_time,
        }
        return render(request, 'hometemplates/booking.html', context)


from .models import Coupon
from .forms import CouponForm
# views.py
from django.shortcuts import redirect

def coupon(request, slot_id):
    print(slot_id,'llllllllllllllfff')
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_code = coupon_form.cleaned_data['coupon_code']
            try:
                coupon = Coupon.objects.get(code=coupon_code)

                # Check if the coupon is valid for the user's first login
                if coupon.valid_for_first_login and not request.user.has_used_coupon:
                    request.user.has_used_coupon = True
                    request.user.save()
                    # Redirect to the 'book' view with the slot_id
                    return redirect('bookking', slot_id=slot_id,coupon=coupon_code)
                else:
                    # Coupon is not valid for this user's login status
                    return redirect('booking')
            except Coupon.DoesNotExist:
                # Coupon code does not exist
                return redirect('booking')
    else:
        coupon_form = CouponForm()
    return render(request, 'hometemplates/booking.html', {'coupon_form': coupon_form})



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf_invoice(context):
    template_path = 'order/invoice.html' 
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'  # This header prompts download
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


# views.py
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Booking, Package, Variation

def download_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    variation = booking.variation
    package = variation.package
    slot = booking.slot
    time_ranges = {
    0: '9:00 - 9:30',
    1: '10:00 - 10:30',
    2: '11:00 - 11:30',
    3: '12:00 - 12:30',
    4: '13:00 - 13:30',
    5: '14:00 - 14:30',
    6: '15:00 - 15:30',
    7: '16:00 - 16:30',
    }
    time=slot.timeslot
    formatted_time = time_ranges.get(time, 'Unknown Time Range')

    context = {
        'first_name': booking.user.first_name,
        'last_name': booking.user.last_name,
        'package': package,
        'variation': variation,
        'price': variation.price,
        'date': booking.slot.date,
        'time': formatted_time,  # Make sure to obtain 'formatted_time' as you did before
        'booking_id': booking_id,
    }

    # Generate and return the PDF invoice as a download
    return generate_pdf_invoice(context)

