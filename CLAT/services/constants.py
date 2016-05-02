CERTIFICATE_PATH = '/lms/media/certificate/'

DEFAULT_CERTIFICATE_PNG = '/lms/media/certificate/default/WEB_Certificate_Blank.png'

CERTIFICATE_FONT_FILE = 'DejaVuSans.ttf'

CERTIFICATE_RESULT = ('PASS', 'PARTICIPATE',)

DEMO_VIDEO_TYPE_BUTTON = ('mp4_button', 'youtube_button',)

DEFAULT_COURSE_IMAGE = 'course_demo_images/EDX_demo_course_image.jpg'

COURSE_VIDEO_TYPE = ('mp4', 'articulate',)

DEMO_VIDEO_INITIAL_PATH = 'demo/mp4/'

COURSE_VIDEO_INITIAL_PATH = ('video/mp4', 'video/articulate',)

VIDEO_FILE_EXTENSIONS = ('.mp4', '.zip',)

ROOT_PATH_FOR_VIDEOS = '/lms/media/'

OLD_ROOT_PATH_FOR_VIDEOS = '/CLAT_videos/media/'

PROGRESS_STATUSES = ('WAITING', 'UNDERPROCESS','COMPLETE',)

ACCESS_STATUSES = ('OPEN', 'CLOSE',)

RATING_INFO = {'1':'Bad','2':'Fair','3':'Good','4':'Very Good','5':'Excellent'}

DEFAULT_PROFILE_IMAGE = 'profile_images/CLAT_default_DP.png'

#(Public, Private, isProd,)
METTL_CONFIG = ('4a9bbe63-b533-49de-b1bb-9f6adcc38dc5','66ba7de5-4bff-4ba9-88a4-12b7d8d568f9',True,)

TEST_TYPES = ('I', 'M', 'E','C',)

TEST_STATUS = ('START', 'FINISH',)

TEST_CHECK_FOR = ('PASS', 'GRADED','FAIL',)

END_TEST_MODULE ='end'

PHONE_VERIFY_USES = ('register', 'troubleshoot', 'profile',)

QUIZ_TYPES = ('inline_quiz', 'midterm_quiz', 'casestudy_quiz', 'endterm_quiz',)

IMAGES_EXT_ALLOWED = ['png', 'gif', 'jpg', 'jpeg', 'JPG', 'PNG', 'GIF', 'JPEG']

DEFAULT_COURSE_IMAGE = 'course_demo_images/EDX_demo_course_image.jpg'

PASSWORD_VERIFY_USES = ('student', 'teacher',)

PASSWORD_VERIFY_OPTIONS = ('emailoption', 'mobileoption',)

TRANSACTION_ERROR_BANK = '<h3>Your transaction has been declined from the respective bank side. Try again or contact your bank customer care.</h3>'

TRANSACTION_ERROR_SERVER = '<h3>A server error has occured. If you have paid for the course, kindly mail us your transaction ID\
(received on your registered mobile number) & the course name at <a href="mailto:talktous@Clat.co.in?Subject=Transaction Server Error" target="_top" style="font-weight:bold;">talktous@Clat.co.in</a>. We will fix up the issue.</h3>'

TRANSACTION_FAILURE = '<h3>Your transaction has failed. Try again.</h3>'
 
TRANSACTION_CANCELLED = '<h3>Your transaction has been cancelled.</h3>'


# // start
TYPE_CHOICES = (
		('mp4', 'mp4'),
		('youtube', 'youtube'),
		('articulate', 'articulate'),
)

CERTIFICATE_CHOICES = (
	
		('PASS', 'PASS'),
		('PARTICIPATE', 'PARTICIPATE'),
)



STATUS_CHOICES = (
		('PENDING', 'Pending'),
		('DONE', 'Done'),
		('WAITING','Waiting'),
)


ACCESS_STATUS = (
	('OPEN','OPEN'),
	('CLOSE','CLOSE'),
	)

PROGRESS_STATUS = (
	('WAITING','WAITING'),
	('COMPLETED','COMPLETED'),
	('UNDERPROCESS','UNDERPROCESS'),
	)


ASSESMENT_TEST_CHOICE = (
		('INLINE', 'INLINE'),
		('MIDTERM', 'MIDTERM'),
		('END_COURSE', 'END_COURSE'),
)

INLINE_QUIZ_GAP = 4   # 4 modules

SECTORS_ASSOCIATES_CHOICES = (
		('Auto Components', 'Auto Components'),
		('Automobiles', 'Automobiles'),
		('Aviation', 'Aviation'),
		('Biotechnology', 'Biotechnology'),
		('Chemicals', 'Chemicals'),
		('Construction', 'Construction'),
		('Defence Manufacturing', 'Defence_Manufacturing'),
		('Electrical Machinery', 'Electrical_Machinery'),
		('Electronic System Design and Manufacturing', 'Electronic System Design and Manufacturing'),
		('Food Processing', 'Food Processing'),
		('IT and BPM', 'IT and BPM'),
		('Leather', 'Leather'),
		('Media and Entertainment', 'Media and Entertainment'),
		('Mining', 'Mining'),
		('Oil and Gas', 'Oil and Gas'),
		('Pharmaceuticals', 'Pharmaceuticals'),
		('Ports', 'Ports'),
		('Railways', 'Railways'),
		('Roads and Highways', 'Roads and Highways'),
		('Renewable Energy', 'Renewable Energy'),
		('Space', 'Space'),
		('Textiles', 'Textiles'),
		('Thermal Power', 'Thermal Power'),
		('Tourism and Hospitality', 'Tourism and Hospitality'),
		('Wellness', 'Wellness'),
)

WEEKS = tuple( ( (i,i,) for i in xrange(1,21)) )

# '''Cache configuration'''
CACHE_KEYS = {
	'cvd' : 'cvd%d%d',
	'd' : 'd%d',
	'cda' : 'cda%d',
}
