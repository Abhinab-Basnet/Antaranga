import random
import numpy as np
from .models import Location

def euclidean_distance(a, b):
    """Compute Euclidean distance between two points"""
    return np.linalg.norm(np.array(a) - np.array(b))

def kmeans_manual(data, k=4, max_iter=100):
    #  Randomly initialize k centroids
    centroids = random.sample(data, k)
    for iteration in range(max_iter):
        clusters = [[] for _ in range(k)]
        #  Assign each point to nearest centroid
        for point in data:
            distances = [euclidean_distance(point, c) for c in centroids]
            cluster_idx = distances.index(min(distances))
            clusters[cluster_idx].append(point)
        #  Recompute centroids
        new_centroids = []
        for cluster_points in clusters:
            if cluster_points:
                cluster_mean = np.mean(cluster_points, axis=0).tolist()
            else:
                # If cluster empty, pick a random point as centroid
                cluster_mean = random.choice(data)
            new_centroids.append(cluster_mean)
        #  Check for convergence
        if np.allclose(new_centroids, centroids):
            break
        centroids = new_centroids
    #  Final assignment
    final_assignments = []
    for point in data:
        distances = [euclidean_distance(point, c) for c in centroids]
        cluster_idx = distances.index(min(distances))
        final_assignments.append(cluster_idx)
    return final_assignments, centroids


def get_recommendations(user_input, k=4):

    #  Fetch all locations
    queryset = Location.objects.all()
    if queryset.count() < k:
        return None, None

    #  Convert DB data to list
    data_points = []
    ids = []
    for loc in queryset:
        data_points.append([
            loc.nature_score,
            loc.adventure_score,
            loc.culture_score,
            loc.altitude_score
        ])
        ids.append(loc.id)

    #  Apply manual K-Means
    cluster_assignments, centroids = kmeans_manual(data_points, k=k)

    #  Save cluster_id to DB
    for loc_id, cluster_id in zip(ids, cluster_assignments):
        Location.objects.filter(id=loc_id).update(cluster_id=int(cluster_id))

    # Predict user cluster
    distances_to_centroids = [euclidean_distance(user_input, c) for c in centroids]
    predicted_cluster = distances_to_centroids.index(min(distances_to_centroids))

    #  Compute distance to user input for ranking
    distance_to_user = [euclidean_distance(user_input, point) for point in data_points]

    #  Filter locations in predicted cluster
    cluster_indices = [i for i, c in enumerate(cluster_assignments) if c == predicted_cluster]
    ordered_cluster = sorted(cluster_indices, key=lambda i: distance_to_user[i])
    ordered_ids = [ids[i] for i in ordered_cluster]

    results = list(Location.objects.filter(id__in=ordered_ids))
    results.sort(key=lambda x: ordered_ids.index(x.id))

    #  Fallback if cluster empty
    if not results:
        nearest_indices = sorted(range(len(distance_to_user)), key=lambda i: distance_to_user[i])[:5]
        nearest_ids = [ids[i] for i in nearest_indices]
        results = list(Location.objects.filter(id__in=nearest_ids))
        results.sort(key=lambda x: nearest_ids.index(x.id))
        predicted_cluster = "Nearest Match"

    return results, predicted_cluster
