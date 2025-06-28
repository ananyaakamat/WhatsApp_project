# HTML, CSS & JavaScript Best Practices Guide for AI Assistants

## Table of Contents
1. [Introduction](#introduction)
2. [HTML Best Practices](#html-best-practices)
3. [CSS Best Practices](#css-best-practices)
4. [JavaScript Best Practices](#javascript-best-practices)
5. [Integration & Architecture](#integration--architecture)
6. [Performance Optimization](#performance-optimization)
7. [Accessibility Guidelines](#accessibility-guidelines)
8. [Quick Reference Checklist](#quick-reference-checklist)

## Introduction

This guide provides comprehensive web development best practices for HTML, CSS, and JavaScript specifically designed for AI assistants to understand and apply. It covers modern web standards, semantic markup, responsive design, clean code principles, and performance optimization.

### Key Principles for AI Web Development
- **Semantic HTML**: Use meaningful markup that describes content structure
- **Responsive Design**: Create layouts that work across all devices
- **Progressive Enhancement**: Build from a solid foundation upward
- **Performance First**: Optimize for speed and efficiency
- **Accessibility**: Ensure content is usable by everyone
- **Maintainability**: Write code that's easy to understand and modify

## HTML Best Practices

### Semantic Markup

#### Use Semantic HTML5 Elements
```html
<!-- Good: Semantic structure that describes content -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Title - Site Name</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            <header>
                <h1>Article Title</h1>
                <time datetime="2025-06-28">June 28, 2025</time>
            </header>
            
            <section>
                <h2>Introduction</h2>
                <p>Article content goes here...</p>
            </section>
            
            <section>
                <h2>Main Content</h2>
                <p>More content...</p>
            </section>
        </article>
        
        <aside>
            <h2>Related Articles</h2>
            <ul>
                <li><a href="#article1">Related Article 1</a></li>
                <li><a href="#article2">Related Article 2</a></li>
            </ul>
        </aside>
    </main>
    
    <footer>
        <p>&copy; 2025 Site Name. All rights reserved.</p>
    </footer>
</body>
</html>

<!-- Bad: Non-semantic divs everywhere -->
<div class="page">
    <div class="top-section">
        <div class="menu">
            <div class="menu-item">Home</div>
            <div class="menu-item">About</div>
        </div>
    </div>
    
    <div class="content">
        <div class="article">
            <div class="title">Article Title</div>
            <div class="text">Content...</div>
        </div>
    </div>
    
    <div class="bottom">
        <div class="copyright">Copyright text</div>
    </div>
</div>
```

#### Proper Heading Hierarchy
```html
<!-- Good: Logical heading structure -->
<article>
    <h1>Main Article Title</h1>
    <section>
        <h2>Section Title</h2>
        <h3>Subsection</h3>
        <h3>Another Subsection</h3>
    </section>
    <section>
        <h2>Another Section</h2>
        <h3>Subsection</h3>
    </section>
</article>

<!-- Bad: Skipping heading levels and inconsistent hierarchy -->
<article>
    <h1>Main Title</h1>
    <h4>Should be h2</h4>  <!-- Skipped levels -->
    <h2>This comes after h4</h2>  <!-- Inconsistent -->
    <h1>Another h1 in article</h1>  <!-- Multiple h1s -->
</article>
```

### Forms and Accessibility

#### Proper Form Structure
```html
<!-- Good: Accessible form with proper labels and structure -->
<form action="/submit" method="post" novalidate>
    <fieldset>
        <legend>Personal Information</legend>
        
        <div class="form-group">
            <label for="firstName">First Name *</label>
            <input 
                type="text" 
                id="firstName" 
                name="firstName" 
                required 
                aria-describedby="firstName-error"
                autocomplete="given-name"
            >
            <span id="firstName-error" class="error" aria-live="polite"></span>
        </div>
        
        <div class="form-group">
            <label for="email">Email Address *</label>
            <input 
                type="email" 
                id="email" 
                name="email" 
                required 
                aria-describedby="email-help email-error"
                autocomplete="email"
            >
            <small id="email-help">We'll never share your email</small>
            <span id="email-error" class="error" aria-live="polite"></span>
        </div>
        
        <div class="form-group">
            <fieldset>
                <legend>Preferred Contact Method</legend>
                <input type="radio" id="contact-email" name="contact" value="email">
                <label for="contact-email">Email</label>
                
                <input type="radio" id="contact-phone" name="contact" value="phone">
                <label for="contact-phone">Phone</label>
            </fieldset>
        </div>
    </fieldset>
    
    <button type="submit">Submit</button>
</form>

<!-- Bad: Inaccessible form without proper labels -->
<form>
    <div>
        Name: <input type="text" placeholder="Enter name">  <!-- No label -->
    </div>
    <div>
        <input type="email">  <!-- No label or placeholder -->
    </div>
    <div>
        <input type="radio" name="contact" value="email"> Email
        <input type="radio" name="contact" value="phone"> Phone
        <!-- No labels for radio buttons -->
    </div>
    <input type="submit" value="Submit">
</form>
```

### Meta Tags and SEO

#### Essential Meta Tags
```html
<!-- Good: Complete meta tag setup -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO Meta Tags -->
    <title>Page Title - Site Name</title>
    <meta name="description" content="Concise description of page content for search engines">
    <meta name="keywords" content="relevant, keywords, for, page">
    <meta name="author" content="Author Name">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Page Title">
    <meta property="og:description" content="Description for social media sharing">
    <meta property="og:image" content="https://example.com/image.jpg">
    <meta property="og:url" content="https://example.com/page">
    <meta property="og:type" content="article">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Page Title">
    <meta name="twitter:description" content="Description for Twitter sharing">
    <meta name="twitter:image" content="https://example.com/image.jpg">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
</head>

<!-- Bad: Minimal or missing meta tags -->
<head>
    <title>Page</title>  <!-- Too generic -->
    <!-- Missing viewport, description, and other essential meta tags -->
</head>
```

## CSS Best Practices

### Organization and Structure

#### CSS Architecture (BEM Methodology)
```css
/* Good: BEM naming convention for maintainable CSS */
.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
}

.card__header {
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

.card__title {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

.card__content {
    line-height: 1.6;
}

.card--featured {
    border-color: #007bff;
    box-shadow: 0 4px 8px rgba(0, 123, 255, 0.1);
}

.card--large {
    padding: 2rem;
}

/* Bad: Non-descriptive class names and poor organization */
.blue-box {
    border: 1px solid blue;
}

.big {
    padding: 2rem;
}

.header-thing {
    border-bottom: 1px solid #eee;
}
```

#### CSS Custom Properties (CSS Variables)
```css
/* Good: Using CSS custom properties for maintainable theming */
:root {
    /* Color palette */
    --color-primary: #007bff;
    --color-primary-dark: #0056b3;
    --color-secondary: #6c757d;
    --color-success: #28a745;
    --color-danger: #dc3545;
    --color-warning: #ffc107;
    
    /* Typography */
    --font-family-primary: 'Inter', sans-serif;
    --font-family-secondary: 'Georgia', serif;
    --font-size-base: 1rem;
    --font-size-large: 1.25rem;
    --font-size-small: 0.875rem;
    --line-height-base: 1.6;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Breakpoints */
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
}

.button {
    background-color: var(--color-primary);
    color: white;
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: var(--font-family-primary);
    border: none;
    border-radius: 4px;
    transition: background-color 0.2s ease;
}

.button:hover {
    background-color: var(--color-primary-dark);
}

/* Dark theme support */
@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: #4dabf7;
        --color-primary-dark: #339af0;
    }
}

/* Bad: Hardcoded values throughout CSS */
.button {
    background-color: #007bff;  /* Repeated everywhere */
    padding: 8px 16px;  /* Magic numbers */
}

.card {
    color: #007bff;  /* Same color, but hardcoded again */
}
```

### Responsive Design

#### Mobile-First Approach
```css
/* Good: Mobile-first responsive design */
.container {
    width: 100%;
    padding: var(--spacing-md);
    margin: 0 auto;
}

.grid {
    display: grid;
    gap: var(--spacing-md);
    grid-template-columns: 1fr;  /* Mobile: single column */
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        max-width: 750px;
    }
    
    .grid {
        grid-template-columns: repeat(2, 1fr);  /* Tablet: 2 columns */
    }
}

/* Desktop */
@media (min-width: 992px) {
    .container {
        max-width: 970px;
    }
    
    .grid {
        grid-template-columns: repeat(3, 1fr);  /* Desktop: 3 columns */
    }
}

/* Large desktop */
@media (min-width: 1200px) {
    .container {
        max-width: 1170px;
    }
    
    .grid {
        grid-template-columns: repeat(4, 1fr);  /* Large: 4 columns */
    }
}

/* Bad: Desktop-first approach */
.container {
    width: 1200px;  /* Fixed width, not responsive */
    margin: 0 auto;
}

@media (max-width: 768px) {
    .container {
        width: 100%;  /* Forced to override */
    }
}
```

#### Flexbox and Grid Layouts
```css
/* Good: Modern layout techniques */

/* Flexbox for one-dimensional layouts */
.navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
}

.navigation__menu {
    display: flex;
    gap: var(--spacing-lg);
    list-style: none;
    margin: 0;
    padding: 0;
}

/* Grid for two-dimensional layouts */
.page-layout {
    display: grid;
    grid-template-areas: 
        "header header"
        "sidebar main"
        "footer footer";
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
    gap: var(--spacing-md);
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Responsive grid */
@media (max-width: 768px) {
    .page-layout {
        grid-template-areas: 
            "header"
            "main"
            "sidebar"
            "footer";
        grid-template-columns: 1fr;
    }
}

/* Bad: Float-based layouts and table displays */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}

.sidebar {
    float: left;
    width: 25%;
}

.main {
    float: right;
    width: 75%;
}

.navigation {
    display: table;
    width: 100%;
}

.nav-item {
    display: table-cell;
    text-align: center;
}
```

### Performance and Optimization

#### CSS Performance Best Practices
```css
/* Good: Efficient selectors and optimized CSS */

/* Use classes instead of complex selectors */
.article-title {
    font-size: 2rem;
    font-weight: bold;
    color: var(--color-primary);
}

/* Efficient animations using transform and opacity */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-in.is-visible {
    opacity: 1;
    transform: translateY(0);
}

/* Use will-change for animations */
.animated-element {
    will-change: transform;
}

.animated-element:hover {
    transform: scale(1.05);
    transition: transform 0.2s ease;
}

/* Critical CSS inlining approach */
.above-fold {
    /* Styles for above-the-fold content */
    display: block;
    visibility: visible;
}

/* Bad: Inefficient selectors and animations */

/* Overly specific selectors */
div.container > ul.menu > li.item > a.link {
    color: blue;
}

/* Inefficient animations */
.slow-animation {
    transition: width 0.3s, height 0.3s, left 0.3s, top 0.3s;
}

.slow-animation:hover {
    width: 200px;
    height: 200px;
    left: 100px;
    top: 100px;
}

/* Universal selector performance issues */
* {
    box-sizing: border-box;  /* Better to be more specific */
}
```

## JavaScript Best Practices

### Modern ES6+ Syntax

#### Variables and Functions
```javascript
// Good: Use const/let and modern function syntax
const API_BASE_URL = 'https://api.example.com';
let currentUser = null;

// Arrow functions for simple operations
const multiply = (a, b) => a * b;

// Regular functions for complex operations
function calculateTotal(items) {
    return items.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);
}

// Async/await for asynchronous operations
async function fetchUserData(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        throw error;
    }
}

// Bad: Old-style variable declarations and syntax
var apiUrl = 'https://api.example.com';  // Use const instead
var user;  // Use let instead

function multiply(a, b) {
    return a * b;  // Could be an arrow function
}

// Callback hell instead of async/await
function getUserData(userId, callback) {
    fetch(apiUrl + '/users/' + userId)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            callback(null, data);
        })
        .catch(function(error) {
            callback(error, null);
        });
}
```

#### Object and Array Handling
```javascript
// Good: Modern object and array methods
const users = [
    { id: 1, name: 'John', role: 'admin' },
    { id: 2, name: 'Jane', role: 'user' },
    { id: 3, name: 'Bob', role: 'user' }
];

// Destructuring assignment
const { id, name, role } = users[0];
const [firstUser, secondUser] = users;

// Spread operator for array/object manipulation
const newUser = { id: 4, name: 'Alice', role: 'user' };
const updatedUsers = [...users, newUser];

const userUpdate = { role: 'admin' };
const updatedUser = { ...users[0], ...userUpdate };

// Modern array methods
const adminUsers = users.filter(user => user.role === 'admin');
const userNames = users.map(user => user.name);
const hasAdmin = users.some(user => user.role === 'admin');
const userById = users.find(user => user.id === 2);

// Template literals
const greeting = `Hello, ${name}! You are logged in as ${role}.`;

// Object shorthand
function createUser(name, email, role = 'user') {
    return {
        name,           // Instead of name: name
        email,          // Instead of email: email
        role,           // Instead of role: role
        createdAt: new Date(),
        getId() {       // Method shorthand
            return this.id;
        }
    };
}

// Bad: Old-style object and string manipulation
var user = users[0];
var id = user.id;
var name = user.name;
var role = user.role;

var newUsers = users.concat([newUser]);  // Use spread instead

var greeting = 'Hello, ' + name + '! You are logged in as ' + role + '.';

function createUser(name, email, role) {
    return {
        name: name,
        email: email,
        role: role || 'user',
        createdAt: new Date(),
        getId: function() {
            return this.id;
        }
    };
}
```

### Error Handling and Validation

#### Robust Error Handling
```javascript
// Good: Comprehensive error handling
class ValidationError extends Error {
    constructor(field, message) {
        super(`${field}: ${message}`);
        this.name = 'ValidationError';
        this.field = field;
    }
}

class ApiError extends Error {
    constructor(status, message) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
    }
}

function validateUser(userData) {
    const errors = [];
    
    if (!userData.email || !userData.email.includes('@')) {
        errors.push(new ValidationError('email', 'Valid email is required'));
    }
    
    if (!userData.name || userData.name.trim().length < 2) {
        errors.push(new ValidationError('name', 'Name must be at least 2 characters'));
    }
    
    if (errors.length > 0) {
        throw new ValidationError('validation', 'Multiple validation errors occurred');
    }
}

async function saveUser(userData) {
    try {
        validateUser(userData);
        
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new ApiError(response.status, `Failed to save user: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        if (error instanceof ValidationError) {
            console.warn('Validation failed:', error.message);
            throw error;  // Re-throw validation errors
        } else if (error instanceof ApiError) {
            console.error('API error:', error.message);
            throw error;  // Re-throw API errors
        } else {
            console.error('Unexpected error:', error);
            throw new Error('An unexpected error occurred');
        }
    }
}

// Bad: Poor error handling
function saveUser(userData) {
    try {
        // No validation
        fetch('/api/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        }).then(response => {
            return response.json();  // No error checking
        }).catch(error => {
            console.log('Error');  // Generic error handling
        });
    } catch (e) {
        // Catching everything without specificity
    }
}
```

### DOM Manipulation and Event Handling

#### Modern DOM Interaction
```javascript
// Good: Modern DOM manipulation with proper event handling
class TodoApp {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.todos = [];
        this.init();
    }
    
    init() {
        this.render();
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        // Event delegation for better performance
        this.container.addEventListener('click', (event) => {
            if (event.target.matches('.todo-toggle')) {
                const todoId = parseInt(event.target.dataset.id);
                this.toggleTodo(todoId);
            } else if (event.target.matches('.todo-delete')) {
                const todoId = parseInt(event.target.dataset.id);
                this.deleteTodo(todoId);
            }
        });
        
        // Form submission
        const form = this.container.querySelector('.todo-form');
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const input = form.querySelector('.todo-input');
            this.addTodo(input.value.trim());
            input.value = '';
        });
    }
    
    addTodo(text) {
        if (!text) return;
        
        const todo = {
            id: Date.now(),
            text,
            completed: false
        };
        
        this.todos.push(todo);
        this.render();
    }
    
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.render();
        }
    }
    
    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.render();
    }
    
    render() {
        const todosHtml = this.todos.map(todo => `
            <li class="todo-item ${todo.completed ? 'completed' : ''}">
                <button class="todo-toggle" data-id="${todo.id}">
                    ${todo.completed ? '✓' : '○'}
                </button>
                <span class="todo-text">${this.escapeHtml(todo.text)}</span>
                <button class="todo-delete" data-id="${todo.id}">Delete</button>
            </li>
        `).join('');
        
        this.container.innerHTML = `
            <form class="todo-form">
                <input type="text" class="todo-input" placeholder="Add a todo..." required>
                <button type="submit">Add</button>
            </form>
            <ul class="todo-list">${todosHtml}</ul>
        `;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp('todo-app');
});

