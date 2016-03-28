from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from student.models import Student, EnrolledCourses

# from payu.forms import PayUForm
from .forms import OrderForm
# from payu.utils import generate_hash, verify_hash
from course_mang.utilities import student_required
from course_mang.models import CourseDetail
from CLAT.services.constants import TRANSACTION_CANCELLED, TRANSACTION_FAILURE, TRANSACTION_ERROR_BANK, TRANSACTION_ERROR_SERVER
from student.views import enroll_student
from django.contrib.auth.decorators import login_required
from .models import CoursePayment

import logging
logger = logging.getLogger(__name__)

@login_required
@student_required
def checkout(request):
	if request.method == 'POST':
		if Student.objects.filter(student = request.user.id):
			logger.info('payment.checkout >> checkout POST call')
			initial = {}
			order_form = OrderForm(request.POST)
			course_detail = None

			if order_form.is_valid():
				course_uuid = request.POST.get('productinfo')
				# course_name = _input_product_info.split('::')[0]
				# course_uid = _input_product_info.split('::')[1]
				try:
					course_detail = CourseDetail.objects.get(course_uuid = course_uuid, can_enroll = True)
					# print float(request.POST.get('amount')) == float(course_detail.amount),float(request.POST.get('amount'))
				except Exception as e:
					print e.args
					logger.error('Payment.checkout >>>>>>>>>>'+str(e.args))
					messages.error(request, 'Payment process is corrupted. We save your details for security-process.')
					return redirect('/course/details/'+course_uuid)

				if float(request.POST.get('amount')) == float(course_detail.amount) :
					# Student can't procedd for enroll if student pre-enroll on course ....
					# enr_student = EnrolledCourses.objects.is_student_enrolled(request.user, course_detail)
					# if enr_student:
					# 	messages.info(request, 'You are enrolled on this course.')
					# 	return redirect('/course/details/'+str(course_uuid))
					
					logger.info('payment.checkout >> order_form is valid ')
					print 'payment.checkout >> >>>>>>>>>>>>>>> order_form is valid '
					initial = order_form.cleaned_data
					initial.update({'key': settings.PAYU_INFO['merchant_key'],'user_id': request.user.id,
									'surl': request.build_absolute_uri(reverse('order.success')),
									'furl': request.build_absolute_uri(reverse('order.failure')),
									'curl': request.build_absolute_uri(reverse('order.cancel'))})
					#print 'form validate'
					print initial
					h = generate_hash(initial)
					# Once you have all the information that you need to submit to payu
					# create a payu_form, validate it and render response using
					# template provided by PayU.
					initial.update({'hash': h})
					payu_form = PayUForm(initial)
					if payu_form.is_valid():
						logger.info('payment.checkout >> payu_form is valid ')
						context = {'form': payu_form,
								   'action': "%s" % settings.PAYU_INFO['payment_url']}
						return render(request, 'payment/payment_form.html', context)
					else:
						logger.error('payment.checkout >> payu_form is invalid '+str(payu_form.errors))
						return HttpResponse(status = 500)
				else:
					logger.error('Payment.checkout >>>>>>>>>>Please fill valid details for payment process.'+str(course_uuid))
					messages.error(request, 'Payment process is corrupted. We save your details for security-process.')
					return redirect('/course/details/'+str(course_uuid))
					# return HttpResponse(status = 500)
			else:
				logger.error('payment.checkout >> order_form is invalid valid '+str(order_form.errors))
				return HttpResponse(status = 500)
		else:
			logger.error('payment.checkout >> Not a student object with '+str(request.user))
			messages.info(request, 'Please complete your profile first and then proceed to pay.')
			return redirect('/profile/')
	raise Http404
 
 
@csrf_exempt
def success(request):
	try :
		logger.info('payment.success >> under success')
		#print 'success  '*10
		if request.method == 'POST':
			msg = ''
			#print verify_hash(request.POST)	
			if not verify_hash(request.POST):
				logger.info('payment.success >> Hash ----NOT---- verify')
				# logger.warning("Response data for order (txnid: %s) has been "
				# 			   "tampered. Confirm payment with PayU." %
							   # request.POST.get('txnid'))
				return redirect('order.failure')
			else:
				logger.info('payment.success >> Hash verify')
				logger.warning("Payment for order (txnid: %s) succeeded at PayU" %
							   request.POST.get('txnid'))
				status, extra = enroll_student(request)
				
				# User can enroll ....
				if status == 0:
					logger.info('payment.success >> Under --CAN-- enroll for course ----')
					try:
						# coursepayment = CoursePayment.objects.create( enrolledcourse = extra,
						# 	status = request.POST.get('status'), txnid = request.POST.get('txnid'),
						# 	bank_ref_num = request.POST.get('bank_ref_num'), txnid = request.POST.get('txnid'),
						# 	hash = request.POST.get('hash'), txnid = request.POST.get('txnid'),
						# 	bankcode = request.POST.get('bankcode'), txnid = request.POST.get('txnid'),
						# 	discount = request.POST.get('discount'), txnid = request.POST.get('txnid'),
						# 	mihpayid = request.POST.get('mihpayid'), txnid = request.POST.get('txnid'),
						# 	txnid = request.POST.get('txnid'), txnid = request.POST.get('txnid'),
						# 	txnid = request.POST.get('txnid'), txnid = request.POST.get('txnid')
						# 	)
						extra_data = request.POST.dict()
						coursepayment = CoursePayment.objects.create( enrolledcourse = extra, txnid = extra_data.get('txnid') ,extra_data = extra_data)
						msg = 'You are now enrolled in '+extra.course.course_name+' .'+'<br>Amt. Rcvd = Rs'+ request.POST.get('amount')+'/-,'+'<br>Status = '+request.POST.get('status')+','+'<br>Txn Id = '+request.POST.get('txnid');
						#print 'course payment obj created success .....'
						if coursepayment:
							messages.success(request,msg, extra_tags='safe')
							extra.status = 'COURSE-PAYMENT-SUCCESS'
							extra.save()

							logger.info('payment.success >>  SUCCESS user-email: '+extra_data.get('email'))
					except Exception as e:
						print e.args
						msg += 'There is a problem in saving transaction details!'
						logger.error('payment.success >>  H>>>>T---- '+ msg + ' ' + str(e.args)+' user-email: '+extra_data.get('email','NA')+ ' txnid: '+extra_data.get('txnid','NA')) 
						messages.error(request, msg)
						if extra:
							extra.delete()

					return redirect('/dashboard/')
				
				elif status == 1:
					logger.error('payment.success >>  Unable to enroll'+extra.course_name)
					messages.error(request,'Unable to enroll in '+extra.course_name+' .')
					return redirect('/course/details/'+extra.course_uuid+'/')
				
				elif status == 2:
					logger.error('payment.success >>  You are already enrolled in'+extra.course_name)
					messages.info(request,'You are already enrolled in '+extra.course_name+' .')
					return redirect('/course/videos/'+extra.course_uuid+'/')
				
				else:
					logger.error('payment.success >>  TRANSACTION_ERROR_SERVER')
					return HttpResponse(TRANSACTION_ERROR_SERVER)
		else:
			raise Http404
	except Exception as e:
		logger.error('payment.success >>  '+str(e.args))
		return HttpResponse(TRANSACTION_ERROR_BANK)

@csrf_exempt
def failure(request):
	# print request.POST
	return HttpResponse(TRANSACTION_FAILURE)

@csrf_exempt
def cancel(request):
	# print request.POST
	return HttpResponse(TRANSACTION_CANCELLED)

