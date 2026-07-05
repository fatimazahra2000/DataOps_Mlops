{{ config(materialized='table') }}

SELECT
    r.user_id,
    r.movie_id,
    m.title,
    r.rating,
    m.genres
FROM {{ source('movielens_brut', 'ratings') }} r
JOIN {{ source('movielens_brut', 'movies') }} m ON r.movie_id = m.movie_id