// Bad: Direct DOM manipulation with poor event handling
var todos = [];

function addTodo() {
    var input = document.getElementById('todo-input');
    var text = input.value;
    
    if (text) {
        todos.push({
            id: Math.random(),  // Poor ID generation
            text: text,
            completed: false
        });
        
        input.value = '';
        renderTodos();
    }
}

function renderTodos() {
    var list = document.getElementById('todo-list');
    list.innerHTML = '';  // Inefficient re-rendering
    
    for (var i = 0; i < todos.length; i++) {
        var todo = todos[i];
        var li = document.createElement('li');
        li.innerHTML = todo.text;  // XSS vulnerability
        
        // Individual event listeners (inefficient)
        li.addEventListener('click', function() {
            toggleTodo(todo.id);  // Closure issues
        });
        
        list.appendChild(li);
    }
}
```

### Module Organization

#### ES6 Modules and Code Organization
```javascript
// Good: Modular code organization

// utils.js - Utility functions
export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

export const formatCurrency = (amount, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency
    }).format(amount);
};

export const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

// api.js - API interactions
export class ApiClient {
    constructor(baseUrl, options = {}) {
        this.baseUrl = baseUrl;
        this.defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...this.defaultOptions,
            ...options,
            headers: {
                ...this.defaultOptions.headers,
                ...options.headers
            }
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// components/UserCard.js - Component
import { formatCurrency } from '../utils.js';

export class UserCard {
    constructor(user, container) {
        this.user = user;
        this.container = container;
        this.render();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="user-card">
                <img src="${this.user.avatar}" alt="${this.user.name}" class="user-avatar">
                <div class="user-info">
                    <h3 class="user-name">${this.escapeHtml(this.user.name)}</h3>
                    <p class="user-email">${this.escapeHtml(this.user.email)}</p>
                    <p class="user-balance">Balance: ${formatCurrency(this.user.balance)}</p>
                </div>
            </div>
        `;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    updateUser(newUserData) {
        this.user = { ...this.user, ...newUserData };
        this.render();
    }
}

// main.js - Application entry point
import { ApiClient } from './api.js';
import { UserCard } from './components/UserCard.js';
import { debounce } from './utils.js';

const api = new ApiClient('https://api.example.com');

async function loadUsers() {
    try {
        const users = await api.get('/users');
        const container = document.getElementById('users-container');
        
        users.forEach(user => {
            const userContainer = document.createElement('div');
            container.appendChild(userContainer);
            new UserCard(user, userContainer);
        });
    } catch (error) {
        console.error('Failed to load users:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadUsers);

// Bad: Everything in one file with global variables
var users = [];
var API_URL = 'https://api.example.com';

function formatMoney(amount) {
    return '$' + amount.toFixed(2);  // Poor formatting
}

function loadUsers() {
    fetch(API_URL + '/users')
        .then(response => response.json())
        .then(data => {
            users = data;
            showUsers();
        })
        .catch(error => {
            console.log('Error loading users');
        });
}

function showUsers() {
    var container = document.getElementById('users');
    container.innerHTML = '';
    
    for (var i = 0; i < users.length; i++) {
        var user = users[i];
        var div = document.createElement('div');
        div.innerHTML = '<h3>' + user.name + '</h3><p>' + user.email + '</p>';
        container.appendChild(div);
    }
}
```

## Integration & Architecture

### Component-Based Architecture

#### Reusable Component Pattern
```javascript
// Good: Reusable component with proper lifecycle management
class BaseComponent {
    constructor(element, options = {}) {
        this.element = element;
        this.options = { ...this.defaultOptions, ...options };
        this.state = {};
        this.isDestroyed = false;
        
        this.init();
    }
    
    get defaultOptions() {
        return {};
    }
    
    init() {
        this.bindEvents();
        this.render();
    }
    
    bindEvents() {
        // Override in subclasses
    }
    
    render() {
        // Override in subclasses
    }
    
    setState(newState) {
        if (this.isDestroyed) return;
        
        this.state = { ...this.state, ...newState };
        this.render();
    }
    
    destroy() {
        this.isDestroyed = true;
        this.element.removeEventListener?.();
        this.element = null;
    }
}

class Modal extends BaseComponent {
    get defaultOptions() {
        return {
            closeOnEscape: true,
            closeOnBackdrop: true,
            showCloseButton: true
        };
    }
    
    bindEvents() {
        if (this.options.closeOnEscape) {
            this.handleEscape = (event) => {
                if (event.key === 'Escape') {
                    this.close();
                }
            };
            document.addEventListener('keydown', this.handleEscape);
        }
        
        if (this.options.closeOnBackdrop) {
            this.element.addEventListener('click', (event) => {
                if (event.target === this.element) {
                    this.close();
                }
            });
        }
        
        if (this.options.showCloseButton) {
            const closeButton = this.element.querySelector('.modal__close');
            closeButton?.addEventListener('click', () => this.close());
        }
    }
    
    render() {
        this.element.innerHTML = `
            <div class="modal__backdrop">
                <div class="modal__content">
                    ${this.options.showCloseButton ? '<button class="modal__close">&times;</button>' : ''}
                    <div class="modal__body">
                        ${this.options.content || ''}
                    </div>
                </div>
            </div>
        `;
    }
    
    open() {
        this.setState({ isOpen: true });
        this.element.classList.add('modal--open');
        document.body.classList.add('modal-open');
    }
    
    close() {
        this.setState({ isOpen: false });
        this.element.classList.remove('modal--open');
        document.body.classList.remove('modal-open');
        
        // Emit custom event
        this.element.dispatchEvent(new CustomEvent('modal:closed'));
    }
    
    destroy() {
        if (this.handleEscape) {
            document.removeEventListener('keydown', this.handleEscape);
        }
        document.body.classList.remove('modal-open');
        super.destroy();
    }
}

// Usage
const modal = new Modal(document.getElementById('my-modal'), {
    content: '<h2>Hello World</h2><p>This is modal content.</p>',
    closeOnEscape: true
});

modal.element.addEventListener('modal:closed', () => {
    console.log('Modal was closed');
});

// Bad: Tightly coupled, non-reusable code
function showModal(content) {
    var modal = document.getElementById('modal');
    modal.innerHTML = content;
    modal.style.display = 'block';
    
    // Event listeners added every time
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideModal();
        }
    });
}

function hideModal() {
    var modal = document.getElementById('modal');
    modal.style.display = 'none';
    // No cleanup of event listeners
}
```

### State Management

#### Simple State Management Pattern
```javascript
// Good: Centralized state management
class StateManager {
    constructor(initialState = {}) {
        this.state = { ...initialState };
        this.listeners = new Map();
        this.history = [this.state];
    }
    
    getState() {
        return { ...this.state };
    }
    
    setState(updates) {
        const prevState = { ...this.state };
        this.state = { ...this.state, ...updates };
        this.history.push({ ...this.state });
        
        // Notify listeners
        this.listeners.forEach((callback, key) => {
            callback(this.state, prevState);
        });
    }
    
    subscribe(key, callback) {
        this.listeners.set(key, callback);
        
        // Return unsubscribe function
        return () => {
            this.listeners.delete(key);
        };
    }
    
    undo() {
        if (this.history.length > 1) {
            this.history.pop(); // Remove current state
            this.state = { ...this.history[this.history.length - 1] };
            
            this.listeners.forEach((callback) => {
                callback(this.state);
            });
        }
    }
}

// Application state
const appState = new StateManager({
    user: null,
    todos: [],
    filter: 'all'
});

// Component that reacts to state changes
class TodoList {
    constructor(container) {
        this.container = container;
        this.unsubscribe = appState.subscribe('todoList', (state) => {
            this.render(state.todos, state.filter);
        });
    }
    
    render(todos, filter) {
        const filteredTodos = this.filterTodos(todos, filter);
        
        this.container.innerHTML = filteredTodos.map(todo => `
            <li class="todo ${todo.completed ? 'completed' : ''}">
                ${todo.text}
            </li>
        `).join('');
    }
    
    filterTodos(todos, filter) {
        switch (filter) {
            case 'active':
                return todos.filter(todo => !todo.completed);
            case 'completed':
                return todos.filter(todo => todo.completed);
            default:
                return todos;
        }
    }
    
    destroy() {
        this.unsubscribe();
    }
}

// Actions
const todoActions = {
    addTodo(text) {
        const state = appState.getState();
        const newTodo = {
            id: Date.now(),
            text,
            completed: false
        };
        
        appState.setState({
            todos: [...state.todos, newTodo]
        });
    },
    
    toggleTodo(id) {
        const state = appState.getState();
        const updatedTodos = state.todos.map(todo =>
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        );
        
        appState.setState({ todos: updatedTodos });
    },
    
    setFilter(filter) {
        appState.setState({ filter });
    }
};

// Bad: Global variables and direct DOM manipulation
var todos = [];
var currentFilter = 'all';

function addTodo(text) {
    todos.push({
        id: Math.random(),
        text: text,
        completed: false
    });
    
    renderTodos();  // Manual re-rendering
    updateCounter();  // Manual updates everywhere
}

function renderTodos() {
    var container = document.getElementById('todos');
    // Direct DOM manipulation without proper state management
}
```

## Performance Optimization

### Loading and Bundling

#### Optimized Asset Loading
```html
<!-- Good: Optimized resource loading -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Preload critical resources -->
    <link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/css/critical.css" as="style">
    
    <!-- Critical CSS inlined -->
    <style>
        /* Critical above-the-fold styles here */
        body { font-family: 'Inter', sans-serif; margin: 0; }
        .header { background: #fff; padding: 1rem; }
    </style>
    
    <!-- Non-critical CSS loaded asynchronously -->
    <link rel="stylesheet" href="/css/main.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="/css/main.css"></noscript>
    
    <title>Optimized Page</title>
</head>
<body>
    <header class="header">
        <h1>My Website</h1>
    </header>
    
    <main>
        <!-- Lazy load images -->
        <img src="placeholder.jpg" 
             data-src="actual-image.jpg" 
             alt="Description"
             loading="lazy"
             class="lazy-image">
    </main>
    
    <!-- Critical JavaScript inline -->
    <script>
        // Critical functionality here
        document.documentElement.classList.add('js-enabled');
    </script>
    
    <!-- Non-critical JavaScript deferred -->
    <script src="/js/main.js" defer></script>
</body>
</html>

<!-- Bad: Blocking resources and poor loading strategy -->
<!DOCTYPE html>
<html>
<head>
    <!-- Blocking CSS -->
    <link rel="stylesheet" href="/css/all-styles.css">
    
    <!-- Blocking JavaScript in head -->
    <script src="/js/jquery.js"></script>
    <script src="/js/plugins.js"></script>
    <script src="/js/main.js"></script>
    
    <title>Slow Page</title>
</head>
<body>
    <!-- All images load immediately -->
    <img src="large-image-1.jpg" alt="Image 1">
    <img src="large-image-2.jpg" alt="Image 2">
    <img src="large-image-3.jpg" alt="Image 3">
</body>
</html>
```

#### JavaScript Performance Optimization
```javascript
// Good: Performance-optimized JavaScript
class PerformantComponent {
    constructor(container) {
        this.container = container;
        this.cache = new Map();
        this.rafId = null;
        
        // Throttled scroll handler
        this.handleScroll = this.throttle(this.onScroll.bind(this), 16);
        
        this.init();
    }
    
    init() {
        // Use passive event listeners for better performance
        window.addEventListener('scroll', this.handleScroll, { passive: true });
        
        // Intersection Observer for lazy loading
        this.setupIntersectionObserver();
        
        // Request Animation Frame for smooth animations
        this.startAnimationLoop();
    }
    
    setupIntersectionObserver() {
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadContent(entry.target);
                    this.observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        // Observe all lazy elements
        this.container.querySelectorAll('[data-lazy]').forEach(el => {
            this.observer.observe(el);
        });
    }
    
    loadContent(element) {
        const src = element.dataset.src;
        if (src && !this.cache.has(src)) {
            const img = new Image();
            img.onload = () => {
                element.src = src;
                element.classList.add('loaded');
                this.cache.set(src, true);
            };
            img.src = src;
        }
    }
    
    // Efficient throttling
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // Debounced resize handler
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    onScroll() {
        // Efficient scroll handling
        const scrollY = window.pageYOffset;
        
        // Use CSS transforms for better performance
        this.container.style.transform = `translateY(${scrollY * 0.5}px)`;
    }
    
    startAnimationLoop() {
        const animate = () => {
            if (!this.isDestroyed) {
                this.updateAnimations();
                this.rafId = requestAnimationFrame(animate);
            }
        };
        this.rafId = requestAnimationFrame(animate);
    }
    
    updateAnimations() {
        // Batch DOM reads and writes
        const elements = this.container.querySelectorAll('.animated');
        
        // Read phase
        const positions = Array.from(elements).map(el => ({
            element: el,
            rect: el.getBoundingClientRect()
        }));
        
        // Write phase
        positions.forEach(({ element, rect }) => {
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                element.classList.add('in-view');
            }
        });
    }
    
    destroy() {
        this.isDestroyed = true;
        window.removeEventListener('scroll', this.handleScroll);
        
        if (this.observer) {
            this.observer.disconnect();
        }
        
        if (this.rafId) {
            cancelAnimationFrame(this.rafId);
        }
        
        this.cache.clear();
    }
}

// Bad: Performance-heavy code
class SlowComponent {
    constructor(container) {
        this.container = container;
        
        // No throttling on scroll
        window.addEventListener('scroll', () => {
            this.onScroll();  // Called every scroll event
        });
        
        // Polling instead of Intersection Observer
        setInterval(() => {
            this.checkVisibility();  // Runs every 100ms regardless
        }, 100);
    }
    
    onScroll() {
        // Expensive operations on every scroll
        this.container.querySelectorAll('.item').forEach(item => {
            const rect = item.getBoundingClientRect();  // Forces layout
            item.style.opacity = rect.top < window.innerHeight ? '1' : '0';  // Forces repaint
        });
    }
    
    checkVisibility() {
        // Unnecessary DOM queries
        const items = document.querySelectorAll('.lazy-item');
        items.forEach(item => {
            const rect = item.getBoundingClientRect();  // Expensive on every poll
            if (rect.top < window.innerHeight) {
                this.loadItem(item);
            }
        });
    }
}
```

## Accessibility Guidelines

### Semantic HTML and ARIA

#### Accessible Components
```html
<!-- Good: Accessible component with proper ARIA attributes -->
<div class="dropdown" role="combobox" aria-expanded="false" aria-haspopup="listbox">
    <button type="button" 
            class="dropdown__trigger" 
            aria-labelledby="dropdown-label"
            aria-describedby="dropdown-help">
        Select an option
        <span class="dropdown__arrow" aria-hidden="true">▼</span>
    </button>
    
    <ul class="dropdown__menu" 
        role="listbox" 
        aria-labelledby="dropdown-label"
        hidden>
        <li role="option" aria-selected="false">
            <button type="button">Option 1</button>
        </li>
        <li role="option" aria-selected="false">
            <button type="button">Option 2</button>
        </li>
        <li role="option" aria-selected="true">
            <button type="button">Option 3</button>
        </li>
    </ul>
</div>

<label id="dropdown-label" for="dropdown">Choose your preference</label>
<div id="dropdown-help" class="help-text">Use arrow keys to navigate options</div>

<!-- Good: Accessible form with error handling -->
<form novalidate>
    <div class="form-group">
        <label for="email" class="required">
            Email Address
            <span class="required-indicator" aria-hidden="true">*</span>
        </label>
        <input type="email" 
               id="email" 
               name="email" 
               required 
               aria-describedby="email-help email-error"
               aria-invalid="false">
        <div id="email-help" class="help-text">
            We'll use this to send you important updates
        </div>
        <div id="email-error" class="error-message" aria-live="polite" hidden>
            Please enter a valid email address
        </div>
    </div>
    
    <button type="submit" aria-describedby="submit-help">
        Create Account
    </button>
    <div id="submit-help" class="help-text">
        By creating an account, you agree to our terms of service
    </div>
</form>

<!-- Bad: Inaccessible components -->
<div class="dropdown">
    <div onclick="toggleDropdown()">Select option ▼</div>  <!-- Not focusable -->
    <div class="menu" style="display: none;">  <!-- No ARIA attributes -->
        <div onclick="selectOption(1)">Option 1</div>  <!-- Not semantic -->
        <div onclick="selectOption(2)">Option 2</div>
    </div>
</div>

<form>
    <input type="text" placeholder="Email">  <!-- No label -->
    <div class="error">Invalid email</div>  <!-- No connection to input -->
    <div onclick="submit()">Submit</div>  <!-- Not a button -->
</form>
```

#### Keyboard Navigation
```javascript
// Good: Proper keyboard navigation support
class AccessibleMenu {
    constructor(menuElement) {
        this.menu = menuElement;
        this.menuItems = Array.from(this.menu.querySelectorAll('[role="menuitem"]'));
        this.currentIndex = 0;
        
        this.init();
    }
    
    init() {
        this.menu.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Set initial focus
        this.menuItems.forEach((item, index) => {
            item.setAttribute('tabindex', index === 0 ? '0' : '-1');
        });
    }
    
    handleKeyDown(event) {
        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                this.moveToNext();
                break;
                
            case 'ArrowUp':
                event.preventDefault();
                this.moveToPrevious();
                break;
                
            case 'Home':
                event.preventDefault();
                this.moveToFirst();
                break;
                
            case 'End':
                event.preventDefault();
                this.moveToLast();
                break;
                
            case 'Enter':
            case ' ':
                event.preventDefault();
                this.activateCurrentItem();
                break;
                
            case 'Escape':
                event.preventDefault();
                this.closeMenu();
                break;
        }
    }
    
    moveToNext() {
        this.currentIndex = (this.currentIndex + 1) % this.menuItems.length;
        this.updateFocus();
    }
    
    moveToPrevious() {
        this.currentIndex = this.currentIndex === 0 
            ? this.menuItems.length - 1 
            : this.currentIndex - 1;
        this.updateFocus();
    }
    
    moveToFirst() {
        this.currentIndex = 0;
        this.updateFocus();
    }
    
    moveToLast() {
        this.currentIndex = this.menuItems.length - 1;
        this.updateFocus();
    }
    
    updateFocus() {
        // Remove focus from all items
        this.menuItems.forEach(item => {
            item.setAttribute('tabindex', '-1');
        });
        
        // Focus current item
        const currentItem = this.menuItems[this.currentIndex];
        currentItem.setAttribute('tabindex', '0');
        currentItem.focus();
    }
    
    activateCurrentItem() {
        const currentItem = this.menuItems[this.currentIndex];
        currentItem.click();
    }
    
    closeMenu() {
        this.menu.setAttribute('aria-expanded', 'false');
        this.menu.hidden = true;
        
        // Return focus to trigger
        const trigger = document.querySelector('[aria-controls="' + this.menu.id + '"]');
        if (trigger) {
            trigger.focus();
        }
    }
}

// Focus management for modals
class AccessibleModal {
    constructor(modalElement) {
        this.modal = modalElement;
        this.focusableElements = this.getFocusableElements();
        this.previousActiveElement = null;
    }
    
    open() {
        this.previousActiveElement = document.activeElement;
        
        this.modal.hidden = false;
        this.modal.setAttribute('aria-modal', 'true');
        
        // Focus first focusable element
        if (this.focusableElements.length > 0) {
            this.focusableElements[0].focus();
        }
        
        // Trap focus within modal
        this.modal.addEventListener('keydown', this.handleKeyDown.bind(this));
    }
    
    close() {
        this.modal.hidden = true;
        this.modal.setAttribute('aria-modal', 'false');
        
        // Return focus to previous element
        if (this.previousActiveElement) {
            this.previousActiveElement.focus();
        }
        
        this.modal.removeEventListener('keydown', this.handleKeyDown);
    }
    
    handleKeyDown(event) {
        if (event.key === 'Tab') {
            this.trapFocus(event);
        } else if (event.key === 'Escape') {
            event.preventDefault();
            this.close();
        }
    }
    
    trapFocus(event) {
        const firstFocusable = this.focusableElements[0];
        const lastFocusable = this.focusableElements[this.focusableElements.length - 1];
        
        if (event.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstFocusable) {
                event.preventDefault();
                lastFocusable.focus();
            }
        } else {
            // Tab
            if (document.activeElement === lastFocusable) {
                event.preventDefault();
                firstFocusable.focus();
            }
        }
    }
    
    getFocusableElements() {
        const focusableSelectors = [
            'button:not([disabled])',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            'a[href]',
            '[tabindex]:not([tabindex="-1"])'
        ];
        
        return Array.from(this.modal.querySelectorAll(focusableSelectors.join(', ')));
    }
}

// Bad: No keyboard support or focus management
class InaccessibleMenu {
    constructor(menuElement) {
        this.menu = menuElement;
        
        // Only mouse support
        this.menu.addEventListener('click', (event) => {
            if (event.target.matches('.menu-item')) {
                this.selectItem(event.target);
            }
        });
    }
    
    // No keyboard navigation
    // No focus management
    // No ARIA attributes
}
```

## Quick Reference Checklist

### HTML Best Practices ✅
- [ ] Use semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`)
- [ ] Proper heading hierarchy (h1 → h2 → h3, no skipping levels)
- [ ] All images have meaningful `alt` attributes
- [ ] Forms have proper labels associated with inputs
- [ ] Use `lang` attribute on `<html>` element
- [ ] Include viewport meta tag for responsive design
- [ ] Use meaningful page titles and meta descriptions

### CSS Best Practices ✅
- [ ] Use consistent naming convention (BEM recommended)
- [ ] Mobile-first responsive design approach
- [ ] Use CSS custom properties for theming
- [ ] Efficient selectors (avoid deep nesting)
- [ ] Use modern layout techniques (Flexbox/Grid)
- [ ] Optimize for performance (critical CSS, lazy loading)
- [ ] Support dark mode with `prefers-color-scheme`

### JavaScript Best Practices ✅
- [ ] Use `const`/`let` instead of `var`
- [ ] Use arrow functions appropriately
- [ ] Handle errors properly with try/catch
- [ ] Use async/await for asynchronous operations
- [ ] Implement proper event delegation
- [ ] Use ES6+ features (destructuring, spread, template literals)
- [ ] Modular code organization with ES6 modules

### Performance Optimization ✅
- [ ] Minimize HTTP requests
- [ ] Optimize images (use appropriate formats, lazy loading)
- [ ] Minify and compress CSS/JavaScript
- [ ] Use CDN for static assets
- [ ] Implement browser caching
- [ ] Critical CSS inlined, non-critical CSS loaded async
- [ ] Use Web Workers for heavy computations

### Accessibility Guidelines ✅
- [ ] Proper color contrast ratios (WCAG 2.1 AA)
- [ ] Keyboard navigation support for all interactive elements
- [ ] Screen reader support with ARIA attributes
- [ ] Focus management for dynamic content
- [ ] Alternative text for images and media
- [ ] Form validation with clear error messages
- [ ] Support for reduced motion preferences

### Security Considerations ✅
- [ ] Validate and sanitize all user inputs
- [ ] Use HTTPS for all connections
- [ ] Implement Content Security Policy (CSP)
- [ ] Avoid inline scripts and styles
- [ ] Properly encode output to prevent XSS
- [ ] Use secure authentication methods
- [ ] Regular security audits and updates

This guide provides a comprehensive foundation for building modern, accessible, and performant web applications using HTML, CSS, and JavaScript following current industry best practices.