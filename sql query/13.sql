WITH batsmen_pairs AS (
    SELECT
        o.match_id,
        o."inning",
        unnest(string_to_array(o.batsmen, ', ')) AS batsman,
        o.over AS over_num,
        o.runs::int AS runs
    FROM overs o
),
batting_positions AS (
    SELECT
        match_id,
        "inning",
        batsman,
        ROW_NUMBER() OVER (PARTITION BY match_id, "inning" ORDER BY MIN(over_num)) AS position,
        SUM(runs) AS total_runs
    FROM batsmen_pairs
    GROUP BY match_id, "inning", batsman
),
partnerships AS (
    SELECT
        b1.match_id,
        b1."inning",
        b1.batsman AS batsman1,
        b2.batsman AS batsman2,
        (b1.total_runs + b2.total_runs) AS partnership_runs
    FROM  batting_positions b1
    JOIN batting_positions b2
      ON b1.match_id = b2.match_id
     AND b1."inning" = b2."inning"
     AND b2.position = b1.position + 1
)
SELECT *
FROM partnerships
WHERE partnership_runs >= 100
ORDER BY match_id, "inning", partnership_runs DESC;










