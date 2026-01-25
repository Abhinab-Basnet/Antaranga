from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse

from .models import Location, UserProfile, Message, ClusterHistory
from .utils import get_recommendations

@login_required
def home(request):
    return render(request, 'app/index.html')

@login_required
def survey(request):
    return render(request, 'app/survey.html')

@login_required
def recommend(request):
    if request.method == "POST":
        try:
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

            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.cluster_id = cluster_id
            profile.save()
            
            ClusterHistory.objects.get_or_create(user=request.user, cluster_id=cluster_id)
            
            image_map = {
                'Everest Base Camp': 'app/assets/images/ebc.jpg',
                'Pokhara (Lakeside)': 'app/assets/images/pokhara.jpg',
                'Kathmandu Durbar Square': 'app/assets/images/kathmandu.jpg',
                'Chitwan National Park': 'app/assets/images/chitwan.jpg',
                'Lumbini (Birthplace of Buddha)': 'app/assets/images/lumbini.jpg',
                'Annapurna Base Camp': 'app/assets/images/abc.jpg',
                'Bhaktapur Durbar Square': 'app/assets/images/bhaktapur.jpg',
                'Nagarkot (Sunrise View)': 'app/assets/images/nagarkot.jpg',
                'Rara Lake': 'app/assets/images/rara.jpg',
                'Muktinath Temple': 'app/assets/images/muktinath.jpg',
                'Ghorepani Poon Hill': 'app/assets/images/poonhill.jpg',
                'Janakpur (Janaki Temple)': 'app/assets/images/janakpur.jpg',
                'Bandipur Village': 'app/assets/images/bandipur.jpg',
                'Langtang Valley': 'app/assets/images/langtang.jpg',
                'Manaslu Circuit': 'app/assets/images/manaslu.jpg',
                'Ilam (Tea Gardens)': 'app/assets/images/ilam.jpeg',
                'Upper Mustang (Lo Manthang)': 'app/assets/images/mustang.jpg',
                'Gosaikunda Lake': 'app/assets/images/gosaikunda.jpg',
                'Patan Durbar Square': 'app/assets/images/patan.jpg',
                'Bardia National Park': 'app/assets/images/bardia.jpg',
            }

            for loc in recommendations:
                loc.manual_image = image_map.get(loc.name, 'app/assets/images/default.jpg')
            
            return render(request, 'app/results.html', {
                'locations': recommendations,
                'cluster': cluster_id
            })

        except Exception as e:
            return redirect('survey')
    
    return redirect('survey')

@login_required
def messenger(request, username=None):
    unlocked_clusters = ClusterHistory.objects.filter(user=request.user).values_list('cluster_id', flat=True).distinct()
    
    current_selected_cluster = request.GET.get('cluster')
    
    if not current_selected_cluster:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        current_selected_cluster = user_profile.cluster_id
    
    matches = []
    if current_selected_cluster is not None:
        matches = UserProfile.objects.filter(
            cluster_id=current_selected_cluster
        ).exclude(user=request.user)

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
        'current_cluster': int(current_selected_cluster) if current_selected_cluster else None,
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