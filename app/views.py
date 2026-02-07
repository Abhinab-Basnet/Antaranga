import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages

# Import your models and the dictionary
from .models import Location, UserProfile, Message, ClusterHistory
from .utils import get_recommendations
from .data import DESTINATIONS  

@login_required
def home(request):
    """Renders the landing page."""
    return render(request, 'app/index.html')

@login_required
def survey(request):
    """Renders the recommendation survey/ritual."""
    return render(request, 'app/survey.html')

@login_required
def dashboard(request):
    """
    The Advanced Intelligence Dashboard.
    Fetches real-time profile data, clustering history, and top matches.
    """
    # 1. Fetch the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # 2. Calculate technical stats
    clusters_unlocked = ClusterHistory.objects.filter(user=request.user).values_list('cluster_id', flat=True).distinct().count()
    
   
    total_destinations = len(DESTINATIONS) if DESTINATIONS else 0
    

    lookup_key = profile.top_match_name.lower().replace(' ', '').replace('(', '').replace(')', '') if profile.top_match_name else ""
    top_place = DESTINATIONS.get(lookup_key)

    
    if profile.nature_score > 0 or profile.adventure_score > 0:
        match_score = round(85 + (profile.nature_score / 20), 1)
        if match_score > 99.8: match_score = 99.8 
    else:
        match_score = 0

    context = {
        'profile': profile,
        'total_places': total_destinations,
        'clusters_count': clusters_unlocked,
        'top_place': top_place,
        'inference_time': 0.042, 
        'match_score': match_score,
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def results(request):
    """
    Persistent Results View: Fetches saved recommendations from the database
    based on the user's saved cluster_id and plays music based on that cluster.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if not profile.top_match_name:
        messages.warning(request, "Please complete the survey first.")
        return redirect('survey')

 
    recommendations = list(Location.objects.filter(cluster_id=profile.cluster_id))

    
    music_map = {
        0: 'culture_vibes.mp3',   # Traditional / Heritage
        1: 'mountain_epic.mp3',   # High Altitude / Trekking
        2: 'adventure_rock.mp3',  # Adrenaline / Action
        3: 'nature_zen.mp3'       # Peaceful / Lakes / Spiritual
    }
   
    selected_music = music_map.get(profile.cluster_id, 'nature_zen.mp3')

    
    slug_map = {
        'Everest Base Camp': 'everestbasecamp',
        'Pokhara (Lakeside)': 'pokharalakeside',
        'Kathmandu Durbar Square': 'kathmandudurbarsquare',
        'Chitwan National Park': 'chitwannationalpark',
        'Lumbini (Birthplace of Buddha)': 'lumbini',
        'Annapurna Base Camp': 'annapurnabasecamp',
        'Bhaktapur Durbar Square': 'bhaktapur',
        'Nagarkot (Sunrise View)': 'nagarkot',
        'Rara Lake': 'raralake',
        'Muktinath Temple': 'muktinath',
        'Ghorepani Poon Hill': 'ghorepanipoonhill',
        'Janakpur (Janaki Temple)': 'janakpur',
        'Bandipur Village': 'bandipurvillage',
        'Langtang Valley': 'langtangvalley',
        'Manaslu Circuit': 'manaslucircuit',
        'Ilam (Tea Gardens)': 'ilamteagardens',
        'Upper Mustang (Lo Manthang)': 'uppermustang',
        'Gosaikunda Lake': 'gosaikundalake',
        'Patan Durbar Square': 'patan',
        'Bardia National Park': 'bardianationalpark',
        'Kanchenjunga Base Camp': 'kanchenjungabasecamp',
        'Makalu Barun Valley': 'makalubarunvalley',
        'Dhaulagiri Circuit': 'dhaulagiricircuit',
        'Api Nampa Conservation': 'apinampa',
        'Rolwaling Valley': 'rolwalingvalley',
        'Tsho Rolpa Lake': 'tshorolpalake',
        'Cho Oyu Base Camp': 'chooyubasecamp',
        'Mardi Himal Base Camp': 'mardihimal',
        'Island Peak (Imja Tse)': 'islandpeak',
        'Lobuche East': 'lobucheeast',
        'Pathivara Devi Temple': 'pathivara',
        'Halesi Mahadev Cave': 'halesimahadev',
        'Swayambhunath Stupa': 'swayambhunath',
        'Dakshinkali Temple': 'dakshinkali',
        'Tengboche Monastery': 'tengboche',
        'Namobuddha Monastery': 'namobuddha',
        'Budhanilkantha': 'budhanilkantha',
        'Changunarayan Temple': 'changunarayan',
        'Kopan Monastery': 'kopanmonastery',
        'Muktinath Valley': 'muktinathvalley',
        'Bajrayogini Temple': 'bajrayogini',
        'Bindhyabasini Temple': 'bindhyabasini',
        'Ghalegaun Homestay': 'ghalegaun',
        'Sirubari Village': 'sirubari',
        'Dhampus Village': 'dhampus',
        'Balthali Village': 'balthali',
        'Tansen Palpa': 'tansenpalpa',
        'Kakani': 'kakani',
        'Barpak Village': 'barpak',
        'Gupteshwor Cave': 'gupteshworcave',
        'Sikles Village': 'sikles',
        'Daman Viewpoint': 'daman',
        'Koshi Tappu Reserve': 'koshitappu',
        'Shuklaphanta National Park': 'shuklaphanta',
        'Parsa National Park': 'parsanationalpark',
        'Blackbuck Conservation': 'blackbuckconservation',
        'Beeshazar Lake': 'beeshazarlake',
        'Jagadishpur Reservoir': 'jagadishpur',
        'Shey Phoksundo Lake': 'sheyphoksundo',
        'Khaptad National Park': 'khaptadnationalpark',
        'Dhorpatan Reserve': 'dhorpatan',
        'Tilicho Lake': 'tilicholake',
        'Begnas Lake': 'begnaslake',
        'Rupa Lake': 'rupalake',
        'Badimalika': 'badimalika',
        'The Last Resort': 'thelastresort',
        'Kushma Bungee': 'kushmabungee',
        'Sarangkot Paragliding': 'sarangkot',
        'Trisuli River Rafting': 'trisulirafting',
        'Kalinchowk Bhagwati': 'kalinchowk',
        'Chandragiri Hills': 'chandragiri'
    }

    for loc in recommendations:
      
        loc.target_slug = slug_map.get(loc.name, slugify(loc.name).replace('-', ''))
        
        if loc.target_slug in DESTINATIONS:
            loc.manual_image = DESTINATIONS[loc.target_slug].get('hero_image')
        else:
            loc.manual_image = 'app/assets/images/default.jpg'
    
   
    top_locations = recommendations[:10]
    all_locations = recommendations  

    return render(request, 'app/results.html', {
        'top_locations': top_locations, 
        'all_locations': all_locations, 
        'locations': recommendations,   
        'cluster': profile.cluster_id,
        'profile': profile,
        'music_file': selected_music   
    })

@login_required
def reset_survey(request):
    """Hard Reset: Clears user scores so they can retake the survey."""
    profile = get_object_or_404(UserProfile, user=request.user)
    profile.nature_score = 0
    profile.adventure_score = 0
    profile.culture_score = 0
    profile.altitude_score = 0
    profile.top_match_name = ""
    profile.cluster_id = 0
    profile.save()
    
    messages.info(request, "Vibe DNA purged. You may begin a new ritual.")
    return redirect('survey')

def detail(request, destination_slug):
    """Renders the detail page using the rich data from data.py."""
    lookup_key = destination_slug.replace('-', '')
    place_data = DESTINATIONS.get(lookup_key)

    if not place_data:
        place_data = DESTINATIONS.get(destination_slug)

    if not place_data:
        return render(request, '404.html', status=404)
        
    return render(request, 'app/detail.html', {'place': place_data})

@login_required
def recommend(request):
    """Processes survey input, saves to DB, then redirects to results."""
    if request.method == "POST":
        try:
            # 1. Gather Score Data
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
            primary_match_name = recommendations[0].name if recommendations else "None"

         
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.cluster_id = cluster_id
            profile.nature_score = round(nature * 10, 1)
            profile.adventure_score = round(adventure * 10, 1)
            profile.culture_score = round(culture * 10, 1)
            profile.altitude_score = round(altitude * 10, 1)
            profile.top_match_name = primary_match_name
            profile.save()

           
            ClusterHistory.objects.get_or_create(user=request.user, cluster_id=cluster_id)
            
           
            return redirect('results')

        except Exception as e:
            print(f"Error in recommendation logic: {e}")
            return redirect('survey')
    
    return redirect('survey')

@login_required
@login_required
def messenger(request, username=None):
    # 1. Get all clusters the user has ever 'unlocked' through surveys
    unlocked_clusters = ClusterHistory.objects.filter(user=request.user).values_list('cluster_id', flat=True).distinct()
    
    # 2. Check if a specific cluster was requested via the dropdown (?cluster=X)
    cluster_param = request.GET.get('cluster')
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Use the requested cluster, otherwise fall back to the user's current profile cluster
    if cluster_param and cluster_param.isdigit():
        current_selected_cluster = int(cluster_param)
    else:
        current_selected_cluster = user_profile.cluster_id
    
    # 3. Filter matches based on the SELECTED cluster
    matches = UserProfile.objects.filter(cluster_id=current_selected_cluster).exclude(user=request.user)

    active_chat_user = None
    chat_history = []

    if username:
        active_chat_user = get_object_or_404(User, username=username)
        chat_history = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=active_chat_user)) |
            (Q(sender=active_chat_user) & Q(receiver=request.user))
        ).order_by('timestamp')

    # Note: If you use WebSockets (which we have set up), this POST block 
    # acts as a backup, but usually, the WebSocket handles the sending.
    if request.method == "POST" and active_chat_user:
        msg_content = request.POST.get('content')
        if msg_content:
            Message.objects.create(sender=request.user, receiver=active_chat_user, content=msg_content)
            url = reverse('messenger_with_user', kwargs={'username': username})
            if cluster_param: 
                url += f"?cluster={cluster_param}"
            return redirect(url)

    return render(request, 'app/chat.html', {
        'matches': matches,
        'unlocked_clusters': unlocked_clusters,
        'current_cluster': current_selected_cluster, # This tells the HTML which one is active
        'active_chat_user': active_chat_user,
        'chat_history': chat_history,
    })

def signup_view(request):
    """Handles new user registration."""
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