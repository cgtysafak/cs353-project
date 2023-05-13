from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

class HomeView(View):
    def get(self, request):
        user_type = request.session['user_type']
        return render(request, 'career/home.html', {'user_type': user_type})

class UsersView(View):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM User;")
        users = cursor.fetchall()

        cursor.close()

        return render(request, 'career/users.html', {'users': users})

class LoginView(View):
    def get(self, request):
        return render(request, 'career/login.html')

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            statement = "SELECT * FROM User Where username= '" + username + "' AND password='" + password + "'"
            cursor = connection.cursor()
            cursor.execute(statement)
            user = cursor.fetchone()
            cursor.close()

        except:
            print("db cannot be found")
            return render(request, 'career/login.html')

        if user != None:
                request.session['username'] = username
                request.session['user_id'] = user[0]
                request.session['user_type'] = user[7]
                print("--------------------", request.session['user_type'])
                success = True
                context = {'success': success, 'username': username}
                # return JsonResponse(context)
                messages.success(request, 'You logged the system successfully')
                return HttpResponseRedirect("/home")
        else:
            messages.error(request, 'User cannot be found')
            return render(request, 'career/login.html')


class SignUpView(View):
    def get(self, request):
        return render(request, 'career/signup.html')

    def post(self, request):
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        passwordver = request.POST.get("passwordverification", "")
        fullname = request.POST.get("fullname", "")
        user_type = request.POST.get("usertype", "")
        registration_time = datetime.now() + timedelta(hours=3)


        if(password != passwordver):
            print("passwords are not same")
            return render(request, 'career/signup.html')
        else:
            if username !="" and email != "" and password != "":
                parameters = [fullname, username, password, email, registration_time, user_type]
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO User(full_name, username, password, email_address, date_of_registration, user_type) VALUES(%s,%s,%s,%s,%s, %s);",
                    parameters)
                cursor.close()
                connection.commit()

                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM USER WHERE username = '" + username + "'")
                user_id = cursor.fetchone()
                cursor.close()

                cursor = connection.cursor()
                cursor.execute("INSERT INTO NonAdmin(user_id) VALUES(%s);", user_id)
                cursor.close()
                connection.commit()
                print(user_type)

                if user_type == "Job Hunter":
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO RegularUser(user_id) VALUES(%s);", user_id)
                    cursor.close()
                    connection.commit()

                elif user_type == "Recruiter":
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO Recruiter(user_id) VALUES(%s);", user_id)
                    cursor.close()
                    connection.commit()

                elif user_type == "Career Expert":
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO CareerExpert(user_id) VALUES(%s);", user_id)
                    cursor.close()
                    connection.commit()

                request.session['username'] = username
                request.session['user_id'] = user_id
                request.session['type'] = user_type

                print("user is successfully created")
                return HttpResponseRedirect("/home")
            else:
                print("Please fill all information")
                return render(request, 'career/signup.html')


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect("/")


#class ExperienceView(View):

"""
def login(request):
    if request.method == 'POST':
        # get username and password from front-end
        post = request.POST
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        t = request.POST.get("type", "")
        # check if user exists if exists and password is correct send to index, if not show a warning
        try:
            stmt = "SELECT u_id, username, pw FROM " + t + " WHERE username = '" + username + "' AND pw = '" + password +"'"
            cursor = connection.cursor()
            cursor.execute(stmt)
            r = cursor.fetchone()
            cursor.close()
        except:
            print("db not exist")
            return render(request, 'travel/Login.html')


        if (r != None):
            request.session['username'] = username
            request.session['u_id'] = r[0]
            request.session[t] = True
            request.session['type'] = t
            return HttpResponseRedirect("/")
        else:
            return render(request, 'travel/Login.html')
    else:
        return render(request, 'travel/Login.html')
"""