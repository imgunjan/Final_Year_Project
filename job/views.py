from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def admin_login(request):
    error = ""
    if request.method == "POST":
        user_name = request.POST["uname"]
        password = request.POST["pwd"]
        user = authenticate(username=user_name, password=password)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    dictionary = {"error": error}
    return render(request, "admin_login.html", dictionary)


def user_login(request):
    error = ""
    if request.method == "POST":
        user_email = request.POST["uname"]
        password = request.POST["pwd"]
        user = authenticate(username=user_email, password=password)
        if user:
            try:
                user1 = EmployeeUser.objects.get(user=user)
                if user1.type == "employee":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    dictionary = {"error": error}
    return render(request, "user_login.html", dictionary)


def recruiter_login(request):
    error = ""
    if request.method == "POST":
        user_email = request.POST["uname"]
        password = request.POST["pwd"]
        user = authenticate(username=user_email, password=password)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    dictionary = {"error": error}
    return render(request, "recruiter_login.html", dictionary)


def recruiter_signup(request):
    error = ""
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        password = request.POST["pwd"]
        email = request.POST["email"]
        contact_number = request.POST["contact"]
        gender = request.POST["gender"]
        image = request.FILES["image"]
        company = request.POST["company"]
        try:
            user = User.objects.create_user(
                first_name=first_name,
                username=email,
                password=password,
                last_name=last_name,
            )
            Recruiter.objects.create(
                user=user,
                mobile=contact_number,
                image=image,
                gender=gender,
                type="recruiter",
                company=company,
                status="pending",
            )
            error = "No"
        except:
            error = "Yes"
    dictionary = {"error": error}
    return render(request, "recruiter_signup.html", dictionary)


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    return render(request, "admin_home.html")


def user_home(request):
    if not request.user.is_authenticated:
        return redirect("user_login")
    return render(request, "user_home.html")


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect("recruiter_login")
    return render(request, "recruiter.html")


def Logout(request):
    logout(request)
    return render(request, "index.html")


def user_signup(request):
    error = ""
    if request.method == "POST":
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        password = request.POST["pwd"]
        email = request.POST["email"]
        contact_number = request.POST["contact"]
        gender = request.POST["gender"]
        image = request.FILES["image"]
        try:
            user = User.objects.create_user(
                first_name=first_name,
                username=email,
                password=password,
                last_name=last_name,
            )
            EmployeeUser.objects.create(
                user=user,
                mobile=contact_number,
                image=image,
                gender=gender,
                type="employee",
            )
            error = "No"
        except:
            error = "Yes"
    dictionary = {"error": error}

    return render(request, "user_signup.html", dictionary)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    data = EmployeeUser.objects.all()
    dictionary = {"data": data}
    return render(request, "view_users.html", dictionary)


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    employee = User.objects.get(id=pid)
    employee.delete()
    return redirect("view_users")


def delete_recruiter(request, pid):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    recruiter = User.objects.get(id=pid)
    recruiter.delete()
    return redirect("recruiter_all")


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    data = Recruiter.objects.filter(status="pending")
    dictionary = {"data": data}
    return render(request, "recruiter_pending.html", dictionary)


def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    error = ""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method == "POST":
        s = request.POST["status"]
        recruiter.status = s
        try:
            recruiter.save()
            error = "no"
        except:
            error = "yes"
    dictionary = {"recruiter": recruiter, "error": error}
    return render(request, "change_status.html", dictionary)


def change_password_admin(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    error = ""
    if request.method == "POST":
        old_pass = request.POST["currentpassword"]
        new_pass = request.POST["newpassword"]
        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                error = "no"
            else:
                error = "no"

        except:
            error = "yes"
    dictionary = {"error": error}
    return render(request, "change_password_admin.html", dictionary)


def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    data = Recruiter.objects.filter(status="Accept")
    dictionary = {"data": data}
    return render(request, "recruiter_accepted.html", dictionary)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    data = Recruiter.objects.filter(status="Reject")
    dictionary = {"data": data}
    return render(request, "recruiter_rejected.html", dictionary)


def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")
    data = Recruiter.objects.all()
    dictionary = {"data": data}
    return render(request, "recruiter_all.html", dictionary)
