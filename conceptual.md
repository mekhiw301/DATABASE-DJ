### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
PostgreSQL is an advanced, open-source relational database management system (RDBMS). It supports SQL standards and includes powerful features such as complex queries, transactions, indexing, and support for procedural languages.

- What is the difference between SQL and PostgreSQL?
SQL is a language used to query and manage relational databases. PostgreSQL is a specific implementation of an SQL-based database — it’s a system that uses SQL to allow users to store, retrieve, and manipulate data.

- In `psql`, how do you connect to a database?
psql database_name


- What is the difference between `HAVING` and `WHERE`?
WHERE filters rows before grouping or aggregation.

HAVING filters groups after aggregation.
Use WHERE for raw data filtering and HAVING to filter summary results.

- What is the difference between an `INNER` and `OUTER` join?
INNER JOIN returns only matching rows in both tables.

OUTER JOIN returns all rows from one or both tables, filling in NULL where there is no match.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
LEFT OUTER JOIN: all rows from the left table + matches from the right

RIGHT OUTER JOIN: all rows from the right table + matches from the left

- What is an ORM? What do they do?
An ORM (Object-Relational Mapper) allows developers to interact with a database using the syntax of their programming language (like Python) instead of raw SQL. It maps database tables to classes and rows to objects.

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
  AJAX (client-side): Request is made from the browser; often used to update parts of a page dynamically without reloading.

requests (server-side): Request is made from the backend; useful for APIs or integrating external data into server responses.

- What is CSRF? What is the purpose of the CSRF token?
CSRF (Cross-Site Request Forgery) is a type of attack where a user is tricked into submitting a malicious request. A CSRF token is a unique, secret value included in forms to ensure the request came from the intended user/session and not an external attacker.



- What is the purpose of `form.hidden_tag()`?
form.hidden_tag() in WTForms includes hidden fields in a form, especially for security features like the CSRF token. It helps prevent CSRF attacks by embedding a token in each form submission.