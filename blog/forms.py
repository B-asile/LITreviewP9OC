from django import forms
from django.contrib.auth import get_user_model

from .models import Ticket, Review

user = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta():
        model = Ticket
        fields = ['title', 'description', 'image']
        labels = {"title": "titre"}


class ReviewForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    #rating = forms.ChoiceField(choices=SELECT_RATING, widget=forms.CheckboxSelectMultiple())
    rating = forms.IntegerField(min_value=0, max_value=5)
    class Meta():
        model = Review
        fields = ['headline', 'rating', 'body']
        labels = {"headline": "titre",
                  "rating": "note",
                  "body": "commentaire"
                  }


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['follows']

class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)
