WITH match_winners AS (
    SELECT
        matchid,
        toss_winner,
        toss_decision,
        split_part(status, ' won', 1) AS winner
    FROM matcheslive
    WHERE toss_winner IS NOT NULL
      AND toss_decision IS NOT NULL
      AND status IS NOT NULL
)
SELECT
    toss_winner AS team,
    toss_decision,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_wins,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS toss_win_percentage
FROM match_winners
GROUP BY toss_winner, toss_decision
ORDER BY toss_win_percentage DESC;



















