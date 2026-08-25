from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Course, Student, Faculty, Payment, SiteSetting

# Create your views here.

# -------------------------
# Authentication Views
# -------------------------

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")

    return render(request, "auth/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

# -------------------------
# Dashboard
# -------------------------

@login_required
def dashboard_view(request):
    # Get site settings for navigation
    settings = SiteSetting.objects.first()

    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_faculty = Faculty.objects.count()
    total_payments = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    due_fees = Student.objects.aggregate(total=Sum("due_fee"))["total"] or 0

    return render(request, "dashboard.html", {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_faculty": total_faculty,
        "total_payments": total_payments,
        "due_fees": due_fees,
        "settings": settings,
    })

# -------------------------
# CRUD for Course
# -------------------------

@login_required
def course_list(request):
    courses = Course.objects.all()
    settings = SiteSetting.objects.first()
    return render(request, "course/list.html", {
        "courses": courses,
        "settings": settings
    })

@login_required
def course_add(request):
    if request.method == "POST":
        name = request.POST["name"]
        fee = request.POST["fee"]
        description = request.POST["description"]
        Course.objects.create(name=name, fee=fee, description=description)
        messages.success(request, "Course added successfully!")
        return redirect("course_list")

    settings = SiteSetting.objects.first()
    return render(request, "course/add.html", {"settings": settings})

@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.name = request.POST["name"]
        course.fee = request.POST["fee"]
        course.description = request.POST["description"]
        course.save()  # This will trigger signal to update student fees
        messages.success(request, "Course updated successfully!")
        return redirect("course_list")

    settings = SiteSetting.objects.first()
    return render(request, "course/update.html", {
        "course": course,
        "settings": settings
    })

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_name = course.name
    course.delete()
    messages.success(request, f"Course '{course_name}' deleted successfully!")
    return redirect("course_list")

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    settings = SiteSetting.objects.first()
    return render(request, "course/detail.html", {
        "course": course,
        "settings": settings
    })

# -------------------------
# CRUD for Student
# -------------------------

@login_required
def student_list(request):
    students = Student.objects.all()
    settings = SiteSetting.objects.first()
    return render(request, "student/list.html", {
        "students": students,
        "settings": settings
    })

@login_required
def student_add(request):
    if request.method == "POST":
        # Create student first
        student = Student(
            first_name=request.POST["first_name"],
            middle_name=request.POST.get("middle_name", ""),
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            phone_number=request.POST["phone_number"],
            gender=request.POST["gender"],
            city=request.POST["city"],
            address=request.POST["address"],
        )

        if request.FILES.get("profile_picture"):
            student.profile_picture = request.FILES["profile_picture"]

        student.save()

        # Handle course enrollment
        course_ids = request.POST.getlist("courses")
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)
            student.courses.set(courses)

        # Calculate fees after course assignment
        student.calculate_fees()

        messages.success(request, f"Student '{student.first_name} {student.last_name}' added successfully!")
        return redirect("student_list")

    courses = Course.objects.all()
    settings = SiteSetting.objects.first()
    return render(request, "student/add.html", {
        "courses": courses,
        "settings": settings
    })

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.first_name = request.POST["first_name"]
        student.middle_name = request.POST.get("middle_name", "")
        student.last_name = request.POST["last_name"]
        student.email = request.POST["email"]
        student.phone_number = request.POST["phone_number"]
        student.gender = request.POST["gender"]
        student.city = request.POST["city"]
        student.address = request.POST["address"]

        if request.FILES.get("profile_picture"):
            student.profile_picture = request.FILES["profile_picture"]

        student.save()

        # Handle course enrollment updates
        course_ids = request.POST.getlist("courses")
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)
            student.courses.set(courses)
        else:
            student.courses.clear()

        # Recalculate fees after changes
        student.calculate_fees()

        messages.success(request, f"Student '{student.first_name} {student.last_name}' updated successfully!")
        return redirect("student_list")

    courses = Course.objects.all()
    settings = SiteSetting.objects.first()
    return render(request, "student/update.html", {
        "student": student,
        "courses": courses,
        "settings": settings
    })

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student_name = f"{student.first_name} {student.last_name}"
    student.delete()
    messages.success(request, f"Student '{student_name}' deleted successfully!")
    return redirect("student_list")

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    payments = student.payments.all().order_by('-payment_date')
    settings = SiteSetting.objects.first()
    return render(request, "student/detail.html", {
        "student": student,
        "payments": payments,
        "settings": settings
    })

# -------------------------
# CRUD for Faculty
# -------------------------

@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()
    settings = SiteSetting.objects.first()
    return render(request, "faculty/list.html", {
        "faculties": faculties,
        "settings": settings
    })

