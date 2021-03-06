from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

CATEGORY_CHOICES = (
 ('intership','Internship'),
 ('scholarship','Scholarship'),
 ('programmes', 'Programmes'),
    ('other', 'Other'),

)

ACCESS_CATEGORY = (
    ('students', 'Students'),
    ('faculty_and_professors', 'Faculty_and_Professors'),
    ('all', 'All'),
)


ACCESS_TYPE = (
    ('normal_user', 'Normal_User'),
    ('institute_admin', 'Institute_Admin'),
    ('super_admin', 'Super_Admin'),
)

class General_User_Table(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.PROTECT)
    access_type = models.CharField(max_length=50, choices=ACCESS_TYPE, default='normal_user')

    def __str__(self):
        return str(self.user_name)

class Institute(models.Model):
    institute_user_name = models.ForeignKey('General_User_Table', related_name='institute', on_delete=models.PROTECT, default='N/A')
    institute_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    institute_type = models.CharField(max_length=100)
    institute_profile_pic_path = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    director_pic_path = models.CharField(max_length=50)

    def __str__(self):
        return str(self.institute_name)

class Normal_User_Table(models.Model):
    user_name = models.ForeignKey('General_User_Table', related_name='normal_user', on_delete=models.PROTECT)
    institute_user_name = models.ForeignKey('Institute', related_name='user_institute', on_delete=models.PROTECT, default='N/A')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    profile_pic_path = models.ImageField(upload_to='profile_pic', default='samvad\media\big.jpg')
    skill_set = models.CharField(max_length=1000)
    category = models.CharField(max_length=50, choices=ACCESS_CATEGORY)
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user_name)+str(self.institute_user_name)


class Newsfeed(models.Model):
    number = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    news_feed_type =  models.CharField(max_length=100,choices=CATEGORY_CHOICES,default='other')
    date =  models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=2000)
    image = models.CharField(max_length=100)
    intended_for = models.CharField(max_length=50, choices=ACCESS_CATEGORY, default='all')

    def __str__(self):
        return str(self.user_name)

class Societies(models.Model):
    institute_name = models.ForeignKey('Institute',  on_delete=models.PROTECT)
    society = models.CharField(max_length=50)
    profile_pic_path = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return str(self.institute_name)


class Interest(models.Model):
    interest_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.interest_name)

class User_Interest(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.PROTECT)
    interest_name = models.ForeignKey(Interest, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("user_name", "interest_name")

    def __str__(self):
        return (str(self.user_name)+"/"+str(self.interest_name) + "/" +str(self.id))

class NewsfeedScore(models.Model):
    newsfeed = models.ForeignKey(Newsfeed, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    score = models.CharField(max_length = 20)

    def __str__(self):
        return (str(self.newsfeed.description[:10]) + " category:-" + self.category + " score:-" + self.score)

class Scholarship(models.Model):
    user_name = models.ForeignKey(User,  on_delete=models.PROTECT)
    status =  models.CharField(max_length=50)
    info =  models.CharField(max_length=100)
    category =  models.CharField(max_length=100)
    upload_date =  models.CharField(max_length=50)
    expir_date =  models.CharField(max_length=50)
    description =  models.CharField(max_length=1000)

    def __str__(self):
        return (str(self.user_name) + " " + str(self.info))

class Internship(models.Model):
    user_name = models.ForeignKey(User,  on_delete=models.PROTECT)
    status =  models.CharField(max_length=50)
    info =  models.CharField(max_length=100)
    category =  models.CharField(max_length=100)
    upload_date =  models.CharField(max_length=50)
    expir_date =  models.CharField(max_length=50)
    description =  models.CharField(max_length=1000)

    def __str__(self):
        return (str(self.user_name) + " " + str(self.info))

class Project(models.Model):
    user_name = models.ForeignKey(User,  on_delete=models.PROTECT)
    status =  models.CharField(max_length=50)
    info =  models.CharField(max_length=100)
    category =  models.CharField(max_length=100)
    upload_date =  models.CharField(max_length=50)
    expir_date =  models.CharField(max_length=50)
    description =  models.CharField(max_length=1000)

    def __str__(self):
        return (str(self.user_name) + " " + str(self.info))

class Comment(models.Model):
    post = models.ForeignKey('Newsfeed',  related_name='comments', on_delete=models.PROTECT)
    user_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description
