from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Student(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address = models.TextField()
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    admission_date = models.DateField(auto_now_add=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_fees(self):
        """Calculate and update student fees"""
        # Calculate total fee from enrolled courses
        total_fee = sum(course.fee for course in self.courses.all())

        # Calculate paid amount from payments
        paid_fee = self.payments.aggregate(total=Sum("amount"))["total"] or 0

        # Calculate due fee
        due_fee = total_fee - paid_fee

        # Update the fields directly to avoid recursion
        Student.objects.filter(pk=self.pk).update(
            total_fee=total_fee,
            paid_fee=paid_fee,
            due_fee=due_fee
        )

        # Refresh the instance to reflect changes
        self.refresh_from_db()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Only calculate fees if not a new record (ManyToMany not available yet)
        if not is_new:
            self.calculate_fees()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Faculty(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Faculties"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate student fees when payment is saved
        self.student.calculate_fees()

    def delete(self, *args, **kwargs):
        student = self.student
        super().delete(*args, **kwargs)
        # Recalculate student fees when payment is deleted
        student.calculate_fees()

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.first_name} {self.student.last_name}"

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default='Student Management System')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    footer_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"Settings for {self.site_name}"

# Signal handlers to automatically update student fees

@receiver(m2m_changed, sender=Student.courses.through)
def update_student_fees_on_course_change(sender, instance, action, pk_set, **kwargs):
    """Update student fees when courses are added/removed"""
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.calculate_fees()

@receiver(post_save, sender=Course)
def update_student_fees_on_course_save(sender, instance, **kwargs):
    """Update all student fees when course fee changes"""
    for student in instance.students.all():
        student.calculate_fees()
