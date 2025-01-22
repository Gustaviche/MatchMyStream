import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def mark_as_seen(serie):
    serie_title = serie['Titre']  # On accède directement à la clé 'Titre'

    # Vérification si la liste viewed_series existe dans st.session_state
    if 'viewed_series' not in st.session_state:
        st.session_state.viewed_series = []

    # Vérification si le film est déjà marqué comme vu
    if serie_title in st.session_state.viewed_series:
        st.session_state.viewed_series.remove(serie_title)  # Retirer le titre de la liste des films vus
        st.success(f"La série **{serie_title}** a été retiré de votre liste.")
    else:
        st.session_state.viewed_series.append(serie_title)  # Ajouter le titre à la liste des films vus
        st.success(f"Vous avez mis la série **{serie_title}** dans votre liste !")

# Fonction principale
def recommend_series_keyword(df_series, query, n_neighbors=10, threshold_distance=0.9, stopwords=None):
    if stopwords is None:
        stopwords = ['le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'd\'', 
                     'en', 'que', 'qui', 'à', 'dans', 'sur', 'pour', 'avec', 
                     'sans', 'est', 'et', 'il', 'elle', 'ils', 'elles', 'nous', 
                     'vous', 'ça', 'ce', 'ces']
    
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    tfidf_series_matrix = vectorizer.fit_transform(df_series['lemmatized_text'])
    
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(tfidf_series_matrix)
    
    query_tfidf_series = vectorizer.transform([query])
    distances, indices = knn.kneighbors(query_tfidf_series)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if dist < threshold_distance:
            serie_info = ({
                'Titre': df_series.iloc[idx]['name'],
                'Année de sortie' : df_series.iloc[idx]['startYear'],
                'Genres': df_series.iloc[idx]['genres'],
                'Réalisateur': df_series.iloc[idx]['creators'],
                'Acteurs': df_series.iloc[idx]['cast'],
                'Synopsis': df_series.iloc[idx]['overview'],
                'Distance': dist,
                'Affiche': df_series.iloc[idx]['poster_path'],
                'Video': df_series.iloc[idx]['key']
            })
            results.append(serie_info)

    return results

def top_10(df_series, genre):
    # Initialisation de la liste des résultats
    results = []

    # Filtrer les films en fonction du genre
    if genre:
        filtered_df_series = df_series[df_series['genres'].str.contains(genre, case=False, na=False)]
        
        # Trier les films par note moyenne et popularité (en ordre décroissant)
        sorted_df_series = filtered_df_series.sort_values(by=['popularity', 'averageRating'], ascending=[False, False])
        
        # Sélectionner les 10 premiers films après tri
        top_10_films = sorted_df_series.head(10)
        
        # Si des films sont trouvés, les ajouter à la liste des résultats
        for _, serie in top_10_films.iterrows():
                serie_info = {
                    'Titre': serie['name'],
                    'Genres': serie['genres'],
                    'Année de sortie': serie['startYear'],
                    'Réalisateur': serie['creators'],
                    'Acteurs': serie['cast'],
                    'Note moyenne': serie['averageRating'],
                    'Popularité': serie['popularity'],
                    'Affiche': serie['poster_path'],
                    'Synopsis': serie['overview'],
                    'Video' : serie['key']
                }
                results.append(serie_info)

    return results

# Fonction pour recommander des films par genre
def recommend_series_genres(df_series, user_genres, n_neighbors=10, metric='cosine'):
    # 1. Préparation des genres
    mlb = MultiLabelBinarizer()

    # Transformer les genres en colonnes binaires
    genre_features = mlb.fit_transform(df_series['genres'].apply(lambda x: x.split(', ')))  # Assurez-vous de séparer les genres en liste
    genre_columns = mlb.classes_  # Noms des colonnes générées

    # Ajouter les colonnes binaires au DataFrame
    df_series_genres = pd.DataFrame(genre_features, columns=genre_columns)
    df_series = pd.concat([df_series, df_series_genres], axis=1)

    # 2. Création du modèle KNN
    X_genres = df_series[genre_columns]
    knn_model = NearestNeighbors(n_neighbors=n_neighbors, metric=metric)
    knn_model.fit(X_genres)

    # 3. Créer le vecteur utilisateur basé sur les genres
    user_vector = [1 if genre in user_genres else 0 for genre in genre_columns]
    user_vector_df_series = pd.DataFrame([user_vector], columns=genre_columns)

    # 4. Trouver les films les plus proches
    distances, indices = knn_model.kneighbors(user_vector_df_series)

    # 5. Créer des résultats détaillés sous forme de dictionnaires
    results = []

    for i in range(n_neighbors):
        idx = indices[0][i]  # L'index du film recommandé
        row = df_series.iloc[idx]  # Le film correspondant à cet index
        serie_info = ({
            'Titre': row['name'],
            'Année de sortie' : row['startYear'],
            'Genres': row['genres'],
            'Réalisateur': row['creators'],
            'Acteurs': row['cast'],
            'Synopsis': row['overview'],
            'Affiche': row['poster_path'],
            'Video': row['key']
        })
        results.append(serie_info)

    return results

