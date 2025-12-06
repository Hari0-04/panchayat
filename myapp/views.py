from urllib import request
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, JsonResponse
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Supervisor, Signup, Admins, Post, Area, Complaint, Request
from django.contrib.auth.models import User




def signup_pub(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phoneno")
        password = request.POST.get("password")
        conpass = request.POST.get("conpass")
        address = request.POST.get("address")

        # Validation
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "signuppage.html", {
                "username": username,
                "phoneno": phone,
                "address": address
            })

        if password != conpass:
            messages.error(request, "Passwords do not match.")
            return render(request, "signuppage.html", {
                "username": username,
                "phoneno": phone,
                "address": address
            })

        # Save new user
        new_user = Signup(
            username=username,
            phoneno=phone,
            password=password,
            conpass=conpass,
            address=address
        )
        new_user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("loginpage")  # URL name of your login page

    # GET request
    return render(request, "signuppage.html")


def welcome(request):
    return render(request, "Welcomepage.html")
def welcome2(request):
    return render(request, "Welcomeadmin.html")
def welcome3(request):
    return render(request, "Welcomesupervisor.html")
def welcome4(request):
    return render(request, "Welcomeeo.html")

def Startpage(request):
    return render(request, "Startpage.html")
from django.shortcuts import render, redirect
from .models import Signup, Login, Complaint, Request

def loginpage(request):
    if request.method == "POST":
        phoneno = request.POST.get("phoneno")
        password = request.POST.get("password")

        user = Signup.objects.filter(phoneno=phoneno, password=password).first()

        if user:
            # Save login only if authentication is successful
            new_det=Login(phoneno=phoneno, password=password)
            new_det.save()
         # change to your main page URL name
            total_complaints = Complaint.objects.filter(phone=phoneno).count()
            total_requests = Request.objects.filter(phone_number=phoneno).count()

            return render(request, "Mainpage.html", {
                "user": user,
                'total_complaints': total_complaints,
                'total_requests': total_requests
            })
        else:
            return render(request, "loginpage.html", {"error": "Invalid phone number or password."})

    return render(request, "loginpage.html")

def loginpage2(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)

        # Try to find a matching admin
        user = Admins.objects.filter(username=username, password=password).first()
        
        if user:
            request.session['admin_username'] = user.username
            messages.success(request, "✅ Login Successful!")
            return redirect("Mainpageadmin")
        else:
            messages.error(request, "❌ Invalid username or password.")
            return render(request, "loginpageadmin.html")
    return render(request, "loginpageadmin.html")

def loginpage3(request):
    if request.method == "POST":
        supervisor_id = request.POST.get("supervisor_id")
        password = request.POST.get("password")

        # Filter by correct field names
        user = Supervisor.objects.filter(supervisor_id=supervisor_id, password=password).first()

        if user:
            request.session['supervisor_id'] = user.supervisor_id
            messages.success(request, "✅ Login Successful!")
            return redirect("Mainsupervisor")  # or your supervisor main page
        else:
            messages.error(request, "❌ Invalid ID or password.")
            return render(request, "loginsupervisor.html")
    return render(request, "loginsupervisor.html")

def loginpage4(request):
    if request.method == "POST":
        emp_number = request.POST.get("emp_number")
        password = request.POST.get("password")

        # Filter EOLogin with matching emp_number and password
        user = EOLogin.objects.filter(emp_id=emp_number, password=password).first()

        if user:
            request.session['emp_number'] = user.emp_id
            messages.success(request, "✅ Login Successful!")
            return redirect("eo_mainpage")  # Replace with your EO main page
        else:
            messages.error(request, "❌ Invalid ID or password.")
            return render(request, "loginpageeo.html")  # EO login template

    return render(request, "loginpageeo.html")




def logout(request):
    return render(request, "loginpage.html")
def logout2(request):
    return render(request, "loginpageadmin.html")
def logout3(request):
    return render(request, "loginsupervisor.html")
def logout4(request):
    return render(request, "loginpageeo.html")
# request and complaint

def complaint_form(request): 
    supervisors = Supervisor.objects.all()  # fetch supervisors for both GET and POST

    if request.method == "POST":
        # Get form data
        complaintType = request.POST.getlist("complaintType")  # for multiple checkboxes
        otherType = request.POST.get("otherType")
        description = request.POST.get("description")
        file = request.FILES.get("file")
        date_time = request.POST.get("datetime")  
        username = request.POST.get("username") 
        phone = request.POST.get("phone") 
        address = request.POST.get("address")  
        location = request.POST.get("location") 
        supname = request.POST.get("supervisor") 

        # Handle 'Others'
        if "Others" in complaintType:
            complaint_type_value = otherType
        else:
            complaint_type_value = ", ".join(complaintType)
        
        # Save to database
        new_det = Complaint(
            complaint_type=complaint_type_value,
            description=description,
            file=file,
            date_time=date_time,
            user=username,
            phone=phone,
            address=address,
            location=location,
            supervisor=supname
        )
        new_det.save()

        # Return with supervisors again so dropdown remains populated
        return render(request, "complaint_form.html", {
            "supervisors": supervisors,
            "success": True
        })

    # ✅ GET request - must pass supervisors here too!
    return render(request, "complaint_form.html", {
        "supervisors": supervisors
    })




