last_video_seen = """with ordered_videos AS (
  SELECT
    i.course_branch_item_name as name,
    ROW_NUMBER() OVER (
  --    PARTITION BY m.course_module_id
  --    ORDER BY course_branch_module_order, course_branch_lesson_order, course_branch_item_order
        ORDER BY course_branch_module_order, course_branch_lesson_order, course_branch_item_order
    ) as ord 
  FROM course_branch_items i
      JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
      JOIN course_branch_modules m USING (course_module_id, course_branch_id)
  WHERE course_branch_id = %s
    AND m.course_module_id = %s
    AND i.course_item_type_id=1
),
video_progress AS (
  SELECT i.course_item_id, p.penn_user_id, course_branch_item_name, course_branch_item_order, p.course_progress_ts
  --from active_users a
  --join course_progress p
  --  using (penn_user_id)
  FROM course_progress p
    JOIN course_progress_state_types USING (course_progress_state_type_id)
    JOIN course_branch_items i USING (course_item_id)
    JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
    JOIN course_branch_modules m USING (course_module_id, course_branch_id)
  WHERE course_branch_id = %s
    AND m.course_module_id = %s
    AND i.course_item_type_id=1
    AND course_progress_state_type_desc = 'started'
    and p.course_progress_ts > %s and p.course_progress_ts < %s
)
, user_last AS (
  SELECT penn_user_id, MAX(p.course_progress_ts) as ts
  FROM video_progress p
  GROUP BY 1
 ),
user_last_name AS (
  SELECT v.penn_user_id, course_branch_item_name AS NAME
  FROM video_progress v
  JOIN user_last on v.penn_user_id=user_last.penn_user_id AND v.course_progress_ts = user_last.ts
),
counts AS (
SELECT ord, NAME AS video, COUNT(penn_user_id) AS last_seen
FROM ordered_videos LEFT JOIN user_last_name USING (NAME)
GROUP BY 1,2
)
SELECT video, last_seen FROM counts ORDER BY ord;
"""

watched = """WITH ordered_videos AS (
      SELECT
        i.course_branch_item_name AS NAME,
        ROW_NUMBER() OVER (
      --    PARTITION BY m.course_module_id
            ORDER BY course_branch_module_order, course_branch_lesson_order, course_branch_item_order
        ) AS ord 
      FROM course_branch_items i
          JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
          JOIN course_branch_modules m USING (course_module_id, course_branch_id)
      WHERE course_branch_id = %s
        AND m.course_module_id = %s
        AND i.course_item_type_id=1 -- video
    ),
    counts AS (
    SELECT ord, name as video, COUNT(distinct penn_user_id) AS watched
    FROM ordered_videos ov
    LEFT JOIN course_branch_items i ON i.course_branch_item_name = ov.name
    JOIN course_progress p USING (course_item_id) 
    JOIN course_progress_state_types
      USING (course_progress_state_type_id)
      JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
      JOIN course_branch_modules m USING (course_module_id, course_branch_id)
    WHERE course_branch_id = %s
      AND m.course_module_id = %s
      AND i.course_item_type_id=1 -- video
      AND course_progress_state_type_desc = 'started'
      AND p.course_progress_ts > %s AND p.course_progress_ts < %s
    GROUP BY 1, 2
    ORDER BY ord
  )
  SELECT video, watched FROM counts ORDER BY ord;

    """

active_users_enrolled = """WITH active_users AS (
  SELECT DISTINCT penn_user_id FROM on_demand_session_memberships 
    JOIN course_progress p USING (penn_user_id)
    JOIN course_branch_items i USING (course_item_id)
    JOIN course_progress_state_types USING (course_progress_state_type_id)
  WHERE on_demand_session_id= %s AND i.course_branch_id = %s AND i.course_item_type_id=1
    AND course_progress_state_type_desc = 'started' AND p.course_progress_ts > %s AND
    p.course_progress_ts < %s
)
SELECT COUNT(*) FROM active_users;
"""

active_users_time = """with u as (
SELECT distinct penn_user_id
FROM course_progress p
JOIN course_progress_state_types
  USING (course_progress_state_type_id)
JOIN course_branch_items i using (course_item_id)
JOIN course_branch_lessons l using (course_lesson_id, course_branch_id)
JOIN course_branch_modules m using (course_module_id, course_branch_id)
WHERE course_branch_id = %s
  AND i.course_item_type_id=1
  AND course_progress_state_type_desc = 'started'
  AND p.course_progress_ts > %s and p.course_progress_ts < %s
)
select count(distinct penn_user_id) from u;
"""

active_users_module = """with u as (
SELECT distinct penn_user_id
FROM course_progress p
JOIN course_progress_state_types
  USING (course_progress_state_type_id)
JOIN course_branch_items i using (course_item_id)
JOIN course_branch_lessons l using (course_lesson_id, course_branch_id)
JOIN course_branch_modules m using (course_module_id, course_branch_id)
WHERE course_branch_id = %s
  AND m.course_module_id = %s
  AND i.course_item_type_id=1
  AND course_progress_state_type_desc = 'started'
  AND p.course_progress_ts > %s and p.course_progress_ts < %s
)
select count(distinct penn_user_id) from u;
"""


users_enrolled = """
SELECT COUNT (DISTINCT penn_user_id) FROM on_demand_session_memberships JOIN on_demand_sessions USING (on_demand_session_id) WHERE on_demand_session_id= %s;
"""

last_assignment = """
WITH ordered_assignments AS (
  SELECT 
    --i.course_item_id,
    i.course_branch_item_name AS NAME,
    ROW_NUMBER() OVER (
  --    PARTITION BY m.course_module_id
  --    ORDER BY course_branch_module_order, course_branch_lesson_order, course_branch_item_order
        ORDER BY course_branch_module_order, course_branch_lesson_order, course_branch_item_order
    ) AS ord 
  FROM course_branch_items i
      JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
      JOIN course_branch_modules m USING (course_module_id, course_branch_id)
  WHERE i.course_branch_id = %s AND m.course_module_id = %s
    AND (i.course_item_type_id=10 or i.course_item_type_id = 6)
),
assignments_progress AS (
  SELECT i.course_item_id, p.penn_user_id, course_branch_item_name, course_branch_item_order, p.course_progress_ts
  FROM course_progress p
  JOIN course_progress_state_types
    USING (course_progress_state_type_id)
  JOIN course_branch_items i USING (course_item_id)
      JOIN course_branch_lessons l USING (course_lesson_id, course_branch_id)
      JOIN course_branch_modules m USING (course_module_id, course_branch_id)
  WHERE i.course_branch_id = %s AND m.course_module_id = %s
    AND (i.course_item_type_id=10 or i.course_item_type_id = 6)
    AND course_progress_state_type_desc = 'started'
    AND p.course_progress_ts > %s and p.course_progress_ts < %s
)
, user_last AS (
  SELECT penn_user_id, MAX(ap.course_progress_ts) as ts
  FROM assignments_progress ap
  GROUP BY 1
 ),
user_last_name AS (
  SELECT ap.penn_user_id, course_branch_item_name AS NAME
  FROM assignments_progress ap
  JOIN user_last ON ap.penn_user_id=user_last.penn_user_id AND ap.course_progress_ts = user_last.ts
),
counts AS (
SELECT ord, NAME, COUNT(penn_user_id) AS co
FROM ordered_assignments JOIN user_last_name USING (NAME)
GROUP BY 1,2
)
SELECT DISTINCT(ord), NAME, co AS last_seen FROM counts ORDER BY ord;--  join user_last_name on cc.name=user_last_name.name order by ord;
"""
