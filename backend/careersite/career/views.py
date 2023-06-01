from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from datetime import date
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.middleware.csrf import get_token

class HomeView(View):
    def get(self, request):
        if 'username' in request.session:
            user_type = request.session['user_type']
            username = request.session['username']
            return render(request, 'career/home.html', {'user_type': user_type, 'username': username})
        return HttpResponseRedirect("/login")

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

                # These are required if we want to redirect to home page after signup
                # 
                # request.session['username'] = username
                # request.session['user_id'] = user_id
                # request.session['user_type'] = user_type

                print("user is successfully created")
                return HttpResponseRedirect("/login")
            else:
                print("Please fill all information")
                return render(request, 'career/signup.html')

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return HttpResponseRedirect("/")


# #######  JOB LISTING-DETAILS-APPLY VİEWS  ###############
class JobListingsView(View):
    def get( self, request ):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Company as C JOIN Job as J WHERE C.company_id = J.company_id")
        jobs = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT job_id FROM Application WHERE user_id = %s;", [request.session['user_id']])
        applied_jobs = cursor.fetchall()
        cursor.close()
        
        applied_job_ids = []
        
        for applied_job in applied_jobs:
            applied_job_ids.append(applied_job[0])
            

        return render(request, 'career/joblist.html', {
            'jobs': jobs,
            'user_type': request.session['user_type'],
            'applied_job_ids': applied_job_ids,
        });


class JobDescriptionView(View):
    def get(self, request, job_id):
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM Job j JOIN Company c ON j.company_id = c.company_id WHERE job_id = %s;", [job_id])
        job = cursor.fetchone()
        cursor.close()

        return render(request, 'career/jobdetails.html', {'job': job})

class PastApplicationsView(View):
    def get(self, request):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Application as A JOIN Job as J JOIN Company as C WHERE A.job_id=J.job_id AND J.company_id = C.company_id AND A.user_id=%s ORDER BY A.date DESC", [user_id])
        pastJobs = cursor.fetchall()
        cursor.close()

        return render(request, 'career/past-applications.html', {'pastJobs': pastJobs})

# #######  JOB ADD EDIT DELETE VİEWS  ###############
class AddJobView(View):
    def get(self, request):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM User NATURAL JOIN Recruiter WHERE user_id = %s;", [user_id])
        recruiter = cursor.fetchone()
        cursor.close()

        if recruiter is None:
            return redirect('job-list')
        else:
            return render(request, 'career/add_job.html')

    def post(self, request):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM NonAdmin NATURAL JOIN Recruiter WHERE user_id = %s;", user_id)
        cursor.close()

        recruiter = cursor.fetchone()
        if recruiter is None:
            return redirect('job-list')
        else:
            title = request.POST.get("title", "")
            due_date = request.POST.get("due_date", "")
            profession = request.POST.get("profession", "")
            location = request.POST.get("location", "")
            job_requirements = request.POST.get("job_requirements", "")
            description = request.POST.get("description", "")

            if title != "":
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Job(company_id, recruiter_id, title, due_date, profession, location, "
                               "job_requirements, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
                               (recruiter[1], recruiter[0], title, due_date, profession, location, job_requirements,
                                description))
                connection.commit()
                cursor.close()
                messages.success(request, "Message is added")

                return redirect('job-list')

            else:
                return render(request, 'career/add-job.html')


class ApplyJob(View):
    def get(self, request, job_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Application WHERE user_id = %s AND job_id = %s;", [user_id, job_id])
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            messages.error('You already applied this job')
            return redirect('job-list')
        else:
            date = datetime.now()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Application(user_id, job_id, date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
                           (user_id, job_id, date))
            connection.commit()
            cursor.close()
            messages.success(request, 'You applied this job successfully')

        return redirect('job-list')

# #######  POST AND COMMENT VİEWS (ADD, DELETE, LİST)   ###############
class PostListView(View):
    def get(self, request):

        ordering = request.GET.get('ordering', '')  # Default ordering if not provided

        user_id = request.session['user_id']

        query = "SELECT * FROM POST NATURAL JOIN User WHERE 1=1"
        params = []

        if ordering == 'title':
            query += " ORDER BY title"
        elif ordering == 'date':
            query += " ORDER BY date"

        cursor = connection.cursor()
        cursor.execute(query, params)
        posts = cursor.fetchall()

        cursor.close()

        return render(request, 'career/post_list.html', {'posts': posts, 'user_id': user_id})


class AddPostView(View):
    def get(self, request):
        # cursor = connection.cursor()
        # cursor.close()
        return render(request, 'career/add_post.html')

    def post(self, request):
        user_id = request.session['user_id']
        content = request.POST.get("content", "")
        title = request.POST.get("title","")
        if content != "":
            date = datetime.now() + timedelta(hours=3)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Post(user_id, title, content, date) VALUES(%s, %s, %s, %s);",
                           (user_id, title, content, date));
            connection.commit()
            cursor.close()
            messages.success(request, "Message is added")
            return redirect('/post-list')
        return render(request, 'career/add_post.html')


class DeletePostView(View):
    def get(self, request, post_id):
        print('deneme')
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Post WHERE post_id = %s;", [post_id])
        post_user_id = cursor.fetchone()
        cursor.close()

        csrf_token = get_token(request)
        headers = {'X-CSRFToken': csrf_token}
        if post_user_id[0] != user_id:
            messages.error(request, "You are not permitted to delete this post")

        else:
            cursor = connection.cursor()
            print('deneme')
            cursor.execute('DELETE FROM Comment WHERE post_id = %s', (post_id,))
            cursor.execute('DELETE FROM Post WHERE post_id = %s', (post_id,))
            connection.commit()
            cursor.close()

        return redirect("/post-list", headers=headers)


class PostDetailView(View):
    def get(self, request, post_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Post NATURAL JOIN User WHERE post_id = %s;", [post_id])
        post = cursor.fetchone()
        cursor.close()

        # get all comments which belong to chosen post
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Comment NATURAL JOIN User WHERE post_id = %s", [post_id])
        comments = cursor.fetchall()
        cursor.close()

        context = {'user_id': user_id, 'post':post, 'comments': comments}
        return render(request, 'career/post_detail.html', context)

    # for comment section
    def post(self, request, post_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Post WHERE post_id =%s", [post_id])
        post = cursor.fetchone()
        cursor.close()

        # get all comments which belong to chosen post
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Comment WHERE post_id =%s ", [post_id])
        comments = cursor.fetchall()
        cursor.close()

        content = request.POST.get("content", "")
        date = datetime.now() + timedelta(hours=3)

        cursor = connection.cursor()
        cursor.execute("INSERT INTO Comment(user_id, post_id, CONTENT, date) VALUES(%s, %s, %s, %s);",
                       (user_id, post_id, content, date))
        connection.commit()
        cursor.close()

        context = {'user_id': user_id, 'post': post, 'comments': comments}
        return redirect("post-detail", post_id=post_id)


class DeleteCommentView(View):
    def get(self, request, comment_id):
        user_id = request.session['user_id']
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, post_id FROM Comment WHERE comment_id = %s", [comment_id])
        result = cursor.fetchone()
        if result is None:
            messages.error(request, 'comment-cannot-be-found')
            return redirect('post-detail', post_id=post_id)

        comment_user_id = result[0]
        post_id = result[1]
        cursor.close()
        if comment_user_id != user_id:
            messages.error(request, "You are not permitted to delete this post")

        else:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM Comment WHERE comment_id = %s', [comment_id])
            connection.commit()
            cursor.close()

        return redirect('post-detail', post_id=post_id)



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











