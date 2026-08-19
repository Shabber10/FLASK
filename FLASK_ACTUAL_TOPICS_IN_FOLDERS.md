# 📊 Actual Topics and Subtopics Present in Workspace Files

This document lists every single Topic (H1), Section (H2), and Sub-section (H3) extracted directly from the actual markdown files across all 30 Day folders.

---

## 📁 DAY 01 - Introduction to Flask and Web Architecture

### 📄 File: [0. Web Fundamentals for Absolute Beginners.md](DAY 01 - Introduction to Flask and Web Architecture\0. Web Fundamentals for Absolute Beginners.md)
*   **Title (H1)**: Day 01 - Module 0: Web Fundamentals for Absolute Beginners
    *   **Section (H2)**: 1. What is Web Development?
    *   **Section (H2)**: 2. Webpage vs. Website vs. Web Application
        *   *Sub-section (H3)*: 📄 1. Webpage
        *   *Sub-section (H3)*: 🌐 2. Website
        *   *Sub-section (H3)*: ⚙️ 3. Web Application
    *   **Section (H2)**: 3. Static Website vs. Dynamic Website
        *   *Sub-section (H3)*: 📄 Static Webpage Example (HTML only)
        *   *Sub-section (H3)*: ⚙️ Dynamic Webpage Example (Flask + Python)
*   **Title (H1)**: render_template injects dynamic data into HTML placeholders!
    *   **Section (H2)**: 4. What is the World Wide Web (WWW)?
        *   *Sub-section (H3)*: The Internet vs. The World Wide Web
    *   **Section (H2)**: 5. Web Browser vs. Web Server
        *   *Sub-section (H3)*: 🧑‍💻 Web Browser
        *   *Sub-section (H3)*: 🖥️ Web Server
    *   **Section (H2)**: 6. Detailed URL Breakdown
    *   **Section (H2)**: 7. How the Internet Works (Step-by-Step)
        *   *Sub-section (H3)*: 🍕 Pizza Order Real-World Analogy
    *   **Section (H2)**: 8. Web Request-Response Architecture & Flowchart
    *   **Section (H2)**: 9. Client-Server Restaurant Analogy
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Introduction to Flask and WSGI Architecture.md](DAY 01 - Introduction to Flask and Web Architecture\1. Introduction to Flask and WSGI Architecture.md)
*   **Title (H1)**: Day 01 - Module 1: Introduction to Flask & WSGI Architecture
    *   **Section (H2)**: 1. What is Flask?
    *   **Section (H2)**: 2. What is a Framework & Why is Flask a "Microframework"?
        *   *Sub-section (H3)*: 🔹 What is a Framework?
        *   *Sub-section (H3)*: 🔹 Why is Flask called a Microframework?
    *   **Section (H2)**: 3. Advantages & Disadvantages of Flask
        *   *Sub-section (H3)*: ✅ Advantages
        *   *Sub-section (H3)*: ❌ Disadvantages
    *   **Section (H2)**: 4. Real-World Applications of Flask
    *   **Section (H2)**: 5. What is WSGI? (Web Server Gateway Interface)
        *   *Sub-section (H3)*: Definition & Acronym
    *   **Section (H2)**: 6. Restaurant Mental Model of Flask & WSGI
    *   **Section (H2)**: 7. Low-Level Raw WSGI Callable Example
    *   **Section (H2)**: 8. The 3 Core Pillars Behind Flask
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Minimal Flask Application and Environment Setup.md](DAY 01 - Introduction to Flask and Web Architecture\2. Minimal Flask Application and Environment Setup.md)
*   **Title (H1)**: Day 01 - Module 2: Minimal Flask Application & Environment Setup
    *   **Section (H2)**: 1. Line-by-Line Breakdown of a Minimal Flask App
*   **Title (H1)**: 1. Import the Flask class from the flask module
*   **Title (H1)**: 2. Create an instance of the Flask application
*   **Title (H1)**: 3. Define a route for the home page (root URL '/')
*   **Title (H1)**: This function returns a message when the root URL is accessed
*   **Title (H1)**: 4. Define a route for '/course'
*   **Title (H1)**: 5. Define a dynamic route that captures any string passed in the URL
*   **Title (H1)**: 6. Run the application only if this script is executed directly
        *   *Sub-section (H3)*: 🚀 1. Importing Flask
        *   *Sub-section (H3)*: 🏗️ 2. Creating Flask App
        *   *Sub-section (H3)*: 🌐 3. Defining Routes
        *   *Sub-section (H3)*: 🟢 4. Running the Flask App
    *   **Section (H2)**: 2. Introduction to `render_template()` Function
        *   *Sub-section (H3)*: 🔍 What is `render_template()`?
*   **Title (H1)**: Looks inside 'templates/' folder for 'home.html'
*   **Title (H1)**: Looks inside 'templates/' folder for 'index.html'
        *   *Sub-section (H3)*: 🗂️ Mandatory Flask Project Folder Structure
        *   *Sub-section (H3)*: 📄 Example `templates/home.html`:
        *   *Sub-section (H3)*: 📄 Example `templates/index.html`:
    *   **Section (H2)**: 3. Core Flask App Summary Table
    *   **Section (H2)**: 4. Environment Variables (`.env` & `.flaskenv`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 01 - Introduction to Flask and Web Architecture\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 01: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Zero-Knowledge Acronym Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. The WSGI Standard Signature Callable (`W-E-S-S`)
        *   *Sub-section (H3)*: 2. Context Local Proxies (`A-R-C-G`)
    *   **Section (H2)**: ⚡ Quick-Reference Commands Cheatsheet
        *   *Sub-section (H3)*: Environment & Package Setup
*   **Title (H1)**: 1. Create virtual environment
*   **Title (H1)**: 2. Activate virtual environment (Windows Command Prompt / PowerShell)
*   **Title (H1)**: 2. Activate virtual environment (Linux / macOS Terminal)
*   **Title (H1)**: 3. Install Flask & dotenv support
        *   *Sub-section (H3)*: CLI Operations
*   **Title (H1)**: Run Development WSGI Server (Uses .flaskenv automatically)
*   **Title (H1)**: Run on Specific Host & Port
*   **Title (H1)**: List All Registered Routes in Application
    *   **Section (H2)**: 📋 Core Code Snippets
        *   *Sub-section (H3)*: 1. Minimal Flask App
        *   *Sub-section (H3)*: 2. Pushing Application Context Manually
        *   *Sub-section (H3)*: 3. Custom WSGI Middleware
*   **Title (H1)**: Intercept incoming request or modify response

### 📄 File: [5. Practice and Interview Questions.md](DAY 01 - Introduction to Flask and Web Architecture\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 01: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the difference between a Client and a Server on the Web?
        *   *Sub-section (H3)*: Q2: What does WSGI stand for, and what does it do in plain English?
        *   *Sub-section (H3)*: Q3: What is the IP address `127.0.0.1` and what does it mean?
        *   *Sub-section (H3)*: Q4: What is the difference between an HTTP `GET` request and an HTTP `POST` request?
        *   *Sub-section (H3)*: Q5: What does an HTTP status code `404` mean? What about `200` and `500`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What does `__name__` do when passed to `app = Flask(__name__)`?
        *   *Sub-section (H3)*: Q7: Why is Flask called a "Micro-framework"? Does it mean it can't handle large applications?
        *   *Sub-section (H3)*: Q8: Explain the difference between Application Context and Request Context in Flask.
        *   *Sub-section (H3)*: Q9: Why should `debug=True` NEVER be enabled in production environments?
        *   *Sub-section (H3)*: Q10: What are `.env` and `.flaskenv` files used for in Flask applications?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is PEP 3333 and what problem did WSGI solve in Python web development?
        *   *Sub-section (H3)*: Q12: Explain the exact signature and requirements of a WSGI application callable.
        *   *Sub-section (H3)*: Q13: How do WSGI Middlewares work in Flask? Provide a code example.
        *   *Sub-section (H3)*: Q14: What is the main difference between WSGI and ASGI?
        *   *Sub-section (H3)*: Q15: Write a pure WSGI callable that parses query string parameters without using any third-party framework.

## 📁 DAY 02 - Routing, Request and Response Objects

### 📄 File: [0. Routing and Request-Response Fundamentals for Beginners.md](DAY 02 - Routing, Request and Response Objects\0. Routing and Request-Response Fundamentals for Beginners.md)
*   **Title (H1)**: Day 02 - Module 0: Routing & Request-Response Fundamentals for Beginners
    *   **Section (H2)**: 1. What is URL Routing?
    *   **Section (H2)**: 2. Four Main Ways Clients Send Data to Flask
    *   **Section (H2)**: 3. HTTP Methods (Verbs) & Real-Life Analogies
    *   **Section (H2)**: 4. In-Memory (RAM) Storage vs. Database Storage in Flask
        *   *Sub-section (H3)*: 🧠 How In-Memory (RAM) Storage Behaves
        *   *Sub-section (H3)*: 💾 Comparison Table: RAM vs. Database
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. URL Routing, Converters and HTTP Methods.md](DAY 02 - Routing, Request and Response Objects\1. URL Routing, Converters and HTTP Methods.md)
*   **Title (H1)**: Day 02 - Module 1: URL Routing, Converters & HTTP Methods
    *   **Section (H2)**: 1. Dynamic Routing & Built-in URL Converters
        *   *Sub-section (H3)*: Syntax:
        *   *Sub-section (H3)*: 🧠 Flask Built-in URL Converters
        *   *Sub-section (H3)*: Code Examples for Each Built-in Converter
*   **Title (H1)**: 1. string (Default)
*   **Title (H1)**: 2. int (Integer only)
*   **Title (H1)**: 'a' and 'b' are automatically converted to integers!
*   **Title (H1)**: 3. float (Decimal numbers)
*   **Title (H1)**: 4. path (Allows slashes)
    *   **Section (H2)**: 2. Dynamic Parameters vs. Query Parameters
    *   **Section (H2)**: 3. Custom URL Converters
        *   *Sub-section (H3)*: Example: Custom Even Number Converter
*   **Title (H1)**: Register converter on url_map
    *   **Section (H2)**: 4. Navigation & Redirection: `redirect()` vs `url_for()`
        *   *Sub-section (H3)*: 1. `redirect()`
        *   *Sub-section (H3)*: 2. `url_for()`
*   **Title (H1)**: url_for('home') -> generates '/'
*   **Title (H1)**: url_for('courses') -> generates '/course'
    *   **Section (H2)**: 5. Why `redirect(url_for('function_name'))` is Recommended (Best Practice)
        *   *Sub-section (H3)*: ⚖️ Comparison Table: Hardcoded Path vs `redirect(url_for(...))`
        *   *Sub-section (H3)*: 🔍 Code Proof: Single Place Update Advantage
*   **Title (H1)**: Recommended approach: uses function name 'dashboard'
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Deep Dive into Request and Response Objects.md](DAY 02 - Routing, Request and Response Objects\2. Deep Dive into Request and Response Objects.md)
*   **Title (H1)**: Day 02 - Module 2: Deep Dive into Request & Response Objects
    *   **Section (H2)**: 1. Query Parameters — `request.args` (GET)
        *   *Sub-section (H3)*: 🔹 What is `request.args`?
        *   *Sub-section (H3)*: 🔹 What is an `ImmutableMultiDict`?
        *   *Sub-section (H3)*: 🛒 Shopping List Analogy
        *   *Sub-section (H3)*: 🔹 Access Methods Summary Table for `request.args`
        *   *Sub-section (H3)*: 🧪 Practical `request.args` Code Example with `jsonify()`
    *   **Section (H2)**: 2. Form Data — `request.form` (POST)
        *   *Sub-section (H3)*: 🔹 What is Form Data?
        *   *Sub-section (H3)*: 🔹 Access Methods for `request.form`
        *   *Sub-section (H3)*: 📄 Full Registration Form Example (`app.py` + `templates/`)
*   **Title (H1)**: Form submitted (POST request) -> read inputs from request.form
*   **Title (H1)**: render success page with submitted user details
*   **Title (H1)**: Page first loaded (GET request) -> show registration form
    *   **Section (H2)**: 3. JSON Data — `request.get_json()` vs `request.json`
        *   *Sub-section (H3)*: 🔹 Definition
        *   *Sub-section (H3)*: ⚙️ Difference Between `request.get_json()` and `request.json`
        *   *Sub-section (H3)*: 🧪 Complete API CRUD Example (POST, PUT, DELETE)
*   **Title (H1)**: In-memory storage list (stored in RAM)
*   **Title (H1)**: 1. POST - Add new user
*   **Title (H1)**: 2. PUT - Update user age
*   **Title (H1)**: 3. DELETE - Remove user by ID
*   **Title (H1)**: 4. RESET - Reset in-memory RAM data
    *   **Section (H2)**: 4. What is `jsonify()` in Flask?
*   **Title (H1)**: Converts Python dictionary -> JSON response
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 02 - Routing, Request and Response Objects\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 02: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Routing & Request Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Built-in URL Converters (`S-I-F-P-U-A`)
        *   *Sub-section (H3)*: 2. Request Data Attributes (`A-F-J-H-F`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Registering Custom Regex Converter
        *   *Sub-section (H3)*: 2. Dynamic URL Building with `url_for()`
*   **Title (H1)**: Unmapped keyword arguments automatically become query string parameters
*   **Title (H1)**: Output: "http://127.0.0.1:5000/search?q=flask&page=2"
        *   *Sub-section (H3)*: 3. Custom Response with Headers & Secure Cookies
        *   *Sub-section (H3)*: 4. Redirection: Hardcoded vs Dynamic `url_for()`
*   **Title (H1)**: ❌ Hardcoded Redirect (Fragile! Breaks if URL path changes):
*   **Title (H1)**: ✅ Dynamic Redirect (Best Practice! Binds to Python view function name 'admin'):
*   **Title (H1)**: Dynamic Redirect with Parameters:
*   **Title (H1)**: Aborting with HTTP error status code:

### 📄 File: [5. Practice and Interview Questions.md](DAY 02 - Routing, Request and Response Objects\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 02: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is URL Routing in Flask?
        *   *Sub-section (H3)*: Q2: What is the difference between a Path Parameter (`/user/42`) and a Query Parameter (`/search?q=flask`)?
        *   *Sub-section (H3)*: Q3: What HTTP verb is used to read data vs submit form data?
        *   *Sub-section (H3)*: Q4: What is an HTTP Cookie and why do websites use them?
        *   *Sub-section (H3)*: Q5: How do you extract query parameters from a URL in Flask?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `path` and `string` URL converters in Flask?
        *   *Sub-section (H3)*: Q7: What type of data structure is `request.args` and how do you extract multiple values for the same key?
        *   *Sub-section (H3)*: Q8: Why is `url_for()` preferred over hardcoding URLs in templates and redirects?
        *   *Sub-section (H3)*: Q9: What happens if a client sends invalid JSON to a route calling `request.get_json()`?
        *   *Sub-section (H3)*: Q10: What is the difference between `redirect()` and `abort()` in Flask?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Explain how Werkzeug matches incoming URL paths to Flask view functions.
        *   *Sub-section (H3)*: Q12: How do you create a custom URL converter in Flask that converts path values to custom Python objects?
        *   *Sub-section (H3)*: Q13: How do you set HTTP-only, Secure, and SameSite flags when returning cookies in Flask?
        *   *Sub-section (H3)*: Q14: How does Flask handle HTTP `HEAD` and `OPTIONS` requests automatically?
        *   *Sub-section (H3)*: Q15: Explain the valid return types of a Flask view function.

## 📁 DAY 03 - Request Lifecycle and Context Locals

### 📄 File: [0. Contexts and Request Lifecycle Fundamentals for Beginners.md](DAY 03 - Request Lifecycle and Context Locals\0. Contexts and Request Lifecycle Fundamentals for Beginners.md)
*   **Title (H1)**: Day 03 - Module 0: Contexts & Request Lifecycle Fundamentals for Beginners
    *   **Section (H2)**: 1. What does "Context" mean in Plain English?
    *   **Section (H2)**: 2. The Danger of Standard Global Variables in Web Apps
*   **Title (H1)**: Standard Python script (ONLY 1 USER RUNS THIS AT A TIME)
        *   *Sub-section (H3)*: Why Global Variables Fail in Web Applications 🚨
    *   **Section (H2)**: 3. How Flask Solves Concurrency: Context Locals (`g` & `request`)
    *   **Section (H2)**: 4. What is the Request Lifecycle?
    *   **Section (H2)**: 5. What are Lifecycle Hooks?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Application and Request Contexts in Flask.md](DAY 03 - Request Lifecycle and Context Locals\1. Application and Request Contexts in Flask.md)
*   **Title (H1)**: Day 03 - Module 1: Application & Request Contexts in Flask
    *   **Section (H2)**: 1. The Concurrency Problem & `LocalProxy`
*   **Title (H1)**: When you call `request.method`, Werkzeug inspects Python's `contextvars`
*   **Title (H1)**: for the active thread/coroutine -> resolves the correct Request object dynamically!
    *   **Section (H2)**: 2. Dual-Layer Context Architecture
        *   *Sub-section (H3)*: 1. Application Context (`app_context`)
        *   *Sub-section (H3)*: 2. Request Context (`request_context`)
    *   **Section (H2)**: 3. Manually Pushing Contexts (CLI Scripts & Testing)
        *   *Sub-section (H3)*: 1. Pushing Application Context (`app.app_context()`)
*   **Title (H1)**: Push application context manually for standalone scripts
        *   *Sub-section (H3)*: 2. Pushing Request Context (`app.test_request_context()`)
*   **Title (H1)**: Simulate an incoming HTTP request for unit testing
    *   **Section (H2)**: 4. In-Memory `g` vs. Cookie `session`
        *   *Sub-section (H3)*: Code Comparison:
*   **Title (H1)**: 1. Storing data in `g` (EXPIRES as soon as this request finishes!)
*   **Title (H1)**: 2. Storing data in `session` (PERSISTS across future browser requests!)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Request Lifecycle Hooks and Context Processors.md](DAY 03 - Request Lifecycle and Context Locals\2. Request Lifecycle Hooks and Context Processors.md)
*   **Title (H1)**: Day 03 - Module 2: Request Lifecycle Hooks & Context Processors
    *   **Section (H2)**: 1. Complete Request Lifecycle Execution Pipeline
    *   **Section (H2)**: 2. The 3 Core Lifecycle Hook Decorators
        *   *Sub-section (H3)*: 1. `@app.before_request` & Request Short-Circuiting
