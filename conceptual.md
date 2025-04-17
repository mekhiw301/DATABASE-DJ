### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?

### PostgreSQL (often called "Postgres") is a powerful, open-source Object-Relational Database Management System (ORDBMS). It uses and extends the SQL language. It's known for its reliability, robustness, feature completeness, data integrity, and adherence to SQL standards. It supports complex queries, various data types (including JSON, arrays, and custom types), advanced indexing, and high concurrency.

- What is the difference between SQL and PostgreSQL?

### SQL (Structured Query Language) is the standard language used to communicate with relational databases. It's used to define database structure, manipulate data (insert, update, delete), and query data (select).

### PostgreSQL is a specific database management system (DBMS) – a piece of software that stores, manages, and retrieves data. PostgreSQL implements the SQL standard, meaning you use SQL commands to interact with a PostgreSQL database. PostgreSQL also adds its own extensions and features beyond the basic SQL standard (like specific functions, data types, and procedural languages like PL/pgSQL).

- In `psql`, how do you connect to a database?

### psql is the command-line interface for PostgreSQL. To connect, you typically use the following format:

### psql [options] [database_name] [username]

- What is the difference between `HAVING` and `WHERE`?

### WHERE filters rows before any grouping or aggregation occurs. It operates on individual rows based on column values. You cannot use aggregate functions (like COUNT(), SUM(), AVG()) directly in the WHERE clause.

### HAVING filters groups of rows after the GROUP BY clause has been applied and aggregate functions have been calculated. It operates on the summarized results of the groups. It's specifically designed to filter based on the results of aggregate functions.

- What is the difference between an `INNER` and `OUTER` join?

### INNER JOIN: Returns only the rows where the join condition is met in both tables. If a row in one table doesn't have a matching row in the other table (based on the join condition), that row is excluded from the result set. It finds the intersection of the two tables based on the condition.

### OUTER JOIN: Returns all rows from at least one of the tables, even if there's no match in the other table. If there isn't a match for a row, the columns from the non-matching table will contain NULL values. There are three types: LEFT OUTER JOIN, RIGHT OUTER JOIN, and FULL OUTER JOIN.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?

### LEFT OUTER JOIN (or simply LEFT JOIN): Returns all rows from the left table (the table listed before the LEFT JOIN keyword) and the matched rows from the right table. If there is no match in the right table for a row from the left table, NULL values are returned for all columns of the right table.

### RIGHT OUTER JOIN (or simply RIGHT JOIN): Returns all rows from the right table (the table listed after the RIGHT JOIN keyword) and the matched rows from the left table. If there is no match in the left table for a row from the right table, NULL values are returned for all columns of the left table.

### LEFT JOIN is generally more commonly used than RIGHT JOIN.

- What is an ORM? What do they do?

### ORM stands for Object-Relational Mapper.

### It's a programming technique and a type of library/tool that creates a "bridge" between object-oriented programming languages (like Python, Java, Ruby) and relational databases (like PostgreSQL, MySQL).

What they do:

### Mapping: They map database tables to classes (models) and table rows to objects (instances of those classes) in the programming language. Columns in the table map to attributes of the object.

### Abstraction: They allow developers to interact with the database (querying, inserting, updating, deleting data) using the objects and methods of their programming language, rather than writing raw SQL queries directly. The ORM translates these object operations into SQL commands behind the scenes.

### Relationship Handling: They help manage relationships between tables (like one-to-many, many-to-many) using object-oriented concepts (e.g., accessing related objects via attributes).

### Database Independence (Partial): They can sometimes provide a layer of abstraction that makes it easier to switch between different database systems, although database-specific features might still require adjustments.

- What are some differences between making HTTP requests using AJAX
  and from the server side using a library like `requests`?

  ### AJAX (e.g., fetch or XMLHttpRequest in Browser JS)

### Server-Side (e.g., requests in Python, axios in Node.js)

### AJAX runs in the User's Browser

### (Client-Side) Runs on the Web Server

### AJAX: User interaction or client-side script

### Server-side: application logic

### AJAX: Update parts of a page without full reload, fetch data dynamically for the UI, submit forms asynchronously.

### Server-Side: Communicate with other APIs/microservices, fetch data needed to render a page, perform server-to-server tasks.

### AJAX has access to the browser's DOM, window object. Automatically sends cookies associated with the domain.

### Server-Side runs within the server process. No access to user's DOM. Cookies must be managed explicitly if needed.

### AJAX subject to browser security policies like the Same-Origin Policy (SOP) and CORS (Cross-Origin Resource Sharing).

### Server-side is not subject to browser CORS policies (though the target server might have its own restrictions). Can often access internal network resources.

### AJAX uses the user's computer resources and network connection. Server-side uses the server's resources and network connection.

### AJAX: Making a web page feel more interactive and dynamic. Server-Side: Integrating with third-party services, building microservice architectures.

- What is CSRF? What is the purpose of the CSRF token?

### CSRF stands for Cross-Site Request Forgery. It's a type of web security vulnerability attack.

### How it works: An attacker tricks a victim (who is logged into a legitimate website) into unknowingly submitting a malicious request to that legitimate website through the victim's browser. Because the browser automatically includes authentication cookies with requests to the legitimate site, the malicious request appears valid to the server, potentially allowing the attacker to perform actions on behalf of the victim (like changing their email, transferring funds, etc.).

### Purpose of CSRF Token: The CSRF token is a defense mechanism against CSRF attacks. It's a unique, secret, unpredictable value generated by the server-side application and associated with the user's current session.

### The token is embedded within legitimate HTML forms (usually as a hidden input field).

### When the user submits the form, the browser sends this token back along with the other form data.

### The server validates that the token received matches the one it generated for that session.

- What is the purpose of `form.hidden_tag()`?

### In the context of Flask-WTF (which integrates WTForms with Flask), form.hidden_tag() is a helper function used within Jinja2 templates when rendering a form.

### Its primary purpose is to render any hidden fields defined within the corresponding WTForms Form object.

### Most importantly, when CSRF protection is enabled in Flask-WTF, this automatically includes rendering the hidden CSRF token input field (<input type="hidden" name="csrf_token" value="...">).

### Including {{ form.hidden_tag() }} inside your HTML <form> tag ensures that the necessary hidden data, especially the CSRF token, is submitted along with the visible form fields, allowing the server to perform CSRF validation. It can also render any other fields you explicitly define as HiddenField in your form class.
