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
        request.session['phoneno'] = phoneno  # Save phone number in session
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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Supervisor


def loginpage3(request):
    if request.method == "POST":
        supervisor_id = request.POST.get("supervisor_id")
        password = request.POST.get("password")

        user = Supervisor.objects.filter(supervisor_id=supervisor_id, password=password).first()

        if user:
            # STORE INTEGER ID
            request.session["supervisor_id"] = user.id
            messages.success(request, "Login Successful!")
            return redirect("supervisor_tasks")

        messages.error(request, "Invalid ID or password")
        return render(request, "loginsupervisor.html")

    return render(request, "Mainsupervisor.html")


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

from django.shortcuts import render, get_object_or_404
from .models import Complaint, Supervisor

# View to add area
# models.py
# Area model is defined in the app's models.py and already imported at the top of this file,
# so do not redefine it here to avoid duplicate definitions and syntax errors.
from django.shortcuts import render, redirect
from .models import Area

def add_area(request):
    if request.method == "POST":
        area_name = request.POST.get("name")
        if area_name:
            Area.objects.create(name=area_name)
            return redirect("add_area")

    return render(request, "add_area.html")


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

# complaint form view
def complaint_form(request):
    if request.method == "POST":

        user = request.POST.get("user")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        area_name = request.POST.get("area_name")
        location = request.POST.get("location")
        description = request.POST.get("description")
        other_type = request.POST.get("otherType")
        file = request.FILES.get("file")

        complaint_types = request.POST.getlist("complaintType")

        # Validation
        if not complaint_types:
            messages.error(request, "Please select at least one complaint type.")
            return redirect("mainpage")

        # Handle Others
        if "Others" in complaint_types:
            complaint_types.remove("Others")
            if other_type:
                complaint_types.append(other_type)

        complaint_type_final = ", ".join(complaint_types)

        # Get supervisor using Area ForeignKey
        supervisor = Supervisor.objects.filter(
            area__name=area_name
        ).first()

        supervisor_name = supervisor.supervisor_name if supervisor else None

        Complaint.objects.create(
            user=user,
            phone=phone,
            address=address,
            area_name=area_name,
            location=location,
            complaint_type=complaint_type_final,
            description=description,
            file=file,
            date_time=timezone.now(),
            supervisor=supervisor,
            supervisor_name=supervisor_name
        )

        messages.success(request, "✅ Complaint submitted successfully!")
        return redirect("mainpage")

    return redirect("mainpage")


def requestform(request):
    if request.method == "POST":

        name = request.POST.get("name")
        phone_number = request.POST.get("phone")
        address = request.POST.get("address")
        area_name = request.POST.get("area_name")
        other_type = request.POST.get("otherType")

        request_types = request.POST.getlist("requestType")

        # Validation
        if not request_types:
            messages.error(request, "Please select at least one request type.")
            return redirect("mainpage")

        # Handle Others
        if "Others" in request_types:
            request_types.remove("Others")
            if other_type:
                request_types.append(other_type)

        request_type_final = ", ".join(request_types)

        # Get supervisor using Area FK
        supervisor = Supervisor.objects.filter(
            area__name=area_name
        ).first()

        Request.objects.create(
            name=name,
            phone_number=phone_number,
            address=address,
            area_name=area_name,
            request_type=request_type_final,
            other_type=other_type,
            supervisor=supervisor
        )

        messages.success(request, "✅ Request submitted successfully!")
        return redirect("mainpage")

    return redirect("mainpage")


# =========================
# MODELS FOR POSTS, ACHIEVEMENTS, TASKShtl

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

from django.shortcuts import render
from .models import Supervisor, Area

def Tasks(request):
    supervisors = Supervisor.objects.all()
    areas = Area.objects.all()

    return render(request, "task.html", {
        "supervisors": supervisors,
        "areas": areas
    })
  
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

# View to add area
def Add_area(request):
    if request.method == "POST":
        name = request.POST.get('name')

        if Area.objects.filter(name=name).exists():
            messages.error(request, "❌ Area already exists!")
        else:
            Area.objects.create(name=name)
            messages.success(request, "✅ Area added successfully!")

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

from .models import Request, Complaint

from .models import Area, Complaint, Request

def mainpage(request):
    phoneno = request.session.get("phoneno", None)
    print("SESSION PHONE:", phoneno)

    # Fetch areas for dropdown
    areas = Area.objects.all()

    # Tracking counts (safe when session is empty)
    total_complaints = Complaint.objects.filter(phone=phoneno).count() if phoneno else 0
    total_requests = Request.objects.filter(phone_number=phoneno).count() if phoneno else 0

    return render(request, "Mainpage.html", {
        "areas": areas,
        "total_complaints": total_complaints,
        "total_requests": total_requests,
    })

 


def Mainpageadmin(request):
    admin_username = request.session.get('admin_username')
    print("admins: ",admin_username)

    # Count all complaints from all users
    total_complaints = Complaint.objects.count()

    # Count all requests from all users
    total_requests = Request.objects.count()
    supervisors = Supervisor.objects.all()
    eos= EOLogin.objects.all()
    print("totals: ",total_complaints, total_requests)

    return render(request, "Mainpageadmin.html", {
        "admin_username": admin_username,
        "total_complaints": total_complaints,
        "total_requests": total_requests,
        "supervisors": supervisors,
        "eos": eos
        })