*   **Title (H1)**: 1. Store request start timestamp on g
*   **Title (H1)**: 2. Short-circuit unauthorized access to protected routes
*   **Title (H1)**: Returns early response -> View function execution is SKIPPED!
        *   *Sub-section (H3)*: 2. `@app.after_request`
        *   *Sub-section (H3)*: 3. `@app.teardown_request`
    *   **Section (H2)**: 3. Global Template Context Processors (`@app.context_processor`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 03 - Request Lifecycle and Context Locals\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 03: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Context & Lifecycle Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Global Context Proxies (`A-R-C-G`)
        *   *Sub-section (H3)*: 2. Request Lifecycle Order (`B-V-A-T`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Request Latency Audit & Header Injection
        *   *Sub-section (H3)*: 2. Guaranteed Database Connection Teardown
        *   *Sub-section (H3)*: 3. Injecting Template Globals
        *   *Sub-section (H3)*: 4. Manually Pushing Contexts in CLI Scripts / Tests
*   **Title (H1)**: Pushing App Context
*   **Title (H1)**: Pushing Request Context

### 📄 File: [5. Practice and Interview Questions.md](DAY 03 - Request Lifecycle and Context Locals\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 03: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a "Context" in Flask in simple terms?
        *   *Sub-section (H3)*: Q2: Why are standard Python global variables dangerous in web applications?
        *   *Sub-section (H3)*: Q3: What is Flask's `g` object and what is it used for?
        *   *Sub-section (H3)*: Q4: What is the difference between `@app.before_request` and `@app.teardown_request`?
        *   *Sub-section (H3)*: Q5: How do you pass global variables to all Jinja2 HTML templates automatically?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `g` and `session` in Flask?
        *   *Sub-section (H3)*: Q7: Explain what happens if `@app.before_request` returns a response object instead of `None`.
        *   *Sub-section (H3)*: Q8: Compare `@app.after_request` and `@app.teardown_request`. When would you use each?
        *   *Sub-section (H3)*: Q9: What error occurs when accessing `current_app` outside an HTTP request, and how do you fix it in CLI scripts?
        *   *Sub-section (H3)*: Q10: How do you simulate an incoming HTTP request in unit tests to test `request.args`?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is a `LocalProxy` in Flask and how does it prevent race conditions in multi-threaded web servers?
        *   *Sub-section (H3)*: Q12: Why shouldn't heavy database connections or socket objects be stored inside the `session` object?
        *   *Sub-section (H3)*: Q13: Can multiple `@app.before_request` functions be registered, and in what order do they execute?
        *   *Sub-section (H3)*: Q14: How does Flask 3.x handle context isolation in asynchronous (`async`/`await`) routes?
        *   *Sub-section (H3)*: Q15: Write a custom lifecycle hook pattern that measures database query duration on `g`.

## 📁 DAY 04 - Jinja2 Templating Engine Masterclass

### 📄 File: [0. Jinja2 Templating Fundamentals for Beginners.md](DAY 04 - Jinja2 Templating Engine Masterclass\0. Jinja2 Templating Fundamentals for Beginners.md)
*   **Title (H1)**: Day 04 - Module 0: Jinja2 Templating Fundamentals for Beginners
    *   **Section (H2)**: 1. What is `render_template()` in Flask?
        *   *Sub-section (H3)*: 🔍 Definition & Purpose
*   **Title (H1)**: Looks inside 'templates/' folder for 'home.html'
        *   *Sub-section (H3)*: 🔍 How it Works:
    *   **Section (H2)**: 2. What is Jinja2 in Simple Words?
        *   *Sub-section (H3)*: Why is Jinja2 Used?
*   **Title (H1)**: app.py (Flask Python Backend)
    *   **Section (H2)**: 3. Jinja2 Syntax Guide
    *   **Section (H2)**: 4. Control Flow in Jinja2 (`if`, `else`, `for`)
        *   *Sub-section (H3)*: 🌟 1. Using `if` and `else` in Jinja2
        *   *Sub-section (H3)*: 🔁 2. Using `for` Loop in Jinja2
    *   **Section (H2)**: 5. Flask Project Folder Structure & Static Files
        *   *Sub-section (H3)*: 📄 Loading Static Files with `url_for('static', filename='...')`
    *   **Section (H2)**: 6. Template Inheritance (`{% extends %}` & `{% block %}`)
        *   *Sub-section (H3)*: 📄 `templates/base.html` (Master Layout)
        *   *Sub-section (H3)*: 📄 `templates/home.html` (Child Page)
        *   *Sub-section (H3)*: 📄 `templates/about.html` (Child Page)
    *   **Section (H2)**: 7. Reusable Components with `{% include %}`
        *   *Sub-section (H3)*: ⚖️ Inheritance (`extends`) vs Inclusion (`include`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Jinja2 Fundamentals, Control Flow and Filters.md](DAY 04 - Jinja2 Templating Engine Masterclass\1. Jinja2 Fundamentals, Control Flow and Filters.md)
*   **Title (H1)**: Day 04 - Module 1: Jinja2 Fundamentals, Control Flow & Filters
    *   **Section (H2)**: 1. How Jinja2 Compiles Templates Under the Hood
    *   **Section (H2)**: 2. Delimiters & Whitespace Control
    *   **Section (H2)**: 3. Control Flow & The `loop` Helper Variable
        *   *Sub-section (H3)*: 1. Conditionals (`if / elif / else`)
        *   *Sub-section (H3)*: 2. Loops & The `loop` Metadata Object
    *   **Section (H2)**: 4. Filters & Custom Filter/Test Registration
        *   *Sub-section (H3)*: Essential Built-in Filters
        *   *Sub-section (H3)*: Registering Custom Jinja Filters & Tests
*   **Title (H1)**: 1. Custom Filter using Decorator (Used as {{ price|currency('$') }})
*   **Title (H1)**: 2. Custom Test using Decorator (Used as {% if number is prime %})
    *   **Section (H2)**: 5. Autoescaping & XSS Security
        *   *Sub-section (H3)*: Overriding Autoescaping Safely
*   **Title (H1)**: Safe: Mark trusted HTML in Python code
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Template Inheritance, Macros and Context Processors.md](DAY 04 - Jinja2 Templating Engine Masterclass\2. Template Inheritance, Macros and Context Processors.md)
*   **Title (H1)**: Day 04 - Module 2: Template Inheritance, Macros & Dynamic Layouts
    *   **Section (H2)**: 1. Template Inheritance Architecture
        *   *Sub-section (H3)*: 1. Base Layout (`templates/base.html`)
        *   *Sub-section (H3)*: 2. Child Template (`templates/dashboard.html`)
    *   **Section (H2)**: 2. Reusable UI Components with Jinja2 Macros
        *   *Sub-section (H3)*: 1. Defining Macros (`templates/macros.html`)
        *   *Sub-section (H3)*: 2. Importing & Using Macros in Templates
    *   **Section (H2)**: 3. Template Includes (`{% include %}`) vs. Macros
        *   *Sub-section (H3)*: 1. Includes (`{% include %}`)
        *   *Sub-section (H3)*: 2. Macros (`{% macro %}`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 04 - Jinja2 Templating Engine Masterclass\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 04: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Jinja2 Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Jinja2 Syntax Delimiters (`E-S-C-W`)
        *   *Sub-section (H3)*: 2. Useful `loop` Helper Properties
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Template Inheritance Skeleton
        *   *Sub-section (H3)*: 2. Custom Filter & Test Registration
*   **Title (H1)**: Custom Filter (Used as {{ val|currency }})
*   **Title (H1)**: Custom Test (Used as {% if val is even_num %})
        *   *Sub-section (H3)*: 3. Reusable Macro Definition & Usage

### 📄 File: [5. Practice and Interview Questions.md](DAY 04 - Jinja2 Templating Engine Masterclass\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 04: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is Jinja2 and why does Flask use it?
        *   *Sub-section (H3)*: Q2: What is the difference between `{{ ... }}` and `{% ... %}` in Jinja2?
        *   *Sub-section (H3)*: Q3: What is Template Inheritance and why is it useful?
        *   *Sub-section (H3)*: Q4: How do comments work in Jinja2 templates?
        *   *Sub-section (H3)*: Q5: How do you pass variables from Python into a Jinja2 template?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is a Jinja2 Filter and how do you apply one?
        *   *Sub-section (H3)*: Q7: What does the `loop.cycle()` method do inside a Jinja2 `for` loop?
        *   *Sub-section (H3)*: Q8: What is the difference between a Jinja2 Macro and an Include (`{% include %}`)?
        *   *Sub-section (H3)*: Q9: How do you register a custom filter in Flask? Show both decorator and direct assignment syntax.
*   **Title (H1)**: 1. Decorator Syntax
*   **Title (H1)**: 2. Direct Assignment Syntax
        *   *Sub-section (H3)*: Q10: How do you bind static CSS and JavaScript files in Flask templates safely?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How does Jinja2 compile templates under the hood and why does this boost performance?
        *   *Sub-section (H3)*: Q12: What is `super()` in Jinja2 template inheritance and when would you use it?
        *   *Sub-section (H3)*: Q13: How does Jinja2 protect applications against Cross-Site Scripting (XSS)?
        *   *Sub-section (H3)*: Q14: Explain the security risk of using the `|safe` filter in Jinja2 templates.
        *   *Sub-section (H3)*: Q15: What are Jinja2 Tests and how do they differ from Filters?

## 📁 DAY 05 - Web Forms, Validation and Flask-WTF

### 📄 File: [0. Web Forms and Validation Fundamentals for Beginners.md](DAY 05 - Web Forms, Validation and Flask-WTF\0. Web Forms and Validation Fundamentals for Beginners.md)
*   **Title (H1)**: Day 05 - Module 0: Web Forms & Validation Fundamentals for Beginners
    *   **Section (H2)**: 1. What is a Web Form in Plain English?
    *   **Section (H2)**: 2. The Nightmare of Raw HTML Form Handling 😫
*   **Title (H1)**: MANUAL FORM HANDLING (PAINFUL & DANGEROUS!)
*   **Title (H1)**: 1. Manual Validation: Check if empty
*   **Title (H1)**: 2. Manual Validation: Check email format
        *   *Sub-section (H3)*: Why Manual Form Handling Causes Massive Pain:
    *   **Section (H2)**: 3. What is a CSRF Attack? (Cross-Site Request Forgery)
        *   *Sub-section (H3)*: 🏦 The Bank Transfer Analogy
        *   *Sub-section (H3)*: How Flask-WTF Stops CSRF Attacks 🛡️
    *   **Section (H2)**: 4. What is Flask-WTF & WTForms?
        *   *Sub-section (H3)*: The Magic of Flask-WTF:
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. HTML Forms vs Flask-WTF and CSRF Protection.md](DAY 05 - Web Forms, Validation and Flask-WTF\1. HTML Forms vs Flask-WTF and CSRF Protection.md)
*   **Title (H1)**: Day 05 - Module 1: HTML Forms vs Flask-WTF & CSRF Protection
    *   **Section (H2)**: 1. Raw HTML Forms vs. Flask-WTF
    *   **Section (H2)**: 2. Defining WTForms Form Classes
    *   **Section (H2)**: 3. Cross-Site Request Forgery (CSRF) Protection
        *   *Sub-section (H3)*: What is a CSRF Attack?
        *   *Sub-section (H3)*: How Flask-WTF Prevents CSRF
*   **Title (H1)**: Enabling Global CSRF Protection for AJAX / Fetch API Requests
    *   **Section (H2)**: 4. Processing Forms in View Functions
*   **Title (H1)**: Executed ONLY when request is POST AND form data + CSRF token are valid
*   **Title (H1)**: Save user to database...
*   **Title (H1)**: GET request or validation failure: render form with error messages
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Custom Form Validators and File Upload Handling.md](DAY 05 - Web Forms, Validation and Flask-WTF\2. Custom Form Validators and File Upload Handling.md)
*   **Title (H1)**: Day 05 - Module 2: Custom Form Validators & File Upload Handling
    *   **Section (H2)**: 1. Custom Form Validation
        *   *Sub-section (H3)*: 1. In-Line Custom Validators (Method Naming Pattern)
*   **Title (H1)**: Executed automatically when validating `username` field
        *   *Sub-section (H3)*: 2. Standalone Reusable Custom Validators
    *   **Section (H2)**: 2. Secure File Upload Processing
        *   *Sub-section (H3)*: 🚨 Why Unsanitized File Uploads Are Dangerous:
        *   *Sub-section (H3)*: 🛡️ 4-Point Security Checklist for File Uploads:
        *   *Sub-section (H3)*: Implementation Example
*   **Title (H1)**: Enforce Maximum 16 Megabyte File Upload Size
*   **Title (H1)**: 1. Sanitize Filename to strip directory traversal characters (../)
*   **Title (H1)**: 2. Save file safely to disk
    *   **Section (H2)**: 3. Categorized Flash Messaging
*   **Title (H1)**: Sending Categorized Flash Messages
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 05 - Web Forms, Validation and Flask-WTF\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 05: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Web Forms & Security Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Anti-CSRF Protection Lifecycle (`C-S-R-F`)
        *   *Sub-section (H3)*: 2. File Upload Security Checklist (`S-E-C-U-R-E`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. WTForms Form Definition with In-line Validator
*   **Title (H1)**: In-line Custom Validator
        *   *Sub-section (H3)*: 2. Secure File Upload Handler
        *   *Sub-section (H3)*: 3. Form Template Rendering with CSRF & Errors

### 📄 File: [5. Practice and Interview Questions.md](DAY 05 - Web Forms, Validation and Flask-WTF\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 05: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is an HTML Web Form and what is its purpose?
        *   *Sub-section (H3)*: Q2: What is Form Validation and why is it necessary?
        *   *Sub-section (H3)*: Q3: What does CSRF stand for and what is a CSRF attack in simple terms?
        *   *Sub-section (H3)*: Q4: Why is using raw `request.form.get()` inefficient compared to Flask-WTF?
        *   *Sub-section (H3)*: Q5: How do you display a hidden anti-CSRF security token inside a Jinja template?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What does `form.validate_on_submit()` check under the hood?
        *   *Sub-section (H3)*: Q7: How do you implement an in-line custom validator method inside a `FlaskForm` class?
        *   *Sub-section (H3)*: Q8: Why is `secure_filename()` necessary when saving user-uploaded files?
        *   *Sub-section (H3)*: Q9: How do you restrict the maximum file upload size in a Flask application?
*   **Title (H1)**: Limit upload size to 16 Megabytes
        *   *Sub-section (H3)*: Q10: What HTML attribute is required on `<form>` elements to support file uploads?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How does Flask-WTF generate and verify anti-CSRF tokens cryptographically?
        *   *Sub-section (H3)*: Q12: How do you pass custom parameters into a standalone WTForms validator function?
        *   *Sub-section (H3)*: Q13: How can you enable CSRF protection for non-HTML form requests, such as AJAX or Fetch API calls?
        *   *Sub-section (H3)*: Q14: How do categorized flash messages work in Flask, and how are they rendered in Jinja2 templates?
        *   *Sub-section (H3)*: Q15: How do `FileRequired()` and `FileAllowed()` validators work in Flask-WTF?

## 📁 DAY 06 - Database Fundamentals and Flask-SQLAlchemy

### 📄 File: [0. Database Fundamentals for Absolute Beginners.md](DAY 06 - Database Fundamentals and Flask-SQLAlchemy\0. Database Fundamentals for Absolute Beginners.md)
*   **Title (H1)**: Day 06 - Module 0: Database Fundamentals & mysql-connector-python for Beginners
    *   **Section (H2)**: 1. What is a Database in Plain English?
    *   **Section (H2)**: 2. What is a Relational Database (MySQL)?
        *   *Sub-section (H3)*: Key MySQL Relational Database Concepts Table
    *   **Section (H2)**: 3. What is `mysql-connector-python`?
        *   *Sub-section (H3)*: Installing `mysql-connector-python`:
    *   **Section (H2)**: 4. Connection Parameters in `mysql-connector-python`
*   **Title (H1)**: MySQL Server Configuration
*   **Title (H1)**: Establish Connection
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Relational Mapping and Model Definition.md](DAY 06 - Database Fundamentals and Flask-SQLAlchemy\1. Relational Mapping and Model Definition.md)
*   **Title (H1)**: Day 01 - Module 1: Database Setup & Table Definition with mysql-connector-python
    *   **Section (H2)**: 1. Database Connection Helper Pattern
    *   **Section (H2)**: 2. Table Creation with Raw SQL (`CREATE TABLE IF NOT EXISTS`)
*   **Title (H1)**: SQL Table Definition Script
    *   **Section (H2)**: 3. MySQL Data Types Reference Table
    *   **Section (H2)**: 4. MySQL Column Constraints & Options
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. CRUD Operations and Database Session Management.md](DAY 06 - Database Fundamentals and Flask-SQLAlchemy\2. CRUD Operations and Database Session Management.md)
*   **Title (H1)**: Day 06 - Module 2: Complete MySQL CRUD Operations with mysql-connector-python
    *   **Section (H2)**: 1. What is CRUD in Plain English?
    *   **Section (H2)**: 2. Complete `mysql-connector-python` CRUD Implementation
        *   *Sub-section (H3)*: 1. Create (Insert New Record into MySQL)
*   **Title (H1)**: SAFE: Use parameterized placeholders (%s)
        *   *Sub-section (H3)*: 2. Read (Fetch Records from MySQL)
*   **Title (H1)**: A. Read ALL Records
*   **Title (H1)**: B. Read SINGLE Record by ID
        *   *Sub-section (H3)*: 3. Update (Modify Existing MySQL Record)
        *   *Sub-section (H3)*: 4. Delete (Remove MySQL Record)
    *   **Section (H2)**: 3. SQL Injection Defense Rule 🛡️
