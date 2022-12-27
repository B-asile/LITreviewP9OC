from itertools import chain

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from authentication.models import User
from . import models, forms


@login_required
def home(request):
    ''' search for tickets affiliated with the user
     profile & according to UserFollow'''
    profile_tickets = models.Ticket.objects.filter(user=request.user)
    follow_tickets = models.Ticket.objects.filter(
        user__in=models.UserFollows.objects.filter(
            user=request.user).values_list('followed_user'))
    profile_reviews = models.Review.objects.filter(user=request.user)
    follow_reviews = models.Review.objects.filter(
        user__in=models.UserFollows.objects.filter(
            user=request.user).values_list('followed_user'))
    other_reviews = models.Review.objects.filter(
        ticket__user=request.user).difference(profile_reviews, follow_reviews)
    tickets_and_reviews = sorted(chain(profile_tickets, follow_tickets,
                                       profile_reviews, follow_reviews,
                                       other_reviews),
                                 key=lambda instance: instance.time_created,
                                 reverse=True)
    return render(request, 'home.html', context={
        'tickets_and_reviews': tickets_and_reviews
    })


@login_required
def posts(request):
    '''search & display of tickets & reviews
     only associated with the identified user '''
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda element: element.time_created,
                                 reverse=True)
    return render(request, 'posts.html', context={
        'tickets_and_reviews': tickets_and_reviews
    })


@login_required
def create_ticket(request):
    '''ticket creation'''
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'ticket.html', context={'ticket_form': ticket_form})


@login_required
def create_review(request):
    '''review creation'''
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        print(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {'ticket_form': ticket_form,
               'review_form': review_form}
    return render(request, 'create_review.html', context=context)


@login_required
def edit_review(request, review_id):
    '''function to modify a review'''
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST,
                                         request.FILES,
                                         instance=review)
            if edit_form.is_valid():
                review = edit_form.save(commit=False)
                review.save()
            return redirect('home')
    return render(request, "edit.html", context={'edit_form': edit_form})


@login_required
def delete_review(request, review_id):
    '''delete review'''
    review = get_object_or_404(models.Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('home')
    return render(request, 'delete_review.html', context={'review': review})


def follow_users(request):
    '''display of the followed users as well as those who follow.
        Display & selection of users to follow'''
    main_user = models.UserFollows()
    followed = models.UserFollows.objects.filter(
        user=request.user)
    following = models.UserFollows.objects.filter(
        followed_user=request.user)
    if request.method == 'POST':
        try:
            searched_user = request.POST.get('username')
            check = 0
            for find_user in User.objects.all():
                if str(searched_user) == str(find_user):
                    check = check + 1
            if check > 0:
                pass
            else:
                raise IntegrityError
            followed_user = User.objects.get(
                username=searched_user
            )
            main_user.followed_user = followed_user
            if followed_user == request.user:
                raise IntegrityError
            else:
                main_user.user = request.user
                main_user.save()
            return redirect('reviews-follow_user')
        except IntegrityError:
            messages.error(request,
                           'erreur de saisie, veuillez recommencer'
                           )
    return render(request,'followUser.html', context={
        'followed': followed,
        'following': following
    })


''''
@login_required
def follow_users(request):
    form = forms.FollowUsersForm
    followed = models.UserFollows.objects.filter(
        user=request.user)
    following = models.UserFollows.objects.filter(
        followed_user=request.user)
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST)
        try:
            if form.is_valid():
                follow_users = form.save(commit=False)
                #print(request.POST['followed_user'])
                #print(request.user.id)
                if str(request.user.id) == str(request.POST[
                                                   'followed_user'
                                               ]):
                    raise IntegrityError
                else:
                    follow_users.user = request.user
                    follow_users.save()
            return redirect('reviews-follow_user')
        except IntegrityError:
            messages.error(request,
                           'vous êtes déjà abonné à cet utilisateur ou'
                           ' vous ne pouvez pas vous suivre!'
                           )
    return render(request, 'followUser.html',
                  context={
                      'form': form,
                      'followed': followed,
                      'following': following
                  })
'''


@login_required()
def delete_followed(request, followed_user_id):
    '''deleting a tracked user'''
    followed_user = get_object_or_404(models.UserFollows, id=followed_user_id)
    if request.method == 'POST':
        followed_user.delete()
        return redirect('reviews-follow_user')
    return render(request, "delete_followed.html", context={
        'followed_user': followed_user
    })


@login_required
def edit_ticket(request, ticket_id):
    '''function to modify a ticket'''
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST,
                                         request.FILES,
                                         instance=ticket)
            if edit_form.is_valid():
                ticket = edit_form.save(commit=False)
                ticket.save()
                return redirect('home')
    return render(request, "edit.html", context={'edit_form': edit_form})


@login_required
def delete_ticket(request, ticket_id):
    '''function to delete a ticket'''
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        print('coucou')
        ticket.delete()
        return redirect('home')
    return render(request, 'delete_ticket.html', context={'ticket': ticket})


@login_required
def reply_to_ticket(request, ticket_id):
    '''function creating a review in response to a ticket'''
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            ticket.reviewed = True
            ticket.save()
            return redirect('home')
    return render(request, 'reply_ticket.html', context={
        'ticket': ticket, 'review_form': review_form, 'response': True
    })
