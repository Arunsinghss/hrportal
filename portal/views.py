from portal.models import *
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, FormView
from django.shortcuts import render,reverse,render_to_response
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect



class Login(TemplateView):

	template_name = "portal/login.html"



class Logout(TemplateView):

	def get(self, request, *args,**kwargs):
		logout(request)	
		return HttpResponseRedirect(reverse('portal:login'))



class Success(TemplateView):

	template_name = "portal/success.html"



class Validate(TemplateView):
		
	def post(self, request, *args, **kwargs):

		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username,password=password)
			print('username=',username,'password=',password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':'queries'}))
			else:
				return HttpResponseRedirect(reverse('portal:login'))
		except Exception as e:
			print(e)
			return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':'queries'}))



class AddUser(TemplateView):

	template_name = 'portal/dashboard.html'
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):

		try:
			data = request.POST.dict()
			user_name = request.POST.get('username',None)
			first_name = request.POST.get('firstname',None)
			last_name = request.POST.get('lastname',None)
			email = request.POST.get('email',None)
			password = request.POST.get('password',None)
			context = dict()

			if not user_name or not last_name or not first_name or not password or not email:
				return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':'configure'}))
		
			if Employee.objects.filter(Q(employee__email=email)| Q(employee__username=user_name)).exists():
				return self.render_to_response(context)
				
			else:
				new_user = User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=password)
				new_user.save()
				employee = Employee.objects.create(employee=new_user)
				employee.save()
				return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':'configure'}))

		except Exception as e:
			print(e)		
			return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':'configure'}))



class Dashboard(TemplateView):
	
	template_name = 'portal/dashboard.html'	
	@method_decorator(login_required)
	def get(self, request, tab=None, *args, **kwargs):

		try:
			questions = Question.objects.all()
			myquestions = Question.objects.filter(asked_by=request.user)
			# page = request.GET.get('page', 1)

			context = dict()
			conversations = dict()	
			myconversations = dict()
			today = timezone.now().date()

			for question in questions:
				all_answer = Answer.objects.filter(question=question)
				answers = list()
				if all_answer:
					for answer in all_answer:
						answers.append(answer)
				conversations.update({question:answers})


			# or
			# for question in questions:
			# 	question.all_answer = Answer.objects.filter(question=question)	

			if not tab:
				tab = 'queries'

			# paginator = Paginator(conversations, 3)

			# if page:
			# 	try:
			# 		conversation = paginator.get_page(page)
			# 	except PageNotAnInteger:
			# 		conversation = paginator.get_page(1)
			# 	except EmptyPage:
			# 		conversation = paginator.get_page(paginator.num_pages)

			context.update({
				'conversations': conversations,
				'tab': tab,
				'conversationlen': len(conversations)
			})

			for myquestion in myquestions:
				my_ques_ans = Answer.objects.filter(question=myquestion)
				answers = list()
				if my_ques_ans:
					for answer in my_ques_ans:
						answers.append(answer)
				myconversations.update({myquestion:answers})


			context.update({
				'myconversations': myconversations,
				'myconversationlen': len(myconversations)
			})

			try:
				emp = Employee.objects.get(employee=request.user)
			except Exception as e:
				print(e)	

			policies = Policy.objects.filter(start_date__lte=today,end_date__gte=today,is_archieved=False)	
			print("policies=",policies)

			employees = Employee.objects.all()
			context.update({
				'employees': employees,
				'policies': policies,
				'employee': emp
			})

			if emp.is_admin:
				context.update({
					'is_admin': True
				})

			return self.render_to_response(context)

		except Exception as e:
			print(e)	
			return HttpResponse("bad request")





class AddQuestion(TemplateView):

	template_name = 'portal/dashboard.html'
	@method_decorator(login_required)
	def post(self, request, tab=None, *args, **kwargs):

		try:
			user = request.user
			question = request.POST.get('question',None)

			if question:
				question = Question.objects.create(asked_by=user,question=question)
				question.save()

				return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':tab}))

		except Exception as e:
			print(e)
			return HttpResponseRedirect(reverse('portal:dashboard',kwargs = {'tab':tab}))