*   **Title (H1)**: ❌ VULNERABLE TO SQL INJECTION (DO NOT DO THIS!):
*   **Title (H1)**: ✅ 100% SAFE PARAMETERIZED QUERY (DO THIS!):
    *   **Section (H2)**: 4. Transaction Error Handling & Rollback (`conn.rollback()`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 06 - Database Fundamentals and Flask-SQLAlchemy\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 06: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Zero-Knowledge Acronym Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. `mysql-connector-python` Pipeline (`C-E-F-C`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Database Connection Helper
        *   *Sub-section (H3)*: 2. Parameterized CRUD Operations
*   **Title (H1)**: CREATE
*   **Title (H1)**: READ (Dict Cursor)
*   **Title (H1)**: UPDATE
*   **Title (H1)**: DELETE

### 📄 File: [5. Practice and Interview Questions.md](DAY 06 - Database Fundamentals and Flask-SQLAlchemy\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 06: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is `mysql-connector-python` and why is it needed in Flask applications?
        *   *Sub-section (H3)*: Q2: Why must you call `conn.commit()` after executing an `INSERT`, `UPDATE`, or `DELETE` query?
        *   *Sub-section (H3)*: Q3: What is the difference between `cursor.fetchall()` and `cursor.fetchone()`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q4: Why is `cursor = conn.cursor(dictionary=True)` recommended when building Flask web apps?
        *   *Sub-section (H3)*: Q5: Explain how `%s` placeholders prevent SQL Injection attacks.
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q6: What is Connection Pooling in `mysql-connector-python`, and why is it essential in high-traffic Flask apps?
        *   *Sub-section (H3)*: Q7: How do you handle database errors and transaction rollbacks using `mysql.connector.Error`?

## 📁 DAY 07 - Advanced Querying, Filtering and Transactions

### 📄 File: [0. Querying, Filtering and Pagination Fundamentals for Beginners.md](DAY 07 - Advanced Querying, Filtering and Transactions\0. Querying, Filtering and Pagination Fundamentals for Beginners.md)
*   **Title (H1)**: Day 07 - Module 0: Querying, Filtering & Pagination Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Database Querying & Filtering in Plain English?
    *   **Section (H2)**: 2. Common SQLAlchemy Filter Operators Table
    *   **Section (H2)**: 3. Combining Logical Filters (`and_`, `or_`, `not_`)
*   **Title (H1)**: Find Active Users who are EITHER Admins OR Editors
    *   **Section (H2)**: 4. Why Pagination is Crucial for Performance
*   **Title (H1)**: Fetches Page #2 with 20 items per page
*   **Title (H1)**: Pagination Metadata:
    *   **Section (H2)**: 5. Database Transactions & Rollbacks (`db.session.rollback()`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Complex Queries and Filter Operators.md](DAY 07 - Advanced Querying, Filtering and Transactions\1. Complex Queries and Filter Operators.md)
*   **Title (H1)**: Day 07 - Module 1: Complex Queries & Filter Operators
    *   **Section (H2)**: 1. Filter Expressions in SQLAlchemy 2.0+
*   **Title (H1)**: Basic Filter Statement
    *   **Section (H2)**: 2. Comparison & Pattern Match Operators
    *   **Section (H2)**: 3. Combining Logical Operators (`and_`, `or_`, `not_`)
*   **Title (H1)**: Complex Query Example:
*   **Title (H1)**: Find active products in ('Electronics', 'Computers')
*   **Title (H1)**: WHERE (Price is between $100 and $500 OR Rating >= 4.5)
    *   **Section (H2)**: 4. Sorting Results (`order_by`)
*   **Title (H1)**: 1. Single Column Ascending (Low to High) / Descending (High to Low)
*   **Title (H1)**: 2. Multi-Column Sorting (Sort by Category A-Z, then Price High to Low)
    *   **Section (H2)**: 5. Result Slicing Bounds (`limit` and `offset`)
*   **Title (H1)**: Fetch 10 records starting from row 20 (Simulates Page 3 offset)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Pagination, Aggregations and Transaction Control.md](DAY 07 - Advanced Querying, Filtering and Transactions\2. Pagination, Aggregations and Transaction Control.md)
*   **Title (H1)**: Day 07 - Module 2: Pagination, Aggregations & Transaction Control
    *   **Section (H2)**: 1. Flask-SQLAlchemy Pagination Architecture
*   **Title (H1)**: Create Paginated Query Statement
        *   *Sub-section (H3)*: The `Pagination` Helper Object Attributes
    *   **Section (H2)**: 2. SQL Aggregations (`func`) & `group_by`
*   **Title (H1)**: 1. Basic Aggregation (Average Price across all products)
*   **Title (H1)**: 2. Grouped Aggregation with HAVING clause
*   **Title (H1)**: Get Category, Product Count, and Avg Price WHERE Product Count > 2
    *   **Section (H2)**: 3. Nested Transactions & Savepoints (`begin_nested()`)
*   **Title (H1)**: Outer Transaction: Create Order
*   **Title (H1)**: Savepoint (Nested Transaction Checkpoint)
*   **Title (H1)**: Sub-operation: Add bonus gift item
*   **Title (H1)**: Rollback ONLY to savepoint; parent 'order' remains safe!
*   **Title (H1)**: Commit full parent transaction
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 07 - Advanced Querying, Filtering and Transactions\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 07: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Advanced Querying & Filtering Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. SQL Query Statement Pipeline Order (`S-W-G-H-O-L`)
        *   *Sub-section (H3)*: 2. Common `func` Aggregation Functions
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Multi-Condition Filtering Query
        *   *Sub-section (H3)*: 2. Flask-SQLAlchemy `db.paginate()` Usage
        *   *Sub-section (H3)*: 3. Nested Transaction Savepoint (`begin_nested()`)

### 📄 File: [5. Practice and Interview Questions.md](DAY 07 - Advanced Querying, Filtering and Transactions\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 07: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is Database Filtering in simple terms?
        *   *Sub-section (H3)*: Q2: What is the difference between `like()` and `ilike()` in SQLAlchemy?
        *   *Sub-section (H3)*: Q3: What is Pagination and why is it used on websites?
        *   *Sub-section (H3)*: Q4: What is an Aggregation in SQL?
        *   *Sub-section (H3)*: Q5: How do you search for records containing a specific keyword anywhere in their name?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does `db.paginate()` calculate the total page count under the hood?
        *   *Sub-section (H3)*: Q7: How do you perform multi-column ordering in SQLAlchemy 2.0?
        *   *Sub-section (H3)*: Q8: How do `and_()` and comma-separated arguments inside `where()` differ?
        *   *Sub-section (H3)*: Q9: How do you search for `NULL` or non-`NULL` values using SQLAlchemy?
*   **Title (H1)**: Find products without a category
*   **Title (H1)**: Find products with a valid category
        *   *Sub-section (H3)*: Q10: How do you retrieve a distinct list of values for a specific column?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is the difference between `WHERE` and `HAVING` clauses in SQL queries?
*   **Title (H1)**: Select categories with average price > 100 where stock > 0
        *   *Sub-section (H3)*: Q12: What is a Savepoint in database transaction management and how is it used in SQLAlchemy?
        *   *Sub-section (H3)*: Q13: What is the difference between `func.count(1)` and `func.count(Model.column_name)`?
        *   *Sub-section (H3)*: Q14: How do you perform case-insensitive exact matching in SQLAlchemy?
        *   *Sub-section (H3)*: Q15: How do `limit()` and `offset()` work together for manual API pagination?

## 📁 DAY 08 - Advanced Relationships, Cascades and Lazy Loading

### 📄 File: [0. Database Relationships and Performance Fundamentals for Beginners.md](DAY 08 - Advanced Relationships, Cascades and Lazy Loading\0. Database Relationships and Performance Fundamentals for Beginners.md)
*   **Title (H1)**: Day 08 - Module 0: Database Relationships & Performance Fundamentals for Beginners
    *   **Section (H2)**: 1. What is a Database Relationship in Plain English?
    *   **Section (H2)**: 2. The 3 Types of Database Relationships
        *   *Sub-section (H3)*: How Many-to-Many Works: The Junction Table
    *   **Section (H2)**: 3. What is Cascade Delete?
    *   **Section (H2)**: 4. What is the N+1 Query Problem?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. One-to-Many, Many-to-Many and Cascades.md](DAY 08 - Advanced Relationships, Cascades and Lazy Loading\1. One-to-Many, Many-to-Many and Cascades.md)
*   **Title (H1)**: Day 08 - Module 1: Relationships & Cascade Operations
    *   **Section (H2)**: 1. One-to-Many & One-to-One Mappings
        *   *Sub-section (H3)*: One-to-Many Relationship
*   **Title (H1)**: One-to-Many: Author has multiple posts
*   **Title (H1)**: 'backref' automatically adds an '.author' attribute to Post instances
        *   *Sub-section (H3)*: One-to-One Relationship
*   **Title (H1)**: uselist=False instructs SQLAlchemy to treat user.profile as a single object, not a list
    *   **Section (H2)**: 2. Many-to-Many Relationships
*   **Title (H1)**: Association Table linking Posts and Tags
*   **Title (H1)**: Point to Tag model using 'secondary=post_tags' parameter
    *   **Section (H2)**: 3. Understanding Cascade Operations
*   **Title (H1)**: Cascade: If Post is deleted OR a Comment is removed from post.comments list, delete Comment from DB!
        *   *Sub-section (H3)*: Cascade Options Matrix
    *   **Section (H2)**: 4. `backref` vs. `back_populates`
*   **Title (H1)**: Modern SQLAlchemy 2.0 Standard: back_populates Example
*   **Title (H1)**: Points explicitly to 'parent' attribute on Child
*   **Title (H1)**: Points explicitly to 'children' attribute on Parent
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Lazy Loading Strategies and Performance Impact.md](DAY 08 - Advanced Relationships, Cascades and Lazy Loading\2. Lazy Loading Strategies and Performance Impact.md)
*   **Title (H1)**: Day 08 - Module 2: Lazy Loading Strategies & Performance Tuning
    *   **Section (H2)**: 1. The N+1 Query Problem Deep Dive
*   **Title (H1)**: Query 1: Fetch 100 Posts
*   **Title (H1)**: Triggers 1 SEPARATE SELECT query per post to fetch author! (100 extra queries!)
*   **Title (H1)**: Total DB Queries Executed: 1 + 100 = 101 queries!
    *   **Section (H2)**: 2. SQLAlchemy Loading Strategies Matrix
    *   **Section (H2)**: 3. Explicit Eager Loading (`selectinload` & `joinedload`)
*   **Title (H1)**: 1. Eager Load Collection using selectinload (2 SQL queries total for 100 posts)
*   **Title (H1)**: Fast: Comments already pre-loaded into memory!
*   **Title (H1)**: 2. Eager Load Scalar Relationship using joinedload (1 SQL JOIN query total)
    *   **Section (H2)**: 4. Dynamic Loading for Massive Collections (`lazy='dynamic'`)
*   **Title (H1)**: Returns query object instead of list
*   **Title (H1)**: Filter and paginate directly on the relationship attribute!
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 08 - Advanced Relationships, Cascades and Lazy Loading\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 08: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Relationships & Performance Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Lazy Loading Strategies (`S-J-S-D`)
        *   *Sub-section (H3)*: 2. Cascade Options (`A-D-O`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. One-to-Many with Cascade Delete-Orphan
        *   *Sub-section (H3)*: 2. Many-to-Many Association Table
        *   *Sub-section (H3)*: 3. Explicit Eager Loading Query

### 📄 File: [5. Practice and Interview Questions.md](DAY 08 - Advanced Relationships, Cascades and Lazy Loading\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 08: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a Database Relationship in simple terms?
        *   *Sub-section (H3)*: Q2: What is a Foreign Key?
        *   *Sub-section (H3)*: Q3: What is the difference between a One-to-Many and a Many-to-Many relationship?
        *   *Sub-section (H3)*: Q4: What is Cascade Delete and why is it useful?
        *   *Sub-section (H3)*: Q5: Where do you declare `db.ForeignKey` versus `db.relationship`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the N+1 query problem and how do you resolve it in SQLAlchemy?
        *   *Sub-section (H3)*: Q7: What is the difference between `backref` and `back_populates` in `db.relationship`?
        *   *Sub-section (H3)*: Q8: What does `cascade='all, delete-orphan'` mean and how does `delete-orphan` differ from `delete`?
        *   *Sub-section (H3)*: Q9: How do you create a One-to-One relationship in Flask-SQLAlchemy?
        *   *Sub-section (H3)*: Q10: How do `lazy='joined'` and `lazy='selectin'` differ under the hood?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: When should you use `lazy='dynamic'` on a relationship?
        *   *Sub-section (H3)*: Q12: How do you handle Many-to-Many relationships that require additional payload columns (e.g. `assigned_date`, `role`)?
        *   *Sub-section (H3)*: Q13: What is the difference between DB-level foreign key CASCADE (`ondelete='CASCADE'`) and ORM-level `cascade='all, delete'`?
        *   *Sub-section (H3)*: Q14: What happens if you access a `lazy='select'` relationship attribute after `db.session.close()`?
        *   *Sub-section (H3)*: Q15: How do you write a self-referential relationship (e.g. Category parent/child trees or Manager/Employee hierarchies)?

## 📁 DAY 09 - Database Migrations with Flask-Migrate

### 📄 File: [0. Database Migrations Fundamentals for Beginners.md](DAY 09 - Database Migrations with Flask-Migrate\0. Database Migrations Fundamentals for Beginners.md)
*   **Title (H1)**: Day 09 - Module 0: Database Migrations Fundamentals for Beginners
    *   **Section (H2)**: 1. What is a Database Migration in Plain English?
    *   **Section (H2)**: 2. Why `db.create_all()` Fails in Production Apps
    *   **Section (H2)**: 3. What are Alembic and Flask-Migrate?
    *   **Section (H2)**: 4. The 4 Essential Migration Commands (`I-M-U-D`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Schema Evolution and Flask-Migrate CLI.md](DAY 09 - Database Migrations with Flask-Migrate\1. Schema Evolution and Flask-Migrate CLI.md)
*   **Title (H1)**: Day 09 - Module 1: Schema Evolution & Flask-Migrate CLI
    *   **Section (H2)**: 1. Initializing Flask-Migrate in Python
*   **Title (H1)**: Bind Flask-Migrate extension to Flask app and SQLAlchemy db
    *   **Section (H2)**: 2. Complete `flask db` CLI Command Reference
    *   **Section (H2)**: 3. Standard Migration Lifecycle Workflow
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Alembic Under the Hood and Data Migrations.md](DAY 09 - Database Migrations with Flask-Migrate\2. Alembic Under the Hood and Data Migrations.md)
*   **Title (H1)**: Day 09 - Module 2: Alembic Under the Hood & Data Migrations
    *   **Section (H2)**: 1. Inside the `migrations/` Directory
    *   **Section (H2)**: 2. The `alembic_version` Tracking Table
    *   **Section (H2)**: 3. Structure of an Autogenerated Revision Script
*   **Title (H1)**: Executed when running `flask db upgrade`
*   **Title (H1)**: Executed when running `flask db downgrade`
    *   **Section (H2)**: 4. Manual Data Migrations (Populating Existing Rows)
*   **Title (H1)**: Step 1: Add column as nullable initially
*   **Title (H1)**: Step 2: Populate default value for all existing database rows!
*   **Title (H1)**: Step 3: Alter column constraint to NOT NULL
    *   **Section (H2)**: 5. Handling SQLite Constraints (`render_as_batch=True`)
*   **Title (H1)**: Enable Batch Mode for SQLite compatibility
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 09 - Database Migrations with Flask-Migrate\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 09: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Database Migrations Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: Migration Lifecycle Workflow (`I-M-U-D`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-Migrate Python Setup (with SQLite Batch Mode)
*   **Title (H1)**: Always use render_as_batch=True for SQLite support!
        *   *Sub-section (H3)*: 2. Manual Data Migration inside Revision Script (`upgrade()`)
*   **Title (H1)**: 1. Add column as nullable initially
*   **Title (H1)**: 2. Populate existing rows with default data!
*   **Title (H1)**: 3. Enforce NOT NULL constraint
        *   *Sub-section (H3)*: 3. Inspection & Version Checking CLI Commands
*   **Title (H1)**: Show active database revision hash
*   **Title (H1)**: Show latest available script revision hash
*   **Title (H1)**: Show full migration history
*   **Title (H1)**: Force DB version pointer to specific revision without running SQL

### 📄 File: [5. Practice and Interview Questions.md](DAY 09 - Database Migrations with Flask-Migrate\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 09: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a Database Migration in simple terms?
        *   *Sub-section (H3)*: Q2: Why should `db.create_all()` NEVER be used in production applications?
        *   *Sub-section (H3)*: Q3: What is the difference between Alembic and Flask-Migrate?
        *   *Sub-section (H3)*: Q4: What are the 4 main CLI commands used in Flask-Migrate?
        *   *Sub-section (H3)*: Q5: Where are autogenerated migration scripts stored?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does Alembic know which migrations have already been applied to a database?
        *   *Sub-section (H3)*: Q7: What are `upgrade()` and `downgrade()` functions inside revision scripts?
        *   *Sub-section (H3)*: Q8: What does `flask db stamp <revision_hash>` do and when would you use it?
        *   *Sub-section (H3)*: Q9: What schema changes CANNOT be autogenerated by `flask db migrate`?
        *   *Sub-section (H3)*: Q10: How do `flask db current` and `flask db heads` differ?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why does SQLite fail on standard `ALTER TABLE` statements and how does `render_as_batch=True` solve it?
        *   *Sub-section (H3)*: Q12: How do you safely add a non-nullable (`NOT NULL`) column to a database table that already contains millions of live rows?
*   **Title (H1)**: 1. Add column as nullable initially
*   **Title (H1)**: 2. Populate default data for all existing rows!
*   **Title (H1)**: 3. Enforce NOT NULL constraint
        *   *Sub-section (H3)*: Q13: What strategy should be used to achieve zero-downtime database migrations during production deployments?
        *   *Sub-section (H3)*: Q14: What is `env.py` inside the `migrations/` directory and why is it important?
        *   *Sub-section (H3)*: Q15: What happens if two developers on a team create separate migrations simultaneously resulting in multiple "heads"?

## 📁 DAY 10 - Multiple Databases, Binds and Raw SQL

### 📄 File: [0. Multiple Databases and Raw SQL Fundamentals for Beginners.md](DAY 10 - Multiple Databases, Binds and Raw SQL\0. Multiple Databases and Raw SQL Fundamentals for Beginners.md)
*   **Title (H1)**: Day 10 - Module 0: Multiple Databases & Raw SQL Fundamentals for Beginners
    *   **Section (H2)**: 1. Why Would an Application Need More Than 1 Database?
    *   **Section (H2)**: 2. What is a Database Bind in Flask-SQLAlchemy?
*   **Title (H1)**: Primary Default Database
*   **Title (H1)**: Secondary Additional Databases (BINDS)
*   **Title (H1)**: Belongs to Primary Database automatically
*   **Title (H1)**: Explicitly bound to the 'audit' database!
    *   **Section (H2)**: 3. What is Raw SQL & Parameter Binding?
        *   *Sub-section (H3)*: ⚠️ The Hacker Danger: SQL Injection
*   **Title (H1)**: DANGEROUS! Never concatenate raw strings!
        *   *Sub-section (H3)*: ✅ The Solution: Parameter Binding with `text()`
*   **Title (H1)**: SAFE! Parameter binding automatically sanitizes input!
    *   **Section (H2)**: 4. What is Connection Pooling?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Multiple Database Binds and Raw SQL.md](DAY 10 - Multiple Databases, Binds and Raw SQL\1. Multiple Database Binds and Raw SQL.md)
*   **Title (H1)**: Day 10 - Module 1: Multiple Database Binds & Raw SQL
    *   **Section (H2)**: 1. Multiple Database Binds Architecture
*   **Title (H1)**: Primary Default Database URI
*   **Title (H1)**: Secondary Database Binds Dictionary
    *   **Section (H2)**: 2. Binding Models to Specific Databases (`__bind_key__`)
*   **Title (H1)**: 1. Connected to Primary Database (primary.db)
*   **Title (H1)**: 2. Connected to Analytics Database (analytics.db)
    *   **Section (H2)**: 3. Safe Raw SQL Execution (`sqlalchemy.text`)
*   **Title (H1)**: SAFE: Using text() with bound parameter placeholders (:search_term)
*   **Title (H1)**: Execute query passing parameters dictionary
*   **Title (H1)**: Process Row objects
    *   **Section (H2)**: 4. Retrieving Underlying Engines (`db.get_engine`)
*   **Title (H1)**: Get Engine instance for 'analytics' database bind
*   **Title (H1)**: Execute raw SQL directly against analytics engine
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Database Connection Pooling and Session Scopes.md](DAY 10 - Multiple Databases, Binds and Raw SQL\2. Database Connection Pooling and Session Scopes.md)
*   **Title (H1)**: Day 10 - Module 2: Connection Pooling & Session Scopes
    *   **Section (H2)**: 1. Connection Pool Parameters (`SQLALCHEMY_ENGINE_OPTIONS`)
    *   **Section (H2)**: 2. SQLAlchemy Connection Pool Implementations
    *   **Section (H2)**: 3. Session Scopes & Preventing Connection Leaks
