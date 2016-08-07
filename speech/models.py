from django.db import models

# Create your models here.
class Greeting(models.Model):
	when = models.DateTimeField('date created', auto_now_add=True)

class Student(models.Model):
	student_id = models.AutoField(primary_key=True)
	f_name = models.CharField(max_length=30)
	l_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=30)

	def __str__(self):
		return self.f_name

class Class(models.Model):
	class_id = models.AutoField(primary_key=True)
	class_name = models.CharField(max_length=30)
	num_enrollments = models.IntegerField(default=0)

	def __str__(self):
		return self.class_name

	def get_class_id(self):
		return self.class_id

class Enrollments(models.Model):
	student_id = models.ManyToManyField(Student)
	class_id = models.ManyToManyField(Class)

class Topic(models.Model):
	class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
	topic_id = models.AutoField(primary_key=True)
	topic_name = models.CharField(max_length=30)
	num_questions = models.IntegerField(default=0)

	def __str__(self):
		return self.topic_name

class Question(models.Model):
	class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
	topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
	question_id = models.AutoField(primary_key=True)
	question_subject = models.CharField(max_length=100, default='QUESTION')
	question_text = models.CharField(max_length=300)
	num_attempts = models.IntegerField(default=0)
	num_accepted = models.IntegerField(default=0)
	is_user_generated = models.BooleanField(default=False)
	is_mandatory = models.BooleanField(default=False)
	percent_to_pass = models.FloatField(default=.50)

	def __str__(self):
		return self.question_text


class Testing(models.Model):
	test_id = models.AutoField(primary_key=True)
	topic_name = models.CharField(max_length=100)
	question_subject = models.CharField(max_length=100)
	question_text = models.CharField(max_length=5000)

class Completion(models.Model):
	pass
	# come back to this

class SelfStudy(models.Model):
	pass
	# come back to this