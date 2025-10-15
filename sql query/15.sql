WITH match_keywords AS (
    SELECT
        matchdesc,
        matchid,
        status,
        -- Determine winning team
        CASE 
            WHEN COALESCE(team1_inngs1_runs,0) + COALESCE(team1_inngs2_runs,0) >
                 COALESCE(team2_inngs1_runs,0) + COALESCE(team2_inngs2_runs,0)
                 THEN team1
            ELSE team2
        END AS winner,
        CASE
            WHEN status ILIKE '%run%' THEN
                CAST(regexp_replace(status, '[^0-9]', '', 'g') AS INTEGER)
            WHEN status ILIKE '%wicket%' THEN
                CAST(regexp_replace(status, '[^0-9]', '', 'g') AS INTEGER)
            ELSE NULL
        END AS margin,
        CASE
            WHEN status ILIKE '%run%' THEN 'runs'
            WHEN status ILIKE '%wicket%' THEN 'wickets'
            ELSE NULL
        END AS margin_type,
        LOWER(regexp_replace(matchdesc, '[^0-9a-z ]', '', 'g')) AS clean_matchdesc
    FROM matchesr
    WHERE status ILIKE '%run%' OR status ILIKE '%wicket%'
),
filtered_close_matches AS (
    SELECT *
    FROM match_keywords
    WHERE (margin_type = 'runs' AND margin < 50)
       OR (margin_type = 'wickets' AND margin < 5)
),
lean_clean AS (
    SELECT
        *,
        LOWER(regexp_replace(match_desc, '[^0-9a-z ]', '', 'g')) AS clean_lean_desc
    FROM matchlean
)
SELECT
    ml.batsman_name,
    COUNT(DISTINCT fcm.matchid) AS total_close_matches,
    ROUND(AVG(CAST(ml.runs AS NUMERIC)), 2) AS avg_runs_in_close,
    SUM(
        CASE 
            WHEN fcm.winner = ml.team1 OR fcm.winner = ml.team2
            THEN 1 ELSE 0 
        END
    ) AS close_matches_won
FROM lean_clean ml
JOIN filtered_close_matches fcm
  ON (
      fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 1) || '%'
      OR fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 2) || '%'
      OR fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 3) || '%'
      OR ml.clean_lean_desc LIKE '%' || SPLIT_PART(fcm.clean_matchdesc, ' ', 1) || '%'
     )
WHERE ml.batsman_name IS NOT NULL
  AND ml.runs IS NOT NULL
GROUP BY ml.batsman_name
HAVING COUNT(DISTINCT fcm.matchid) >= 1
ORDER BY avg_runs_in_close DESC
LIMIT 20;


















