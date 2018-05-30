import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.db.models.fields import *
from django.contrib.auth.models import User



class EffectiveDated(models.Model):

	start_date = models.DateField(null=True,blank=True)
	end_date = models.DateField(null=True,blank=True)
	is_archieved = models.BooleanField(default=False)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.start_date,self.end_date,self.is_archieved)



class Employee(models.Model):

	uuid = models.UUIDField(default=uuid.uuid4,)
	employee = models.ForeignKey(User,on_delete=models.CASCADE)
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.employee.first_name,self.employee.last_name,self.employee.email)

	@property	
	def get_full_name(self):
		return '{0} {1}'.format(self.employee.first_name,self.employee.last_name)

	@property
	def get_document(self):
		return Document.objects.filter(employee=self)	



class Question(models.Model):

	question = models.CharField(max_length=1024)
	asked_by = models.ForeignKey(User,on_delete=models.CASCADE) 
	likes = models.PositiveIntegerField(default=0)
	is_resolved = models.BooleanField(default=False)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.question,self.asked_by.first_name,self.likes)

	@property	
	def total_likes(self):
		return self.likes

	@property
	def get_answers(self):
		return Answer.objects.filter(question=self)

	@property
	def get_comments(self):
		return Comment.objects.filter(question=self)	




class Answer(models.Model):
	
	answer = models.CharField(max_length=1024)
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	answered_by = models.ForeignKey(User,on_delete=models.CASCADE) 
	likes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.question,self.answer,self.answered_by.first_name)

	@property
	def total_likes(Self):
		return self.likes

	@property	
	def get_comments(self):
		return Comment.objects.filter(answer=self)	

	@property
	def get_full_name(self):
		return '{0} {1}'.format(self.answered_by.first_name,self.answered_by.last_name)		

	@property
	def get_comment(self):
		return Comment.objects.filter(answer=self)	

	@property
	def get_comment_count(self):
		return Comment.objects.filter(answer=self).count()	

		

class Policy(EffectiveDated):

	version = models.CharField(max_length=10)
	file = models.FileField(upload_to='media/')
	likes = models.PositiveIntegerField(default=0)


	def __str__(self):
		return '{0} - {1}'.format(self.file,self.version)

	@property
	def get_comment_count(self):
		return Comment.objects.filter(policy=self).count()

	@property
	def get_file_name(self):
		return self.file.name.split('/')[-1]

	@property
	def get_comment(self):
		return Comment.objects.filter(policy=self)	



class Comment(models.Model):
	
	comment = models.CharField(max_length=500)
	commented_by = models.ForeignKey(Employee,on_delete=models.CASCADE)
	question = models.ForeignKey(Question,null=True,blank=True,on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer,null=True,blank=True,on_delete=models.CASCADE)
	policy = models.ForeignKey(Policy,null=True,blank=True,on_delete=models.CASCADE)


	def __str__(self):
		return '{0} - {1}'.format(self.commented_by.get_full_name,self.comment)	



class Document(models.Model):

	file = models.FileField(upload_to='media/')
	employee = models.ForeignKey(Employee,on_delete=models.CASCADE)

	def __str__(self):
		return '{0}-{1}'.format(self.file,self.employee)	

	@property
	def get_file_name(self):
		return self.file.name.split('/')[-1]	



class Queries(models.Model):

	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer,on_delete=models.CASCADE)

	@property
	def question_comments(self):
		return Comment.objects.filter(question=self.question)

	@property	
	def answer_comments(self):
		return Comment.objects.file_name(answer=self.answer)

	@property
	def question_like_count(Self):
		return self.question.likes

	@property
	def answer_like_count(self):
		return self.answer.likes