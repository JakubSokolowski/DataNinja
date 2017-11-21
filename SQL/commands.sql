/*Selects all the different categories and the ad count of each category*/

SELECT categories.name,
       count(ads.category_id) AS counter
  FROM ads
       JOIN
       categories ON ads.category_id = categories.category_id
 GROUP BY categories.name
 ORDER BY counter DESC;

/* Selects all the adds from category and its children */
WITH RECURSIVE cte (
    category_id,
    name,
    parent_id
)
AS (
    SELECT category_id,
           name,
           parent_id
      FROM categories
     WHERE name = 'Dla Dzieci'
    UNION ALL
    SELECT p.category_id,
           p.name,
           p.parent_id
      FROM categories p
           INNER JOIN
           cte ON p.parent_id = cte.category_id
)
SELECT id,
       full_description
  FROM ads
 WHERE category_id IN (
           SELECT category_id
             FROM cte
       );