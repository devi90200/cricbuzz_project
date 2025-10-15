WITH lean_clean AS (
    SELECT
        batsman_name,
        runs::NUMERIC AS runs,
        strike_rate::NUMERIC AS strike_rate,
        LOWER(regexp_replace(match_desc, '[^0-9a-z ]', '', 'g')) AS clean_match_desc
    FROM matchlean
    WHERE batsman_name IS NOT NULL AND runs IS NOT NULL
),
venue_clean AS (
    SELECT
        matchid,
        LOWER(regexp_replace(matchdesc, '[^0-9a-z ]', '', 'g')) AS clean_matchdesc,
        startdate
    FROM venuematches
    WHERE startdate IS NOT NULL
),
match_with_year AS (
    SELECT
        lc.batsman_name,
        lc.runs,
        lc.strike_rate,
        EXTRACT(YEAR FROM TO_TIMESTAMP(CAST(vc.startdate AS BIGINT)/1000)) AS year
    FROM lean_clean lc
    JOIN venue_clean vc
      ON lc.clean_match_desc LIKE '%' || SPLIT_PART(vc.clean_matchdesc, ' ', 1) || '%'
         OR vc.clean_matchdesc LIKE '%' || SPLIT_PART(lc.clean_match_desc, ' ', 1) || '%'
    WHERE TO_TIMESTAMP(CAST(vc.startdate AS BIGINT)/1000) >= DATE '2020-01-01'
)
SELECT
    batsman_name,
    year,
    ROUND(AVG(runs), 2) AS avg_runs,
    ROUND(AVG(strike_rate), 2) AS avg_strike_rate,
    COUNT(*) AS matches_played
FROM match_with_year
GROUP BY batsman_name, year
HAVING COUNT(*) >= 1
ORDER BY batsman_name, year;
