*   **Title (H1)**: Return connection back to the connection pool!
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 10 - Multiple Databases, Binds and Raw SQL\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 10: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Multi-Database & Raw SQL Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: Multi-Database Configuration Steps (`B-I-N-D`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Multi-Database Configuration & Model Binding
*   **Title (H1)**: Uses Primary DB
*   **Title (H1)**: Uses Audit DB
        *   *Sub-section (H3)*: 2. Safe Raw SQL Query with Parameter Binding
        *   *Sub-section (H3)*: 3. Production Connection Pool Configuration

### 📄 File: [5. Practice and Interview Questions.md](DAY 10 - Multiple Databases, Binds and Raw SQL\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 10: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: Why would a real-world web application use more than one database?
        *   *Sub-section (H3)*: Q2: What is a Database Bind in Flask-SQLAlchemy?
        *   *Sub-section (H3)*: Q3: What is Raw SQL and when would you use it instead of ORM models?
        *   *Sub-section (H3)*: Q4: What is Connection Pooling in simple terms?
        *   *Sub-section (H3)*: Q5: How do you assign an ORM model class to a secondary database bind?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How do you safely execute raw SQL queries in Flask-SQLAlchemy to prevent SQL Injection?
        *   *Sub-section (H3)*: Q7: What does `db.create_all()` do when multiple database binds are configured?
        *   *Sub-section (H3)*: Q8: What is the difference between `fetchone()`, `fetchall()`, and `scalar()` on a raw SQL result object?
        *   *Sub-section (H3)*: Q9: How do you retrieve the underlying SQLAlchemy `Engine` for a specific database bind?
        *   *Sub-section (H3)*: Q10: What happens if a raw SQL query raises a database error during a transaction?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Can a single `db.session.commit()` perform an atomic two-phase commit across multiple database binds?
        *   *Sub-section (H3)*: Q12: Explain `pool_size` and `max_overflow` in `SQLALCHEMY_ENGINE_OPTIONS`.
        *   *Sub-section (H3)*: Q13: Why is `NullPool` recommended for Serverless environments (like AWS Lambda or Google Cloud Functions)?
        *   *Sub-section (H3)*: Q14: How do you prevent Connection Leaks in long-running background tasks or standalone CLI scripts?
        *   *Sub-section (H3)*: Q15: How do you configure Flask-Migrate when using multiple database binds?

## 📁 DAY 11 - Modular Development with Flask Blueprints

### 📄 File: [0. Modular Architecture and Blueprints Fundamentals for Beginners.md](DAY 11 - Modular Development with Flask Blueprints\0. Modular Architecture and Blueprints Fundamentals for Beginners.md)
*   **Title (H1)**: Day 11 - Module 0: Modular Architecture & Blueprints Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Modular Architecture in Plain English?
    *   **Section (H2)**: 2. Why Single-File `app.py` Scripts Fail at Scale
    *   **Section (H2)**: 3. What is a Flask Blueprint?
    *   **Section (H2)**: 4. Can a Blueprint Run by Itself?
    *   **Section (H2)**: 5. How `url_for()` Works with Blueprints (Namespacing)
*   **Title (H1)**: Route inside auth blueprint:
*   **Title (H1)**: Inside HTML templates or python code:
*   **Title (H1)**: Instead of: url_for('login')
*   **Title (H1)**: You MUST use: url_for('auth.login')  <-- 'blueprint_name.function_name'
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Modularizing Large Applications.md](DAY 11 - Modular Development with Flask Blueprints\1. Modularizing Large Applications.md)
*   **Title (H1)**: Day 11 - Module 1: Modularizing Large Applications
    *   **Section (H2)**: 1. Defining a Flask Blueprint
*   **Title (H1)**: Define Blueprint instance
*   **Title (H1)**: Route registered on the blueprint (accessible at /auth/login)
*   **Title (H1)**: Route registered on the blueprint (accessible at /auth/logout)
    *   **Section (H2)**: 2. Registering Blueprints on the Main Application
*   **Title (H1)**: Import blueprint objects from sub-modules
*   **Title (H1)**: Register Blueprints onto Flask application
    *   **Section (H2)**: 3. Blueprint-Specific Request Hooks & Handlers
*   **Title (H1)**: Executes BEFORE any route handler inside auth_bp!
*   **Title (H1)**: App-level error handler registered by this blueprint
    *   **Section (H2)**: 4. Enterprise Package Directory Layout
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Blueprint Subdomains and Asset Isolation.md](DAY 11 - Modular Development with Flask Blueprints\2. Blueprint Subdomains and Asset Isolation.md)
*   **Title (H1)**: Day 11 - Module 2: Blueprint Subdomains & Asset Isolation
    *   **Section (H2)**: 1. Subdomain Routing with Blueprints
*   **Title (H1)**: SERVER_NAME is required for Flask subdomain matching during local development
*   **Title (H1)**: Admin Blueprint bound to 'admin' subdomain (admin.mycompany.local:5000)
    *   **Section (H2)**: 2. Template & Static Asset Isolation
    *   **Section (H2)**: 3. Cross-Blueprint URL Generation (`url_for`)
*   **Title (H1)**: 1. Routing to a view function inside the SAME blueprint
*   **Title (H1)**: 2. Routing to a view function in a DIFFERENT blueprint
*   **Title (H1)**: 3. Referencing static assets inside a blueprint
    *   **Section (H2)**: 4. Nesting Blueprints (Parent & Child Modules)
*   **Title (H1)**: Parent API Blueprint (/api)
*   **Title (H1)**: Child v1 Blueprint (/v1)
*   **Title (H1)**: Register child blueprint onto parent blueprint!
*   **Title (H1)**: Register parent blueprint onto main Flask app (Final URL: /api/v1/users)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 11 - Modular Development with Flask Blueprints\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 11: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Blueprints & Modular Architecture Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: Blueprint Lifecycle Steps (`R-E-G-I-S-T-E-R`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Defining & Registering a Blueprint
*   **Title (H1)**: 1. Instantiate Blueprint
*   **Title (H1)**: 2. Register on Main App
        *   *Sub-section (H3)*: 2. Cross-Blueprint `url_for()` References
*   **Title (H1)**: Route to view function in SAME blueprint (relative dot prefix)
*   **Title (H1)**: Route to view function in DIFFERENT blueprint (absolute blueprint.endpoint)
*   **Title (H1)**: Reference static assets inside a blueprint
        *   *Sub-section (H3)*: 3. Blueprint Subdomain & Nested Registration
*   **Title (H1)**: Subdomain Blueprint
*   **Title (H1)**: Nested Blueprints (Flask 2.0+)

### 📄 File: [5. Practice and Interview Questions.md](DAY 11 - Modular Development with Flask Blueprints\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 11: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a Flask Blueprint in simple terms?
        *   *Sub-section (H3)*: Q2: Can a Flask Blueprint run as a standalone web application?
        *   *Sub-section (H3)*: Q3: Why do enterprise developers use Blueprints instead of putting all routes in `app.py`?
        *   *Sub-section (H3)*: Q4: How do you register a Blueprint named `auth_bp` onto a Flask app with a `/auth` prefix?
        *   *Sub-section (H3)*: Q5: How do you generate a URL to a route defined inside a Blueprint?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does `@bp.before_request` differ from `@app.before_request`?
        *   *Sub-section (H3)*: Q7: What is Template Shadowing in Blueprints and how do you prevent it?
        *   *Sub-section (H3)*: Q8: How do relative and absolute `url_for()` references differ inside a Blueprint view function?
        *   *Sub-section (H3)*: Q9: Can you override a Blueprint's `url_prefix` during registration on the main app?
        *   *Sub-section (H3)*: Q10: How do you serve static assets (CSS, JS, images) from inside a specific Blueprint?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do you configure Blueprint Subdomain Routing in Flask?
        *   *Sub-section (H3)*: Q12: How do Nested Blueprints work in Flask 2.0+?
        *   *Sub-section (H3)*: Q13: What is the difference between `@bp.errorhandler` and `@bp.app_errorhandler`?
        *   *Sub-section (H3)*: Q14: How does `@bp.context_processor` work?
        *   *Sub-section (H3)*: Q15: How should Blueprints be structured when implementing the Application Factory Pattern?

## 📁 DAY 12 - Application Factory Pattern and Environment Config

### 📄 File: [0. Application Factory and Config Fundamentals for Beginners.md](DAY 12 - Application Factory Pattern and Environment Config\0. Application Factory and Config Fundamentals for Beginners.md)
*   **Title (H1)**: Day 12 - Module 0: Application Factory & Config Fundamentals for Beginners
    *   **Section (H2)**: 1. What is a Design Pattern in Plain English?
    *   **Section (H2)**: 2. What is the Application Factory Pattern?
*   **Title (H1)**: Old Beginner Way (Global App Instance)
*   **Title (H1)**: Professional Factory Pattern Way
*   **Title (H1)**: Configure app, bind extensions, and register blueprints here...
    *   **Section (H2)**: 3. Why Global `app` Causes Circular Import Bugs
    *   **Section (H2)**: 4. What are Environment Configurations?
    *   **Section (H2)**: 5. Environment Variables & `.env` Files
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Application Factory Pattern.md](DAY 12 - Application Factory Pattern and Environment Config\1. Application Factory Pattern.md)
*   **Title (H1)**: Day 12 - Module 1: Application Factory Pattern
    *   **Section (H2)**: 1. The Deferred Extension Initialization Pattern
*   **Title (H1)**: extensions.py
*   **Title (H1)**: Instantiate extension objects unattached to any app
*   **Title (H1)**: factory.py
*   **Title (H1)**: Bind extensions to active app instance
    *   **Section (H2)**: 2. Complete `create_app()` Factory Signature
*   **Title (H1)**: 1. Load Application Configuration
*   **Title (H1)**: 2. Initialize Extensions
*   **Title (H1)**: 3. Register Blueprints
*   **Title (H1)**: 4. Register Global Error Handlers & Request Hooks
    *   **Section (H2)**: 3. Testing Benefits of the Application Factory
*   **Title (H1)**: test_auth.py
*   **Title (H1)**: Create isolated app for testing
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Multi-Environment Configurations and Dotenv Management.md](DAY 12 - Application Factory Pattern and Environment Config\2. Multi-Environment Configurations and Dotenv Management.md)
*   **Title (H1)**: Day 12 - Module 2: Multi-Environment Configurations & Dotenv Management
    *   **Section (H2)**: 1. Class-Based Configuration Inheritance
    *   **Section (H2)**: 2. Loading Settings (`app.config.from_object`)
*   **Title (H1)**: Map configuration string keys to Config classes
*   **Title (H1)**: Load settings from object path
    *   **Section (H2)**: 3. Managing Secrets with `python-dotenv`
        *   *Sub-section (H3)*: Example `.env` File:
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 12 - Application Factory Pattern and Environment Config\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 12: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Application Factory & Config Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: Application Factory Steps (`F-A-C-T-O-R-Y`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Class-Based Configuration Hierarchy
        *   *Sub-section (H3)*: 2. Application Factory Skeleton with Deferred Binding
*   **Title (H1)**: Unattached global extension instance
*   **Title (H1)**: Deferred Extension Binding
*   **Title (H1)**: Blueprint Registration
        *   *Sub-section (H3)*: 3. `.env` Secret Key Management

### 📄 File: [5. Practice and Interview Questions.md](DAY 12 - Application Factory Pattern and Environment Config\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 12: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the Application Factory Pattern in Flask?
        *   *Sub-section (H3)*: Q2: Why is putting `app = Flask(__name__)` globally at the top of a file problematic in large projects?
        *   *Sub-section (H3)*: Q3: What is an Environment Configuration in web development?
        *   *Sub-section (H3)*: Q4: What is a `.env` file and why should it be added to `.gitignore`?
        *   *Sub-section (H3)*: Q5: How do you load a Python configuration class into a Flask app?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does the Deferred Extension Binding pattern (`db.init_app(app)`) work?
        *   *Sub-section (H3)*: Q7: Why is `sqlite:///:memory:` ideal for a `TestingConfig` class?
        *   *Sub-section (H3)*: Q8: How does `python-dotenv` integrate with Flask CLI commands?
        *   *Sub-section (H3)*: Q9: How can you dynamically select a configuration class based on an environment variable?
        *   *Sub-section (H3)*: Q10: What is the difference between `DEBUG = True` and `TESTING = True`?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How does the Application Factory Pattern support concurrent application instances in WSGI servers or test runners?
        *   *Sub-section (H3)*: Q12: How does the Application Factory Pattern align with the 12-Factor App methodology (III. Config)?
        *   *Sub-section (H3)*: Q13: What happens if an extension method requires `app` during global instantiation?
        *   *Sub-section (H3)*: Q14: How do you handle `current_app` inside blueprint view functions when using an Application Factory?
        *   *Sub-section (H3)*: Q15: How should production `SECRET_KEY` settings be generated and secured?

## 📁 DAY 13 - Custom CLI Commands and Flask Extensions

### 📄 File: [0. Custom CLI Commands and Extensions Fundamentals for Beginners.md](DAY 13 - Custom CLI Commands and Flask Extensions\0. Custom CLI Commands and Extensions Fundamentals for Beginners.md)
*   **Title (H1)**: Day 13 - Module 0: Custom CLI Commands & Extensions Fundamentals for Beginners
    *   **Section (H2)**: 1. What is a CLI in Plain English?
    *   **Section (H2)**: 2. Why Do Web Apps Need Custom CLI Commands?
    *   **Section (H2)**: 3. What is Click?
    *   **Section (H2)**: 4. What is a Flask Extension?
        *   *Sub-section (H3)*: How Custom Extensions Work
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Custom CLI Commands.md](DAY 13 - Custom CLI Commands and Flask Extensions\1. Custom CLI Commands.md)
*   **Title (H1)**: Day 13 - Module 1: Custom CLI Commands
    *   **Section (H2)**: 1. Registering Custom CLI Commands (`@app.cli.command`)
*   **Title (H1)**: Register command: accessible via $ flask hello
    *   **Section (H2)**: 2. Arguments vs. Options in Click
*   **Title (H1)**: 1. Positional Argument (Required)
*   **Title (H1)**: 2. Flag Option with Default Value (Optional)
    *   **Section (H2)**: 3. Requiring Application Context (`@with_appcontext`)
    *   **Section (H2)**: 4. Terminal Prompts & Styling (`click.style`)
    *   **Section (H2)**: 5. Grouping CLI Commands (`AppGroup`)
*   **Title (H1)**: Define CLI Command Group
*   **Title (H1)**: Register group on app ($ flask user create alice)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Authoring Reusable Custom Flask Extensions.md](DAY 13 - Custom CLI Commands and Flask Extensions\2. Authoring Reusable Custom Flask Extensions.md)
*   **Title (H1)**: Day 13 - Module 2: Authoring Reusable Custom Flask Extensions
    *   **Section (H2)**: 1. Extension Architecture Standards & Conventions
    *   **Section (H2)**: 2. Authoring a Custom Extension Class Skeleton
*   **Title (H1)**: 1. Set default configuration settings
*   **Title (H1)**: 2. Store extension instance reference on app.extensions
*   **Title (H1)**: 3. Register request lifecycle hooks
    *   **Section (H2)**: 3. Bundling CLI Commands Inside Custom Extensions
*   **Title (H1)**: Bundling custom CLI command inside extension!
    *   **Section (H2)**: 4. Retrieving Extension Instances (`app.extensions`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 13 - Custom CLI Commands and Flask Extensions\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 13: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Custom CLI Commands & Extensions Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. CLI Command Creation (`C-O-M-M-A-N-D`)
        *   *Sub-section (H3)*: 2. Custom Extension Authoring (`E-X-T-E-N-D`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Custom CLI Command with Arguments, Options & Prompts
*   **Title (H1)**: Run DB operation here
        *   *Sub-section (H3)*: 2. Custom Flask Extension Skeleton Class
*   **Title (H1)**: Attach request hook

### 📄 File: [5. Practice and Interview Questions.md](DAY 13 - Custom CLI Commands and Flask Extensions\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 13: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a CLI in web development?
        *   *Sub-section (H3)*: Q2: Why should database seeding or table resets be built as CLI commands rather than HTTP web routes?
        *   *Sub-section (H3)*: Q3: What Python library powers Flask's command-line interface?
        *   *Sub-section (H3)*: Q4: What is a Flask Extension?
        *   *Sub-section (H3)*: Q5: How do you register a custom terminal command on a Flask app instance?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: Why is `@with_appcontext` required on CLI commands that interact with databases?
        *   *Sub-section (H3)*: Q7: What is the difference between `@click.argument` and `@click.option`?
        *   *Sub-section (H3)*: Q8: What standard pattern should every custom Flask extension class follow for initialization?
        *   *Sub-section (H3)*: Q9: Where does a custom extension store its instance reference on the Flask application?
        *   *Sub-section (H3)*: Q10: How do you ask a user for a Yes/No confirmation in a Click CLI command?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do you group related CLI commands under a custom command namespace (e.g., `flask user create`, `flask user delete`)?
        *   *Sub-section (H3)*: Q12: How can a custom extension automatically register CLI commands onto the host Flask app?
        *   *Sub-section (H3)*: Q13: How does `app.config.setdefault()` help when authoring custom extensions?
        *   *Sub-section (H3)*: Q14: How do you test custom CLI commands using `pytest`?
        *   *Sub-section (H3)*: Q15: How can a custom extension attach request lifecycle hooks dynamically?

## 📁 DAY 14 - Session Management and Cookie Security

### 📄 File: [0. Sessions and Cookie Security Fundamentals for Beginners.md](DAY 14 - Session Management and Cookie Security\0. Sessions and Cookie Security Fundamentals for Beginners.md)
*   **Title (H1)**: Day 14 - Module 0: Sessions & Cookie Security Fundamentals for Beginners
    *   **Section (H2)**: 1. What is HTTP Statelessness?
    *   **Section (H2)**: 2. What is a Cookie and what is a Session?
    *   **Section (H2)**: 3. Client-Side vs. Server-Side Sessions
    *   **Section (H2)**: 4. Why Passwords Should NEVER Go into Sessions!
    *   **Section (H2)**: 5. Cookie Security Flags in Plain English
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Flask Session Mechanics and Security.md](DAY 14 - Session Management and Cookie Security\1. Flask Session Mechanics and Security.md)
*   **Title (H1)**: Day 14 - Module 1: Flask Session Mechanics & Security
    *   **Section (H2)**: 1. How Default Flask Sessions Work (`itsdangerous`)
    *   **Section (H2)**: 2. The Flask `session` Dictionary API
*   **Title (H1)**: 1. Store data in session
*   **Title (H1)**: 2. Set permanent session lifetime (Defaults to 31 days)
*   **Title (H1)**: 3. Read data from session safely
*   **Title (H1)**: 4. Clear all session data completely
    *   **Section (H2)**: 3. Enterprise Cookie Security Configuration Flags
*   **Title (H1)**: 1. Block client-side JavaScript access (Mitigates XSS cookie theft)
*   **Title (H1)**: 2. Force cookie transmission over HTTPS connections only (Mitigates MITM sniffing)
*   **Title (H1)**: 3. Restrict cross-site requests (Mitigates CSRF attacks)
*   **Title (H1)**: 4. Configure permanent session expiration window (e.g. 7 days)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Server-Side Sessions with Redis and Flask-Session.md](DAY 14 - Session Management and Cookie Security\2. Server-Side Sessions with Redis and Flask-Session.md)
*   **Title (H1)**: Day 14 - Module 2: Server-Side Sessions with Redis & Flask-Session
    *   **Section (H2)**: 1. Limitations of Client-Side Session Cookies
    *   **Section (H2)**: 2. Server-Side Session Architecture (`Flask-Session`)
    *   **Section (H2)**: 3. Configuring `Flask-Session` with Redis
*   **Title (H1)**: 1. Configure Server-Side Session Storage Type
*   **Title (H1)**: 2. Connect Redis Engine Instance
*   **Title (H1)**: 3. Initialize Flask-Session Extension
    *   **Section (H2)**: 4. Supported Server-Side Backends
    *   **Section (H2)**: 5. Instant Session Revocation
