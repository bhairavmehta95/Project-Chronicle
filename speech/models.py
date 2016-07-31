from django.db import models

# Create your models here.
class Greeting(models.Model):
	when = models.DateTimeField('date created', auto_now_add=True)

class Student(models.Model):
	student_id = models.IntegerField()
	f_name = models.CharField(max_length=30)
	l_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=30)

	def __str__(self):
		return self.f_name

class Class(models.Model):
	class_id = models.IntegerField()
	class_name = models.CharField(max_length=30)
	num_enrollments = models.IntegerField()

	def __str__(self):
		return self.class_name

	def get_class_id(self):
		return self.class_id

class Enrollments(models.Model):
	student_id = models.ManyToManyField(Student)
	class_id = models.ManyToManyField(Class)

class Topic(models.Model):
	class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
	topic_id = models.IntegerField()
	topic_name = models.CharField(max_length=30)
	num_questions = models.IntegerField()

	def __str__(self):
		return self.topic_name

class Question(models.Model):
	class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
	topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
	question_id = models.IntegerField()
	question_text = models.CharField(max_length=300)
	num_attempts = models.IntegerField()
	num_accepted = models.IntegerField()
	is_user_generated = models.BooleanField()
	is_mandatory = models.BooleanField()
	percent_to_pass = models.FloatField()

	def __str__(self):
		return self.question_id

class Completion(models.Model):
	pass
	# come back to this

class SelfStudy(models.Model):
	pass
	# come back to this