def afficher_series(results):
    if results:
        # Pour chaque série dans les résultats
        for series in results:
            # Création de colonnes pour l'affichage
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(series.get('Titre', 'Titre inconnu'))  # Gérer les titres manquants

            with col2:
                # Utilisation de l'id et du titre pour générer une clé unique
                titre = series.get('Titre', 'Titre inconnu')
                identifiant = series.get('id', 'unknown')  # Utiliser l'identifiant unique
                key = f"btn_{titre}_{identifiant}"  # Générer une clé unique avec titre et id
                
                if st.button(f"**Ajouter à ma liste**", key=key):
                    mark_as_seen(series)

            # Affichage des détails et médias du film
            col1, col2 = st.columns([1, 2])
            with col1:
                # Affiche ou message si non disponible
                affiche = series.get('Affiche')
                if affiche:
                    st.image(affiche, caption=series.get('Titre', 'Sans titre'), use_container_width=True)
                else:
                    st.write("Affiche indisponible")
            with col2:
                # Vidéo ou message d'indisponibilité
                video = series.get('Video')
                if video:
                    try:
                        st.video(video)
                    except Exception:
                        st.write("Erreur lors de l'affichage de la vidéo")
                else:
                    st.write("Vidéo indisponible")

            # Autres informations sur le film
            st.write(f"**Genres** : {series.get('Genres', 'Non spécifié')}")
            st.write(f"**Année de sortie** : {series.get('Année de sortie', 'Inconnue')}")
            st.write(f"**Réalisateur** : {series.get('Réalisateur', 'Non spécifié')}")
            st.write(f"**Acteurs** : {series.get('Acteurs', 'Non spécifiés')}")
            st.write(f"**Synopsis** : {series.get('Synopsis', 'Non disponible')}")

            # Ligne de séparation entre les films
            st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)

def afficher_ma_liste(df_series):
    if st.session_state.get('viewed_series', []):  # Vérifie si la clé existe et contient des éléments
        st.write("Voici les séries que vous avez vues :")
        
        for serie_title in st.session_state['viewed_series']:
            # Recherche dans le DataFrame
            filtered_series = df_series[df_series['name'] == serie_title]
            
            if not filtered_series.empty:  # Vérification si des résultats existent
                serie = filtered_series.iloc[0]  # Récupérer la première correspondance

                # Mise en page avec deux colonnes
                col1, col2 = st.columns([1, 2])
                with col1:
                    if pd.notna(serie['poster_path']):  # Vérification si l'URL existe et n'est pas NaN
                        st.image(serie['poster_path'], caption=serie['name'], use_container_width=True)
                with col2:
                    st.write(f"**Genres :** {serie['genres']}")
                    st.write(f"**Créateurs :** {serie['creators']}")
                    st.write(f"**Acteurs :** {serie['cast']}")
                    st.write(f"**Synopsis :** {serie['overview']}")

                    # Bouton pour supprimer la série de la liste
                    if st.button(f"Supprimer {serie['name']}", key=f"remove_{serie_title}"):
                        st.session_state['viewed_series'].remove(serie_title)  # Retirer la série
                        st.success(f"La série '{serie_title}' a été supprimée de votre liste.")
                        st.rerun()  # Recharge la page pour mettre à jour
            else:
                st.warning(f"Aucune série trouvée pour le titre : {serie_title}")

            st.markdown("<hr style='border: 2px solid #f08080;'>", unsafe_allow_html=True)
    else:
        st.write("Vous n'avez pas mis de séries dans votre liste.")
