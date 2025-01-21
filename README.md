# URLShortener

Project Proposal: URL Shortener
Team Members: Tim Gross, Josh Moskoff, Lucah Maniscalco

Overview
The Self-Hosted URL Shortener is an open-source, privacy-focused tool for creating and managing shortened URLs. It allows users to track essential click analytics, such as time, location, and referrer. The project is designed to be centrally hosted, providing users with ease of access.
This project will leverage React for the frontend, Python for backend, and Firebase for the database. The focus will be on building an intuitive user interface, efficient URL shortening, and a useful analytics dashboard.

Core Features
1. URL Shortening
Generate unique shortened URLs for long links.
Option for custom aliases (e.g., example.com/custom-alias).
Collision-free hash generation for automatically generated URLs.
2. Link Analytics Dashboard
Track key metrics for each shortened URL:
Total clicks.
Click timestamps.
Referrer (platform or website that initiated the click).
Geographic location (optional, based on IP).
Visual representation of analytics (e.g., bar charts, tables).
3. Link Management
Add password protection to links for restricted access.
Set expiration dates to automatically deactivate links after a certain period.
Dashboard for managing, editing, and deleting shortened links.
4. Privacy Focus
Avoid invasive tracking or reliance on cookies.
Anonymize location data and avoid unnecessary user data collection.

Notable Features
Self-Hosting: Centrally hosted website for access
Customizable Settings: Allow users to enable or disable features like analytics tracking.
Responsive UI: Mobile- and desktop-friendly design for managing URLs on any device.
Scalability: A lightweight architecture that can scale for larger datasets with minimal changes.

Milestones
Phase 1 – Concept & Design (2 Weeks)
Finalize requirements and core features.
Design user interface and define backend API endpoints.
Create mockups for the dashboard and analytics views.
Phase 2 – Backend Development (3 Weeks)
Set up Firebase backend for URL storage.
Implement URL shortening logic with collision-free hashing.
Develop analytics tracking for clicks (timestamp, referrer, location).
Phase 3 – Frontend Development (3 Weeks)
Set up React.js with a focus on building an intuitive user interface.
Create forms for URL shortening and link management.
Integrate analytics visualization using libraries like D3.
Phase 4 – Testing and Debugging (2 Weeks)
Perform unit and integration testing for both frontend and backend.
Test for edge cases, including hash collisions, expired links, and invalid inputs.
Phase 5 – Deployment and Documentation (1 Week)
Write comprehensive user and developer documentation.
Publish the website

Presumptive Tech Stack
Frontend
React.js: For building a dynamic and responsive UI.
D3: For rendering analytics graphs and charts.
Backend
FastAPI: For API development and server-side logic.
Hashlib: For generating unique URL hashes.
Firebase: A lightweight database for storing URLs and analytics.
Other Tools
Github: For version control and code storage.

Development Strategy
To maximize collaboration and learning, all team members will participate in each stage of development. Peer programming will be used extensively to ensure code quality, reduce bugs, and share knowledge across the team.

Goals
Deliver a fully functional, privacy-focused URL shortener by the end of the project.
Learn and apply best practices for full-stack web development.
Create a robust, scalable, and well-documented open-source tool that can be used by the developer community.


