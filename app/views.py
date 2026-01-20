from django.shortcuts import render, redirect
from .utils import get_recommendations
from .models import Location 

# 1. ADD THIS BACK: Landing Page View
def home(request):
    """Renders the main Antaranga landing page."""
    return render(request, 'app/index.html')

# 2. ADD THIS BACK: Survey Form View
def survey(request):
    """Renders the survey page."""
    return render(request, 'app/survey.html')

# 3. K-Means Logic & Results View
def recommend(request):
    """Processes survey data and returns clustered recommendations."""
    if request.method == "POST":
        try:
            # 1. Aggregate the slider data
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
            
            # 2. Get recommendations from K-Means
            recommendations, cluster_id = get_recommendations(user_input)
            
            # 3. THE IMAGE MAP
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

            # 4. Attach image paths to the results
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