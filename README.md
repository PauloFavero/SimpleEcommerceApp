# SimpleEcommerceApp

A simple backend to simulate an e-commerce application using FastAPI, PyMongo and Pydantic.

## Run Instructions

1. Building the images:
   `docker compose build`

2. Launch server and databases: `docker compose up -d`
   - Access localhost:3000/docs to have full acess to the swagger documentation.

## App Folder Structure

- config: This folder contains classes to handle configurations for uvicorn, mondogb and the server itself.
- entities: The entities folder contain the anemic domain models built with pydantic.
- infra: The infra folder is responsible for everything in the most external layer of the application.
  - data: This folder holds data models at the database level which include \_id and created_at fields, for example.
  - mongo: Helper functions and queries for each repository (collection) used in the app along with the db connection handler.
- server:
  - routes: Contains the endpoints for the E-Commerce API.
  - main.py: Launcher the webserver using FastAPI.

## Features:

The goal of API is manage the users, products and shopping carts for an e-commerce application. In terms of funcionalities, it allows the following:

- Users Endpoints:

  1.  Registers User. When a user is created, a shooping cart is also created for this user (just a trick to make things simple).
  2.  Get user by id.
  3.  Get a paginated list of users.
  4.  Delete User.
  5.  Replace user resource by an updated version.
  6.  Partially update a given user document.

- Products Endpoints:

  1.  Registers products.
  2.  Get product by id.
  3.  Get a paginated list of products sorted by a given field in a given orders and also it can filter by a category.
  4.  Delete product.
  5.  Replace product resource by an updated version.
  6.  Partially update a given product.

- Shopping Cart Endpoints
  1.  Create shopping cart.
  2.  Fetch a shopping cart by its id.
  3.  Add items to a shopping cart.
  4.  Remove items from shopping cart.
  5.  Clear shopping cart.
  6.  Delete shopping cart.

### Nice to have features

- User authentication endpoint.
- API authentication and authorization based on user role.
- Handle products stock availability

## DEV Tools:

**Linter:**
To run pylint in the app folder, execute the following command: `pylint ./app/`

**Formmater:**
To run black in the app folder, execute the following command: `black ./app/`

**Type Checker:**
To run mypy in the app folder, execute the following command: `mypy ./app/`
