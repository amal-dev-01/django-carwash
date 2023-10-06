from django.shortcuts import render, redirect,HttpResponse
from home.models import Booking,Variation,Package
from .models import Payment
from django.shortcuts import get_object_or_404
from django.conf import settings
import razorpay


def payment(request, id):

    booking = Booking.objects.get(pk=id)
    variation = booking.variation
    package = variation.package
    price = booking.price
    total = int(price)*100
    slot = booking.slot_id
    print(slot,'slot')
    user = request.user
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment_order = client.order.create({
        'amount': total, 
        'currency': 'INR',
        'payment_capture': 1,  
    })

    order_id = payment_order['id']
    

    context = {
        'order_id': order_id,
        'total': total,
        'package': package.id,
        'booking_id':booking.id,
    }

    return render(request, 'order/pay.html', context)


def success(request):
    print('hiiiiiiiiii')
    try:
        user = request.user
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        booking_id = request.GET.get('booking_id')
        print(booking_id)
        package = request.GET.get('package')
        package = get_object_or_404(Package, id=package)
        booking = Booking.objects.get(id=booking_id)
        variation = booking.variation
        price = booking.price
        slot = booking.slot
        slot.is_available = False
        slot.save()
        
        payment = Payment( 
            user=user,
            razorpay_payment_id=razorpay_payment_id,
            booking_id=booking_id,
            package=package,
            amount_paid=price,
        )
        payment.save()
    
        booking.is_paid = True
        booking.is_ordered = True
        booking.save()
        return redirect('pdf', id=booking.id)
    except Exception as e:
        print(e)
   
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    return HttpResponse('hpnrgon')


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage


def pdf(request,id):
    user=request.user
    booking_id=id
    booking=Booking.objects.get(id=id)
    variation=booking.variation
    package=variation.package
    vechile_type=variation.vechile_type
    price=booking.price
    slot=booking.slot
    date=slot.date
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
    template_path = 'order/invoice.html' 
    total_price = price

    context = {
      'first_name':user.first_name,
      'last_name':user.last_name,
      'package':package,
      'variation':variation,
      'price':total_price,
      'date':date,
      'time':formatted_time,
      'booking_id':booking_id
    }
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="output.pdf"' 
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    subject = 'Your Car Wash Invoice'
    message = 'Please find your invoice attached below.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = user.email 

    email = EmailMessage(subject, message, from_email, [recipient])
    email.attach('invoice.pdf', response.content, 'application/pdf')    
    email.send()
    return render(request, 'order/invoice.html', context)
    