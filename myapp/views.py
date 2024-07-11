
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from .forms import PackageForm, get_tracking_form, ReplyForm, phone_number_validator, CustomSMSForm
from .utils import read_customer_data
from twilio.rest import Client
from django.contrib import messages
import re
from django.urls import reverse
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from .models import ScannedPackageLog
from decouple import config

# Load customer data
customer_data = read_customer_data("C:/Users/Mail All Center/Downloads/Mailbox SMS Cx/CurrentMailboxes.csv")

customer_data['Phone Number'] = customer_data['Phone Number'].apply(lambda x: re.sub(r'\D', '', str(x)))
customer_data['Phone Number'] = customer_data['Phone Number'].apply(lambda x: x[1:] if x.startswith('1') else x)


<<<<<<< HEAD
=======
# Twilio credentials (retrieved from environment variables)
>>>>>>> b447718 (environment created)
ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')


client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(to, body):
    # to = +18722799667
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid

def fetch_messages(request):
    twilio_messages = []
    try:
        messages_from_twilio = client.messages.list(to=TWILIO_PHONE_NUMBER)
        # print(f"Fetched {len(messages_from_twilio)} messages from Twilio.")
        
        for message in messages_from_twilio:
              # Extract and clean the phone number
            number = message.from_
            clean_number = re.sub(r'\D', '', number)  # Remove any non-digit characters
            if clean_number.startswith('1'):
                clean_number = clean_number[1:]  # Remove leading '1' if present

            # print(f"Clean number: {clean_number}")

            # Look up the customer name using the cleaned phone number
            customer_row = customer_data[customer_data['Phone Number'].str.contains(clean_number, na=False)]
            if not customer_row.empty:
                customer_name = customer_row.iloc[0]['Customer']
            else:
                customer_name = "Unknown"
            
            # print(f"Customer name: {customer_name}")

            twilio_messages.append({
                "sender": number,
                "message": message.body,
                "timestamp": message.date_sent.strftime("%Y-%m-%d %H:%M:%S"),
                "customer_name": customer_name,
                "reply_url": reverse('send_reply'),
            })

    except Exception as e:
        messages.error(request, f"Failed to fetch messages: {str(e)}")
        return render(request, 'chat_messages.html', {'twilio_messages': []})
    
    return render(request, 'chat_messages.html', {'twilio_messages': twilio_messages[::-1]})



@csrf_exempt
def send_reply(request):
    if request.method == 'POST':
        try:
            reply_message = request.POST.get('reply_message')
            to_number = request.POST.get('to_number')

            if not reply_message or not to_number:
                return HttpResponse(status=400, content="Missing required fields: 'reply_message' and 'to_number'")

            # Log the message details
            print(f"Sending reply: {reply_message} to {to_number}")

            # Send SMS reply
            message_sid = send_sms(to_number, reply_message)

            if message_sid:
               messages.success(request, 'SMS sent successfully!')
               return redirect('index')
            else:
                return HttpResponse(status=500, content="Failed to send reply")

        except Exception as e:
            # Log the exception for debugging
            print(f"Error in send_reply: {str(e)}")
            return HttpResponse(status=500, content=f"Internal Server Error: {str(e)}")
    else:
        return HttpResponseNotAllowed(['POST'])

def custom_sms(request):
    if request.method == 'POST':
        form = CustomSMSForm(request.POST)
        if form.is_valid():
            to_number = form.cleaned_data['to_number']
            reply_message = form.cleaned_data['body']

            phone_number_cleaned = phone_number_validator(to_number)
            send_sms(phone_number_cleaned, reply_message)
            messages.success(request, 'SMS sent successfully!')
            return redirect('index')  # Redirect back to the index page
    else:
        form = CustomSMSForm()
    return render(request, 'custom_sms.html', {'form': form})


def index(request):
    package_form = PackageForm()    
    tracking_form = None
    # print(package_form)

    if request.method == 'POST':
        package_form = PackageForm(request.POST)
        
        if package_form.is_valid():
            mailbox_number = int(package_form.cleaned_data['mailbox_number'])
            # print("Mailbox_numer: ",mailbox_number)
            num_packages = int(package_form.cleaned_data['num_packages'])
            tracking_form_class = get_tracking_form(mailbox_number, num_packages)
            tracking_form = tracking_form_class(request.POST)

            if tracking_form.is_valid():
                tracking_numbers = []
                for i in range(num_packages):
                    tracking_numbers.append(tracking_form.cleaned_data[f'tracking_number_{i+1}'])

                # Look up customer information
                customer = customer_data[customer_data['Nbr'] == mailbox_number]
                customer_name = customer.iloc[0]['Customer']
                # print(customer_name)
                if not customer.empty:
                    customer_name = customer.iloc[0]['Customer']
                    
                    phone_number = customer.iloc[0]['Phone Number']
                    # print(phone_number)

                     # Validate and clean phone number
                    phone_number_cleaned = phone_number_validator(phone_number)

                    # Send SMS for each tracking number
                    for tracking_number in tracking_numbers:
                        sms_body = f"Hello {customer_name} !, your package with tracking no. {tracking_number} has arrived and ready for pick up at Maill All Center."
                        # sms_body = f"Hello {customer_name} !, It's time to renew your Mailbox# {mailbox_number}. Please stop by at Mail All Center at your convienence."
                        send_sms(phone_number_cleaned, sms_body)

                      # Log the package scan
                        ScannedPackageLog.objects.create(
                            customer_name=customer_name,
                            phone_number=phone_number_cleaned,
                            tracking_number=tracking_number
                        )


                    messages.success(request, 'SMS sent successfully!')
                    return redirect('index')  # Redirect to the index page
                    # return render_to_response('index', message='Sms sent successfully!!')
                else:
                    return HttpResponse('Mailbox number not found.')
    else:
        package_form = PackageForm()

    return render(request, 'index.html', {'package_form': package_form, 'tracking_form': tracking_form})


def phone_number_validator(phone_number):
    pattern = re.compile(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$')
    match = pattern.match(phone_number)
    if match:
        return ''.join(match.groups('')[:4])
    return phone_number


def package_log(request):
    logs = ScannedPackageLog.objects.all().order_by('-timestamp')  
    # print(logs)
    return render(request, 'package_log.html', {'logs': logs})