from django import forms
import validators
from user_login.form import MyForm
from course_mang.models import CourseDetail, CourseVideos, CourseWeek, CourseInformation, CourseImage
import utilities
import datetime
from CLAT.services import course_service

class CourseDetailForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(attrs={'type':"text",'id':"course_name",'placeholder':"Please Enter your Course Name",'autocomplete':"off",'class':"text-sbox", 'autocomplete':'off'}),max_length=200, label='Course Name')
    course_sectors_and_associates = forms.ChoiceField(choices=utilities.SECTORS_ASSOCIATES_CHOICES,widget=forms.Select(attrs={'class':"selectpicker text-sbox"}))
    course_demo_file_url = forms.URLField(widget=forms.URLInput(attrs={'id':"youtube_demo_url",'placeholder':"Please enter a valid You Tube URL.",'class':"text-sbox",'style':"width: 40em;onblur=checkYoutubeURL(this);",'autocomplete':'off'}),max_length=200,required=False)
    course_durations =  forms.ChoiceField(choices=utilities.WEEKS,widget=forms.Select(attrs={'class':"selectpicker text-sbox"}))
    show_video = forms.BooleanField(initial=True,required=False)
    
    def clean(self):
        data = self.cleaned_data['course_name']
        if CourseDetail.objects.filter(course_name=data).count() > 0:
            raise forms.ValidationError("We already have a course with this name")    

        if self.cleaned_data['course_demo_file_url'] == "" and self.cleaned_data['course_demo_file'] == None:
            msg = "Either provide a Youtube URL or a MP4 video"
            self._errors['course_demo_file_url']=msg
            self._errors['course_demo_file']=msg
            raise forms.ValidationError(msg)

    class Meta:
        model = CourseDetail
        fields=('course_name','course_sectors_and_associates','course_demo_file','course_demo_file_url','course_durations')


'''
Course Information form
'''
class CourseInformationForm(forms.ModelForm):
    course_description = forms.CharField(widget=forms.Textarea(attrs={'id':"course_description",'placeholder':"Please enter your Course Description.",'class':"text-sbox",'rows':'5','autocomplete':'off'})) #Text area can't have label
    course_objective = forms.CharField(widget=forms.Textarea(attrs={'id':"course_objective",'placeholder':"Please enter your Course Objective ( what you want the student to learn ).",'class':"text-sbox",'rows':'5','autocomplete':'off'})) #Text area can't have label


    class Meta:
        model = CourseInformation
        fields = ('course_objective', 'course_description')

'''
Course Image form
'''
class CourseImageForm(forms.ModelForm):
    picture=forms.ImageField(label='Course Image',required=False,error_messages ={'invalid':"Image files only"},\
                                   widget=forms.FileInput(attrs={'id':'course_image_file_upload'}))
    
    class Meta:
        model = CourseImage
        fields = ('picture',)


'''
Course Week form
'''
class CourseWeekForm(forms.ModelForm):

    week_module_name = forms.CharField(widget=forms.TextInput(attrs={'class':"text-sbox",'name':"module_name" ,'id':"module_name",'autocomplete':'off'}),validators = [validators.validate_weekly_module_name])
    week_detail = forms.CharField(widget=forms.Textarea(attrs={'style':"width:100%;resize:none;text-transform:lowercase;",'cols':"10",'rows':"4",'placeholder':"Please enter the details of each weekly added modules...",'name':"weekly_module_details",'id':"weekly_module_details",'autocomplete':'off'}))
    
    def clean_week_module_name(self):   
        data = self.cleaned_data['week_module_name']
        if CourseWeek.objects.filter(week_module_name=data).count() > 0:
            raise forms.ValidationError("We already have a module with this name!!!")
        return data

    class Meta:
        model = CourseWeek
        fields=('week_module_name','week_detail',)


'''
Course Videos form
'''
class CourseVideosForm(forms.ModelForm):

    video_file = forms.FileField(widget=forms.FileInput(attrs={'id':'articulate_file','type':'file','placeholder':'File format must be in .zip or mp4 format','class':'text-sbox','onchange':'checkForMime(this)'}),required=False)
    module_name = forms.CharField(widget=forms.Select(attrs={'type':'text','class':'text-sbox','id':'module_name','onblur':'checkModuleName(this)','autocomplete':'off'}))
    video_url = forms.URLField(widget=forms.URLInput(attrs={'id':"youtube_course_url",'placeholder':"Please enter a valid You Tube URL.",'class':"text-sbox",'style':"width: 40em;",'onblur':"checkYoutubeURL(this);",'autocomplete':'off'}),max_length=200,required=False)
    video_type = forms.ChoiceField(widget=forms.Select(attrs={'class':"selectpicker text-sbox",'id':'video_type'}),choices=utilities.TYPE_CHOICES)

    def clean(self):
        video_type_value = self.cleaned_data['video_type']

        if self.cleaned_data['video_url'] == "" and self.cleaned_data['video_file'] == None:          
            msg = "Either provide a Youtube URL, a MP4 video or a ZIP file"
            self._errors['video_url']=msg
            self._errors['video_file']=msg
            raise forms.ValidationError(msg)

        if self.cleaned_data['video_file'] != None and video_type_value !='youtube':
            if video_type_value == 'mp4':
                print('mp4')
                validated = validators.validate_file_extension(self.cleaned_data['video_file'],'mp4')
                if validated == 1:  # File extension not supported
                    msg = "MP4 file expected!!!"
                    self._errors['video_file'] = msg
                    raise forms.ValidationError(msg)

            if video_type_value == 'articulate':
                print('articulate')
                validated = validators.validate_file_extension(self.cleaned_data['video_file'],'zip')
                if validated == 1:  # File extension not supported
                    msg = "ZIP file expected!!!"
                    self._errors['video_file'] = msg
                    raise forms.ValidationError(msg)

        if video_type_value == "youtube":
            validated = validators.validate_yut_url(self.cleaned_data['video_url'])
            if validated == 1:
                msg = "Youtube video link expected!!!"
                self._errors['video_url'] = msg
                raise forms.ValidationError(msg)

    class Meta:
        model = CourseVideos
        fields=('video_file','module_name','video_url','video_type',)
