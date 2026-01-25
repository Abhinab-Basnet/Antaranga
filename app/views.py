from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import get_recommendations
from .models import Location 
from .data import DESTINATIONS  # The file we perfected earlier

# 1. Landing Page View
def home(request):
    """Renders the main Antaranga landing page."""
    return render(request, 'app/index.html')

# 2. Survey Form View
def survey(request):
    """Renders the survey page."""
    return render(request, 'app/survey.html')

# 3. Destination Detail View (THE ORACLE PAGE)
def detail(request, destination_slug):
    """
    Renders the specialized big orange typography page.
    It fetches data from the hardcoded DESTINATIONS dictionary 
    using a slug (e.g., 'pokharalakeside').
    """
    place = DESTINATIONS.get(destination_slug)
    if not place:
        # Fallback if slug isn't in data.py
        return render(request, '404.html', status=404)
        
    return render(request, 'app/detail.html', {'place': place})

# 4. K-Means Logic & Results View
@login_required
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
                'Everest Base Camp': 'app/assets/images/ebc_hero.jpg',
                'Pokhara (Lakeside)': 'app/assets/images/annapurna.jpg',
                'Bandipur Village': 'app/assets/images/bandipur_hero.jpg',
                'Ilam (Tea Gardens)': 'app/assets/images/ilam_hero.jpg',
                # ... add others as needed
            }

            # Link Results to Slugs for the Detail Page
            slug_map = {
                'Everest Base Camp': 'everestbasecamp',
                'Pokhara (Lakeside)': 'pokharalakeside',
                'Bandipur Village': 'bandipur-village',
                'Ilam (Tea Gardens)': 'ilam-tea-gardens',
            }

            for loc in recommendations:
                loc.manual_image = image_map.get(loc.name, 'app/assets/images/default.jpg')
                # We attach the slug so the 'View Details' button knows where to go
                loc.target_slug = slug_map.get(loc.name, '#')
            
            return render(request, 'app/results.html', {
                'locations': recommendations,
                'cluster': cluster_id
            })

        except Exception as e:
            print(f"Error in recommendation logic: {e}")
            return redirect('survey')
    
    return redirect('survey')