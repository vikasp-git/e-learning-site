from django.shortcuts import render
import pyrebase
from django.contrib import auth
from django.conf import settings
from django.core.files.storage import FileSystemStorage
config = {
    'apiKey': "AIzaSyDacvxdaPmR8qgOqHWXSFKYqJQP1aaDae0",
    'authDomain': "kritiapp-2f73b.firebaseapp.com",
    'databaseURL': "https://kritiapp-2f73b.firebaseio.com",
    'projectId': "kritiapp-2f73b",
    'storageBucket': "kritiapp-2f73b.appspot.com",
    'messagingSenderId': "924829656507",
    'appId': "1:924829656507:web:753c82b560e4a375d1d09e",
  'measurementId': "G-13JKYMC09Z"
  }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def home(request):
    return render(request,'home.html')

def postsign(request):     #login with credentials
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email,password)
    except:
        message = "invalid credentials..Try signing up"           # if wrong credentials returns to home page
        return render(request, "home.html", {"msg":message})

    if email in ['cse@iitg.ac.in','eee@iitg.ac.in','codingclub@iitg.ac.in','finance@iitg.ac.in']: # if email belongs to these
        user_id = user['localId']
        name = database.child('ClubDept').child(user_id).child("name").get()
        all_courses = database.child(name.val()).child("courses").get()

        courses=[]
        count=0
        try:
            for course in all_courses:
                courses.append(str(count)+" "+course.key())
                count+=1
        except:
            pass
        session_id=user['idToken']
        request.session['user_id'] = str(session_id)
        return render(request,'upload.html',{"name": name.val(), "courses": courses})

    else:
        user_id = user['localId']
        name = database.child('Users').child(user_id).child("name").get()
        session_id = user['idToken']
        request.session['user_id'] = str(session_id)
        return render(request, "index.html", {"name": name.val()} )

def upload(request):
    idtoken= request.session['user_id']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    user_id = a['localId']
    name = database.child("Users").child(user_id).child("name").get()
    return render(request, "upload_common.html", {"name": name.val()})

def logout(request):      # logout of the website
    auth.logout(request)
    return render(request,'home.html')

def logout(request):
    auth.logout(request)
    return render(request,'home.html')

def postsignup(request):

    name=request.POST.get('name')
    roll=request.POST.get('rollno')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data={"name":name,"roll":roll}
        database.child("Users").child(uid).set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    return render(request,"home.html")



def create(request):

    return render(request,'upload_home.html')

def upload_save(request):
    dept = request.POST.get('dept')
    OverView =request.POST.get('overview')
    url = request.POST.get('url')
    title = request.POST.get('vtitle')
    data_json = {
        'bookOverview': OverView,
        'url': url
    }
    database.child(dept).child('Reading').child(title).set(data_json)
    return render(request,'Welcome.html')

def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print(("mili"+str(millis)))
    # dept = request.POST.get('dept')
    
    vtitle = request.POST.get('vtitle')
    OverView =request.POST.get('progress')
    url = request.POST.get('url')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    dept = database.child("ClubDept").child(a).child("name").get()
    if request.POST.get('work'):
        Title = request.POST.get('work')
    else:
        all_courses = database.child(dept.val()).child("courses").get()
        courses = []
        try:
            for course in all_courses.each():
                courses.append(course.key())
        except :
            pass
        # print (";;;;;;;;;;;;;;;;;;;;",courses)
        count = request.POST.get('title')