# forgot password

otp_store = {}
def Forgotpassword(request):
    if request.method == "POST":
        phoneno = request.POST.get("phoneno")
        try:
            user = Signup.objects.get(phoneno=phoneno)
        except Signup.DoesNotExist:
            return HttpResponse("User not found")

        # Generate OTP
        otp = random.randint(100000, 999999)
        otp_store[phoneno] = otp

        # Send OTP via SMS/email (here just printing for testing)
        print(f"OTP for {phoneno}: {otp}")

        # Redirect to verify OTP page
        return render(request, "verify_otp.html", {"phoneno": phoneno})

    return render(request, "Forgotpassword.html")

# Step 2: Verify OTP and reset password
def verify_otp(request):
    if request.method == "POST":
        phoneno = request.POST.get("phoneno")
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if str(otp_store.get(phoneno)) != entered_otp:
            return HttpResponse("Invalid OTP")

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match")

        user = Signup.objects.get(phoneno=phoneno)
        user.set_password(new_password)  # This will save the new password
        otp_store.pop(phoneno, None)

        return HttpResponse("Password updated successfully")


# request 

def requestform(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone_number = request.POST.get("phone")
        address = request.POST.get("address")
        request_type = request.POST.get("requestType")
        other_type = request.POST.get("otherType")

        if "Others" in request_type:
            request_type_value = other_type
        else:
            request_type_value = ", ".join(request_type)
        # Save to database
        new_det=request(
            name=name,
            phone_number=phone_number,
            address=address,
            request_type=request_type_value,
            other_type=other_type
        )
        new_det.save()

    return render(request, "request_form.html")


# =========================
# MODELS FOR POSTS, ACHIEVEMENTS, TASKS

def Posts(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        created_at = request.POST.get("datetime") or timezone.now()
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        new_det=Post(
            title=title,
            message=message,
            image=image,
            video=video,
            created_at=created_at
        )
        new_det.save()
        return redirect('Posts')  # redirect to post list after submission
    return render(request, "posts.html")

def Tasks(request):
    supervisors=Supervisor.objects.all()
    areas=Area.objects.all()
    return render(request, "task.html",{"supervisors": supervisors,"areas": areas})    
import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EOLogin, Supervisor

# Helper functions
from django.contrib.auth.hashers import make_password
import random, string

def generate_id(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def Add_supervisor(request):

    if request.method == "POST":
        role = request.POST.get("role")
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        # Generate fresh ID + password on submission
        password = generate_password()

        if role == "EO":
            user_id = generate_id("EO")
            EOLogin.objects.create(emp_id=user_id, name=name, phone=phone, password=password)

        elif role == "Supervisor":
            user_id = generate_id("SUP")
            Supervisor.objects.create(supervisor_id=user_id, name=name, phone=phone, password=password)


        else:
            messages.error(request, "Invalid role selected.")
            return redirect("Add_supervisor")

        messages.success(
            request,
            f"{role} created successfully!\nID: {user_id}\nPassword: {password}"
        )
        return redirect("Add_supervisor")

    # For GET (initial load)
    return render(request, "Addsupervisor.html")




def Add_area(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if Area.objects.filter(name=name).exists():
            messages.error(request, "❌ Area already exists!")
        else:
            new_det = Area(name=name)
            new_det.save()
            messages.success(request, "✅ Area added successfully!")
        # ✅ Use redirect so the message displays properly and doesn't repeat on refresh
        return redirect('Mainpageadmin')  
    return render(request, "Add_area.html")
@login_required
def upload_profile(request):
    if request.method == "POST" and request.FILES.get("profile_image"): # logged-in user
        profile_image = request.FILES["profile_image"]
        new_det=Signup(profile_image=profile_image)
        new_det.save()
        messages.success(request, "✅ Profile updated successfully!")
    else:
        messages.error(request, "❌ No file selected or invalid request!")
    return redirect("Mainpage")

def Mainpage(request):
    return render(request, "Mainpage.html")

from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone

def Mainpageadmin(request):
    admin_username = request.session.get('admin_username', None)

    # Total counts
    total_complaints = Complaint.objects.count()
    total_requests = Request.objects.count()

    # Month labels
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    # Complaints grouped by month
    complaints_month = (
        Complaint.objects.annotate(month=ExtractMonth('date_time'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Requests grouped by month
    requests_month = (
        Request.objects.annotate(month=ExtractMonth('id'))  # If you have created_at field, use that
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Create lists initialized to 0 for 12 months
    complaints_data = [0] * 12
    requests_data = [0] * 12

    # Fill complaints
    for item in complaints_month:
        complaints_data[item['month'] - 1] = item['count']

    # Fill requests
    for item in requests_month:
        requests_data[item['month'] - 1] = item['count']

    return render(request, "Mainpageadmin.html", {
        "admin_username": admin_username,
        "total_complaints": total_complaints,
        "total_requests": total_requests,
        "months": month_labels,
        "complaints_data": complaints_data,
        "requests_data": requests_data,
    })




def view_complaints(request):
    complaints = Complaint.objects.all().order_by('-id')  # latest first
    return render(request, 'view_complaints.html', {'complaints': complaints})  


def eo_dashboard(request):
    return render(request, 'eomain.html')

# your public signup model

def public_signups(request):
    public_users = Signup.objects.all()
    context = {
        'public_users': public_users
    }
    return render(request, 'public_signups.html', context)


# views.py
def eo_complaints(request):
    complaints = Complaint.objects.all()
    context = {
        'complaints': complaints,
        'admin_username': request.session.get('eo_emp_number'),
    }
    return render(request, 'eo_complaints.html', context)


def eo_requests(request):
    # Fetch all requests from DB
    requests = Request.objects.all()

    context = {
        'requests': requests 
    }
    return render(request, 'eo_requests.html', context)


def notification_page(request):
    posts = Post.objects.all()
    return render(request, "notificationpage.html", {"posts": posts})



def delete_post(request, post_id):   # for supervisor 
    userid = request.session.get('supervisor_id')
    print(userid)
    if not userid:
        return redirect('supervisor_login')  # use correct login name

    post = get_object_or_404(Post, id=post_id)
    post.delete()

    messages.success(request, "🗑️ Notification deleted successfully!")
    return redirect('notification_page')



def delete_post2(request, post_id):
    username = request.session.get('username')
    if not username:
        return redirect('loginpage')

    post = get_object_or_404(Post, id=post_id)

    deleted_list = post.deleted_by.split(",") if post.deleted_by else []
    if username not in deleted_list:
        deleted_list.append(username)
        post.deleted_by = ",".join(deleted_list)
        post.save()

    messages.success(request, "🗑️ Notification deleted successfully!")
    return redirect('notification_page2')

def Mainsupervisor(request):
    return render(request, "Mainsupervisor.html")

def complaints_supervisor(request):
    return render(request, "complaintssupervisor.html")

def requests_supervisor(request):
    return render(request, "requestssupervisor.html")


def Admpubsignup(request):
    public_users = Signup.objects.all()
    context = {
        'public_users': public_users
    }
    return render(request, "admpubsignup.html", context)

# Remove automatic ID/passcode generation if admin enters manually

import random
import string
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Supervisor, EOLogin


# # Auto ID generator
# def generate_id(prefix, length=6):
#     return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# def create_user(request):
#     if request.method == "POST":

#         role = request.POST.get("role")
#         password = request.POST.get("password")

#         # Validate
#         if not role or not password:
#             messages.error(request, "All fields are required.")
#             return redirect("admin_dashboard")

#         # -----------------------------------------------------
#         # EO LOGIN CREATION  (Same Function)
#         # -----------------------------------------------------
#         if role == "EO":
#             eo_id = generate_id("EO")

#             eo = EOLogin.objects.create(
#                 emp_number=eo_id,
#                 password=make_password(password)
#             )

#             messages.success(request, f"EO Login Created Successfully! ID: {eo_id}")
#             return redirect("admin_dashboard")

#         # -----------------------------------------------------
#         # SUPERVISOR LOGIN CREATION  (Same Function)
#         # -----------------------------------------------------
#         elif role == "Supervisor":
#             sup_id = generate_id("SUP")

#             Supervisor.objects.create(
#                 supervisor_id=sup_id,
#                 password=make_password(password)
#             )

#             messages.success(request, f"Supervisor Login Created Successfully! ID: {sup_id}")
#             return redirect("admin_dashboard")

#         else:
#             messages.error(request, "Invalid role selected.")
#             return redirect("admin_dashboard")

#     return redirect("admin_dashboard")


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import EOLogin


def login4(request):
    if request.method == "POST":
        emp_number = request.POST.get("emp_number")
        password = request.POST.get("password")

        # Check if EO ID exists
        try:
            user = EOLogin.objects.get(emp_number=emp_number)
        except EOLogin.DoesNotExist:
            messages.error(request, "❌ Invalid Employee Number or Password.")
            return redirect('login4')

        # Check password
        if check_password(password, user.password):
            request.session['eo_emp_number'] = user.emp_number  # Save session
            messages.success(request, "✅ Login Successful!")
            return redirect('eo_dashboard')  # Your EO Dashboard URL
        else:
            messages.error(request, "❌ Invalid Employee Number or Password.")
            return redirect('login4')

    return render(request, "loginpageeo.html")

def create_admin_user(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if role and username and password:
            # Create user
            user = User.objects.create_user(username=username, password=password)
            # Optional: you can save the role in user profile or groups
            messages.success(request, f"{role} account created successfully!")
        return redirect('mainadmin')  # your admin page URL name
    else:
        return redirect('mainadmin')
    

def Posts(request):
    posts=Post.objects.all().order_by('-created_at')
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        created_at = request.POST.get("datetime") or timezone.now()
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        new_det=Post(
            title=title,
            message=message,
            image=image,
            video=video,
            created_at=created_at
        )
        new_det.save()
        posts=Post.objects.all().order_by('-created_at')
        return redirect('Posts')  # redirect to post list after submission
    return render(request, "posts.html", {"posts": posts})
