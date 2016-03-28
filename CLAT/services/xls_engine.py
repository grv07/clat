import xlwt


def initiate():
	style0 = xlwt.easyxf('font: name Times New Roman,height 270,color-index red, bold on',
				num_format_str='#,##0.00')
			
	style2 = xlwt.easyxf('font: name Times New Roman,,height 240, color-index blue, bold on',
	num_format_str='#,##0.00')

	style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
	wb = xlwt.Workbook()

	return (style0, style1, style2, wb,)

def get_city_state_name(user_obj):
	city_state_name = ''
	try:		
		city  = user_obj.address.city_obj
		city_state_name = city.city_name+', '+city.city_state+','
	except Exception as e:
		print e.args
	return city_state_name

def get_address(user_obj):
	_str_address = ''
	city_state_name = get_city_state_name(user_obj)
	addr = user_obj.address

	if addr.street1:
		_str_address += addr.street1+', '
	if addr.street2:
		_str_address += addr.street2+', '
	if city_state_name:
		_str_address += city_state_name+' '
	if addr.pincode:
		_str_address += addr.pincode			

	return 	_str_address


def all_teachers(_list):
	style0, style1, style2, wb = initiate()

	ws = wb.add_sheet('All Teachers data')
	ws.row(0).height_mismatch = True
	ws.row(0).height = 20*20
	ws.row(1).height_mismatch = True
	ws.row(1).height = 20*20
	ws.col(0).width = 9000
	ws.col(1).width = 2100
	ws.col(2).width = 18000
	ws.col(3).width = 5000
	ws.col(4).width = 12000
	ws.col(5).width = 5000
	ws.write(1, 0, 'Name', style2)
	ws.write(1, 1, 'Gender', style2)
	ws.write(1, 2, 'Address', style2)
	ws.write(1, 3, 'Phone Number', style2)
	ws.write(1, 4, 'Higher Education', style2)
	ws.write(1, 5, 'Date of Birth', style2)
	for i,teacher in enumerate(_list):
		ws.write(i+2, 0, teacher.full_name)
		ws.write(i+2, 1, teacher.gender)
		address = get_address(teacher)
		ws.write(i+2, 2, address)
		ws.write(i+2, 3, teacher.phone_number)
		ws.write(i+2, 4, teacher.higher_education)
		dob = teacher.d_o_b.strftime("%B %d, %Y")
		ws.write(i+2, 5, dob)
	return wb	


def all_students(_list):
	style0, style1, style2, wb = initiate()

	ws = wb.add_sheet('All Students data')
	ws.row(0).height_mismatch = True
	ws.row(0).height = 20*20
	ws.row(1).height_mismatch = True
	ws.row(1).height = 20*20
	ws.col(0).width = 9000
	ws.col(1).width = 2100
	ws.col(2).width = 18000
	ws.col(3).width = 5000
	ws.col(4).width = 12000
	ws.col(5).width = 5000
	ws.write(1, 0, 'Name', style2)
	ws.write(1, 1, 'Gender', style2)
	ws.write(1, 2, 'Address', style2)
	ws.write(1, 3, 'Phone Number', style2)
	ws.write(1, 4, 'Higher Education', style2)
	ws.write(1, 5, 'Date of Birth', style2)
	for i,student in enumerate(_list):
		ws.write(i+2, 0, student.full_name)
		ws.write(i+2, 1, student.gender)
		address = get_address(student)
		ws.write(i+2, 2, address)
		ws.write(i+2, 3, student.phone_number)
		ws.write(i+2, 4, student.higher_education)
		dob = student.d_o_b.strftime("%B %d, %Y")
		ws.write(i+2, 5, dob)
	return wb
def all_courses(_list):
	style0, style1, style2, wb = initiate()

	ws = wb.add_sheet('All Courses data')
	ws.row(0).height_mismatch = True
	ws.row(0).height = 20*20
	ws.row(1).height_mismatch = True
	ws.row(1).height = 20*20
	ws.col(0).width = 9000
	ws.col(1).width = 9000
	ws.col(2).width = 9000
	ws.col(3).width = 9000
	ws.write(1, 0, 'Course Name', style2)
	ws.write(1, 1, 'Course Duration', style2)
	ws.write(1, 2, 'Course Type', style2)
	ws.write(1, 3, 'Teacher Name', style2)
	for i,course in enumerate(_list):
		ws.write(i+2, 0, course.course_name)
		ws.write(i+2, 1, course.course_durations)
		ws.write(i+2, 2, course.course_sectors_and_associates)
		ws.write(i+2, 3, course.teacher.full_name)
	return wb					