class AddAnswer(View):

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		try:
			user = request.user
			answer = request.POST.get('reply',None)
			qid = request.POST.get('qid',None)

			if not qid or not answer:
				data = {
					'success':False,
					'error':'Something went wrong..please try again'
				}
				return JsonResponse(data)

			else:
				question = Question.objects.filter(id=qid)
				if question:
					answer = Answer.objects.create(answered_by=request.user,question=question[0],answer=answer)
					answer.save()
					query = Queries.objects.create(question=question[0],answer=answer)
					query.save()

					new_reply = '<span>re : {0}</span><p><i class="Tiny material-icons themecolor">tag_faces</i><a class="resolved">{1}</a><span id="{2}" class="bigmarginlike" style="margin-left:46em;"><label for="{2}" class="themecolor like">{3}</label><i class="material-icons likebutton dropdown-trigger" tab="queries" id="{2}" name="{3}"  data-target="{2}">thumb_up</i><label for="{4}" class="themecolor comment smallleft">{4}</label><i class="material-icons chatbutton comment modal-trigger" name="{4}">chat</i></span></p>'.format(answer.answer,answer.get_full_name,answer.id,answer.likes,answer.get_comment_count)

					data = {
						'success': True,
						'newreply': new_reply
					}
					return JsonResponse(data)

		except Exception as e:
			print(e)
			data = {
				'success':False
			}
			return JsonResponse(data)



class UploadPolicy(TemplateView):

	template_name = 'portal/dashboard.html'
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):

		try:
			file = request.FILES['myfile']	
			version = request.POST.get('version',None)
			start_date = request.POST.get('startdate',None)
			end_date = request.POST.get('enddate',None)
			policy_id = request.POST.get('policy',None)

			if not start_date or not end_date or not version or not file:
				return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':'configure'}))
			else:
				start_date = datetime.strptime(start_date, '%b %d, %Y')
				end_date = datetime.strptime(end_date, '%b %d, %Y')
				if policy_id:
					try:
						policy = Policy.objects.get(id=policy_id)
					except Exception as e:
						print(e)	
						return HttpResponse("bad request")

					if policy:
						policy.is_archieved = True
						policy.save()
						new_policy = Policy.objects.create(file=file, version=version, start_date=start_date, end_date=end_date)
						new_policy.save()
						return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':'configure'}))	

				else:	
					policy = Policy.objects.create(file=file, version=version, start_date=start_date, end_date=end_date)
					policy.save()
					return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':'configure'}))	

		except Exception as e:
			print(e)	
			return HttpResponse("bad request")



class UserDocument(TemplateView):

	template_name = 'portal/dashboard.html'
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):

		try:
			file = request.FILES.get('myfile')
			emp_list = request.POST.getlist('emp')
			if emp_list:
				tab = 'empwork'
			else:
				tab = 'mywork'		

			if not file:
				return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':tab}))

			if file:
				if emp_list:
					for emp in emp_list:
						try:
							employee = Employee.objects.get(id=emp)
						except Exception as e:
							print(e)
						if employee:	
							document = Document.objects.create(file=file, employee=employee)
							document.save()
				else:
					employee = Employee.objects.get(employee=request.user)
					document = Document.objects.create(file=file, employee=employee)
					document.save()

				return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':tab}))	

		except Exception as e:
			print(e)	
			return HttpResponseRedirect(reverse('portal:dashboard',kwargs={'tab':tab}))



class Like(View):
	
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):		

		try:
			aid = request.POST.get('aid',None)
			tab = request.POST.get('tab',None)

			if tab:
				query_list = ['allqueries','queries']
				other_list = ['policies']

				if tab in query_list and not aid:
					data = {
						'success':False,
						'message':"something went wrong"
					}
					return JsonResponse(data)


				if tab in query_list:
					try:
						answer = Answer.objects.get(id=aid)
					except Exception as e:
						print(e)
						data = {
							'success':False,
							'message':"something went wrong"
						}
						return JsonResponse(data)

					if answer:
						answer.likes += 1
						answer.save()

					data = {
						'success':True,
						'likes':answer.likes,
						'tab':tab
					}
					return JsonResponse(data)

				else:
					try:
						policy = Policy.objects.get(id=aid)
					except Exception as e:
						data = {
							'success':False,
							'message':"something went wrong"
						}
						return JsonResponse(data)

					if policy:
						policy.likes += 1
						policy.save()

					data = {
						'success':True,
						'likes':policy.likes,
						'tab':tab
					}
					return JsonResponse(data)	

		except Exception as e:
			print(e)
			data = {
					'success':False,
					'message':"something went wrong"
				}
			return JsonResponse(data)



