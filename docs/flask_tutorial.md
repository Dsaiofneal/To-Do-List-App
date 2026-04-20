# Flask Learning Guide for This Project

This file explains how your app is structured and how to write routes in a beginner-friendly way.

## 1. What Flask Is

Flask is a small Python web framework.

Think of it like this:
- A URL comes in (example: /api/health)
- Flask finds the matching function
- Your function returns text or JSON

## 2. Core Project Flow

- main.py creates the Flask app.
- main.py registers the blueprint from routes/tasks.py.
- The blueprint owns task-related URLs.

## 3. Route Anatomy

A route has 3 parts:
1. Decorator (which URL and method)
2. Python function (logic)
3. Return value (text or JSON)

Example shape:

@app.get("/hello")
def hello():
    return jsonify({"message": "hi"})

## 4. JSON Basics

JSON is text used for data exchange. It is very close to Python dictionaries.

JSON example:
{
  "field": "Buy milk"
}

Important differences:
- JSON uses double quotes
- true/false are lowercase in JSON
- null in JSON is None in Python

## 5. Reading JSON in Flask

Use request.get_json(silent=True) in a POST route.

- If body is valid JSON, you get a Python dict
- If invalid or missing, you get None

Then validate required fields before using them.

## 6. Recommended Practice Pattern

Use this order in POST routes:
1. Parse JSON
2. Validate body exists
3. Validate each required field
4. Build output object
5. Return response with status code

## 7. Useful Status Codes

- 200: OK (normal GET success)
- 201: Created (successful POST create)
- 400: Bad Request (invalid user input)
- 404: Not Found

## 8. Quick Local Testing

PowerShell example:

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/tasks/taskadd" -ContentType "application/json" -Body '{"field":"Buy milk"}'

Then GET:

Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:5000/api/tasks/tasks"

## 9. Learning URLs Added

- /learn/example/add-task returns the JSON example file.
- /learn/tutorial returns this tutorial file content.

Open these in your browser while the app is running.
