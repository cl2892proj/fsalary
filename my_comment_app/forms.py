
from django import forms
from django_comments.forms import CommentForm
from my_comment_app.models import MPTTComment


class MPTTCommentForm(CommentForm):
    parent = forms.ModelChoiceField(
                    queryset=MPTTComment.objects.all(), 
                    required=False, 
                    widget=forms.HiddenInput)

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the parent field
        data = super(MPTTCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data
