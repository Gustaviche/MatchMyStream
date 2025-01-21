## MatchMyStream

MatchMyStream est une application interactive permettant aux utilisateurs de découvrir et de gérer leurs films et séries préférés. Grâce à l'intégration de l'API TMDB, et des datasets du site IMDB, l'application permet de récupérer des informations sur les films et les séries, d'afficher des recommandations personnalisées et de gérer une liste de contenus déjà vus. Les utilisateurs peuvent également consulter des informations détaillées, telles que les genres, acteurs, réalisateurs, et bien plus encore.

# Fonctionnalités principales
* Recherche de films et séries : Trouvez vos films et séries préférés via une interface intuitive.
* Affichage des détails : Consultez les informations détaillées telles que les genres, réalisateurs, acteurs, synopsis, et affiches.
* Liste personnalisée : Ajoutez des films et des séries à votre liste des contenus vus et gérez-les facilement.
* Recommandations intelligentes : Découvrez des films et séries similaires à ceux que vous avez déjà appréciés.

# Structure du projet

Voici une vue d'ensemble des fichiers et dossiers principaux de ce projet :

MatchMyStream/
├── app.py                 # Point d'entrée de l'application Streamlit
├── film_utils.py          # Fonctions utilitaires liées aux films
├── series_utils.py        # Fonctions utilitaires liées aux séries
├── requirements.txt       # Liste des dépendances
├── config.py              # Configuration de l'API (ex: clé API TMDB)
├── poster_film.jpg        # Fond pour les films
├── poster_series.jpg      # Fond pour les séries
└── README.md              # Ce fichier

# Technologies utilisées
* Streamlit : Framework pour la création rapide d'applications interactives.
* Pandas : Librairie pour la manipulation des données.
* Requests : Utilisée pour interagir avec l'API TMDB.
* TMDB API : Source de données pour les films et séries.
* Python 3.x : Langage de programmation utilisé pour le développement.

Ce projet est sous licence MIT.


