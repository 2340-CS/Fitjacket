from django.shortcuts import render
from django.shortcuts import render
from accounts.models import FitUser 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import FitUser


# Create your views here.
def home_page(request): 
    return render(request, "home.html")

def contact_page(request): 
    return render(request, "contact.html")

@login_required
def social_page(request):
    query = request.GET.get('query', '')
    search_results = []
    
    if query:
        search_results = FitUser.objects.filter(
            Q(username__icontains=query)
        ).exclude(id=request.user.id)

    if request.method == "POST":
        action = request.POST.get('action')
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

        return redirect('social')

    context = {
        'search_results': search_results,
        'friends': request.user.friends.all(),
        'friend_requests': request.user.friend_requests_received.all(),
    }
    return render(request, 'social.html', context)
