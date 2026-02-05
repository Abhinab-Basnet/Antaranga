import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from .models import Location

def get_recommendations(user_input, k=4):
    """
    user_input = [nature, adventure, culture, altitude]
    """
    
    queryset = Location.objects.all()
    if queryset.count() < k:
        return None, None

    
    df = pd.DataFrame(list(queryset.values(
        'id', 'nature_score', 'adventure_score', 'culture_score', 'altitude_score'
    )))
    
    features = ['nature_score', 'adventure_score', 'culture_score', 'altitude_score']
    
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    
    
    for _, row in df.iterrows():
        Location.objects.filter(id=row['id']).update(cluster_id=row['cluster'])
    
    
    scaled_user = scaler.transform([user_input])
    predicted_cluster = kmeans.predict(scaled_user)[0]
    
    
    return Location.objects.filter(cluster_id=predicted_cluster), predicted_cluster