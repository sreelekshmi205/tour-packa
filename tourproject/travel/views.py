from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, LoginForm, PackageForm, BookingForm
from .models import Package, Booking

# Home Page
def home(request):
    return render(request, 'travel/home.html')

# User Registration
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Important!
            user.save()
            messages.success(request, "Registered successfully")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'travel/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(request, username=uname, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect('package_list')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'travel/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')

# View Approved Packages
def package_list(request):
    packages = Package.objects.filter(approved=True)
    return render(request, 'travel/package_list.html', {'packages': packages})

# Package Detail View
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk, approved=True)
    return render(request, 'travel/package_detail.html', {'package': package})

# Book a Package
@login_required
def book_package(request, pk):
    package = get_object_or_404(Package, pk=pk, approved=True)
    if request.method == 'POST':
        Booking.objects.create(user=request.user, package=package)
        messages.success(request, "Package booked successfully.")
        return redirect('package_list')
    return render(request, 'travel/book_package.html', {'package': package})

# Vendor Dashboard
@login_required
def vendor_dashboard(request):
    packages = Package.objects.filter(vendor=request.user)
    return render(request, 'travel/vendor_dashboard.html', {'packages': packages})

# Add New Package (Vendor)
@login_required
def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user
            package.save()
            messages.success(request, "Package added. Awaiting admin approval.")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm()
    return render(request, 'travel/add_package.html', {'form': form})

# Edit Package (Vendor)
@login_required
def edit_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Package updated successfully.")
            return redirect('vendor_dashboard')
    else:
        form = PackageForm(instance=package)
    return render(request, 'travel/edit_package.html', {'form': form})

# Delete Package (Vendor)
@login_required
def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk, vendor=request.user)
    if request.method == 'POST':
        package.delete()
        messages.success(request, "Package deleted successfully.")
        return redirect('vendor_dashboard')
    return render(request, 'travel/confirm_delete.html', {'package': package})

# Admin Dashboard - List of Unapproved Packages
@login_required
def admin_dashboard(request):
    pending = Package.objects.filter(approved=False)
    return render(request, 'travel/admin_dashboard.html', {'packages': pending})

# Approve Package (Admin)
@login_required
def approve_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.approved = True
    package.save()
    messages.success(request, "Package approved successfully.")
    return redirect('admin_dashboard')
