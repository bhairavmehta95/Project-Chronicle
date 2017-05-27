from django.db import models

# Create your models here.

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key = True)
    f_name = models.CharField(max_length = 30)
    l_name = models.CharField(max_length = 30)
    user_id_login = models.IntegerField(default = 0)

    def __str__(self):
        return "{} {}".format(self.f_name, self.l_name)

    def get_teacher_id(self):
        return self.teacher_id

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, blank=True, null=True)
    class_name = models.CharField(max_length=100)
    num_enrollments = models.IntegerField(default=0)
    class_key = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.class_name

    def get_class_id(self):
        return self.class_id

    def get_class_key(self):
        return self.class_key


class Student(models.Model):
    student_id = models.AutoField(primary_key = True)
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    user_id_login = models.IntegerField(default = 0)

    def __str__(self):
        return self.f_name

    def get_id(self):
        return self. student_id

class Enrollments(models.Model):
    student_id = models.ForeignKey(Student)
    class_id = models.ForeignKey(Class)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return str(self.id)

class Topic(models.Model):
    class_id = models.ForeignKey(Class)
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=100)
    num_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.topic_name

class Question(models.Model):
    class_id = models.ForeignKey(Class)
    topic_id = models.ForeignKey(Topic)
    question_id = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100, default='QUESTION')
    num_attempts = models.IntegerField(default=0)
    num_accepted = models.IntegerField(default=0)
    is_user_generated = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=False)
    percent_to_pass = models.FloatField(default=.50)

    def __str__(self):
        return self.question_title

class Completion(models.Model):
    completion_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question)
    student_id = models.ForeignKey(Student)
    transcript = models.TextField()
    percent_scored = models.FloatField(default = 0)

    def __str__(self):
        return self.completion_id

class RawText(models.Model):
    question_id = models.ForeignKey(Question)
    raw_text = models.TextField()

    def __str__(self):
        return self.raw_text

class PrimaryKeyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question)
    keyword = models.CharField(max_length=100)
    point_value = models.IntegerField()
    number_of_hits = models.IntegerField(default=0)

class SecondaryKeyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question)
    keyword = models.CharField(max_length=100)
    point_value = models.IntegerField()
    number_of_hits = models.IntegerField(default=0)

class TopicProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student)
    topic_id = models.ForeignKey(Topic)
    class_id = models.ForeignKey(Class)
    num_answered = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)