from django.shortcuts import render
from django.db.models import Count
from .models import Complaint, Request, Supervisor, Area
from django.utils import timezone
def AdminTasks(request):
    # complaint status counts
    complaint_stats = Complaint.objects.values('status').annotate(count=Count('status'))
    complaint_stats = {
        'submitted': 0,
        'verified': 0,
        'pending': 0,
        'completed': 0,
        **{c['status']: c['count'] for c in complaint_stats}
    }

    # request status counts
    request_stats = Request.objects.values('status').annotate(count=Count('status'))
    request_stats = {
        'submitted': 0,
        'verified': 0,
        'pending': 0,
        'completed': 0,
        **{r['status']: r['count'] for r in request_stats}
    }

    complaints = Complaint.objects.all()
    requests = Request.objects.all()
    supervisors = Supervisor.objects.all()
    areas = Area.objects.all()

    return render(request, "tasks.html", {
        "complaints": complaints,
        "requests": requests,
        "supervisors": supervisors,
        "areas": areas,
        "complaint_stats": complaint_stats,
        "request_stats": request_stats,   # ← REQUIRED
    })

# views.py
from django.shortcuts import render
from django.db.models import Count
from .models import Complaint, Request

def analytics_dashboard(request):
    # Complaints by type
    complaints = Complaint.objects.values('complaint_type').annotate(count=Count('complaint_type'))
    complaint_data = {c['complaint_type']: c['count'] for c in complaints}

    # Requests by type
    requests = Request.objects.values('request_type').annotate(count=Count('request_type'))
    request_data = {r['request_type']: r['count'] for r in requests}

    return render(request, 'Mainpageadmin.html', {
        'complaint_data': complaint_data,
        'request_data': request_data,
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


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Supervisor, EOLogin


# ----------------------
# MAIN ADMIN PAGE
# ----------------------
# def Mainpageadmin(request):
#     supervisors = Supervisor.objects.all()
#     eos = EOLogin.objects.all()

#     return render(request, "mainpageadmin.html", {
#         "supervisors": supervisors,
#         "eos": eos,
#         "admin_username": request.session.get("admin_username"),
#     })


# ----------------------
# DELETE USER (Supervisor / EO)
# ----------------------

import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Supervisor, EOLogin

logger = logging.getLogger(__name__)

def delete_user(request, role, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        if role == "supervisor":
            user = Supervisor.objects.get(id=user_id)
        elif role == "eo":
            user = EOLogin.objects.get(id=user_id)
        else:
            return JsonResponse({"error": "Invalid role"}, status=400)

        user.delete()
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from .models import Signup
# Do not perform database queries at import time; query inside views instead
# PublicSignup.objects.all()
def signup_list(request):
    public_users = Signup.objects.all()
    return render(request, "eomain.html", {"public_users": public_users})



from django.shortcuts import render
from .models import Complaint, Request
from django.db.models import Count

def dashboard_stats(request):

    # Total Counts
    total_complaints = Complaint.objects.count()
    total_requests = Request.objects.count()

    # Latest Table Entries
    complaints = Complaint.objects.all().order_by('-id')
    requests_list = Request.objects.all().order_by('-id')

    # Complaint Chart Data
    complaint_data = Complaint.objects.values('complaint_type').annotate(count=Count('complaint_type'))
    complaint_types = [c['complaint_type'] for c in complaint_data]
    complaint_counts = [c['count'] for c in complaint_data]

    # Request Chart Data
    request_data = Request.objects.values('request_type').annotate(count=Count('request_type'))
    request_types = [r['request_type'] for r in request_data]
    request_counts = [r['count'] for r in request_data]

    context = {
        "total_complaints": total_complaints,
        "total_requests": total_requests,
        "complaints": complaints,
        "requests": requests_list,
        "complaint_types": complaint_types,
        "complaint_counts": complaint_counts,
        "request_types": request_types,
        "request_counts": request_counts,
    }

    return render(request, "Mainpage.html", context)



# views.py
from django.shortcuts import render, redirect
from .models import Complaint, Request, Supervisor

def supervisor_tasks(request):

    # Get supervisor ID from session
    sid = request.session.get("supervisor_id")
    if not sid:
        return redirect("supervisor_login")

    supervisor = Supervisor.objects.get(id=sid)

    # Fetch tasks assigned to this supervisor
    complaints = Complaint.objects.filter(supervisor=supervisor)
    requests_qs = Request.objects.filter(supervisor=supervisor)

    # Status counts
    complaint_stats = {
        "submitted": complaints.filter(status="submitted").count(),
        "verified": complaints.filter(status="verified").count(),
        "pending": complaints.filter(status="pending").count(),
        "completed": complaints.filter(status="completed").count(),
    }

    request_stats = {
        "submitted": requests_qs.filter(status="submitted").count(),
        "verified": requests_qs.filter(status="verified").count(),
        "pending": requests_qs.filter(status="pending").count(),
        "completed": requests_qs.filter(status="completed").count(),
    }

    return render(request, "supervisor_tasks.html", {
        "supervisor": supervisor,
        "complaints": complaints,
        "requests": requests_qs,
        "complaint_stats": complaint_stats,
        "request_stats": request_stats,
    })
