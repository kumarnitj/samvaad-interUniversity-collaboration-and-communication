from django.shortcuts import render
from django.template import loader

from basicapp.forms import UserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from basicapp.models import (General_User_Table, Newsfeed, Institute, Internship,
                            Project, Interest, User_Interest, NewsfeedScore, Comment)
from basicapp.forms import UserForm, InstituteProfileInfoForm, addUserForm, addNewsFeedForm, uploadProfilePicForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (View, TemplateView,
                                   ListView, DetailView,
                                   CreateView, UpdateView,
                                   DeleteView)


from django.db import connection
from django.shortcuts import redirect
import paralleldots
paralleldots.set_api_key("nUV2Ym1gQr8REXKIZQzgKQkDBUkBaUSK6Qukfcx4LwE")

# Create your views here.

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                n1 = General_User_Table.objects.filter(user_name__username__icontains=username)
                print(n1[0].access_type)
            if n1[0].access_type == 'institute_admin':
                return HttpResponseRedirect(reverse('instituteAdmin'))
            elif n1[0].access_type == 'super_admin':
                return HttpResponseRedirect(reverse('superAdmin'))
            elif n1[0].access_type == 'normal_user':
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print('someone tried login and failed')
            print('username : {} and password {}'.format(username, password))
            return HttpResponse("invalid comb of username password")
    else:
        return render(request, 'basicapp/login.html', {})



@login_required
def index(request):
    n3 = User_Interest.objects.filter(user_name__username__icontains=request.user.username)
    user_interests = []
    for n in n3:
        print(n.interest_name)
        user_interests.append(n.interest_name)

    n2= Newsfeed.objects.all()
    n1 = General_User_Table.objects.filter(user_name__username__icontains=request.user.username)
    return render(request, 'basicapp/index.html', {'user_interests':user_interests,'user_record':n1})

@login_required
def instituteAdmin(request):
    n2= Newsfeed.objects.all()
    return render(request, 'basicapp/instituteAdmin.html',{'news_feed':n2,})


@csrf_protect
def superAdmin(request):

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        # profile_form = UserProfileInfoForm(data = request.POST)
        institute_form = InstituteProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user_name = user

            profile.save()

            institute = institute_form.save(commit=False)
            institute.user_name = user
            institute.save()

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        # profile_form = UserProfileInfoForm()
        institute_form = InstituteProfileInfoForm()

    return render(request, 'basicapp/superAdmin.html', {'user_form':user_form, 'profile_form':profile_form, 'institute_form': institute_form})

def addUser(request):
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        add_user_form = addUserForm(data = request.POST)

        if user_form.is_valid() and add_user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = add_user_form.save(commit=False)
            profile.user_name = user
            profile.access_type = 'Normal_User'
            profile.save()

            # add code for putting details into general user table and Normal user table

        else:
            print(user_form.errors, add_user_form.errors)
    else:
        user_form = UserForm()
        add_user_form = addUserForm()

    return render(request, 'basicapp/adduser.html', {'user_form':user_form, 'add_user_form':add_user_form})


class NewsFeedDetail(DetailView):
    context_object_name= 'newsfeed_detail'
    model=Newsfeed
    template_name= 'basicapp/feed_details.html'

def userAccountInfo(request):
    n1 = Internship.objects.filter(user_name__username__icontains = request.user.username)
    n2 = Project.objects.filter(user_name__username__icontains = request.user.username)
    n3 = User_Interest.objects.filter(user_name__username__icontains = request.user.username)
    updateProfilePicForm = uploadProfilePicForm()
    return render(request, 'basicapp/UserProfilePage.html', {'internships': n1, 'projects': n2, 'interests': n3, 'updateProfilePicForm': updateProfilePicForm})

@login_required
def instituteprofilepage(request):
    return render(request, 'basicapp/InstituteProfilePage.html')

@login_required
def InstituteExtra(request):
    return render(request, 'basicapp/InstituteExtras.html')


@login_required
def institutesocities(request):
    return render(request, 'basicapp/InstituteSocities.html')

@login_required
def internships(request):
    feed=Newsfeed.objects.filter(news_feed_type__exact = 'internship')
    return render(request, 'basicapp/UserExtras.html', {'feed':feed})

def scholarships(request):
    feed=Newsfeed.objects.filter(news_feed_type__exact = 'scholarship')
    return render(request, 'basicapp/UserExtras.html', {'feed':feed})

def programmes(request):
    feed = Newsfeed.objects.filter(news_feed_type__exact = 'programmes')
    return render(request, 'basicapp/UserExtras.html', {'feed':feed})


@login_required
@csrf_protect
def loadNewsFeed(request):
    # interests = User_Interest.objects.filter(user_name__username__icontains=request.user.username)
    newsfeeds = Newsfeed.objects.all().order_by('-date')
    res = {}

    i = 0
    for newsfeed in newsfeeds:
        score_ = NewsfeedScore.objects.filter(newsfeed = newsfeed)
        a = {}
        tag = []
        a['user_name'] = newsfeed.user_name
        a['description'] = newsfeed.description
        a['news_feed_type'] = newsfeed.news_feed_type
        a['date'] = newsfeed.date
        a['image'] = newsfeed.image
        a['intended_for'] = newsfeed.intended_for
        a['id'] = newsfeed.id
        a['score'] = {}
        for score__ in score_:
            a['score'][score__.category] = float(score__.score)
            tag.append(score__.category)
        a['tags'] = tag
        # To add comments
        j = 0  #Comments length
        comments = Comment.objects.filter(post = newsfeed)
        a['comments'] = {}
        for comment in comments:
            b = {}
            b['user_name'] = comment.user_name
            b['description'] = comment.description
            b['created_date'] = comment.created_date
            a['comments'][str(j)] = b
            j = j + 1;
        a['comments_length'] = j
        res[str(i)] = a
        i=i+1
    res['length'] = i
    return JsonResponse(res)

