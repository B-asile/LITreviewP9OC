from django import forms
from django.contrib.auth import get_user_model

from .models import Ticket, Review, UserFollows

user = get_user_model()

rating_values = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
]

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    class Meta():
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "titre"}


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    #rating = forms.ChoiceField(choices=SELECT_RATING, widget=forms.CheckboxSelectMultiple())
    #rating = forms.IntegerField(min_value=0, max_value=5)
    rating = forms.ChoiceField(choices=rating_values, widget=forms.RadioSelect)

    class Meta():
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "titre",
                  "rating": "note",
                  "body": "commentaire"
                  }


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)
