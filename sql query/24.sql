WITH split_batsmen AS (
    -- Step 1: Split comma-separated batsmen into individual rows
    SELECT
        match_id,
        inning,
        unnest(string_to_array(batsmen, ', ')) AS batsman,
        runs
    FROM overs
),
partnership_pairs AS (
    -- Step 2: Get consecutive batsmen per match + inning
    SELECT
        match_id,
        inning,
        batsman AS batsman1,
        LEAD(batsman) OVER (
            PARTITION BY match_id, inning
            ORDER BY match_id, inning
        ) AS batsman2,
        runs
    FROM split_batsmen
),
partnership_runs_per_inning AS (
    -- Step 3: Sum runs for each partnership in a given match + inning
    SELECT
        match_id,
        inning,
        batsman1,
        batsman2,
        SUM(runs) AS partnership_runs
    FROM partnership_pairs
    WHERE batsman2 IS NOT NULL
    GROUP BY match_id, inning, batsman1, batsman2
),
partnership_summary AS (
    -- Step 4: Aggregate per pair across all innings/matches
    SELECT
        batsman1,
        batsman2,
        COUNT(*) AS total_partnerships,
        ROUND(AVG(partnership_runs)::numeric, 2) AS avg_partnership_runs,
        MAX(partnership_runs) AS highest_partnership,
        SUM(CASE WHEN partnership_runs >= 20 THEN 1 ELSE 0 END) AS good_partnerships
    FROM partnership_runs_per_inning
    GROUP BY batsman1, batsman2
)
-- Step 5: Calculate success rate rounded to 2 decimals
SELECT
    batsman1,
    batsman2,
    total_partnerships,
    avg_partnership_runs,
    highest_partnership,
    good_partnerships,
    ROUND((good_partnerships::float / total_partnerships * 100)::numeric, 2) AS success_rate
FROM partnership_summary
ORDER BY success_rate DESC, avg_partnership_runs DESC
LIMIT 20;














































