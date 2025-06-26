Website Functionality (Backend):
I built the backend in Flask. It has a REST API that handles all content operations such as create, read (GET), and delete. The frontend uses JavaScript fetch() calls to communicate 
with the API and load the content to the frontend. Once data is created/posted it is stored in an SQLite database. I used SQLAlchemy as the ORM layer to map Python classes to database 
tables. This lets me interact with the database through model instances without writing SQL. 

Each content type (e.g. Insight post, portfolio post, press release post) is defined as a model. When an API request comes in, 
Flask parses the input, runs validation, updates the database through SQLAlchemy, and returns a JSON response.

For the admin system, the admin panel can post new entries or delete them. It is secured with a login and password. This is where only the admin can access to post insights, 
portfolios, or press releases on the website. These changes go directly into the database and are instantly available to the frontend with a clean UI.

Each API route is built for a specific action. /api/insights is used to get all posts or add a new one. /api/insights/<id> is used to get a specific post or delete it.
To make the frontend dynamic, I built everything to fetch data by ID. For example, when loading a portfolio item, the JS reads the id from the URL and makes a 
GET request like /api/portfolio/5, which returns the data that gets injected into the page.

In short: Flask handles routing, SQLAlchemy manages data, and the whole site stays dynamic through RESTful JSON APIs.
