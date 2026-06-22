from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Program, Registration, Feedback, Instructor
from django.http import JsonResponse
import random
from django.templatetags.static import static

def homepage(request):
    return render(request, 'homepage.html')

def admin_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_staff = True
            user.save()
            messages.success(request, "Admin registered succesfully")
            return redirect('admin_login')
        
    return render(request, 'admin_register.html')


def admin_login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'admin_login.html')

def instructor_login(request):
    if request.method == 'POST' :
        email = request.POST.get('insEmail')
        insId = request.POST.get('insId')
    
        try:
            instructor = Instructor.objects.get(insEmail=email, insId=insId)
            request.session['instructor_id'] = instructor.insId
            return redirect('instructor_dashboard', insId=instructor.insId)
        except Instructor.DoesNotExist:
            messages.error(request, 'Invalid Username or Password')

    return render(request, 'instructor_login.html')

def admin_dashboard(request):
    program_count = Program.objects.count()
    registration_count = Registration.objects.count()
    feedback_count = Feedback.objects.count()
    instructor_count = Instructor.objects.count()

    context = {
        'program_count' : program_count,
        'registration_count' : registration_count,
        'feedback_count' : feedback_count,
        'instructor_count': instructor_count, 
    }

    return render(request, 'admin_dashboard.html', context)

def instructor_dashboard(request, insId):
    instructor = Instructor.objects.get(insId=insId)
    programs = Program.objects.filter(progInstructor=instructor)
    
    return render(request, 'instructor_dashboard.html', {'programs': programs, 'instructor': instructor})

def add_program(request):
    if request.method == 'POST':
        title = request.POST.get('progTitle')
        description = request.POST.get('progDescription')
        date = request.POST.get('progDate')
        time = request.POST.get('progTime')
        instructor_id = request.POST.get('progInstructor')
        venue = request.POST.get('progVenue')
        capacity = request.POST.get('progCapacity')
        registration = request.POST.get('progRegistration') == 'True'
        
        instructor = Instructor.objects.get(insId=instructor_id)

        Program.objects.create(
            progTitle=title,
            progDescription=description,
            progDate=date,
            progTime=time,
            progInstructor=instructor,
            progVenue=venue,
            progCapacity=capacity,
            progRegistration=registration 
        )

        request.session['announcement'] = f"New Program: {title}"

        return redirect('admin_dashboard') 

    instructors = Instructor.objects.all()
    return render(request, 'addprogram.html', {'instructors': instructors})

def add_instructor(request):
    if request.method == 'POST':
        ins_id = request.POST.get('insId')
        name = request.POST.get('insName')
        ic = request.POST.get('insIC')
        email = request.POST.get('insEmail')
        number = request.POST.get('insNumber')

        Instructor.objects.create(
            insId=ins_id,
            insName=name,
            insIc=ic,
            insEmail=email,
            insNumber=number
        )

        return redirect('admin_dashboard') 

    return render(request, 'add_instructor.html')

def dashboard_program(request):
    program_list = Program.objects.all()

    return render(request, 'dashboard_program.html', {'programs': program_list})

def dashboard_instructor(request):
    instructor_list = Instructor.objects.all()

    return render(request, 'dashboard_instructor.html', {'instructor_list': instructor_list})

def dashboard_register(request):
    register_list = Registration.objects.all()

    return render(request, 'dashboard_register.html', {'register': register_list})

def delete_program(request, id):
    if request.method == 'DELETE':
        try:
            program = Program.objects.get(id=id)
            program.delete()
            return JsonResponse({'status': 'success'})
        except Program.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Program Not Found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)

def delete_instructor(request, insId):
    if request.method == 'DELETE':
        try:
            instructor = Instructor.objects.get(insId=insId)
            instructor.delete()
            return JsonResponse({'status': 'success'})
        except Instructor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Program Not Found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)

def delete_register(request, id):
    if request.method == 'DELETE':
        try:
            register = Registration.objects.get(id=id)
            register.delete()
            return JsonResponse({'status': 'success'})
        except Registration.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Program Not Found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)

def delete_feedback(request, id):
    if request.method == 'DELETE':
        try:
            feedback = Feedback.objects.get(id=id)
            feedback.delete()
            return JsonResponse({'status': 'success'})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Program Not Found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)

