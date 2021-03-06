from math import sqrt
import sys
import numpy as np

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones":4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":     {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan":     {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Dan":      {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey":   {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":   {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam":      {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Stroker": 3.0}}

def compute_manhattan_distance(rating1, rating2):
    return compute_minkowski_distance(rating1, rating2, 1)

def compute_euclidean_distance(rating1, rating2):
    return compute_minkowski_distance(rating1, rating2, 2)

def compute_minkowski_distance(rating1, rating2, r=2):
    dist = 0.0
    has_common_rating = False
    for key in rating1:
        if key in rating2:
            has_common_rating = True
            dist += pow(abs(rating1[key]-rating2[key]), r)
    return pow(dist, 1/r) if has_common_rating else sys.maxsize

def compute_user_distance(username, users):
    distances = []
    for user in users:
        if user == username: continue

        dist = compute_manhattan_distance(users[user], users[username])
        distances.append((user, dist))
    return distances

def compute_nearest_neighbor(username, users):
    min_dist, nearest_user = sys.maxsize, ""
    for user in users:
        if user == username: continue

        dist = compute_manhattan_distance(users[user], users[username])
        if dist < min_dist:
            min_dist, nearest_user = dist, user
    return nearest_user

def recommend(username, users):
    nearest_user = compute_nearest_neighbor(username, users)
    if nearest_user == "": return ""

    recommendations = []
    for (filmname, rating) in users[nearest_user].items():
        if filmname not in users[username]:
            recommendations.append((filmname, rating))
    return sorted(recommendations, key=lambda entry: entry[1], reverse=True)

def cosine_similarity(rating1, rating2):
    denominator = np.sqrt(np.sum(np.square(rating1))) * np.sqrt(np.sum(np.square(rating2)))
    nominator = np.sum(x*y for (x,y) in zip(rating1, rating2))
    return nominator / denominator

def pearson_correlation_coefficient(rating1, rating2):
    x_mean, y_mean = np.mean(rating1), np.mean(rating2)
    nominator = np.sum((x-x_mean)*(y-y_mean) for (x,y) in zip(rating1, rating2))
    denominator = np.sqrt(np.sum(np.square(rating1-x_mean))) * np.sqrt(np.sum(np.square(rating2-y_mean)))
    return nominator, denominator, nominator / denominator

def k_nearest_neighbors(username, users, k=1):
    distances = compute_user_distance(username, users)
    return sorted(distances, key=lambda entry: entry[1])[:k]

def recommend_by_k_nearest_neighbor(username, users, k=1):
    distances = compute_user_distance(username, users)
    recommendations = {}
    total_dist = 0.0
    for i in range(k):
        total_dist = total_dist + distances[i][1]
    for i in range(k):
        user, score = distances[i][0], distances[i][1]
        rectified_score = score/total_dist
        for film in users[user]:
            if not film in users[username]:
                if film not in recommendations:
                    recommendations[film] = rectified_score
                else:
                    recommendations[film] += rectified_score
    return recommendations

# Test
print(compute_manhattan_distance(users["Dan"], users["Hailey"]))
print(compute_euclidean_distance(users["Dan"], users["Hailey"]))
print(compute_user_distance("Dan", users))
print(compute_nearest_neighbor("Dan", users))
print(recommend("Dan", users))

print(cosine_similarity([1,2,3], [4,5,6]))
print(pearson_correlation_coefficient([1,2,3], [4,5,6]))
print(k_nearest_neighbors("Dan", users, 10))
print(recommend_by_k_nearest_neighbor("Dan", users, 5))