def addComment(request):
    id = request.GET.get('id')
    comment_description = request.GET.get('comment')
    username = request.GET.get('username')
    newsfeed = Newsfeed.objects.get(pk = id)
    comment_object = Comment()
    comment_object.post = newsfeed
    comment_object.user_name = username
    comment_object.description = comment_description
    comment_object.save()
    data = {}
    data['message'] = 'working'
    print("comment added id: " + id)
    return JsonResponse(data);


@csrf_exempt
def addNewsFeed(request):
    data = {}
    data['status']='false'
    if request.method == 'POST':
        username = request.user.username
        description = request.POST.get('inputContent')
        type = request.POST.get('type')
        intended_for = request.POST.get('intended_for')
        image = request.POST.get('image')
        print('type: ' + str(type))
        newsfeed_object = Newsfeed()
        newsfeed_object.user_name = username
        newsfeed_object.news_feed_type = type
        newsfeed_object.description = description
        newsfeed_object.image = image
        newsfeed_object.intended_for = intended_for
        newsfeed_object.save()
        # to calculate score
        category = { "Sports":['Cricket', 'Football', 'Soccer', 'Swimming', 'Horse Riding', 'Table Tennis', 'Badminton'], 'Artificial Intelligence':['Machine Learning', 'Deep Learning', 'Mimic', 'Linear Regression', 'Logistic Regression'], 'Internet of Things': ['Automation', 'Alexa', 'Siri', 'Google Home'], 'Data Structure and Algorithms':['DFS', 'BFS', 'Array', 'Stacks', 'Queues', 'Recursion', 'Disjoint Set'], 'Competitive Programming':['Codechef', 'Hackerearth', 'Hackerrank', 'Purple'],
        'Management':['Event', 'Time'], 'Developer':['Software Engineering', 'Project', 'APIs', 'Web Development'], 'Blockchain':['Cryptocurrency', 'Bitcoins', 'Etherium'], 'Operting System':[], 'Art':[], 'Gaming':[], 'Virtual Reality':[], 'Microprocessors':[], 'Aviation':[], 'Mechanical Engineering':[], 'Electronics Engineering':[], 'Textile Engineering':[], 'Mining Engineering':[]}

        api_scores = paralleldots.custom_classifier(description, category);
        for api_score in api_scores['taxonomy']:
            tag = api_score['tag']
            score = api_score['confidence_score']
            score_table = NewsfeedScore()
            score_table.newsfeed = newsfeed_object
            score_table.category = tag
            score_table.score = score
            score_table.save()

        data['status']='true'
    # else:
    return JsonResponse(data)

@csrf_exempt
def deleteUserInterest(request):
    data = {}
    print('backend')
    data['status']='false'
    if request.method == 'POST':
        id = request.POST.get('id')
        userInterestObject = User_Interest.objects.get(id = id)
        userInterestObject.delete()
        data['status']='true'
    return JsonResponse(data)

@csrf_exempt
@login_required
def addUserNewInterest(request):
    data = {}
    data['status']='false'
    if request.method == 'POST':
        username = request.user.username
        username = User.objects.get(username = username)
        interest = request.POST.get('interest')
        interest_object = Interest.objects.filter(interest_name = interest)
        if len(interest_object) != 1:
            data['message']='No such Interest Found'
            return JsonResponse(data)
        user_interest_object =  User_Interest.objects.filter(user_name=username,interest_name=interest_object[0].pk)
        if len(user_interest_object) != 0:
            data['message'] = 'Interest already exist'
            return JsonResponse(data)
        user_interest_object = User_Interest()
        user_interest_object.user_name = username
        user_interest_object.interest_name = Interest.objects.get(pk = interest_object[0].pk)
        # user_interest_object.interest_name = interest_object
        user_interest_object.save()
        data['status']='true'
        data['id']=user_interest_object.pk
    return JsonResponse(data)

def searchKeyword(request):
    keyword = request.GET.get('keyword')
    searchResults = User.objects.filter(username__icontains=keyword)
    htmlCode = ''
    for searchResult in searchResults:
        htmlCode += searchResult.username
        htmlCode += '<br>'
    data = {}
    data['result'] = htmlCode
    return JsonResponse(data)

@csrf_exempt
@login_required
def updateProfilePic(request):
    if request.method == 'POST':
        print('inside post method')
        form = uploadProfilePicForm(request.POST, request.FILES)
        print(request.FILES['imageFile'])
        if form.is_valid():
             userInstance = User_Table.objects.filter(user_name__username__icontains = request.user.username)
             userInstance.update(profile_pic_path = request.FILES['imageFile'])
             print(userInstance)
             if userInstance[0].access_type == 'InstituteAdmin':
                 return HttpResponseRedirect(reverse('instituteAdmin'))
             elif userInstance[0].access_type == 'SuperAdmin':
                 return HttpResponseRedirect(reverse('superAdmin'))
             elif userInstance[0].access_type == 'NormalUser':
                 return HttpResponseRedirect(reverse('index'))
             else:
                 return HttpResponse("Account not active")
        else:
            return HttpResponse("Form not valid")
