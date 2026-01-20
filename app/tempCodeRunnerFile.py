import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from .models import Location

def get_recommendations(user_input, k=4):
    """
    user_input = [nature, adventure, culture, altitude]
    """
    # 1. Fetch data from your MySQL 'locations' table
    queryset = Location.objects.all()
    if queryset.count() < k:
        return None, None

    # 2. Convert SQL rows into a Pandas DataFrame
    df = pd.DataFrame(list(queryset.values(
        'id', 'nature_score', 'adventure_score', 'culture_score', 'altitude_score'
    )))
    
    features = ['nature_score', 'adventure_score', 'culture_score', 'altitude_score']
    
    # 3. Normalize the data (Important: Scale 1-10 scores so they have equal weight)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    # 4. Apply K-Means Clustering
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    
    # 5. Save the results back to MySQL cluster_id column
    for _, row in df.iterrows():
        Location.objects.filter(id=row['id']).update(cluster_id=row['cluster'])
    
    # 6. Take user's preference and find their matching cluster
    scaled_user = scaler.transform([user_input])
    predicted_cluster = kmeans.predict(scaled_user)[0]
    
    # Return all locations in the same cluster as the user
    return Location.objects.filter(cluster_id=predicted_cluster), predicted_cluster