from django.forms import ModelForm, Textarea
from reviews.models import OflcPerm_Review 

class ReviewForm(ModelForm):
    class Meta:
        model = OflcPerm_Review 
        fields = ['comment',]
        widgets = {
            'comment': Textarea(attrs={ 'cols':40, 
                                        'rows':5, 
                                        'maxlength':400, 
                                        'class':"form-control",
                                        'placeholder':'comment',
                                        
                                        }) 
        }