@login_required
def faculty_add(request):
    if request.method == "POST":
        Faculty.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            subject=request.POST["subject"]
        )
        messages.success(request, "Faculty member added successfully!")
        return redirect("faculty_list")

    settings = SiteSetting.objects.first()
    return render(request, "faculty/add.html", {"settings": settings})

@login_required
def faculty_update(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)

    if request.method == "POST":
        faculty.first_name = request.POST["first_name"]
        faculty.last_name = request.POST["last_name"]
        faculty.subject = request.POST["subject"]
        faculty.save()
        messages.success(request, f"Faculty '{faculty.first_name} {faculty.last_name}' updated successfully!")
        return redirect("faculty_list")

    settings = SiteSetting.objects.first()
    return render(request, "faculty/update.html", {
        "faculty": faculty,
        "settings": settings
    })

@login_required
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    faculty_name = f"{faculty.first_name} {faculty.last_name}"
    faculty.delete()
    messages.success(request, f"Faculty '{faculty_name}' deleted successfully!")
    return redirect("faculty_list")

@login_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    settings = SiteSetting.objects.first()
    return render(request, "faculty/detail.html", {
        "faculty": faculty,
        "settings": settings
    })

# -------------------------
# CRUD for Payment
# -------------------------

@login_required
def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    settings = SiteSetting.objects.first()
    return render(request, "payment/list.html", {
        "payments": payments,
        "settings": settings
    })

@login_required
def payment_add(request):
    if request.method == "POST":
        student_id = request.POST["student"]
        faculty_id = request.POST.get("faculty")

        payment = Payment.objects.create(
            student_id=student_id,
            faculty_id=faculty_id if faculty_id else None,
            amount=request.POST["amount"],
            remarks=request.POST.get("remarks", "")
        )

        messages.success(request, f"Payment of ${payment.amount} recorded successfully!")
        return redirect("payment_list")

    students = Student.objects.all().order_by('first_name', 'last_name')
    faculties = Faculty.objects.all().order_by('first_name', 'last_name')
    settings = SiteSetting.objects.first()

    return render(request, "payment/add.html", {
        "students": students,
        "faculties": faculties,
        "settings": settings
    })

@login_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == "POST":
        old_amount = payment.amount
        payment.amount = request.POST["amount"]
        payment.remarks = request.POST.get("remarks", "")
        payment.save()  # This will trigger fee recalculation

        messages.success(request, f"Payment updated successfully!")
        return redirect("payment_list")

    settings = SiteSetting.objects.first()
    return render(request, "payment/update.html", {
        "payment": payment,
        "settings": settings
    })

@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    amount = payment.amount
    student_name = f"{payment.student.first_name} {payment.student.last_name}"
    payment.delete()  # This will trigger fee recalculation
    messages.success(request, f"Payment of ${amount} for {student_name} deleted successfully!")
    return redirect("payment_list")

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    settings = SiteSetting.objects.first()
    return render(request, "payment/detail.html", {
        "payment": payment,
        "settings": settings
    })

# -------------------------
# Reports
# -------------------------

@login_required
def reports_view(request):
    # Recalculate all student fees before generating report
    for student in Student.objects.all():
        student.calculate_fees()

    total_fees = Student.objects.aggregate(total=Sum("total_fee"))["total"] or 0
    collected_fees = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    due_fees = Student.objects.aggregate(total=Sum("due_fee"))["total"] or 0
    students_count = Student.objects.count()

    settings = SiteSetting.objects.first()

    return render(request, "reports.html", {
        "total_fees": total_fees,
        "collected_fees": collected_fees,
        "due_fees": due_fees,
        "students_count": students_count,
        "settings": settings,
    })

# -------------------------
# Settings (Site Settings)
# -------------------------

@login_required
def settings_view(request):
    settings = SiteSetting.objects.first()

    if request.method == "POST":
        if not settings:
            settings = SiteSetting.objects.create()

        settings.site_name = request.POST["site_name"]
        settings.footer_text = request.POST.get("footer_text", "")

        if request.FILES.get("logo"):
            settings.logo = request.FILES["logo"]

        settings.save()
        messages.success(request, "Settings updated successfully!")
        return redirect("settings")

    return render(request, "settings.html", {"settings": settings})

# -------------------------
# Utility Functions
# -------------------------

@login_required
def recalculate_all_fees(request):
    """Manual fee recalculation for all students"""
    students = Student.objects.all()
    for student in students:
        student.calculate_fees()

    messages.success(request, f"Fees recalculated for {students.count()} students!")
    return redirect("dashboard")
