Okay, here are the SQL queries for each task, assuming a standard database schema with movies, stars, studios, and a joining table like roles or movie_stars (let's assume roles with movie_id and star_id).

### SQL Queries for `movies_db`

1.  **The title of every movie.**

    ```sql
    SELECT title
    FROM movies;
    ```

2.  **All information on the G-rated movies.**

    ```sql
    SELECT *
    FROM movies
    WHERE rating = 'G';
    ```

3.  **The title and release year of every movie, ordered with the oldest movie first.**

    ```sql
    SELECT title, release_year
    FROM movies
    ORDER BY release_year ASC;
    ```

4.  **All information on the 5 longest movies.**
    _(Assuming a `runtime` column exists in minutes or seconds)_

    ```sql
    SELECT *
    FROM movies
    ORDER BY runtime DESC
    LIMIT 5;
    ```

5.  **A query that returns the columns of `rating` and `total`, tabulating the total number of G, PG, PG-13, and R-rated movies.**

    ```sql
    SELECT rating, COUNT(*) AS total
    FROM movies
    WHERE rating IN ('G', 'PG', 'PG-13', 'R')
    GROUP BY rating;
    ```

    _(Note: If ONLY these ratings exist, the WHERE clause is optional, but safer to include)_

6.  **A table with columns of `release_year` and `average_runtime`, tabulating the average runtime by year for every movie in the database. The data should be in reverse chronological order (i.e. the most recent year should be first).**
    _(Assuming a `runtime` column exists)_

    ```sql
    SELECT release_year, AVG(runtime) AS average_runtime
    FROM movies
    GROUP BY release_year
    ORDER BY release_year DESC;
    ```

7.  **The movie title and studio name for every movie in the database.**
    _(Assuming `movies` has a `studio_id` foreign key referencing `studios.studio_id` and `studios` has a `name` column)_

    ```sql
    SELECT m.title, s.name AS studio_name
    FROM movies m
    JOIN studios s ON m.studio_id = s.studio_id;
    ```

8.  **The star first name, star last name, and movie title for every matching movie and star pair in the database.**
    _(Assuming a `roles` table with `movie_id`, `star_id` foreign keys, and a `stars` table with `first_name`, `last_name`)_

    ```sql
    SELECT s.first_name, s.last_name, m.title
    FROM stars s
    JOIN roles r ON s.star_id = r.star_id
    JOIN movies m ON r.movie_id = m.movie_id;
    ```

9.  **The first and last names of every star who has been in a G-rated movie. The first and last name should appear only once for each star, even if they are in several G-rated movies. _IMPORTANT NOTE_: it's possible that there can be two _different_ actors with the same name, so make sure your solution accounts for that.**
    _(Grouping by the star's unique ID ensures distinct actors)_

    ```sql
    SELECT s.first_name, s.last_name
    FROM stars s
    JOIN roles r ON s.star_id = r.star_id
    JOIN movies m ON r.movie_id = m.movie_id
    WHERE m.rating = 'G'
    GROUP BY s.star_id, s.first_name, s.last_name;
    ```

    _(Alternatively, using DISTINCT after joining on the unique star ID often works)_

    ```sql
    -- Alternative using DISTINCT (relies on join logic ensuring star uniqueness)
    SELECT DISTINCT s.first_name, s.last_name
    FROM stars s
    JOIN roles r ON s.star_id = r.star_id
    JOIN movies m ON r.movie_id = m.movie_id
    WHERE m.rating = 'G';
    ```

10. **The first and last names of every star along with the number of movies they have been in, in descending order by the number of movies. (Similar to #9, make sure that two different actors with the same name are considered separately).**
    _(Use LEFT JOIN to include stars with 0 movies. Group by star ID for uniqueness)_

    ```sql
    SELECT s.first_name, s.last_name, COUNT(r.movie_id) AS number_of_movies
    FROM stars s
    LEFT JOIN roles r ON s.star_id = r.star_id
    GROUP BY s.star_id, s.first_name, s.last_name
    ORDER BY number_of_movies DESC;
    ```

### Bonus Queries

11. **The title of every movie along with the number of stars in that movie, in descending order by the number of stars.**
    _(Use LEFT JOIN to include movies with 0 stars)_

    ```sql
    SELECT m.title, COUNT(r.star_id) AS number_of_stars
    FROM movies m
    LEFT JOIN roles r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id, m.title -- Include movie_id in GROUP BY for correctness if titles aren't unique
    ORDER BY number_of_stars DESC;
    ```

12. **The first name, last name, and average runtime of the five stars whose movies have the longest average.**
    _(Assuming `runtime` column)_

    ```sql
    SELECT s.first_name, s.last_name, AVG(m.runtime) AS average_runtime
    FROM stars s
    JOIN roles r ON s.star_id = r.star_id
    JOIN movies m ON r.movie_id = m.movie_id
    GROUP BY s.star_id, s.first_name, s.last_name
    ORDER BY average_runtime DESC
    LIMIT 5;
    ```

13. **The first name, last name, and average runtime of the five stars whose movies have the longest average, among stars who have more than one movie in the database.**
    _(Add a HAVING clause to filter the grouped results)_

    ```sql
    SELECT s.first_name, s.last_name, AVG(m.runtime) AS average_runtime
    FROM stars s
    JOIN roles r ON s.star_id = r.star_id
    JOIN movies m ON r.movie_id = m.movie_id
    GROUP BY s.star_id, s.first_name, s.last_name
    HAVING COUNT(m.movie_id) > 1
    ORDER BY average_runtime DESC
    LIMIT 5;
    ```

14. **The titles of all movies that don't feature any stars in our database.**
    _(Using LEFT JOIN / IS NULL check)_

    ```sql
    SELECT m.title
    FROM movies m
    LEFT JOIN roles r ON m.movie_id = r.movie_id
    WHERE r.star_id IS NULL; -- Or r.movie_id IS NULL from the roles table
    ```

15. **The first and last names of all stars that don't appear in any movies in our database.**
    _(Using LEFT JOIN / IS NULL check)_

    ```sql
    SELECT s.first_name, s.last_name
    FROM stars s
    LEFT JOIN roles r ON s.star_id = r.star_id
    WHERE r.movie_id IS NULL; -- Or r.star_id IS NULL from the roles table
    ```

16. **The first names, last names, and titles corresponding to every role in the database, along with every movie title that doesn't have a star, and the first and last names of every star not in a movie.**
    _(Use FULL OUTER JOIN centered around the roles table)_

    ```sql
    SELECT
        s.first_name,
        s.last_name,
        m.title
    FROM
        stars s
    FULL OUTER JOIN
        roles r ON s.star_id = r.star_id
    FULL OUTER JOIN
        movies m ON r.movie_id = m.movie_id;
    ```
