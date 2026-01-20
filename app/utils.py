import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from .models import Location

def get_recommendations(user_input, k=4):
    queryset = Location.objects.all()
    
    if queryset.count() < k:
        return queryset, 0 

    # Convert to DataFrame
    df = pd.DataFrame(list(queryset.values(
        'id', 'nature_score', 'adventure_score', 'culture_score', 'altitude_score'
    )))
    
    features = ['nature_score', 'adventure_score', 'culture_score', 'altitude_score']
    
    # Scale and Cluster
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    
    # Predict User's Cluster
    user_input_array = np.array(user_input).reshape(1, -1)
    scaled_user = scaler.transform(user_input_array)
    predicted_cluster = kmeans.predict(scaled_user)[0]
    
    # Filter unique IDs
    recommended_ids = df[df['cluster'] == predicted_cluster]['id'].tolist()
    
    # .distinct() ensures Pokhara won't repeat!
    recommendations = Location.objects.filter(id__in=recommended_ids).distinct()[:6]
    
    return recommendations, predicted_cluster