from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify

# Import your models and the dictionary
from .models import Location, UserProfile, Message, ClusterHistory
from .utils import get_recommendations
from .data import DESTINATIONS  # <--- CRITICAL: Import your rich data

@login_required
def home(request):
    return render(request, 'app/index.html')

@login_required
def survey(request):
    return render(request, 'app/survey.html')

def detail(request, destination_slug):
    """
    Renders the detail page using the rich data from data.py.
    The slug from the URL (e.g., 'everestbasecamp') must match the 
    keys in the DESTINATIONS dictionary.
    """
    # 1. Try to get data from the dictionary first
    # We remove dashes because your data.py keys are 'everestbasecamp' not 'everest-base-camp'
    lookup_key = destination_slug.replace('-', '')
    place_data = DESTINATIONS.get(lookup_key)

    if not place_data:
        # 2. Fallback: If not in dictionary, try a direct match
        place_data = DESTINATIONS.get(destination_slug)

    if not place_data:
        # 3. Last Resort: 404 if it's not in data.py at all
        return render(request, '404.html', status=404)
        
    return render(request, 'app/detail.html', {'place': place_data})

@login_required
def recommend(request):
    if request.method == "POST":
        try:
            # Gather Score Data
            nature = (int(request.POST.get('nature_forests', 5)) + 
                      int(request.POST.get('nature_wildlife', 5)) + 
                      int(request.POST.get('nature_lakes', 5))) / 3

            adventure = (int(request.POST.get('thrill_climb', 5)) + 
                         int(request.POST.get('thrill_extreme', 5)) + 
                         int(request.POST.get('thrill_rugged', 5))) / 3

            culture = (int(request.POST.get('culture_temples', 5)) + 
                       int(request.POST.get('culture_festivals', 5)) + 
                       int(request.POST.get('culture_ethnic', 5))) / 3

            altitude = (int(request.POST.get('terrain_alt', 5)) + 
                        int(request.POST.get('terrain_snow', 5)) +
                        int(request.POST.get('style_peace', 5))) / 3

            user_input = [nature, adventure, culture, altitude]
            
            recommendations, cluster_id = get_recommendations(user_input)

            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.cluster_id = cluster_id
            profile.save()
            ClusterHistory.objects.get_or_create(user=request.user, cluster_id=cluster_id)
            
            # Use specific slug mapping to match data.py keys exactly
            slug_map = {
                'Everest Base Camp': 'everestbasecamp',
                'Pokhara (Lakeside)': 'pokharalakeside',
                'Bandipur Village': 'bandipurvillage',
                'Ilam (Tea Gardens)': 'ilamteagardens',
            }

            for loc in recommendations:
                # We use the slug_map so the button links match data.py keys
                loc.target_slug = slug_map.get(loc.name, slugify(loc.name).replace('-', ''))
                
                # Image fallback: check if it exists in data.py, else use default
                if loc.target_slug in DESTINATIONS:
                    loc.manual_image = DESTINATIONS[loc.target_slug].get('hero_image')
                else:
                    loc.manual_image = 'app/assets/images/default.jpg'
            
            return render(request, 'app/results.html', {
                'locations': recommendations,
                'cluster': cluster_id
            })

        except Exception as e:
            print(f"Error: {e}")
            return redirect('survey')
    
    return redirect('survey')

@login_required
def messenger(request, username=None):
    unlocked_clusters = ClusterHistory.objects.filter(user=request.user).values_list('cluster_id', flat=True).distinct()
    cluster_param = request.GET.get('cluster')
    
    if not cluster_param:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        current_selected_cluster = user_profile.cluster_id
    else:
        try:
            current_selected_cluster = int(cluster_param)
        except ValueError:
            current_selected_cluster = None
    
    matches = []
    if current_selected_cluster is not None:
        matches = UserProfile.objects.filter(cluster_id=current_selected_cluster).exclude(user=request.user)

    active_chat_user = None
    chat_history = []

    if username:
        active_chat_user = get_object_or_404(User, username=username)
        chat_history = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=active_chat_user)) |
            (Q(sender=active_chat_user) & Q(receiver=request.user))
        ).order_by('timestamp')

    if request.method == "POST" and active_chat_user:
        msg_content = request.POST.get('content')
        if msg_content:
            Message.objects.create(sender=request.user, receiver=active_chat_user, content=msg_content)
            url = reverse('messenger_with_user', kwargs={'username': username})
            if current_selected_cluster is not None:
                url += f"?cluster={current_selected_cluster}"
            return redirect(url)

    return render(request, 'app/chat.html', {
        'matches': matches,
        'unlocked_clusters': unlocked_clusters,
        'current_cluster': current_selected_cluster,
        'active_chat_user': active_chat_user,
        'chat_history': chat_history,
    })

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                auth_logout(request)
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})