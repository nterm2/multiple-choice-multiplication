from django import forms 
from .models import Classroom 

class ClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom 
        fields = [
            'classroom_name'
        ]

class JoinClassrooomForm(forms.Form):
    classroom_code = forms.CharField(label="Enter classroom code sent by your teacher", max_length=36)