def edit_instructor(request, insId):
    instructor = get_object_or_404(Instructor, insId=insId)

    if request.method == 'POST':
        new_insId = request.POST.get('insId')
        new_insName = request.POST.get('insName')
        new_insIc = request.POST.get('insIc')
        new_insEmail = request.POST.get('insEmail')
        new_insNumber = request.POST.get('insNumber')

        if (
            instructor.insId != new_insId or
            instructor.insName != new_insName or
            instructor.insIc != new_insIc or
            instructor.insEmail != new_insEmail or
            instructor.insNumber != new_insNumber 
        ):
            instructor.insId = new_insId 
            instructor.insName = new_insName 
            instructor.insIc = new_insIc 
            instructor.insEmail = new_insEmail 
            instructor.insNumber = new_insNumber 
            instructor.save()

        return redirect('dashboard_instructor')
    
    return render(request, 'edit_instructor.html', {'instructor': instructor})

def edit_program(request, id):
    program = get_object_or_404(Program, id=id)

    if request.method == 'POST':
        new_title = request.POST.get('progTitle')
        new_description = request.POST.get('progDescription')
        new_date = request.POST.get('progDate')
        new_time = request.POST.get('progTime')
        new_venue = request.POST.get('progVenue')
        new_capacity = request.POST.get('progCapacity')
        new_instructor_id = request.POST.get('progInstructor')
        new_program = request.POST.get('progRegistration')

        if (
            program.progTitle != new_title or
            program.progDescription != new_description or 
            program.progDate != new_date or 
            program.progTime != new_time or 
            program.progVenue != new_venue or 
            program.progCapacity != new_capacity or 
            program.progInstructor != new_instructor_id or
            program.progRegistration != new_program
        ):
            program.progTitle = new_title
            program.progDescription = new_description
            program.progDate = new_date
            program.progTime = new_time
            program.progVenue = new_venue
            program.progCapacity = new_capacity
            program.progRegistration = new_program
            program.progInstructor = Instructor.objects.get(insId = new_instructor_id)
            program.save()

        return redirect('dashboard_program')
    
    instructors = Instructor.objects.all()

    return render(request, 'edit_program.html',
                   {'program':program, 
                    'instructors':instructors},)

def edit_register(request, id):
    register = get_object_or_404(Registration, id=id)

    if request.method == 'POST':
        new_RegName = request.POST.get('regName')
        new_RegIc = request.POST.get('regIc')
        new_RegEmail = request.POST.get('regEmail')


        if (
            register.regName != new_RegName or
            register.regIc != new_RegIc or
            register.regEmail != new_RegEmail 
        ):
            register.regName = new_RegName 
            register.regIc = new_RegIc 
            register.regEmail = new_RegEmail 
            register.save()

        return redirect('dashboard_register')
    
    return render(request, 'edit_register.html', {'register': register})

def program_list(request):
    programs = Program.objects.all()

    search_query = request.GET.get('search', '')

    if search_query:
        programs = Program.objects.filter(progTitle__icontains=search_query)
    else:
        programs = Program.objects.all()
    

    images = [
        'program1.jpg',
        'program2.jpg',
        'program3.jpg',
        'program4.jpg',
        'program5.jpg',
    ]

    program_images = []
    for p in programs:
        image_url = static(random.choice(images))
        program_images.append({'program': p, 'image': image_url})

    announcement = request.session.pop('announcement', None)

    return render(request, 'program_list.html', {'programs': program_images, 'search':search_query, 'announcement': announcement})
    
def more_info(request, id):
    programs = get_object_or_404(Program, id=id)
    register_count = Registration.objects.filter(regProgram= programs).count()

    return render(request, 'moreinfo.html', {'program': programs, 'registration_count': register_count})

def register_program(request, id):
    programs = get_object_or_404(Program, id=id)

    if request.method == 'POST':
        name = request.POST.get('regName')
        ic = request.POST.get('regIc')
        email = request.POST.get('regEmail')

        Registration.objects.create(
            regProgram= programs,
            regName= name,
            regIc= ic,
            regEmail = email
        )

        return redirect('more_info', id=id)

    return render(request, 'registration.html', {'program':programs})

def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('feedName')
        message = request.POST.get('feedMessage')
        program = request.POST.get('feedProgram')

        program = Program.objects.get(id=program)
        Feedback.objects.create(
            feedName=name,
            feedMessage=message,
            feedProgram=program
        )

    program_list = Program.objects.all()
    return render(request, 'feedback.html', {'program': program_list})

def dashboard_feedback(request):
    feedback = Feedback.objects.all()
    return render(request, 'dashboard_feedback.html', {'feedback': feedback})    
    

        
        





