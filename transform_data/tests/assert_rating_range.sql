SELECT
    user_id,
    movie_id,
    rating
FROM {{ ref('recommandation_prete') }}
WHERE rating < 0.5 OR rating > 5.0