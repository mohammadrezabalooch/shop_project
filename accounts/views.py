from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, OTPVerifyForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import OTPCode
import random
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.views.generic import FormView
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta

# Create your views here.


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        code = random.randint(10000, 99999)

        OTPCode.objects.create(user=user, code=str(code))

        send_mail(
            "کد ورود به وبسایت فروشگاه",
            f"کد ورود کاربر {user.username} {code} میباشد.",
            "sstthh@gmail.com",
            [user.email],
            fail_silently=False,
        )

        self.request.session["user_pk_for_otp"] = user.pk
        return redirect("otp-verify")


class OTPVerifyView(FormView):
    template_name = "registration/otpverify.html"
    form_class = OTPVerifyForm

    def form_valid(self, form):
        user_pk = self.request.session.get("user_pk_for_otp")
        if not user_pk:
            return redirect("login")

        entered_code = form.cleaned_data.get("code")
        user = get_user_model().objects.get(pk=user_pk)

        try:
            otp_record = OTPCode.objects.filter(user=user).latest("created_at")

        except OTPCode.DoesNotExist:
            form.add_error(None, "کد نامعتبر است.")
            return self.form_invalid(form)

        if otp_record.code != entered_code:
            form.add_error(None, "کد وارد شده صحیح نیست.")
            return self.form_invalid(form)

        if timezone.now() > otp_record.created_at + timedelta(minutes=10):
            form.add_error(None, "این فرم منقضی شده است دوباره وارد شوید")
            return self.form_invalid(form)

        login(self.request, user)
        otp_record.delete()
        del self.request.session["user_pk_for_otp"]

        return redirect("productlist")
