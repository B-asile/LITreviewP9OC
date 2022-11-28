from itertools import chain
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from . import models, forms


@login_required
def home(request):
    tickets = models.Ticket.objects.all()

    reviews = models.Review.objects.all()
    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda instance: instance.time_created,
                                 reverse=True)
    return render(request, 'home.html', context={'tickets': tickets,
                                                 'reviews': reviews,
                                                 'tickets_and_reviews': tickets_and_reviews
                                                 })

@login_required
@permission_required('add_ticket', raise_exception=True)
def create_ticket(request):
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
def follow_users(request):
    global form, followed
    if request.method == 'POST':
        try:
            form = forms.FollowUsersForm(request.POST)
            if form.is_valid():
                follow_users = form.save(commit=False)
                follow_users.user = request.user
                follow_users.save()
                return redirect('home')
        except ValueError as e:
            error = str(e)
        return render(request, 'followUser.html', context={'form': form, 'error': error})
    if models.UserFollows.objects.filter(user=request.user):
        followed = models.UserFollows.objects.filter(user=request.user)
    if models.UserFollows.objects.filter(followed_user=request.user):
        following = models.UserFollows.objects.filter(followed_user=request.user)
    return render(request, 'followUser.html', context={'followed': followed, 'following': following})


@login_required
@permission_required('change_ticket', raise_exception=True)
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeletePostForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                ticket = edit_form.save(commit=False)
                ticket.save()
                return redirect('home')
            if 'delete_post' in request.POST:
                delete_form = forms.DeletePostForm(request.POST)
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect('home')
    context = {'edit_form': edit_form,
               'delete_form': delete_form
               }
    return render(request, 'edit.html', context=context)


@login_required
def reply_to_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    return render(request, 'reply_ticket.html', context={'review_form': review_form})