*   **Title (H1)**: Instant Session Revocation in Redis
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 14 - Session Management and Cookie Security\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 14: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Session & Cookie Security Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: Cookie Security Flags (`S-E-C-U-R-E`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Hardened Cookie Security Configuration
        *   *Sub-section (H3)*: 2. Session Dictionary Operations
*   **Title (H1)**: Create session values
*   **Title (H1)**: Read session values safely
*   **Title (H1)**: Clear session upon logout
        *   *Sub-section (H3)*: 3. Server-Side Redis Session Configuration (`Flask-Session`)

### 📄 File: [5. Practice and Interview Questions.md](DAY 14 - Session Management and Cookie Security\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 14: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is HTTP Statelessness in simple terms?
        *   *Sub-section (H3)*: Q2: What is the difference between a Cookie and a Session?
        *   *Sub-section (H3)*: Q3: Is data inside Flask's default client-side session encrypted?
        *   *Sub-section (H3)*: Q4: What happens when a user calls `session.clear()`?
        *   *Sub-section (H3)*: Q5: What is the default lifespan of a Flask session?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does `SESSION_COOKIE_HTTPONLY = True` protect against XSS attacks?
        *   *Sub-section (H3)*: Q7: What does `SESSION_COOKIE_SECURE = True` do?
        *   *Sub-section (H3)*: Q8: What is `SESSION_COOKIE_SAMESITE = 'Lax'` and how does it prevent CSRF?
        *   *Sub-section (H3)*: Q9: How does Flask verify that a client-side session cookie hasn't been tampered with?
        *   *Sub-section (H3)*: Q10: How do you configure a custom session expiration window of 7 days?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why are Server-Side Sessions (using Redis) required for enterprise production systems?
        *   *Sub-section (H3)*: Q12: How does `Flask-Session` store sessions in Redis under the hood?
        *   *Sub-section (H3)*: Q13: How can an administrator implement instant single-user session revocation in Redis?
        *   *Sub-section (H3)*: Q14: What is Session Fixation and how do you prevent it in Flask?
        *   *Sub-section (H3)*: Q15: What happens if `SECRET_KEY` is leaked or changed in a Flask application?

## 📁 DAY 15 - User Authentication and Password Hashing

### 📄 File: [0. Authentication, Password Hashing and RBAC Fundamentals for Beginners.md](DAY 15 - User Authentication and Password Hashing\0. Authentication, Password Hashing and RBAC Fundamentals for Beginners.md)
*   **Title (H1)**: Day 15 - Module 0: Authentication, Password Hashing & RBAC Fundamentals for Beginners
    *   **Section (H2)**: 1. Authentication vs. Authorization in Plain English
    *   **Section (H2)**: 2. The Plaintext Password Crime
    *   **Section (H2)**: 3. What is a One-Way Cryptographic Hash?
        *   *Sub-section (H3)*: Key Properties of Hashes:
    *   **Section (H2)**: 4. What is Flask-Login?
    *   **Section (H2)**: 5. What is Role-Based Access Control (RBAC)?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Password Hashing and Flask-Login.md](DAY 15 - User Authentication and Password Hashing\1. Password Hashing and Flask-Login.md)
*   **Title (H1)**: Day 15 - Module 1: Password Hashing & Flask-Login
    *   **Section (H2)**: 1. Hashing Passwords with Werkzeug (`generate_password_hash`)
*   **Title (H1)**: 1. Hashing a raw password (Uses PBKDF2:SHA256 with random salt by default)
*   **Title (H1)**: Output: scrypt:32768:8:1$vK9...$8d3f...
*   **Title (H1)**: 2. Verifying user login input against stored hash
    *   **Section (H2)**: 2. Integrating `Flask-Login`
        *   *Sub-section (H3)*: Step A: Configure `UserMixin` on your User Model
        *   *Sub-section (H3)*: Step B: Setup `LoginManager` & `user_loader`
    *   **Section (H2)**: 3. Login, Logout, and Route Protection
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Role-Based Access Control and Decorators.md](DAY 15 - User Authentication and Password Hashing\2. Role-Based Access Control and Decorators.md)
*   **Title (H1)**: Day 15 - Module 2: Role-Based Access Control and Decorators
    *   **Section (H2)**: 1. RBAC Permissions Matrix
    *   **Section (H2)**: 2. Why `functools.wraps` is MANDATORY for Flask Decorators
*   **Title (H1)**: BAD (Without @wraps): Overwrites function __name__ to 'wrapper', causing route endpoint collision errors in Flask!
*   **Title (H1)**: GOOD (With @wraps): Preserves original function metadata (__name__, __doc__)!
    *   **Section (H2)**: 3. Authoring Custom RBAC Route Decorators
        *   *Sub-section (H3)*: A. `@admin_required` Decorator
        *   *Sub-section (H3)*: B. Dynamic `@role_required(*allowed_roles)` Decorator
        *   *Sub-section (H3)*: Usage in Flask Route Handlers:
    *   **Section (H2)**: 4. HTTP `401 Unauthorized` vs. `403 Forbidden`
    *   **Section (H2)**: 5. Template-Level Role Checks in Jinja2
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 15 - User Authentication and Password Hashing\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 15: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Auth & RBAC Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Authentication Lifecycle (`A-U-T-H`)
        *   *Sub-section (H3)*: 2. Role-Based Access Control (`R-B-A-C`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Werkzeug Password Hashing
*   **Title (H1)**: Hash password
*   **Title (H1)**: Check password
        *   *Sub-section (H3)*: 2. Flask-Login Setup & User Loader
        *   *Sub-section (H3)*: 3. Custom RBAC Decorator Skeleton

### 📄 File: [5. Practice and Interview Questions.md](DAY 15 - User Authentication and Password Hashing\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 15: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the difference between Authentication and Authorization?
        *   *Sub-section (H3)*: Q2: Why should passwords never be stored in plaintext inside a database?
        *   *Sub-section (H3)*: Q3: What is Salt in password hashing and why is it used?
        *   *Sub-section (H3)*: Q4: What is Flask-Login?
        *   *Sub-section (H3)*: Q5: What methods/properties does `UserMixin` add to a SQLAlchemy User model?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: Why is `functools.wraps(f)` mandatory when writing custom Flask route decorators?
        *   *Sub-section (H3)*: Q7: What is the exact difference between HTTP `401 Unauthorized` and HTTP `403 Forbidden`?
        *   *Sub-section (H3)*: Q8: How does Werkzeug's `check_password_hash()` protect against Timing Attacks?
        *   *Sub-section (H3)*: Q9: What does `@login_manager.user_loader` do?
        *   *Sub-section (H3)*: Q10: How do you log a user out using Flask-Login?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do modern hashing algorithms like Scrypt and Argon2 protect against GPU brute-force attacks?
        *   *Sub-section (H3)*: Q12: How do you construct a dynamic `@role_required(*allowed_roles)` decorator that supports multiple roles?
        *   *Sub-section (H3)*: Q13: How can you enforce password strength policies before hashing passwords in Flask?
        *   *Sub-section (H3)*: Q14: What happens if `load_user(user_id)` returns `None`?
        *   *Sub-section (H3)*: Q15: How should Remember-Me functionality be implemented securely?

## 📁 DAY 16 - REST API Architecture and HTTP Status Codes

### 📄 File: [0. REST API Architecture and Status Codes Fundamentals for Beginners.md](DAY 16 - REST API Architecture and HTTP Status Codes\0. REST API Architecture and Status Codes Fundamentals for Beginners.md)
*   **Title (H1)**: Day 16 - Module 0: REST API Architecture & Status Codes Fundamentals for Beginners
    *   **Section (H2)**: 1. What is an API in Plain English?
    *   **Section (H2)**: 2. What is REST?
        *   *Sub-section (H3)*: What is a Resource?
    *   **Section (H2)**: 3. What are HTTP Verbs in REST?
    *   **Section (H2)**: 4. HTTP Status Code Families
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. REST Principles and Formatting.md](DAY 16 - REST API Architecture and HTTP Status Codes\1. REST Principles and Formatting.md)
*   **Title (H1)**: Day 16 - Module 1: REST Principles & HTTP Status Code Directory
    *   **Section (H2)**: 1. The 6 REST Architectural Constraints
    *   **Section (H2)**: 2. RESTful URL Naming Best Practices
    *   **Section (H2)**: 3. HTTP Method Idempotency
    *   **Section (H2)**: 4. Complete HTTP Status Code Directory
        *   *Sub-section (H3)*: 🟢 2xx Success Codes
        *   *Sub-section (H3)*: 🔴 4xx Client Error Codes
        *   *Sub-section (H3)*: 💥 5xx Server Error Codes
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Standardized JSON Error Payload Architecture.md](DAY 16 - REST API Architecture and HTTP Status Codes\2. Standardized JSON Error Payload Architecture.md)
*   **Title (H1)**: Day 16 - Module 2: Standardized JSON Error Payload Architecture
    *   **Section (H2)**: 1. Why Inconsistent API Errors Break Clients
    *   **Section (H2)**: 2. Enterprise Response Envelope Enclosures
    *   **Section (H2)**: 3. RFC 7807 (Problem Details for HTTP APIs)
    *   **Section (H2)**: 4. Registering Global Flask API Error Handlers
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 16 - REST API Architecture and HTTP Status Codes\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 16: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 REST API & Status Codes Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. HTTP Verbs & Actions (`V-E-R-B-S`)
        *   *Sub-section (H3)*: 2. HTTP Status Code Families (`S-T-A-T-U-S`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Standardized RESTful CRUD Route Mapping
        *   *Sub-section (H3)*: 2. RFC 7807 Error Response Helper

### 📄 File: [5. Practice and Interview Questions.md](DAY 16 - REST API Architecture and HTTP Status Codes\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 16: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is an API in simple terms?
        *   *Sub-section (H3)*: Q2: What is REST?
        *   *Sub-section (H3)*: Q3: What is a Resource in a RESTful API?
        *   *Sub-section (H3)*: Q4: What is the difference between status code `200 OK` and `404 Not Found`?
        *   *Sub-section (H3)*: Q5: Why should API endpoints return JSON instead of HTML web pages?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the exact difference between `PUT` and `PATCH` in RESTful APIs?
        *   *Sub-section (H3)*: Q7: When should an API return `201 Created` versus `204 No Content`?
        *   *Sub-section (H3)*: Q8: What does HTTP Method Idempotency mean? Which HTTP methods are idempotent?
        *   *Sub-section (H3)*: Q9: What is the difference between status code `400 Bad Request` and `422 Unprocessable Entity`?
        *   *Sub-section (H3)*: Q10: Why should RESTful URLs use nouns instead of verbs?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is RFC 7807 (Problem Details for HTTP APIs)?
        *   *Sub-section (H3)*: Q12: What are the 3 common API Versioning strategies in enterprise systems?
        *   *Sub-section (H3)*: Q13: What is HATEOAS in RESTful API design?
        *   *Sub-section (H3)*: Q14: How should a REST API handle pagination for large collections?
        *   *Sub-section (H3)*: Q15: What status code should be returned when a database unique constraint fails (e.g., duplicate email registration)?

## 📁 DAY 17 - Data Serialization and Validation with Marshmallow

### 📄 File: [0. Serialization and Marshmallow Fundamentals for Beginners.md](DAY 17 - Data Serialization and Validation with Marshmallow\0. Serialization and Marshmallow Fundamentals for Beginners.md)
*   **Title (H1)**: Day 17 - Module 0: Serialization & Marshmallow Fundamentals for Beginners
    *   **Section (H2)**: 1. Serialization vs. Deserialization in Plain English
    *   **Section (H2)**: 2. Why Manual `to_dict()` Methods Fail at Scale
*   **Title (H1)**: Beginner Manual Converter (Anti-Pattern in Enterprise APIs)
        *   *Sub-section (H3)*: Why this manual approach breaks down:
    *   **Section (H2)**: 3. What is Marshmallow?
    *   **Section (H2)**: 4. Understanding `dump_only` vs `load_only`
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Marshmallow Schemas and Validation.md](DAY 17 - Data Serialization and Validation with Marshmallow\1. Marshmallow Schemas and Validation.md)
*   **Title (H1)**: Day 17 - Module 1: Marshmallow Schemas & Validation
    *   **Section (H2)**: 1. Defining Marshmallow Field Types
    *   **Section (H2)**: 2. Built-In Marshmallow Validators (`marshmallow.validate`)
    *   **Section (H2)**: 3. Authoring Custom Field Validators (`@validates`)
    *   **Section (H2)**: 4. Capturing `ValidationError` in Flask Routes
*   **Title (H1)**: Deserialize and validate incoming JSON data
*   **Title (H1)**: Return 422 Unprocessable Entity with dict of field error messages!
*   **Title (H1)**: Proceed with saving validated_data...
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Nested Schemas and ORM Integration.md](DAY 17 - Data Serialization and Validation with Marshmallow\2. Nested Schemas and ORM Integration.md)
*   **Title (H1)**: Day 17 - Module 2: Nested Schemas & Flask-Marshmallow Integration
    *   **Section (H2)**: 1. Nested Schemas for Relational Data
*   **Title (H1)**: One-to-Many Nested Relationship Serialization
    *   **Section (H2)**: 2. Flask-Marshmallow & `SQLAlchemyAutoSchema`
*   **Title (H1)**: Automatically builds Marshmallow schema matching Author model!
    *   **Section (H2)**: 3. Schema Lifecycle Hooks (`@post_load`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 17 - Data Serialization and Validation with Marshmallow\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 17: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Marshmallow & Serialization Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Serialization (`D-U-M-P`)
        *   *Sub-section (H3)*: 2. Deserialization & Validation (`L-O-A-D`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Defining a Marshmallow Schema
        *   *Sub-section (H3)*: 2. Handling `ValidationError` in Flask Routes
*   **Title (H1)**: Process validated_dict...
        *   *Sub-section (H3)*: 3. Nested Schemas Serialization

### 📄 File: [5. Practice and Interview Questions.md](DAY 17 - Data Serialization and Validation with Marshmallow\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 17: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the difference between Serialization and Deserialization?
        *   *Sub-section (H3)*: Q2: Why is writing manual `to_dict()` methods on ORM models considered an anti-pattern for enterprise REST APIs?
        *   *Sub-section (H3)*: Q3: What is Marshmallow?
        *   *Sub-section (H3)*: Q4: What does `schema.dump(obj)` return vs `schema.load(data)`?
        *   *Sub-section (H3)*: Q5: What HTTP status code should an API return when Marshmallow validation fails?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `dump_only=True` and `load_only=True` in Marshmallow fields?
        *   *Sub-section (H3)*: Q7: How do you write a custom field validator method in a Marshmallow Schema?
        *   *Sub-section (H3)*: Q8: How do you serialize a list of multiple database objects using Marshmallow?
        *   *Sub-section (H3)*: Q9: How do you serialize nested One-to-Many relationships?
        *   *Sub-section (H3)*: Q10: How does Marshmallow handle `ValidationError` exceptions?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is `SQLAlchemyAutoSchema` in `Flask-Marshmallow`?
        *   *Sub-section (H3)*: Q12: What is the purpose of the `@post_load` decorator in Marshmallow?
        *   *Sub-section (H3)*: Q13: How do you resolve self-referential or circular nested schema references in Marshmallow?
        *   *Sub-section (H3)*: Q14: How does `partial=True` work during `schema.load()`?
        *   *Sub-section (H3)*: Q15: How can you optimize performance when serializing thousands of objects with Marshmallow?

## 📁 DAY 18 - RESTful Extensions and OpenAPI Documentation

### 📄 File: [0. REST Extensions and OpenAPI Documentation Fundamentals for Beginners.md](DAY 18 - RESTful Extensions and OpenAPI Documentation\0. REST Extensions and OpenAPI Documentation Fundamentals for Beginners.md)
*   **Title (H1)**: Day 18 - Module 0: REST Extensions & OpenAPI Documentation Fundamentals for Beginners
    *   **Section (H2)**: 1. What is API Documentation in Plain English?
    *   **Section (H2)**: 2. What is OpenAPI and Swagger UI?
    *   **Section (H2)**: 3. What are Class-Based REST Resources?
*   **Title (H1)**: Function-Based View Routes (Standard Flask)
*   **Title (H1)**: Class-Based REST Resource (Flask-RESTful / Flask-Smorest)
    *   **Section (H2)**: 4. Why Use REST Extensions (`Flask-RESTful` & `Flask-Smorest`)?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Flask-RESTful and OpenAPI.md](DAY 18 - RESTful Extensions and OpenAPI Documentation\1. Flask-RESTful and OpenAPI.md)
*   **Title (H1)**: Day 18 - Module 1: Flask-RESTful & Class-Based Resources
    *   **Section (H2)**: 1. Defining Class-Based `Resource` Classes
*   **Title (H1)**: In-Memory items database
    *   **Section (H2)**: 2. Registering Resources (`api.add_resource`)
*   **Title (H1)**: Bind ItemResource to URL pattern /items/<int:item_id>
    *   **Section (H2)**: 3. Request Parsing (`reqparse.RequestParser`)
*   **Title (H1)**: Parse and validate incoming arguments
    *   **Section (H2)**: 4. Output Field Marshalling (`@marshal_with`)
*   **Title (H1)**: Define output field filtering dictionary
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Flask-Smorest and Swagger UI Integration.md](DAY 18 - RESTful Extensions and OpenAPI Documentation\2. Flask-Smorest and Swagger UI Integration.md)
*   **Title (H1)**: Day 18 - Module 2: Flask-Smorest & Swagger UI Integration
    *   **Section (H2)**: 1. What is Flask-Smorest?
        *   *Sub-section (H3)*: Key Benefits:
    *   **Section (H2)**: 2. Configuring OpenAPI & Swagger UI Metadata
*   **Title (H1)**: OpenAPI 3.0 Configuration Settings
    *   **Section (H2)**: 3. Smorest Blueprints & Method Views
*   **Title (H1)**: 1. Define Marshmallow Schema
*   **Title (H1)**: 2. Define Smorest Blueprint
*   **Title (H1)**: 3. Define Class-Based MethodView Resource
*   **Title (H1)**: new_item_data is ALREADY validated by Marshmallow!
    *   **Section (H2)**: 4. Accessing Live Interactive Swagger UI
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 18 - RESTful Extensions and OpenAPI Documentation\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 18: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 REST Extensions & OpenAPI Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. API Documentation Sequence (`D-O-C-S`)
        *   *Sub-section (H3)*: 2. Flask-Smorest Workflow (`S-M-O-R-E-S-T`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-Smorest OpenAPI Setup
        *   *Sub-section (H3)*: 2. MethodView Class with Schema Validation & Documentation

### 📄 File: [5. Practice and Interview Questions.md](DAY 18 - RESTful Extensions and OpenAPI Documentation\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 18: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is API Documentation and why is it essential for developers?
        *   *Sub-section (H3)*: Q2: What is the difference between OpenAPI and Swagger UI?
        *   *Sub-section (H3)*: Q3: What is a Class-Based REST Resource?
        *   *Sub-section (H3)*: Q4: Why use `Flask-Smorest` instead of manual view functions?
        *   *Sub-section (H3)*: Q5: Where can developers interactively test endpoints in a Flask-Smorest app?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How does `@blp.arguments(Schema)` work in `Flask-Smorest`?
        *   *Sub-section (H3)*: Q7: What does `@blp.response(200, Schema)` do?
        *   *Sub-section (H3)*: Q8: What is the difference between `Flask-RESTful` and `Flask-Smorest`?
        *   *Sub-section (H3)*: Q9: How do you configure Swagger UI in Flask-Smorest?
        *   *Sub-section (H3)*: Q10: How do docstrings on `MethodView` methods affect Swagger UI?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do you document JWT Bearer Token authentication in Swagger UI using `Flask-Smorest`?
        *   *Sub-section (H3)*: Q12: How can enterprise teams use `/openapi.json` to generate client SDKs?
        *   *Sub-section (H3)*: Q13: How do you handle file uploads in `Flask-Smorest` with Marshmallow schemas?
        *   *Sub-section (H3)*: Q14: How does `Flask-Smorest` handle pagination documentation in OpenAPI?
        *   *Sub-section (H3)*: Q15: What is the advantage of OpenAPI 3.0 over Swagger 2.0?

## 📁 DAY 19 - API Authentication with JWT

### 📄 File: [0. JWT Authentication Fundamentals for Beginners.md](DAY 19 - API Authentication with JWT\0. JWT Authentication Fundamentals for Beginners.md)
*   **Title (H1)**: Day 19 - Module 0: JWT Authentication Fundamentals for Beginners
    *   **Section (H2)**: 1. Why Cookie Sessions Fail for APIs
    *   **Section (H2)**: 2. What is a JWT (JSON Web Token)?
    *   **Section (H2)**: 3. The 3 Parts of a JWT (`Header.Payload.Signature`)
    *   **Section (H2)**: 4. Access Tokens vs. Refresh Tokens
    *   **Section (H2)**: 5. Token Revocation & Blacklisting
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Stateless Auth with Flask-JWT-Extended.md](DAY 19 - API Authentication with JWT\1. Stateless Auth with Flask-JWT-Extended.md)
*   **Title (H1)**: Day 19 - Module 1: Stateless Auth with Flask-JWT-Extended
    *   **Section (H2)**: 1. Configuring `Flask-JWT-Extended`
