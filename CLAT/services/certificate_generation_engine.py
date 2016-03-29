from CLAT.services import constants



def create_certificate(certificate_id, fullname, coursename, added_date):
	try:
		from PIL import Image, ImageDraw, ImageFont
		# get an image

		base = Image.open(constants.DEFAULT_CERTIFICATE_PNG)

		import datetime
		d = datetime.datetime.strptime(str(added_date).split(' ')[0], '%Y-%m-%d')
		formated_date = d.strftime('%b %d,%Y')

		# make a blank image for the text, initialized to transparent text color
		base.show()
		txt = Image.new('RGBA', base.size, (255,255,255,0))
		# get a font

		fnt = ImageFont.truetype(constants.CERTIFICATE_FONT_FILE, 15)
		# get a drawing context

		d = ImageDraw.Draw(txt)
		x_fullname = 325
		x_coursename = 325
		# draw text, half opacity
		if len(fullname) > 20:
			x_fullname = 275
		if len(coursename) > 20:
			x_coursename = 250
		if len(coursename) > 40:
			coursename = coursename[:30]

		d.text((x_fullname,350), fullname, font=fnt, fill=(255,255,255,128))
		# draw text, full opacity
		d.text((x_coursename,418), coursename, font=fnt, fill=(255,255,255,255))
		d.text((370,450), str(formated_date), font=fnt, fill=(255,255,255,255))

		out = Image.alpha_composite(base, txt)

		out.show()
		import os

		directory = constants.CERTIFICATE_PATH+str(certificate_id)
		if not os.path.exists(directory):
			os.makedirs(directory)
		img_path = directory+'/cert.png'
		
		out.save(img_path)
		return img_path
	except Exception as e:
		print e.args
		return None
