from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'career/home.html')


class UsersView(View):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM User;")
        users = cursor.fetchall()

        id = users[1][1];
        cursor.close()

        return render(request, 'career/users.html', {'users': users, 'id': id})


class LoginView(View):
    def get(self, request):
        return render(request, 'career/login.html')

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            statement = "SELECT * FROM User Where username= " + username + "AND password " + password + ";"
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
                success = True
                context = {'success': success, 'username': username}
                # return JsonResponse(context)
                return HttpResponseRedirect("/home")
        else:
            return render(request, 'career/login.html')

class SignUpView(View):
    def get(self, request):
        return render(request, 'career/signup.html')


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