*   **Title (H1)**: Cryptographic signing key for JWT tokens (MUST be secret in production!)
*   **Title (H1)**: Configure Access Token Expiration Window (e.g. 15 minutes)
*   **Title (H1)**: Initialize JWT Manager Extension
    *   **Section (H2)**: 2. Generating Access Tokens (`create_access_token`)
*   **Title (H1)**: Create signed access token embedding user.id as identity subject ('sub')
    *   **Section (H2)**: 3. Protecting Endpoints (`@jwt_required`)
*   **Title (H1)**: Retrieve user_id embedded in active JWT token
*   **Title (H1)**: Retrieve full raw JWT payload claims dictionary
    *   **Section (H2)**: 4. Injecting Custom Claims (`@jwt.additional_claims_loader`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Access vs Refresh Tokens and Redis Blacklisting.md](DAY 19 - API Authentication with JWT\2. Access vs Refresh Tokens and Redis Blacklisting.md)
*   **Title (H1)**: Day 19 - Module 2: Access vs Refresh Tokens & Token Revocation
    *   **Section (H2)**: 1. Dual-Token Architecture (Access + Refresh Pair)
*   **Title (H1)**: ... validate credentials ...
    *   **Section (H2)**: 2. Implementing the `/auth/refresh` Endpoint
*   **Title (H1)**: Generate a brand new 15-minute Access Token without re-asking for password!
    *   **Section (H2)**: 3. Token Blacklisting / Revocation (`JTI` Tracking)
*   **Title (H1)**: In-Memory or Redis blocklist storage set
        *   *Sub-section (H3)*: Registering Blocklist Callback (`@jwt.token_in_blocklist_loader`)
    *   **Section (H2)**: 4. Custom Error Response Handlers
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 19 - API Authentication with JWT\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 19: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 JWT Authentication Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Anatomy of a JWT (`H-P-S`)
        *   *Sub-section (H3)*: 2. JWT Token Lifecycle (`J-W-T`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-JWT-Extended Setup
        *   *Sub-section (H3)*: 2. Protecting Routes & Reading User Identity
        *   *Sub-section (H3)*: 3. JTI Revocation Blocklist Callback

### 📄 File: [5. Practice and Interview Questions.md](DAY 19 - API Authentication with JWT\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 19: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a JSON Web Token (JWT)?
        *   *Sub-section (H3)*: Q2: Why are JWTs preferred over browser cookie sessions when building mobile app APIs?
        *   *Sub-section (H3)*: Q3: What is the format of an Authorization header carrying a JWT?
        *   *Sub-section (H3)*: Q4: Are data claims inside a JWT payload encrypted?
        *   *Sub-section (H3)*: Q5: What is the difference between an Access Token and a Refresh Token?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What are the 3 parts of a JWT string?
        *   *Sub-section (H3)*: Q7: What is a JTI (JWT ID) and why is it used?
        *   *Sub-section (H3)*: Q8: How does `@jwt.token_in_blocklist_loader` work in `Flask-JWT-Extended`?
        *   *Sub-section (H3)*: Q9: How do you extract custom claims embedded in a JWT during a request?
        *   *Sub-section (H3)*: Q10: How do you handle expired tokens gracefully in `Flask-JWT-Extended`?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is the fundamental architectural trade-off between Stateless JWTs and Immediate Revocation?
        *   *Sub-section (H3)*: Q12: Where should JWTs be stored in client-side Single Page Applications (SPAs) to prevent XSS vs CSRF attacks?
        *   *Sub-section (H3)*: Q13: How does Symmetric (HS256) signing differ from Asymmetric (RS256) signing for JWTs?
        *   *Sub-section (H3)*: Q14: What is Token Side-Loading / Custom Claims Injection?
        *   *Sub-section (H3)*: Q15: How can an API handle Refresh Token Rotation for enhanced security?

## 📁 DAY 20 - CORS Handling and Rate Limiting

### 📄 File: [0. CORS and Rate Limiting Fundamentals for Beginners.md](DAY 20 - CORS Handling and Rate Limiting\0. CORS and Rate Limiting Fundamentals for Beginners.md)
*   **Title (H1)**: Day 20 - Module 0: CORS & Rate Limiting Fundamentals for Beginners
    *   **Section (H2)**: 1. What is the Same-Origin Policy (SOP)?
    *   **Section (H2)**: 2. What is CORS (Cross-Origin Resource Sharing)?
    *   **Section (H2)**: 3. What is a Preflight Request (`OPTIONS`)?
    *   **Section (H2)**: 4. What is API Rate Limiting?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. CORS and Flask-Limiter.md](DAY 20 - CORS Handling and Rate Limiting\1. CORS and Flask-Limiter.md)
*   **Title (H1)**: Day 18 - Module 1: CORS Architecture & Flask-Limiter Setup
    *   **Section (H2)**: 1. Configuring `Flask-CORS`
*   **Title (H1)**: Enterprise CORS Configuration: Allow specific frontend origins
    *   **Section (H2)**: 2. Preflight `OPTIONS` Header Processing
    *   **Section (H2)**: 3. Rate Limiting with `Flask-Limiter`
*   **Title (H1)**: Initialize Limiter with global default limits
*   **Title (H1)**: 1. Endpoint with default rate limits
*   **Title (H1)**: 2. Endpoint with strict custom rate limits
*   **Title (H1)**: 3. Exempt specific endpoints from rate limits
    *   **Section (H2)**: 4. Handling `HTTP 429 Too Many Requests`
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Rate Limiting Strategies with Redis Storage.md](DAY 20 - CORS Handling and Rate Limiting\2. Rate Limiting Strategies with Redis Storage.md)
*   **Title (H1)**: Day 20 - Module 2: Advanced Rate Limiting & Redis Storage
    *   **Section (H2)**: 1. Why In-Memory Rate Limiting Fails in Production
        *   *Sub-section (H3)*: The Solution: Shared Redis Storage
    *   **Section (H2)**: 2. Rate Limiting Algorithms Compared
    *   **Section (H2)**: 3. Dynamic User-Tier Rate Limits
*   **Title (H1)**: Read user role or tier from JWT claim / API key
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 20 - CORS Handling and Rate Limiting\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 20: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 CORS & Rate Limiting Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. CORS Configuration Steps (`C-O-R-S`)
        *   *Sub-section (H3)*: 2. Rate Limiting Lifecycle (`L-I-M-I-T`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-CORS Configuration
        *   *Sub-section (H3)*: 2. Flask-Limiter & Route Protection
*   **Title (H1)**: Route specific limit
*   **Title (H1)**: Route exemption
        *   *Sub-section (H3)*: 3. Custom HTTP 429 Error Handler

### 📄 File: [5. Practice and Interview Questions.md](DAY 20 - CORS Handling and Rate Limiting\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 20: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the Same-Origin Policy (SOP)?
        *   *Sub-section (H3)*: Q2: What is CORS?
        *   *Sub-section (H3)*: Q3: What is API Rate Limiting?
        *   *Sub-section (H3)*: Q4: What HTTP status code is returned when a client exceeds their rate limit?
        *   *Sub-section (H3)*: Q5: What is `get_remote_address` in Flask-Limiter?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is a Preflight `OPTIONS` Request in CORS?
        *   *Sub-section (H3)*: Q7: What does `supports_credentials=True` do in `Flask-CORS`?
        *   *Sub-section (H3)*: Q8: What header specifies how long a browser can cache a CORS preflight response?
        *   *Sub-section (H3)*: Q9: How do you exempt a specific route from global rate limits in `Flask-Limiter`?
        *   *Sub-section (H3)*: Q10: How can you limit requests based on a custom `X-API-KEY` header instead of IP address?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why does in-memory rate limiting fail on multi-worker Gunicorn server deployments?
        *   *Sub-section (H3)*: Q12: What is the difference between Fixed Window and Sliding Window (Moving Window) rate limiting algorithms?
        *   *Sub-section (H3)*: Q13: How do you implement dynamic rate limits based on User Tiers (Free vs Premium)?
        *   *Sub-section (H3)*: Q14: How should rate limit headers be communicated back to API clients?
        *   *Sub-section (H3)*: Q15: Why is setting `Access-Control-Allow-Origin: *` dangerous when `supports_credentials=True` is enabled?

## 📁 DAY 21 - Background Processing with Celery and Redis

### 📄 File: [0. Celery and Background Processing Fundamentals for Beginners.md](DAY 21 - Background Processing with Celery and Redis\0. Celery and Background Processing Fundamentals for Beginners.md)
*   **Title (H1)**: Day 21 - Module 0: Celery & Background Processing Fundamentals for Beginners
    *   **Section (H2)**: 1. Synchronous vs. Asynchronous Execution in Plain English
    *   **Section (H2)**: 2. What is Celery?
    *   **Section (H2)**: 3. The 3 Core Components of a Celery Architecture
    *   **Section (H2)**: 4. Why Use Redis as both Broker and Result Backend?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Celery Integration with Flask.md](DAY 21 - Background Processing with Celery and Redis\1. Celery Integration with Flask.md)
*   **Title (H1)**: Day 21 - Module 1: Celery Integration with Flask
    *   **Section (H2)**: 1. Modern Flask Factory Integration (`celery_init_app`)
*   **Title (H1)**: Pushes Flask Application Context automatically inside background worker!
    *   **Section (H2)**: 2. Configuring Redis Broker & Result Backend
*   **Title (H1)**: Configure Redis Broker and Result Backend URLs
    *   **Section (H2)**: 3. Defining Celery Tasks (`@celery.task`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Task State Tracking and Redis Result Backend.md](DAY 21 - Background Processing with Celery and Redis\2. Task State Tracking and Redis Result Backend.md)
*   **Title (H1)**: Day 21 - Module 2: Task State Tracking & Redis Result Backend
    *   **Section (H2)**: 1. Triggering Tasks (`.delay` vs `.apply_async`)
*   **Title (H1)**: Run task in 60 seconds
    *   **Section (H2)**: 2. Returning HTTP `202 Accepted` Status Code
*   **Title (H1)**: 1. Queue background task asynchronously
*   **Title (H1)**: 2. Return HTTP 202 Accepted + task_id
    *   **Section (H2)**: 3. Polling Task Status (`AsyncResult`)
*   **Title (H1)**: Query Redis Result Backend for task status
    *   **Section (H2)**: 4. Automatic Task Retries (`self.retry`)
