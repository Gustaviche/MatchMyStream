import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import film_utils

def mark_as_seen(movie):
    movie_title = movie['Titre']  # On accède directement à la clé 'Titre'

    # Vérification si la liste viewed_movies existe dans st.session_state
    if 'viewed_movies' not in st.session_state:
        st.session_state.viewed_movies = []

    # Vérification si le film est déjà marqué comme vu
    if movie_title in st.session_state.viewed_movies:
        st.session_state.viewed_movies.remove(movie_title)  # Retirer le titre de la liste des films vus
        st.success(f"Vous avez retiré **{movie_title}** de votre liste.")
    else:
        st.session_state.viewed_movies.append(movie_title)  # Ajouter le titre à la liste des films vus
        st.success(f"Vous avez mis **{movie_title}** dans votre liste !")

# Fonction principale
def recommend_movies_keyword(df_movies, query, n_neighbors=10, threshold_distance=0.9, stopwords=None):
    if stopwords is None:
        stopwords = ['le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'd\'', 
                     'en', 'que', 'qui', 'à', 'dans', 'sur', 'pour', 'avec', 
                     'sans', 'est', 'et', 'il', 'elle', 'ils', 'elles', 'nous', 
                     'vous', 'ça', 'ce', 'ces']
    
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    tfidf_movies_matrix = vectorizer.fit_transform(df_movies['text_concat'])
    
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(tfidf_movies_matrix)
    
    query_tfidf_movies = vectorizer.transform([query])
    distances, indices = knn.kneighbors(query_tfidf_movies)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if dist < threshold_distance:
            movie_info = ({
                'Titre': df_movies.iloc[idx]['title_y'],
                'Année de sortie' : df_movies.iloc[idx]['startYear'],
                'Genres': df_movies.iloc[idx]['genres_x'],
                'Réalisateur': df_movies.iloc[idx]['director'],
                'Acteurs': df_movies.iloc[idx]['cast'],
                'Synopsis': df_movies.iloc[idx]['overview'],
                'Distance': dist,
                'Affiche': df_movies.iloc[idx]['poster_path'],
                'Video': df_movies.iloc[idx]['key']
            })
            results.append(movie_info)

    return results

def top_10(df_movies, genre):
    # Initialisation de la liste des résultats
    results = []

    # Filtrer les films en fonction du genre
    if genre:
        filtered_df_movies = df_movies[df_movies['genres_x'].str.contains(genre, case=False, na=False)]
        
        # Trier les films par note moyenne et popularité (en ordre décroissant)
        sorted_df_movies = filtered_df_movies.sort_values(by=['averageRating', 'popularity'], ascending=[False, False])
        
        # Sélectionner les 10 premiers films après tri
        top_10_films = sorted_df_movies.head(10)
        
        # Si des films sont trouvés, les ajouter à la liste des résultats
        for _, movie in top_10_films.iterrows():
                movie_info = {
                    'Titre': movie['title_y'],
                    'Genres': movie['genres_x'],
                    'Année de sortie': movie['startYear'],
                    'Réalisateur': movie['director'],
                    'Acteurs': movie['cast'],
                    'Note moyenne': movie['averageRating'],
                    'Popularité': movie['popularity'],
                    'Affiche': movie['poster_path'],
                    'Synopsis': movie['overview'],
                    'Video' : movie['key']
                }
                results.append(movie_info)

    return results

def afficher_films(results):
    if results:
        #st.write("### Films recommandés :")
        for movie in results:
            # Création de colonnes pour l'affichage
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(movie.get('Titre', 'Titre inconnu'))  # Gérer les titres manquants
            with col2:
                # Bouton pour marquer le film comme vu
                if st.button(f"**Ma Liste**", key=f"btn_{movie.get('Titre', 'film inconnu')}"):
                    film_utils.mark_as_seen(movie)

            # Affichage des détails et médias du film
            col1, col2 = st.columns([1, 2])
            with col1:
                # Affiche ou message si non disponible
                affiche = movie.get('Affiche')
                if affiche:
                    st.image(affiche, caption=movie.get('Titre', 'Sans titre'), use_container_width=True)
                else:
                    st.write("Affiche indisponible")
            with col2:
                # Vidéo ou message d'indisponibilité
                video = movie.get('Video')
                if video:
                    try:
                        st.video(video)
                    except Exception:
                        st.write("Erreur lors de l'affichage de la vidéo")
                else:
                    st.write("Vidéo indisponible")

            # Autres informations sur le film
            st.write(f"**Genres** : {movie.get('Genres', 'Non spécifié')}")
            st.write(f"**Année de sortie** : {movie.get('Année de sortie', 'Inconnue')}")
            st.write(f"**Réalisateur** : {movie.get('Réalisateur', 'Non spécifié')}")
            st.write(f"**Acteurs** : {movie.get('Acteurs', 'Non spécifiés')}")
            st.write(f"**Synopsis** : {movie.get('Synopsis', 'Non disponible')}")

            # Ligne de séparation entre les films
            st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)

