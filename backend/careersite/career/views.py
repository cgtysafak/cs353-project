from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        if 'username' in request.session:
            user_type = request.session['user_type']
            username = request.session['username']
            return render(request, 'career/home.html', {'user_type': user_type, 'username': username})
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

        if password != passwordver:
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
    
class JobListingsView(View):
    def get( self, request ):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Job;")
        jobs = cursor.fetchall()
        cursor.close()

        return render(request, 'career/joblist.html', {'jobs': jobs})


class JobDescriptionView(View):
    def get( self, request, job_id ):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Job WHERE job_id = %s;", [job_id])
        job = cursor.fetchall()
        cursor.close()

        return render(request, 'career/jobdescription.html', {'job': job})


# #######  POST AND COMMENT VİEWS (ADD, DELETE, LİST)   ###############
class PostListView(View):
    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Post;")
        posts = cursor.fetchall()
        cursor.close()

        return render(request, 'career/post_list.html', {'posts': posts})


class AddPostView(View):
    def get(self, request):
        cursor = connection.cursor()
        return render(request, 'career/add_post.html')

    def post(self, request):
        user_id = request.session['user_id']
        text = request.POST.get("text", "")
        if text != "":
            date = datetime.now() + timedelta(hours=3)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Post(user_id, TEXT, date) VALUES(%s, %s, %s);", user_id, text, date)
            cursor.close()
            connection.commit()
            messages.success(request, "Message is added")
            return redirect('/postlist')
        return render(request, 'career/add_post.html')


class DeletePostView(View):
    def post(self, request, post_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Post WHERE post_id = " + post_id + "")
        post_user_id = cursor.fetchone()
        cursor.close()
        if post_user_id != user_id:
            messages.error(request, "You are not permitted to delete this post")

        else:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Post WHERE post_id = %s', (post_id,))
            cursor.commit()
            cursor.close()

        return redirect("/postlist")


class PostDetailView(View):
    def get(self, request, post_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Post WHERE post_id = " + post_id + "")
        post = cursor.fetchone()
        cursor.close()

        # get all comments which belong to chosen post
        cursor.execute("SELECT * FROM Comment WHERE post_id = " + post_id + "")
        comments = cursor.fetchall()
        cursor.close()

        context = {'user_id': user_id, 'post':post, 'comments': comments}
        return render(request, 'career/post_detail.html', context)

    # for comment section
    def post(self, request, post_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Post WHERE post_id = " + post_id + "")
        post = cursor.fetchone()
        cursor.close()

        # get all comments which belong to chosen post
        cursor.execute("SELECT * FROM Comment WHERE post_id = " + post_id + "")
        comments = cursor.fetchall()
        cursor.close()

        content = request.POST.get("content", "")
        date = datetime.now() + timedelta(hours=3)

        cursor = connection.cursor()
        cursor.execute("INSERT INTO Comment(user_id, post_id, CONTENT, date) VALUES(%s, %s, %s, );",
                       user_id, post_id, content, date)
        cursor.commit()
        cursor.close()

        context = {'user_id': user_id, 'post': post, 'comments': comments}
        return render(request, 'career/post_detail.html', context)


# #######################################################################################################

# EXPERIENCES AND EDUCATION VİEW PART #

'''
class ExperienceListView(View):
    def get(self, request):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Experience WHERE user_id = " + user_id + "")
        experiences = cursor.fetchall()
        cursor.close()

        return render(request, 'career/experience_list.html', {'experiences': experiences})
'''


class AddExperience(View):
    def get(self, request):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        return render(request, 'career/add_experience.html')