*   **Title (H1)**: Code connecting to SMTP server...
*   **Title (H1)**: Retry task after 10 seconds
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 21 - Background Processing with Celery and Redis\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 21: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Celery & Background Processing Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Celery Architecture Pipeline (`C-E-L-E-R-Y`)
        *   *Sub-section (H3)*: 2. Asynchronous Flow (`A-S-Y-N-C`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Celery Factory Integration
        *   *Sub-section (H3)*: 2. Task Definition & Trigger
*   **Title (H1)**: Long running work...
*   **Title (H1)**: Trigger task asynchronously in route:
        *   *Sub-section (H3)*: 3. Celery Worker Terminal Command

### 📄 File: [5. Practice and Interview Questions.md](DAY 21 - Background Processing with Celery and Redis\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 21: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the difference between Synchronous and Asynchronous execution in web applications?
        *   *Sub-section (H3)*: Q2: What is Celery?
        *   *Sub-section (H3)*: Q3: What is the role of the Message Broker in Celery?
        *   *Sub-section (H3)*: Q4: What is a Celery Worker?
        *   *Sub-section (H3)*: Q5: What HTTP status code should an API return when a background job is successfully queued?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`?
        *   *Sub-section (H3)*: Q7: What is the difference between `.delay()` and `.apply_async()` when calling a Celery task?
        *   *Sub-section (H3)*: Q8: How do you poll the status of a queued task using Celery?
        *   *Sub-section (H3)*: Q9: How do you automatically retry a failing Celery task?
        *   *Sub-section (H3)*: Q10: How do you launch a Celery worker process from the command line?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why is Flask Application Context binding necessary inside Celery tasks, and how is it implemented?
        *   *Sub-section (H3)*: Q12: What is Task Idempotency and why is it critical in distributed Celery architectures?
        *   *Sub-section (H3)*: Q13: What is the difference between Early Acknowledgment and Late Acknowledgment (`task_acks_late=True`) in Celery?
        *   *Sub-section (H3)*: Q14: How does Celery Beat handle recurring cron-like scheduled tasks?
        *   *Sub-section (H3)*: Q15: How can enterprise teams prevent Redis memory exhaustion from storing thousands of Celery task results?

## 📁 DAY 22 - Periodic Tasks and Scheduled Jobs

### 📄 File: [0. Periodic Tasks and Scheduled Jobs Fundamentals for Beginners.md](DAY 22 - Periodic Tasks and Scheduled Jobs\0. Periodic Tasks and Scheduled Jobs Fundamentals for Beginners.md)
*   **Title (H1)**: Day 22 - Module 0: Periodic Tasks & Scheduled Jobs Fundamentals for Beginners
    *   **Section (H2)**: 1. What are Periodic Tasks & Scheduled Jobs?
    *   **Section (H2)**: 2. What is Celery Beat?
    *   **Section (H2)**: 3. What is Cron Syntax & `crontab()`?
*   **Title (H1)**: Every midnight (00:00)
*   **Title (H1)**: Every Monday morning at 9:30 AM
    *   **Section (H2)**: 4. In-Process Alternative: `APScheduler`
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Celery Beat and Scheduled Workflows.md](DAY 22 - Periodic Tasks and Scheduled Jobs\1. Celery Beat and Scheduled Workflows.md)
*   **Title (H1)**: Day 22 - Module 1: Celery Beat & Scheduled Workflows
    *   **Section (H2)**: 1. Defining `beat_schedule` Configurations
*   **Title (H1)**: 1. Define Background Tasks
*   **Title (H1)**: DB cleanup logic...
*   **Title (H1)**: 2. Configure Beat Schedule Dictionary
*   **Title (H1)**: Job 1: Interval Schedule (Runs every 10 minutes)
*   **Title (H1)**: Job 2: Crontab Schedule (Runs every Monday at 9:00 AM)
    *   **Section (H2)**: 2. Master Class `crontab()` Schedule Patterns
*   **Title (H1)**: 1. Every Night at Midnight (00:00)
*   **Title (H1)**: 2. Every 15 Minutes
*   **Title (H1)**: 3. Twice Daily at 8:00 AM and 8:00 PM
*   **Title (H1)**: 4. First Day of Every Month at Midnight
*   **Title (H1)**: 5. Every Weekday (Mon-Fri) at 5:00 PM
    *   **Section (H2)**: 3. Running Celery Beat in Production
        *   *Sub-section (H3)*: Terminal 1: Launch Celery Worker (Executes Tasks)
        *   *Sub-section (H3)*: Terminal 2: Launch Celery Beat (Fires Schedules)
        *   *Sub-section (H3)*: Combined Development Command (Worker + Embedded Beat)
*   **Title (H1)**: Convenient for local development (DO NOT USE IN PRODUCTION MULTI-SERVER CLUSTERS!)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Retry Strategies and Worker Error Handling.md](DAY 22 - Periodic Tasks and Scheduled Jobs\2. Retry Strategies and Worker Error Handling.md)
*   **Title (H1)**: Day 22 - Module 2: Advanced Retries & Error Handling
    *   **Section (H2)**: 1. Automatic Retries with Exponential Backoff & Jitter
    *   **Section (H2)**: 2. Preventing Celery Beat Race Conditions in Clusters
        *   *Sub-section (H3)*: Production Solutions:
    *   **Section (H2)**: 3. Light-Weight In-Process Alternative: `Flask-APScheduler`
*   **Title (H1)**: Configure APScheduler Jobs
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 22 - Periodic Tasks and Scheduled Jobs\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 22: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Periodic Tasks & Celery Beat Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Celery Beat Workflow (`B-E-A-T`)
        *   *Sub-section (H3)*: 2. Cron Expression Fields (`C-R-O-N`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Celery Beat Schedule Configuration
        *   *Sub-section (H3)*: 2. Master Class `crontab()` Expressions
*   **Title (H1)**: Every 15 minutes
*   **Title (H1)**: Every Monday at 9:00 AM
*   **Title (H1)**: 1st of every month at midnight
        *   *Sub-section (H3)*: 3. Celery Beat CLI Command

### 📄 File: [5. Practice and Interview Questions.md](DAY 22 - Periodic Tasks and Scheduled Jobs\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 22: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a Periodic Task / Scheduled Job?
        *   *Sub-section (H3)*: Q2: What is Celery Beat?
        *   *Sub-section (H3)*: Q3: Does Celery Beat execute background task functions itself?
        *   *Sub-section (H3)*: Q4: What is Cron Syntax?
        *   *Sub-section (H3)*: Q5: What is `APScheduler`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: Where do you configure periodic schedules in a Celery application?
        *   *Sub-section (H3)*: Q7: How do you write a `crontab()` schedule in Celery that runs every Monday at 9:00 AM?
        *   *Sub-section (H3)*: Q8: How do you enable exponential backoff and jitter for retrying failing tasks in Celery?
        *   *Sub-section (H3)*: Q9: What command starts the Celery Beat scheduler from the command line?
        *   *Sub-section (H3)*: Q10: What is the difference between an interval schedule and a `crontab()` schedule in Celery Beat?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why is running multiple `celery beat` instances in a multi-server deployment dangerous, and how do you solve it?
        *   *Sub-section (H3)*: Q12: What is the purpose of `retry_jitter=True` in Celery retries?
        *   *Sub-section (H3)*: Q13: How do Dead Letter Queues (DLQ) work in Celery?
        *   *Sub-section (H3)*: Q14: How can you dynamically update `beat_schedule` rules at runtime without restarting the Celery Beat daemon?
        *   *Sub-section (H3)*: Q15: How do you handle timezone shifts (e.g., Daylight Saving Time) in Celery Beat?

## 📁 DAY 23 - Application Caching Strategies

### 📄 File: [0. Caching Strategies Fundamentals for Beginners.md](DAY 23 - Application Caching Strategies\0. Caching Strategies Fundamentals for Beginners.md)
*   **Title (H1)**: Day 23 - Module 0: Caching Strategies Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Caching in Plain English?
    *   **Section (H2)**: 2. Cache Hit vs. Cache Miss
    *   **Section (H2)**: 3. What is Cache Invalidation?
    *   **Section (H2)**: 4. What is `Flask-Caching`?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Caching with Flask-Caching and Redis.md](DAY 23 - Application Caching Strategies\1. Caching with Flask-Caching and Redis.md)
*   **Title (H1)**: Day 23 - Module 1: Caching with Flask-Caching and Redis
    *   **Section (H2)**: 1. Configuring `Flask-Caching`
*   **Title (H1)**: 1. Development In-Memory Cache (SimpleCache)
    *   **Section (H2)**: 2. Supported Cache Backends Compared
    *   **Section (H2)**: 3. Production Enterprise Redis Setup
    *   **Section (H2)**: 4. Custom Cache Key Generators (`make_cache_key`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. View Caching, Memoization and Invalidation Strategies.md](DAY 23 - Application Caching Strategies\2. View Caching, Memoization and Invalidation Strategies.md)
*   **Title (H1)**: Day 23 - Module 2: View Caching, Memoization & Invalidation
    *   **Section (H2)**: 1. View Caching (`@cache.cached`)
    *   **Section (H2)**: 2. Function Memoization (`@cache.memoize`)
    *   **Section (H2)**: 3. Cache Invalidation Strategies
        *   *Sub-section (H3)*: 1. Manual Invalidation
*   **Title (H1)**: 1. Invalidate Memoized Function Cache for this specific product
*   **Title (H1)**: 2. Invalidate View Cache for catalog
        *   *Sub-section (H3)*: 2. Event-Driven ORM Invalidation (`sqlalchemy.event`)
    *   **Section (H2)**: 4. Mitigating Cache Stampede (Thundering Herd)
        *   *Sub-section (H3)*: Enterprise Mitigation Strategies:
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 23 - Application Caching Strategies\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 23: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Application Caching Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Caching Lifecycle (`C-A-C-H-E`)
        *   *Sub-section (H3)*: 2. Cache Hit Performance (`H-I-T-S`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-Caching Configuration
*   **Title (H1)**: Production Redis Setup
        *   *Sub-section (H3)*: 2. View Caching & Function Memoization
*   **Title (H1)**: 1. View Caching (Caches full route response)
*   **Title (H1)**: 2. Function Memoization (Caches function return value per argument)
        *   *Sub-section (H3)*: 3. Cache Invalidation
*   **Title (H1)**: Update DB...

### 📄 File: [5. Practice and Interview Questions.md](DAY 23 - Application Caching Strategies\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 23: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is Application Caching?
        *   *Sub-section (H3)*: Q2: What is the difference between a Cache Hit and a Cache Miss?
        *   *Sub-section (H3)*: Q3: What is Cache Invalidation?
        *   *Sub-section (H3)*: Q4: What is `Flask-Caching`?
        *   *Sub-section (H3)*: Q5: Why is querying RAM faster than querying a Relational Database?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `@cache.cached()` and `@cache.memoize()`?
        *   *Sub-section (H3)*: Q7: What is the difference between `SimpleCache` and `RedisCache` in `Flask-Caching`?
        *   *Sub-section (H3)*: Q8: How do you invalidate a memoized function cache when a database record updates?
        *   *Sub-section (H3)*: Q9: How can you generate custom cache keys incorporating request headers or API keys?
        *   *Sub-section (H3)*: Q10: How does `CACHE_DEFAULT_TIMEOUT` work?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: What is a Cache Stampede (Thundering Herd) and how do you prevent it in high-traffic APIs?
        *   *Sub-section (H3)*: Q12: How can you automate cache invalidation using SQLAlchemy ORM Event Listeners?
        *   *Sub-section (H3)*: Q13: What is Cache Penetration and how do you prevent it?
        *   *Sub-section (H3)*: Q14: What is the difference between Write-Through, Write-Back, and Cache-Aside caching patterns?
        *   *Sub-section (H3)*: Q15: Why is configuring `CACHE_KEY_PREFIX` critical in microservices sharing a single Redis cluster?

## 📁 DAY 24 - Real-Time WebSockets with Flask-SocketIO

### 📄 File: [0. WebSockets and Flask-SocketIO Fundamentals for Beginners.md](DAY 24 - Real-Time WebSockets with Flask-SocketIO\0. WebSockets and Flask-SocketIO Fundamentals for Beginners.md)
*   **Title (H1)**: Day 24 - Module 0: WebSockets & Flask-SocketIO Fundamentals for Beginners
    *   **Section (H2)**: 1. HTTP vs. WebSockets in Plain English
    *   **Section (H2)**: 2. Short Polling vs. WebSockets
    *   **Section (H2)**: 3. What is `Flask-SocketIO`?
    *   **Section (H2)**: 4. Key Socket.IO Concepts: Events, Rooms & Namespaces
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. WebSocket Protocol and Flask-SocketIO.md](DAY 24 - Real-Time WebSockets with Flask-SocketIO\1. WebSocket Protocol and Flask-SocketIO.md)
*   **Title (H1)**: Day 24 - Module 1: WebSocket Protocol & Flask-SocketIO
    *   **Section (H2)**: 1. The WebSocket Protocol Handshake (`HTTP 101`)
    *   **Section (H2)**: 2. Initializing `Flask-SocketIO`
*   **Title (H1)**: Initialize SocketIO with CORS permissions
    *   **Section (H2)**: 3. Registering Event Handlers (`@socketio.on`)
*   **Title (H1)**: Built-in Event: Connection established
*   **Title (H1)**: Built-in Event: Client disconnected
*   **Title (H1)**: Custom Event: Handle incoming chat message
*   **Title (H1)**: Broadcast message to ALL connected clients!
    *   **Section (H2)**: 4. Launching the App with `socketio.run`
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Rooms, Namespaces and Redis Message Brokers.md](DAY 24 - Real-Time WebSockets with Flask-SocketIO\2. Rooms, Namespaces and Redis Message Brokers.md)
*   **Title (H1)**: Day 24 - Module 2: Rooms, Namespaces & Multi-Node Scaling
    *   **Section (H2)**: 1. Multi-Room Group Channels (`join_room` & `leave_room`)
*   **Title (H1)**: Broadcast join notification ONLY to clients inside this room!
*   **Title (H1)**: Target message ONLY to clients in room
    *   **Section (H2)**: 2. Namespaces for Route Multiplexing
*   **Title (H1)**: Register Namespace
    *   **Section (H2)**: 3. Production Scaling with Redis Pub/Sub (`message_queue`)
        *   *Sub-section (H3)*: The Enterprise Solution: Redis Message Queue (Pub/Sub)
*   **Title (H1)**: Multi-Worker Redis Pub/Sub Integration
    *   **Section (H2)**: 4. Production Asynchronous Servers (Eventlet / Gevent)
*   **Title (H1)**: Production Gunicorn Command with Eventlet Workers
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 24 - Real-Time WebSockets with Flask-SocketIO\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 24: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Real-Time WebSockets Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. WebSocket Features (`W-A-L-K-I-E`)
        *   *Sub-section (H3)*: 2. Multi-Room Channels (`R-O-O-M-S`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-SocketIO Server Initialization
*   **Title (H1)**: Handshake connection
*   **Title (H1)**: Room joining & emitting
*   **Title (H1)**: Start server
        *   *Sub-section (H3)*: 2. Client-Side Browser JavaScript (Socket.IO)

### 📄 File: [5. Practice and Interview Questions.md](DAY 24 - Real-Time WebSockets with Flask-SocketIO\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 24: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is a WebSocket?
        *   *Sub-section (H3)*: Q2: What is the main difference between HTTP Polling and WebSockets?
        *   *Sub-section (H3)*: Q3: What is `Flask-SocketIO`?
        *   *Sub-section (H3)*: Q4: What is an Event in `Flask-SocketIO`?
        *   *Sub-section (H3)*: Q5: What is a Room in `Flask-SocketIO`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `send()` and `emit()` in `Flask-SocketIO`?
        *   *Sub-section (H3)*: Q7: What does `broadcast=True` do when emitting an event?
        *   *Sub-section (H3)*: Q8: How do you send a message exclusively to clients inside a specific room?
        *   *Sub-section (H3)*: Q9: Why must you launch your application with `socketio.run(app)` instead of standard `app.run()`?
        *   *Sub-section (H3)*: Q10: What HTTP status code signals a successful WebSocket handshake upgrade?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why does cross-client broadcasting fail when running Gunicorn with multiple worker processes, and how do you solve it?
        *   *Sub-section (H3)*: Q12: Why are asynchronous greenlet worker servers (Eventlet or Gevent) mandatory for WebSockets in production?
        *   *Sub-section (H3)*: Q13: What is the difference between WebSockets and Server-Sent Events (SSE)?
        *   *Sub-section (H3)*: Q14: How does Socket.IO handle client reconnections after network drops?
        *   *Sub-section (H3)*: Q15: How do you secure WebSocket connections with JWT authentication in `Flask-SocketIO`?

## 📁 DAY 25 - Asynchronous Flask and Quart Integration

### 📄 File: [0. Async Flask and Quart Fundamentals for Beginners.md](DAY 25 - Asynchronous Flask and Quart Integration\0. Async Flask and Quart Fundamentals for Beginners.md)
*   **Title (H1)**: Day 25 - Module 0: Async Flask & Quart Fundamentals for Beginners
    *   **Section (H2)**: 1. What is `async` / `await` in Plain English?
    *   **Section (H2)**: 2. WSGI vs. ASGI Explained Simply
    *   **Section (H2)**: 3. Native Async Support in Flask 2.0+
*   **Title (H1)**: Flask 2.0+ Native Async Route!
*   **Title (H1)**: Non-blocking async sleep or async HTTP call
    *   **Section (H2)**: 4. What is Quart?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Async Routes and ASGI Compatibility.md](DAY 25 - Asynchronous Flask and Quart Integration\1. Async Routes and ASGI Compatibility.md)
*   **Title (H1)**: Day 25 - Module 1: Async Routes & ASGI Compatibility
    *   **Section (H2)**: 1. Native `async def` Routes in Flask 2.0+
*   **Title (H1)**: Concurrent Async Helper Function
*   **Title (H1)**: Non-blocking HTTP GET request!
*   **Title (H1)**: Native Async Route in Flask 2.0+
    *   **Section (H2)**: 2. High-Concurrency Parallel Fetching (`asyncio.gather`)
*   **Title (H1)**: ⚠️ Sequential execution would take 1s + 1s + 1s = 3.0 seconds!
*   **Title (H1)**: ✅ Parallel asyncio.gather takes 1.05 seconds total!
    *   **Section (H2)**: 3. The Blocking I/O Trap ⚠️
*   **Title (H1)**: ❌ INCORRECT (Freezes the async event loop for all users!)
*   **Title (H1)**: ✅ CORRECT (Non-blocking async sleep)
*   **Title (H1)**: Offload blocking synchronous function to background thread pool
    *   **Section (H2)**: 4. Deploying Flask as an ASGI App (`WsgiToAsgi`)
*   **Title (H1)**: asgi_app.py
*   **Title (H1)**: Convert WSGI Flask app into an ASGI compatible application
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Comparing Async Flask with Quart and FastAPI.md](DAY 25 - Asynchronous Flask and Quart Integration\2. Comparing Async Flask with Quart and FastAPI.md)
*   **Title (H1)**: Day 25 - Module 2: Comparing Async Flask with Quart and FastAPI
    *   **Section (H2)**: 1. What is Quart?
        *   *Sub-section (H3)*: Side-by-Side Comparison:
*   **Title (H1)**: 1. Flask Syntax (Sync-First)
*   **Title (H1)**: 2. Quart Syntax (Async-Native - Identical API!)
    *   **Section (H2)**: 2. Framework Ecosystem Comparison Table
    *   **Section (H2)**: 3. High-Throughput Async Streaming Responses
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 25 - Asynchronous Flask and Quart Integration\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 25: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Async Flask & Quart Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Asynchronous Execution (`A-S-Y-N-C`)
        *   *Sub-section (H3)*: 2. ASGI Architecture (`A-S-G-I`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Native Async Route in Flask 2.0+
        *   *Sub-section (H3)*: 2. Parallel Concurrency with `asyncio.gather()`
*   **Title (H1)**: Runs all 3 tasks concurrently in ~1 sec total!
        *   *Sub-section (H3)*: 3. Quart Application Setup

### 📄 File: [5. Practice and Interview Questions.md](DAY 25 - Asynchronous Flask and Quart Integration\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 25: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the difference between Synchronous and Asynchronous execution?
        *   *Sub-section (H3)*: Q2: What is the difference between WSGI and ASGI?
        *   *Sub-section (H3)*: Q3: What library powers `async def` routes in Flask 2.0+ under the hood?
        *   *Sub-section (H3)*: Q4: What is Quart?
        *   *Sub-section (H3)*: Q5: What does the `await` keyword do in Python?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: How do you run multiple asynchronous HTTP calls concurrently in parallel?
        *   *Sub-section (H3)*: Q7: What major pitfall occurs if you call `time.sleep(5)` inside a Flask `async def` route?
        *   *Sub-section (H3)*: Q8: How should you handle blocking synchronous functions inside an `async def` route?
        *   *Sub-section (H3)*: Q9: What is the main difference between reading request JSON in Flask vs Quart?
        *   *Sub-section (H3)*: Q10: How do you wrap a Flask WSGI app to run on Uvicorn ASGI server?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why does native `async def` in Flask 2.0+ not provide true ASGI concurrency unless deployed on an ASGI server or Quart?
        *   *Sub-section (H3)*: Q12: How do you implement Server-Sent Events (SSE) streaming responses in Quart?
        *   *Sub-section (H3)*: Q13: What is the difference between CPU-bound tasks and I/O-bound tasks in async architectures?
        *   *Sub-section (H3)*: Q14: How does FastAPI compare to Quart for enterprise microservices?
        *   *Sub-section (H3)*: Q15: How can you handle database connection pooling when using `async` routes in Flask/Quart?

## 📁 DAY 26 - Enterprise Flask Security Hardening

### 📄 File: [0. Web Security and Flask Hardening Fundamentals for Beginners.md](DAY 26 - Enterprise Flask Security Hardening\0. Web Security and Flask Hardening Fundamentals for Beginners.md)
*   **Title (H1)**: Day 26 - Module 0: Web Security & Flask Hardening Fundamentals for Beginners
    *   **Section (H2)**: 1. Why Web Security Matters: The OWASP Top 10
    *   **Section (H2)**: 2. What are HTTP Security Headers in Plain English?
    *   **Section (H2)**: 3. Core Security Headers Explained
    *   **Section (H2)**: 4. What is `Flask-Talisman`?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. CSP, Talisman and Security Headers.md](DAY 26 - Enterprise Flask Security Hardening\1. CSP, Talisman and Security Headers.md)
*   **Title (H1)**: Day 26 - Module 1: CSP, Talisman & Security Headers
    *   **Section (H2)**: 1. Setting Up `Flask-Talisman`
*   **Title (H1)**: 1. Define Strict Content Security Policy (CSP) Directives
*   **Title (H1)**: 2. Attach Talisman Security Hardening Extension
    *   **Section (H2)**: 2. Deep Dive: HTTP Security Headers Injected by Talisman
    *   **Section (H2)**: 3. Dynamic CSP Nonces (`@talisman.nonce`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. SQL Injection, XSS and Sanitization Defense.md](DAY 26 - Enterprise Flask Security Hardening\2. SQL Injection, XSS and Sanitization Defense.md)
*   **Title (H1)**: Day 26 - Module 2: SQL Injection, XSS & Input Sanitization
    *   **Section (H2)**: 1. SQL Injection (SQLi) Defenses
*   **Title (H1)**: ❌ VULNERABLE TO SQL INJECTION (Raw string concatenation!)
*   **Title (H1)**: ✅ SECURE (SQLAlchemy ORM Parameterized Query)
*   **Title (H1)**: SQLAlchemy automatically uses parameterized query placeholders!
    *   **Section (H2)**: 2. Jinja2 Auto-Escaping & The Danger of `|safe`
    *   **Section (H2)**: 3. HTML Input Sanitization with `Bleach`
    *   **Section (H2)**: 4. Static Code Security Auditing (`bandit` & `pip-audit`)
        *   *Sub-section (H3)*: 1. Python Code Vulnerability Scanner (`bandit`)
        *   *Sub-section (H3)*: 2. Dependency Vulnerability Scanner (`pip-audit`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 26 - Enterprise Flask Security Hardening\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 26: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Security Hardening Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. HTTP Security Headers (`H-E-A-D-E-R-S`)
        *   *Sub-section (H3)*: 2. Input Sanitization Defenses (`S-E-C-U-R-E`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Flask-Talisman Setup & CSP Directives
        *   *Sub-section (H3)*: 2. Jinja2 CSP Nonce Injection
        *   *Sub-section (H3)*: 3. HTML Input Sanitization with Bleach
        *   *Sub-section (H3)*: 4. CLI Security Audit Commands

### 📄 File: [5. Practice and Interview Questions.md](DAY 26 - Enterprise Flask Security Hardening\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 26: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What are HTTP Security Headers?
        *   *Sub-section (H3)*: Q2: What is Content Security Policy (CSP)?
        *   *Sub-section (H3)*: Q3: What is Cross-Site Scripting (XSS)?
        *   *Sub-section (H3)*: Q4: What is SQL Injection (SQLi)?
        *   *Sub-section (H3)*: Q5: What is `Flask-Talisman`?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is HSTS (`Strict-Transport-Security`) and why is it important?
        *   *Sub-section (H3)*: Q7: What is Clickjacking and how does `X-Frame-Options: DENY` prevent it?
        *   *Sub-section (H3)*: Q8: Why is the Jinja2 `|safe` filter dangerous when rendering user input?
        *   *Sub-section (H3)*: Q9: What does `session_cookie_http_only=True` accomplish in Flask?
        *   *Sub-section (H3)*: Q10: How does `bleach.clean()` differ from standard HTML escaping (`html.escape()`)?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do CSP Nonces resolve the inline script restriction without using `'unsafe-inline'`?
        *   *Sub-section (H3)*: Q12: How does SQLAlchemy ORM eliminate SQL Injection risks by design?
        *   *Sub-section (H3)*: Q13: What is Subresource Integrity (SRI) and why should it be used for CDN scripts?
        *   *Sub-section (H3)*: Q14: How does `Bandit` perform static security analysis on Python code?
        *   *Sub-section (H3)*: Q15: What is the difference between `SameSite=Strict` and `SameSite=Lax` cookie attributes?

## 📁 DAY 27 - Error Handling, Logging and Observability

### 📄 File: [0. Error Handling and Observability Fundamentals for Beginners.md](DAY 27 - Error Handling, Logging and Observability\0. Error Handling and Observability Fundamentals for Beginners.md)
*   **Title (H1)**: Day 27 - Module 0: Error Handling & Observability Fundamentals for Beginners
    *   **Section (H2)**: 1. What are Error Handling, Logging, and Observability?
    *   **Section (H2)**: 2. The 5 Python Logging Levels
    *   **Section (H2)**: 3. Why Unstructured Text Logs Fail vs. Structured JSON Logging
*   **Title (H1)**: ❌ Unstructured Text Log (Hard for machines to search!)
    *   **Section (H2)**: 4. What is a Request Correlation ID (`X-Request-ID`)?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Structured Logging and Observability.md](DAY 27 - Error Handling, Logging and Observability\1. Structured Logging and Observability.md)
*   **Title (H1)**: Day 27 - Module 1: Structured Logging & Observability
    *   **Section (H2)**: 1. Configuring `dictConfig` for Structured JSON Logs
*   **Title (H1)**: Configure Structured Logging before initializing Flask app!
    *   **Section (H2)**: 2. Using `app.logger` inside Route Handlers
*   **Title (H1)**: Process order...
    *   **Section (H2)**: 3. Injecting Request Correlation IDs (`X-Request-ID`)
*   **Title (H1)**: Extract X-Request-ID from client header or generate a fresh UUID4
*   **Title (H1)**: Pass correlation ID back in response headers for client tracing!
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Centralized Error Handlers and APM Metrics.md](DAY 27 - Error Handling, Logging and Observability\2. Centralized Error Handlers and APM Metrics.md)
*   **Title (H1)**: Day 27 - Module 2: Centralized Error Handlers & APM Observability
    *   **Section (H2)**: 1. Designing a Custom Exception Hierarchy
    *   **Section (H2)**: 2. Centralized Error Handlers (`@app.errorhandler`)
*   **Title (H1)**: 1. Catch Custom Domain Exceptions
*   **Title (H1)**: 2. Catch Standard HTTP 404 Not Found
*   **Title (H1)**: 3. Catch Unhandled 500 Server Crashes (Safety Net!)
*   **Title (H1)**: Log full traceback to file for developer investigation
*   **Title (H1)**: Return clean generic JSON to client (DO NOT expose raw traceback!)
    *   **Section (H2)**: 3. Production Stack Trace Security Rule 🛡️
    *   **Section (H2)**: 4. APM Error Tracking Integration (Sentry)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 27 - Error Handling, Logging and Observability\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 27: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Error Handling & Observability Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Structured Logging Setup (`L-O-G-S`)
        *   *Sub-section (H3)*: 2. Error Handling Lifecycle (`T-R-A-C-E`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Correlation ID Middleware (`X-Request-ID`)
        *   *Sub-section (H3)*: 2. Custom Exception & Centralized Error Handler

### 📄 File: [5. Practice and Interview Questions.md](DAY 27 - Error Handling, Logging and Observability\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 27: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the purpose of Error Handling in web applications?
        *   *Sub-section (H3)*: Q2: What are the 5 standard Python Logging Levels in order of increasing severity?
        *   *Sub-section (H3)*: Q3: Why is Structured JSON Logging preferred over plain text `print()` statements in production?
        *   *Sub-section (H3)*: Q4: How do you log messages in Flask?
        *   *Sub-section (H3)*: Q5: What is a Request Correlation ID (`X-Request-ID`)?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: Why should internal exception stack tracebacks never be exposed to users in production?
        *   *Sub-section (H3)*: Q7: How do you log a full exception traceback to a file while returning a generic JSON error to the user?
        *   *Sub-section (H3)*: Q8: How do you design a custom domain exception hierarchy in Flask?
        *   *Sub-section (H3)*: Q9: How do you prevent log files from filling up a server's hard drive?
        *   *Sub-section (H3)*: Q10: How do you register a global exception handler for HTTP 404 errors?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How does Application Performance Monitoring (APM) with Sentry work in Flask?
        *   *Sub-section (H3)*: Q12: How do you inject Correlation IDs automatically into all Python log records using custom `logging.Filter` classes?
        *   *Sub-section (H3)*: Q13: What is the ELK Stack and how does it ingest Flask logs?
        *   *Sub-section (H3)*: Q14: What is Log Sampling and why is it used in high-traffic production environments?
        *   *Sub-section (H3)*: Q15: How do OpenTelemetry and W3C Trace Context headers (`traceparent`) enable distributed tracing across microservices?

## 📁 DAY 28 - Flask Performance Tuning and Database Optimization

### 📄 File: [0. Performance Tuning and Optimization Fundamentals for Beginners.md](DAY 28 - Flask Performance Tuning and Database Optimization\0. Performance Tuning and Optimization Fundamentals for Beginners.md)
*   **Title (H1)**: Day 28 - Module 0: Performance Tuning & Optimization Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Application Performance Tuning in Plain English?
    *   **Section (H2)**: 2. The N+1 Database Query Problem Explained
    *   **Section (H2)**: 3. Eager Loading vs. Lazy Loading
    *   **Section (H2)**: 4. Response Compression (Gzip) & Code Profiling
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Profiling, Eager Loading and Compression.md](DAY 28 - Flask Performance Tuning and Database Optimization\1. Profiling, Eager Loading and Compression.md)
*   **Title (H1)**: Day 28 - Module 1: Profiling, Eager Loading & Compression
    *   **Section (H2)**: 1. Resolving N+1 Queries with `joinedload` & `selectinload`
*   **Title (H1)**: ❌ UNOPTIMIZED: Causes 101 Database Queries! (N+1 Trap)
*   **Title (H1)**: Accessing author.books triggers a NEW SELECT query per author!
*   **Title (H1)**: ✅ OPTIMIZED: Executed in 1 SINGLE SQL JOIN Query!
*   **Title (H1)**: joinedload performs SQL LEFT OUTER JOIN instantly
        *   *Sub-section (H3)*: When to use `joinedload` vs `selectinload`:
    *   **Section (H2)**: 2. Database Connection Pool Tuning
    *   **Section (H2)**: 3. HTTP Response Compression (`Flask-Compress`)
*   **Title (H1)**: Configurable minimum size threshold (e.g. compress responses > 500 bytes)
    *   **Section (H2)**: 4. Query Pagination (`paginate`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Werkzeug Profiler Middleware and Memory Leak Audits.md](DAY 28 - Flask Performance Tuning and Database Optimization\2. Werkzeug Profiler Middleware and Memory Leak Audits.md)
*   **Title (H1)**: Day 28 - Module 2: Werkzeug Profiler Middleware & Memory Leak Audits
    *   **Section (H2)**: 1. Profiling CPU Execution with Werkzeug `ProfilerMiddleware`
*   **Title (H1)**: Attach Profiler Middleware in Development/Staging
    *   **Section (H2)**: 2. SQLAlchemy Slow Query Event Listener
*   **Title (H1)**: 1. Capture query start timestamp
*   **Title (H1)**: 2. Calculate query duration upon completion
*   **Title (H1)**: Trigger Warning Log for Slow Queries (> 0.20 seconds)
    *   **Section (H2)**: 3. Auditing Memory Leaks with `tracemalloc`
*   **Title (H1)**: Start tracking memory allocations
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 28 - Flask Performance Tuning and Database Optimization\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 28: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Performance Tuning Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Application Performance Optimization (`S-P-E-E-D`)
        *   *Sub-section (H3)*: 2. Database Query Optimization (`E-A-G-E-R`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. SQLAlchemy Eager Loading
*   **Title (H1)**: Left Outer Join (1-to-1 or Many-to-1)
*   **Title (H1)**: SQL IN (...) Clause (1-to-Many)
        *   *Sub-section (H3)*: 2. Response Payload Compression
        *   *Sub-section (H3)*: 3. CPU Execution Profiler
        *   *Sub-section (H3)*: 4. Database Slow Query Logger Listener

### 📄 File: [5. Practice and Interview Questions.md](DAY 28 - Flask Performance Tuning and Database Optimization\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 28: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is the N+1 Query Problem in ORM frameworks?
        *   *Sub-section (H3)*: Q2: How do you fix the N+1 Query Problem in SQLAlchemy?
        *   *Sub-section (H3)*: Q3: What is Gzip response payload compression and why is it used?
        *   *Sub-section (H3)*: Q4: What extension enables Gzip compression in Flask?
        *   *Sub-section (H3)*: Q5: What is Code Profiling?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the difference between `joinedload()` and `selectinload()` in SQLAlchemy?
        *   *Sub-section (H3)*: Q7: What does Werkzeug's `ProfilerMiddleware` do?
        *   *Sub-section (H3)*: Q8: What parameters control database connection pooling in Flask-SQLAlchemy?
        *   *Sub-section (H3)*: Q9: Why is raw `Query.all()` dangerous on large database tables?
        *   *Sub-section (H3)*: Q10: How do you configure minimum payload size thresholds for `Flask-Compress`?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: How do you intercept and log slow SQL queries using SQLAlchemy Engine event listeners?
        *   *Sub-section (H3)*: Q12: How does Python's `tracemalloc` module help diagnose memory leaks in Flask?
        *   *Sub-section (H3)*: Q13: What is Connection Pool Starvation and how do you prevent it in high-concurrency Flask apps?
        *   *Sub-section (H3)*: Q14: What is the difference between B-Tree and Hash indexes in database optimization?
        *   *Sub-section (H3)*: Q15: How does HTTP Caching headers (`Cache-Control: max-age=3600, ETag`) complement server-side performance tuning?

## 📁 DAY 29 - Automated Testing Masterclass with Pytest

### 📄 File: [0. Automated Testing and Pytest Fundamentals for Beginners.md](DAY 29 - Automated Testing Masterclass with Pytest\0. Automated Testing and Pytest Fundamentals for Beginners.md)
*   **Title (H1)**: Day 29 - Module 0: Automated Testing & Pytest Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Automated Testing in Plain English?
    *   **Section (H2)**: 2. The Software Testing Pyramid
    *   **Section (H2)**: 3. What is Pytest?
*   **Title (H1)**: Simple Pytest Function
    *   **Section (H2)**: 4. Key Testing Concepts: Fixtures, Coverage & CI
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Pytest, Test Client and Fixtures.md](DAY 29 - Automated Testing Masterclass with Pytest\1. Pytest, Test Client and Fixtures.md)
*   **Title (H1)**: Day 29 - Module 1: Pytest, Test Client & Fixtures
    *   **Section (H2)**: 1. Project Test Setup (`conftest.py`)
*   **Title (H1)**: conftest.py
    *   **Section (H2)**: 2. Simulating HTTP Requests with `app.test_client()`
*   **Title (H1)**: test_auth_api.py
*   **Title (H1)**: Simulate HTTP POST request with JSON payload
*   **Title (H1)**: 1. Assert Status Code
*   **Title (H1)**: 2. Assert Response JSON
    *   **Section (H2)**: 3. Advanced Fixtures: Authentication Headers
*   **Title (H1)**: 1. Register test user
*   **Title (H1)**: 2. Log in to obtain JWT access token
*   **Title (H1)**: 3. Inject Bearer token header into client environment
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Database Mocking, Coverage and GitHub Actions CI.md](DAY 29 - Automated Testing Masterclass with Pytest\2. Database Mocking, Coverage and GitHub Actions CI.md)
*   **Title (H1)**: Day 29 - Module 2: Database Mocking, Coverage & GitHub Actions CI
    *   **Section (H2)**: 1. Mocking External Services (`pytest-mock` / `unittest.mock`)
*   **Title (H1)**: service.py
*   **Title (H1)**: Real external API call to Stripe
*   **Title (H1)**: test_payment_service.py
*   **Title (H1)**: 1. Create a fake response object
*   **Title (H1)**: 2. Patch requests.post to return fake response instantly
*   **Title (H1)**: 3. Call service function (executes in 0.001s without hitting Stripe network!)
    *   **Section (H2)**: 2. Measuring Code Coverage (`pytest-cov`)
*   **Title (H1)**: Terminal summary output
*   **Title (H1)**: HTML interactive visual coverage report
    *   **Section (H2)**: 3. GitHub Actions Continuous Integration (CI) Pipeline
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 29 - Automated Testing Masterclass with Pytest\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 29: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Automated Testing Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Pytest Fixture Lifecycle (`F-I-X-T-U-R-E`)
        *   *Sub-section (H3)*: 2. Test Verification Rules (`A-S-S-E-R-T`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Root `conftest.py` Setup
        *   *Sub-section (H3)*: 2. Testing Route with Test Client & JSON Assertion
        *   *Sub-section (H3)*: 3. Mocking External API with Pytest-Mock
        *   *Sub-section (H3)*: 4. CLI Pytest & Coverage Commands

### 📄 File: [5. Practice and Interview Questions.md](DAY 29 - Automated Testing Masterclass with Pytest\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 29: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: What is Automated Testing and why is it essential for software development?
        *   *Sub-section (H3)*: Q2: What is `Pytest`?
        *   *Sub-section (H3)*: Q3: What is Flask's `test_client()`?
        *   *Sub-section (H3)*: Q4: What is a Pytest Fixture?
        *   *Sub-section (H3)*: Q5: What is Code Coverage?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: Why should `TESTING = True` be set in Flask test configurations?
        *   *Sub-section (H3)*: Q7: How does fixture teardown work using the `yield` keyword in Pytest?
        *   *Sub-section (H3)*: Q8: What are the different Fixture Scopes in Pytest?
        *   *Sub-section (H3)*: Q9: Why use `sqlite:///:memory:` for database integration tests?
        *   *Sub-section (H3)*: Q10: How do you check JSON response data in Pytest assertions?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Questions
        *   *Sub-section (H3)*: Q11: Why should external third-party API calls (e.g. Stripe, SendGrid) be mocked during automated tests, and how do you mock them?
        *   *Sub-section (H3)*: Q12: How do `@pytest.mark.parametrize` decorators reduce test code duplication?
        *   *Sub-section (H3)*: Q13: How do you achieve database transaction rollback per test to speed up test suites?
        *   *Sub-section (H3)*: Q14: How does a Continuous Integration (CI) pipeline work in GitHub Actions for Flask?
        *   *Sub-section (H3)*: Q15: What is the difference between Fakes, Mocks, and Stubs in automated testing?

## 📁 DAY 30 - Production Capstone and Deployment

### 📄 File: [0. Production Deployment and Architecture Fundamentals for Beginners.md](DAY 30 - Production Capstone and Deployment\0. Production Deployment and Architecture Fundamentals for Beginners.md)
*   **Title (H1)**: Day 30 - Module 0: Production Deployment & Architecture Fundamentals for Beginners
    *   **Section (H2)**: 1. What is Production Deployment in Plain English?
    *   **Section (H2)**: 2. Why `flask run` (Werkzeug) CANNOT Be Used in Production
    *   **Section (H2)**: 3. The 3-Tier Enterprise Production Web Stack
    *   **Section (H2)**: 4. What is Docker & Containerization?
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [1. Production Deployment Guide.md](DAY 30 - Production Capstone and Deployment\1. Production Deployment Guide.md)
*   **Title (H1)**: Day 30 - Module 1: Production Deployment Guide
    *   **Section (H2)**: 1. The 12-Factor App Rules for Enterprise Flask
    *   **Section (H2)**: 2. Production Environment & Secrets Management
*   **Title (H1)**: config.py
    *   **Section (H2)**: 3. Production Database Migration Pipeline
*   **Title (H1)**: Automated Deployment Script Hook
    *   **Section (H2)**: 4. Kubernetes Healthcheck & Readiness Probes (`/healthz` & `/readyz`)
*   **Title (H1)**: Check Database
*   **Title (H1)**: Check Redis
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [2. Gunicorn, Nginx and Docker Containerization.md](DAY 30 - Production Capstone and Deployment\2. Gunicorn, Nginx and Docker Containerization.md)
*   **Title (H1)**: Day 30 - Module 2: Gunicorn, Nginx & Docker Containerization
    *   **Section (H2)**: 1. Gunicorn Production Setup
        *   *Sub-section (H3)*: Worker Formula Rule:
*   **Title (H1)**: Launch Gunicorn with 5 Workers on Port 8000
    *   **Section (H2)**: 2. Nginx Reverse Proxy Configuration
*   **Title (H1)**: /etc/nginx/sites-available/flask_app
*   **Title (H1)**: Static Assets Served Directly by Nginx (Bypasses Flask!)
*   **Title (H1)**: Proxy API Requests to Gunicorn WSGI Server
    *   **Section (H2)**: 3. Production Multi-Stage `Dockerfile`
*   **Title (H1)**: Multi-Stage Dockerfile for Flask
*   **Title (H1)**: Final Production Stage
*   **Title (H1)**: Create non-root system user for container security!
*   **Title (H1)**: Copy installed dependencies and code
    *   **Section (H2)**: 4. Multi-Container Orchestration (`docker-compose.yml`)
    *   **Section (H2)**: 💡 Summary Checklist

### 📄 File: [4. Memory Shortcuts and Cheatsheet.md](DAY 30 - Production Capstone and Deployment\4. Memory Shortcuts and Cheatsheet.md)
*   **Title (H1)**: Day 30: Memory Shortcuts & Cheatsheet
    *   **Section (H2)**: 🔤 Production Deployment Terminology Decoder
    *   **Section (H2)**: 🧠 Memory Mnemonics
        *   *Sub-section (H3)*: 1. Production Launch Checklist (`D-E-P-L-O-Y`)
        *   *Sub-section (H3)*: 2. Dockerfile Best Practices (`D-O-C-K-E-R`)
    *   **Section (H2)**: ⚡ Quick-Reference Code Snippets
        *   *Sub-section (H3)*: 1. Gunicorn Startup Command
*   **Title (H1)**: Gunicorn with 5 workers on 2 CPU Cores
        *   *Sub-section (H3)*: 2. Nginx Reverse Proxy Pass
        *   *Sub-section (H3)*: 3. Production Dockerfile Snippet
        *   *Sub-section (H3)*: 4. Kubernetes Health & Readiness Probes

### 📄 File: [5. Practice and Interview Questions.md](DAY 30 - Production Capstone and Deployment\5. Practice and Interview Questions.md)
*   **Title (H1)**: Day 30: Practice & Technical Interview Questions
    *   **Section (H2)**: 🟢 Level 1: Absolute Beginner Questions
        *   *Sub-section (H3)*: Q1: Why should Flask's built-in development server (`flask run`) never be used in production?
        *   *Sub-section (H3)*: Q2: What is Gunicorn and what role does it play in Flask deployments?
        *   *Sub-section (H3)*: Q3: What is Nginx and why is it placed in front of Gunicorn?
        *   *Sub-section (H3)*: Q4: What is Docker and why is containerization useful?
        *   *Sub-section (H3)*: Q5: What is the difference between `/healthz` and `/readyz` endpoints?
    *   **Section (H2)**: 🟡 Level 2: Intermediate Questions
        *   *Sub-section (H3)*: Q6: What is the recommended formula for calculating Gunicorn worker processes?
        *   *Sub-section (H3)*: Q7: What are the key rules of the 12-Factor App methodology for Flask applications?
        *   *Sub-section (H3)*: Q8: Why should Docker containers run under a non-root system user (`USER appuser`)?
        *   *Sub-section (H3)*: Q9: What does `docker-compose` do?
        *   *Sub-section (H3)*: Q10: How do you handle database migrations during automated production deployments?
    *   **Section (H2)**: 🔴 Level 3: Advanced & Enterprise Capstone Architect Questions
        *   *Sub-section (H3)*: Q11: How do Blue-Green Deployments achieve zero-downtime production updates?
        *   *Sub-section (H3)*: Q12: How does Nginx perform SSL/TLS Termination?
        *   *Sub-section (H3)*: Q13: What happens when a Gunicorn worker process crashes due to an out-of-memory (OOM) exception?
        *   *Sub-section (H3)*: Q14: How do you prevent database connection pool exhaustion when scaling Gunicorn across multiple Docker container replicas?
        *   *Sub-section (H3)*: Q15: Looking back across all 30 Days of the Flask Masterclass, what are the 5 pillars of Enterprise Flask Application Architecture?

