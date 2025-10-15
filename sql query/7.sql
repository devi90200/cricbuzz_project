SELECT 
    CASE 
        WHEN o.match_id IN (48002, 117359, 134832, 134865, 135494) THEN 'T20I'
        WHEN o.match_id IN (122517, 134835, 117360) THEN 'ODI'
        WHEN o.match_id IN (134860, 135500) THEN 'Test'
        ELSE 'Unknown'
    END AS match_format,
    MAX(CAST(o.score AS INTEGER)) AS highest_score
FROM overs o
GROUP BY match_format
ORDER BY highest_score DESC;














    

































