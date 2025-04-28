from django.shortcuts import render
from django.shortcuts import render
from accounts.models import FitUser 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import FitUser, WorkoutGroup, Challenge
from django.utils.timezone import now


# Create your views here.
def home_page(request):
    active_challenges = Challenge.objects.filter(start_date__lte=now(), end_date__gte=now())
    return render(request, 'home.html', {
        'active_challenges': active_challenges,
    })

@login_required
def join_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    challenge.competitors.add(request.user)
    return redirect('home') 

def contact_page(request): 
    return render(request, "contact.html")

@login_required
def social_page(request):
    query = request.GET.get('query', '')
    group_query = request.GET.get('group_query', '')
    
    search_results = []
    group_search_results = []

    # Handle user search
    if query:
        search_results = FitUser.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

    # Handle group search
    if group_query:
        group_search_results = WorkoutGroup.objects.filter(
            Q(name__icontains=group_query)
        )

    if request.method == "POST":
        action = request.POST.get('action')

        if action in ['send_request', 'accept_request', 'decline_request', 'remove_friend']:
            user_id = request.POST.get('user_id')
            target_user = get_object_or_404(FitUser, id=user_id)

            if action == 'send_request':
                request.user.friend_requests_sent.add(target_user)
            elif action == 'accept_request':
                request.user.friends.add(target_user)
                target_user.friends.add(request.user)
                request.user.friend_requests_received.remove(target_user)
            elif action == 'decline_request':
                request.user.friend_requests_received.remove(target_user)
            elif action == 'remove_friend':
                request.user.friends.remove(target_user)
                target_user.friends.remove(request.user)

        elif action == 'create_group':
            group_name = request.POST.get('group_name')
            group_description = request.POST.get('group_description', '')

            if group_name:
                new_group = WorkoutGroup.objects.create(
                    name=group_name,
                    description=group_description
                )
                new_group.members.add(request.user) 

        elif action == 'join_group':
            group_id = request.POST.get('group_id')
            group = get_object_or_404(WorkoutGroup, id=group_id)
            group.members.add(request.user)

        elif action == 'leave_group':
            group_id = request.POST.get('group_id')
            group = get_object_or_404(WorkoutGroup, id=group_id)
            group.members.remove(request.user)

        return redirect('social')

    context = {
        'search_results': search_results,
        'friends': request.user.friends.all(),
        'friend_requests': request.user.friend_requests_received.all(),

        'group_search_results': group_search_results,
        'my_groups': request.user.workout_groups.all(),  
    }
    return render(request, 'social.html', context)