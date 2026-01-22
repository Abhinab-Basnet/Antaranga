from django.shortcuts import render, redirect, Http404
from .utils import get_recommendations
from .models import Location 
from .data import DESTINATIONS  # Import the new dictionary from data.py

# 1. Landing Page View
def home(request):
    """Renders the main Antaranga landing page."""
    return render(request, 'app/index.html')

# 2. Survey Form View
def survey(request):
    """Renders the survey page."""
    return render(request, 'app/survey.html')

# 3. K-Means Logic & Results View
def recommend(request):
    """Processes survey data and returns clustered recommendations."""
    if request.method == "POST":
        try:
            # Aggregate the slider data
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
            
            # Get recommendations from K-Means
            recommendations, cluster_id = get_recommendations(user_input)
            
            # Image Map (Matches the names in your Database/Model)
            image_map = {
                'Everest Base Camp': 'app/assets/images/ebc.jpg',
                'Pokhara (Lakeside)': 'app/assets/images/rara.jpeg',
                'Kathmandu Durbar Square': 'app/assets/images/kds.jpeg',
                'Chitwan National Park': 'app/assets/images/chitwan.jpeg',
                'Lumbini (Birthplace of Buddha)': 'app/assets/images/lumbini.jpg',
                'Annapurna Base Camp': 'app/assets/images/annapurna.jpg',
                'Bhaktapur Durbar Square': 'app/assets/images/bds.jpeg',
                'Nagarkot (Sunrise View)': 'app/assets/images/nagarkot.jpeg',
                'Rara Lake': 'app/assets/images/rara.jpeg',
                'Muktinath Temple': 'app/assets/images/kds.jpg',
                'Ghorepani Poon Hill': 'app/assets/images/poon.jpeg',
                'Janakpur (Janaki Temple)': 'app/assets/images/janaki.jpeg',
                'Bandipur Village': 'app/assets/images/bandipur.jpeg',
                'Langtang Valley': 'app/assets/images/langtang.jpeg',
                'Manaslu Circuit': 'app/assets/images/manaslucircuit.jpeg',
                'Ilam (Tea Gardens)': 'app/assets/images/ilam.jpeg',
                'Upper Mustang (Lo Manthang)': 'app/assets/images/mustang.jpeg',
                'Gosaikunda Lake': 'app/assets/images/gosaikunda.jpeg',
                'Patan Durbar Square': 'app/assets/images/pds.jpeg',
                'Bardia National Park': 'app/assets/images/bardiya.jpeg',
            }

            # Attach image paths to the results
            for loc in recommendations:
                loc.manual_image = image_map.get(loc.name, 'app/assets/images/default.jpg')
            
            return render(request, 'app/results.html', {
                'locations': recommendations,
                'cluster': cluster_id
            })

        except Exception as e:
            print(f"Error in recommendation logic: {e}")
            return redirect('survey')
    
    return redirect('survey')

# 4. NEW: Destination Detail View
def destination_detail(request, place_slug):
    """Fetches detailed info from data.py based on the URL slug."""
    
    # We clean the slug (e.g., 'mount-everest' -> 'mounteverest') 
    # to match the keys in your data.py
    clean_key = place_slug.lower().replace('-', '')
    
    # Fetch from the DESTINATIONS dictionary in data.py
    place = DESTINATIONS.get(clean_key)
    
    if not place:
        # If the place is not in your data.py yet, you can show a 404 or a fallback
        raise Http404("This soul sanctuary is still being mapped by the Oracle.")
        
    return render(request, 'app/detail.html', {'place': place})