# Fonction pour recommander des films par genre
def recommend_movies_genres(df_movies, user_genres, n_neighbors=10, metric='cosine'):
    # 1. Préparation des genres
    mlb = MultiLabelBinarizer()

    # Transformer les genres en colonnes binaires
    genre_features = mlb.fit_transform(df_movies['genres_x'].apply(lambda x: x.split(', ')))  # Assurez-vous de séparer les genres en liste
    genre_columns = mlb.classes_  # Noms des colonnes générées

    # Ajouter les colonnes binaires au DataFrame
    df_movies_genres = pd.DataFrame(genre_features, columns=genre_columns)
    df_movies = pd.concat([df_movies, df_movies_genres], axis=1)

    # 2. Création du modèle KNN
    X_genres = df_movies[genre_columns]
    knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric)
    knn_model.fit(X_genres)

    # 3. Créer le vecteur utilisateur basé sur les genres
    user_vector = [1 if genre in user_genres else 0 for genre in genre_columns]
    user_vector_df_movies = pd.DataFrame([user_vector], columns=genre_columns)

    # 4. Trouver les films les plus proches
    distances, indices = knn_model.kneighbors(user_vector_df_movies)

    # 5. Créer des résultats détaillés sous forme de dictionnaires
    results = []

    for i in range(n_neighbors):
        idx = indices[0][i]  # L'index du film recommandé
        row = df_movies.iloc[idx]  # Le film correspondant à cet index
        movie_info = ({
            'Titre': row['title_y'],
            'Année de sortie' : row['startYear'],
            'Genres': row['genres_x'],
            'Réalisateur': row['director'],
            'Acteurs': row['cast'],
            'Synopsis': row['overview'],
            'Affiche': row['poster_path'],
            'Video': row['key']
        })
        results.append(movie_info)

    return results

def afficher_ma_liste(df_movies):
    if st.session_state.get('viewed_movies', []):  # Vérifie si la clé existe et contient des éléments
        st.write("Voici les films que vous avez vus :")
        
        # Parcours de chaque titre de film dans la liste des films vus
        for movie_title in st.session_state['viewed_movies']:
            # Recherche dans le DataFrame pour obtenir les détails du film
            filtered_movies = df_movies[df_movies['title_y'] == movie_title]
            
            if not filtered_movies.empty:  # Vérification si des résultats existent
                movie = filtered_movies.iloc[0]  # Récupérer la première correspondance
                
                # Utilisation de la mise en page avec 2 colonnes pour plus de clarté
                col1, col2 = st.columns([1, 2])  # Ajuster la proportion des colonnes
                with col1:
                    # Affichage du titre et de l'image
                    if pd.notna(movie['poster_path']):  # Vérification si l'URL existe et n'est pas NaN
                        st.image(movie['poster_path'], caption=movie['title_y'], use_container_width=True)
                    
                with col2:
                    # Affichage des informations supplémentaires du film
                    st.write(f"**Genres :** {movie['genres_x']}")
                    st.write(f"**Réalisateur :** {movie['director']}")
                    st.write(f"**Acteurs :** {movie['cast']}")
                    st.write(f"**Synopsis :** {movie['overview']}")
                    
                    # Bouton pour supprimer le film de la liste
                    if st.button(f"Supprimer {movie['title_y']}", key=f"remove_{movie_title}"):
                        st.session_state['viewed_movies'].remove(movie_title)  # Retirer le film de la liste
                        st.success(f"Le film '{movie_title}' a été supprimé de votre liste.")
                        st.rerun()  # Recharge la page pour afficher la liste mise à jour

                st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)  # Séparation visuelle entre les films
            else:
                st.warning(f"Aucun film trouvé pour le titre : {movie_title}")

    else:
        st.write("Vous n'avez pas mis de films dans votre liste.")
