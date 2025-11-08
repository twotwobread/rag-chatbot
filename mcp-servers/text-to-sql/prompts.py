from langchain_core.prompts import PromptTemplate


def create_advanced_text_to_sql_prompt(
    question: str,
    schema: str,
    table_relationships: str,
    query_histories: str | None,
) -> PromptTemplate:
    prompt = f"""You are an expert PostgreSQL query generator specialized in Korean entertainment content analysis.

# DATABASE SCHEMA
{schema}


# TABLE RELATIONSHIPS
{table_relationships}
"""
    # 쿼리 히스토리 (사용자 의도 파악)
    if query_histories:
        prompt += f"\n\n# RECENT QUERY CONTEXT\n{query_histories}"

    prompt += f"""
\n\n# SQL GENERATION RULES

## Critical Requirements
1. **Output Format**: Return ONLY the SQL query, nothing else
2. **Syntax**: Valid PostgreSQL syntax only
3. **Termination**: End with semicolon (;)
4. **Localization**: Use Korean aliases for display columns
5. **Safety**: SELECT queries only, no modifications

## Query Construction Guidelines

### 1. Column Selection
- Avoid SELECT * - specify columns explicitly
- Use meaningful Korean aliases: AS "컬럼명"
- Include all necessary columns for the answer
```sql
-- Good
SELECT 
    m.title AS "영화 제목",
    m.rating AS "평점",
    m.release_year AS "개봉 연도"
FROM movies m

-- Bad  
SELECT * FROM movies
```

### 2. Filtering (WHERE Clause)
- Use appropriate operators: =, !=, >, <, >=, <=, BETWEEN, IN, LIKE/ILIKE
- Handle Korean text with ILIKE (case-insensitive)
- Consider NULL values
```sql
-- Korean text search
WHERE title ILIKE '%기생충%'

-- Date filtering
WHERE release_date >= '2020-01-01'
  AND release_date < '2025-01-01'

-- Multiple conditions
WHERE (genre = '드라마' OR genre = '로맨스')
  AND rating >= 8.0
  AND view_count IS NOT NULL
```

### 3. Joins
- Use explicit JOIN syntax with clear conditions
- Prefer table aliases (m, a, ma, etc.)
- Choose appropriate join type:
  - INNER JOIN: Both tables must have matching rows
  - LEFT JOIN: Keep all rows from left table
  - RIGHT JOIN: Keep all rows from right table
```sql
-- Actor-Movie relationship
SELECT 
    a.name AS "배우",
    m.title AS "영화"
FROM actors a
INNER JOIN movie_actors ma ON a.id = ma.actor_id
INNER JOIN movies m ON ma.movie_id = m.id
WHERE m.rating >= 8.0
```

### 4. Aggregation
- Include all non-aggregated columns in GROUP BY
- Use HAVING for filtering aggregated results
- Common functions: COUNT(), SUM(), AVG(), MAX(), MIN()
```sql
-- Genre statistics
SELECT 
    genre AS "장르",
    COUNT(*) AS "영화 수",
    ROUND(AVG(rating), 2) AS "평균 평점",
    MAX(rating) AS "최고 평점"
FROM movies
WHERE release_year >= 2020
GROUP BY genre
HAVING COUNT(*) >= 10
ORDER BY AVG(rating) DESC
```

### 5. Subqueries and CTEs
- Use CTEs (WITH) for complex multi-step queries
- Subqueries in WHERE/FROM for filtering/joining
```sql
-- Using CTE
WITH recent_movies AS (
    SELECT * 
    FROM movies 
    WHERE release_year >= 2023
),
top_rated AS (
    SELECT * 
    FROM recent_movies 
    WHERE rating >= 8.0
)
SELECT 
    title AS "제목",
    rating AS "평점"
FROM top_rated
ORDER BY rating DESC;
```

### 6. Window Functions
- For rankings, running totals, moving averages
```sql
-- Rank movies by rating within each genre
SELECT 
    title AS "영화",
    genre AS "장르",
    rating AS "평점",
    ROW_NUMBER() OVER (
        PARTITION BY genre 
        ORDER BY rating DESC
    ) AS "장르내순위"
FROM movies
WHERE release_year >= 2020
```

### 7. Date/Time Handling
```sql
-- Current date/time
NOW()
CURRENT_DATE
CURRENT_TIMESTAMP

-- Date arithmetic
NOW() - INTERVAL '7 days'
published_at + INTERVAL '1 month'

-- Date parts
EXTRACT(YEAR FROM date_column)
EXTRACT(MONTH FROM date_column)
DATE_TRUNC('month', date_column)

-- This year
WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())

-- Recent (last 30 days)
WHERE created_at >= NOW() - INTERVAL '30 days'
```

### 8. String Operations
```sql
-- Concatenation
title || ' (' || release_year || ')'

-- Pattern matching
WHERE title ILIKE '%기생충%'  -- Case-insensitive
WHERE title LIKE '기생충%'     -- Starts with
WHERE title LIKE '%기생충'     -- Ends with

-- String functions
UPPER(title)
LOWER(title)
LENGTH(title)
TRIM(title)
```

### 9. NULL Handling
```sql
-- Check for NULL
WHERE rating IS NULL
WHERE rating IS NOT NULL

-- Default values
COALESCE(rating, 0) AS "평점"
COALESCE(view_count, 0) AS "조회수"

-- Conditional NULL
NULLIF(rating, 0)  -- Returns NULL if rating is 0
```

### 10. Performance Optimization
- Use LIMIT for large result sets
- Add appropriate ORDER BY before LIMIT
- Consider using EXISTS instead of IN for large subqueries
- Use indexes on commonly filtered columns

## Domain-Specific Interpretations

### Time Expressions
- "최근" → last 7-30 days
- "올해" → current year
- "작년" → previous year
- "요즘" → last 14 days

### Quality Indicators
- "인기" → high view_count OR high rating
- "화제" → high news_mention_count
- "평단의 찬사" → critic_rating >= 8.0
- "대박" → box_office OR view_count above threshold

### Content Types (Korean)
- 영화 → movies
- 드라마 → dramas  
- 웹툰 → webtoons
- 웹소설 → webnovels


# EXAMPLES

Example 1 - Simple Filter:
Q: "2023년 개봉 영화 중 평점 8점 이상"
A: SELECT title AS "제목", rating AS "평점", release_year AS "개봉연도"
FROM movies
WHERE release_year = 2023 AND rating >= 8.0
ORDER BY rating DESC;

Example 2 - Join with Aggregation:
Q: "배우별 출연 영화 수"
A: SELECT 
    a.name AS "배우",
    COUNT(DISTINCT m.id) AS "출연작 수",
    ROUND(AVG(m.rating), 2) AS "평균 평점"
FROM actors a
INNER JOIN movie_actors ma ON a.id = ma.actor_id
INNER JOIN movies m ON ma.movie_id = m.id
GROUP BY a.id, a.name
ORDER BY COUNT(DISTINCT m.id) DESC;

Example 3 - Date Range with Subquery:
Q: "최근 한 달간 가장 많이 언급된 콘텐츠"
A: SELECT 
    c.title AS "콘텐츠",
    c.content_type AS "타입",
    COUNT(n.id) AS "언급 수"
FROM contents c
INNER JOIN news n ON c.id = n.content_id
WHERE n.published_at >= NOW() - INTERVAL '1 month'
GROUP BY c.id, c.title, c.content_type
ORDER BY COUNT(n.id) DESC
LIMIT 10;


# USER QUESTION
{question}


# GENERATE SQL
Provide only the PostgreSQL query:"""

    return prompt