class AddComment(View):
	
	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):

		try:
			aid = request.POST.get('aid',None)
			pid = request.POST.get('pid',None)
			comment = request.POST.get('comment',None)

			if not comment:
				data = {
					'success': False
				}
				return JsonResponse(data)

			try:
				emp = Employee.objects.get(employee=request.user)
			except Exception as e:
				print(e)	

			if aid:
				try:
					answer = Answer.objects.get(id=aid)
				except Exception as e:
					data = {
					'success': False
					}
					return JsonResponse(data)

				if answer:
					comment = Comment.objects.create(answer=answer, comment=comment, commented_by=emp)
					comment.save()
					comment = '<li class="commentlistpadding">{0}<a>@{1}</a></li><div class="divider"></div>'.format(comment.comment,comment.commented_by.get_full_name)

					data = {
						'success': True,
						'comment': comment,
					}
					return JsonResponse(data)

			elif pid:
				try:
					policy = Policy.objects.get(id=pid)
				except Exception as e:
					print(e)

				if policy:
					comment = Comment.objects.create(policy=policy, comment=comment, commented_by=emp)
					comment.save()
					comment = '<li class="commentlistpadding">{0}<a>@{1}</a></li><div class="divider"></div>'.format(comment.comment,comment.commented_by.get_full_name)

					data = {
						'success': True,
						'comment': comment,
					}
					return JsonResponse(data)
			else:

				data = {
					'success': False
				}
				return JsonResponse(data)

		except Exception as e:
			print(e)
			data = {
				'success': False
			}
			return JsonResponse(data)



class DeleteFile(TemplateView):
	
	template_name = 'portal/dashboard.html'
	@method_decorator(login_required)

	def post(self, request, *args, **kwargs):

		try:
			tab = request.POST.get('tab',None)
			fid = request.POST.get('fid',None)

			if not tab or not fid:
				data = {
					'success': False,
					'message': 'Something went wrong'
				}
				return JsonResponse(data)

			try:
				document = Document.objects.get(id=fid)	
			except Exception as e:
				print(e)

			if document:
				document.delete()
				data = {
					'success': True,
					'message': 'File deleted successfully',
				}
				return JsonResponse(data)

		except Exception as e:
			data = {
				'success': False,
				'message': 'Something went wrong'
			}
			return JsonResponse(data)



class DownloadPolicy(View):

	@method_decorator(login_required)
	def get(self, request, pid=None, *args, **kwargs):

		try:
			if not pid :
				return HttpResponse("Something went wrong")

			try:
				policy = Policy.objects.get(id=pid)
			except Exception as e:
				print(e)

			if policy:
				filename = policy.file.name
				response = HttpResponse(policy.file,content_type='application/text')
				response['Content-Disposition'] = 'attachment; filename=%s' % filename
				return response	
		except Exception as e:
			print(e)
			return HttpResponse("badrequest")	



class DownloadUserDocument(View):

	@method_decorator(login_required)
	def get(self, request, pid=None, uid=None, *args, **kwargs):

		try:
			if not uid:
				return HttpResponse("Something went wrong")

			try:
				document = Document.objects.get(id=uid)
			except Exception as e:
				print(e)
				return HttpResponse("badrequest")

			if document:
				filename = document.file.name
				response = HttpResponse(document.file,content_type='application/text')
				response['Content-Disposition'] = 'attachment; filename=%s' % filename
				return response	

		except Exception as e:
			print(e)
			return HttpResponse("badrequest")		



class MarkResolved(View):

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):

		try:
			qid = request.POST.get('qid',None)

			if qid:
				try:
					question = Question.objects.get(id=qid)
				except Exception as e:
					data = {
						'success':False
					}
					return JsonResponse(data)

				if question:
					employee = Employee.objects.get(employee=request.user)

					if question.asked_by == request.user or employee.is_admin:
						print("access granted")
						question.is_resolved = True
						question.save()
						data = {
							'success':True
						}
						return JsonResponse(data)
					else:
						data = {
							'success':False
						}
						return JsonResponse(data)	
			else:
				data = {
					'success': False
				}
				return JsonResponse(data)
					
		except Exception as e:					
			data = {
				'success': False
			}
			return JsonResponse(data)

