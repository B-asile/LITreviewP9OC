from django.contrib import admin

from blog.models import Ticket, UserFollows, Review

admin.site.register(Ticket),
admin.site.register(UserFollows),
admin.site.register(Review)
