SELECT
    user_id,
    movie_id,
    COUNT(*) AS nb_notes
FROM {{ ref('recommandation_prete') }}
GROUP BY user_id, movie_id
HAVING COUNT(*) > 1