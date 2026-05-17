# Captains HUD: AI-Powered Cricket Strategy Simulator

Demo Video Link - https://youtu.be/VudXVtMESMY

## Overview
Captains HUD (formerly "Captain Cool") is an interactive, AI-driven web application that simulates high-pressure cricket match scenarios. Users can input a specific match situation (e.g., "19th over, 24 runs to win, heavy dew"), and the application uses Google's Gemini AI to generate strategic decisions, simulate a multi-agent debate, and deliver dynamic live commentary.

## Problem Statement
The goal was to build an application that could demonstrate multi-agent AI interactions in a fun, relatable context. Cricket strategy, with its diverse captaincy styles and high-pressure scenarios, provided the perfect backdrop. The application needed to:
- Emulate the distinct personalities of legendary Indian cricket captains: MS Dhoni (calm/methodical), Virat Kohli (aggressive/passionate), Rohit Sharma (tactical/flexible), and Gautam Gambhir (intense/match-up driven).
- Use a multi-agent architecture (Strategist, Devil's Advocate, Commentator, and Stats Analyst) to debate the scenario.
- Present the data in a minimalist, broadcast-style "Sports HUD" with high-end visual interactions (pressure meters, tickers, animations).
- Handle AI rate limits gracefully using mock fallbacks.

## Features
- **Multi-Agent Simulation**: The Gemini API powers distinct agents that analyze the pitch, make decisions, challenge those decisions, and provide live commentary.
- **Compare Mode**: Run a side-by-side simulation to see how different captains would handle the exact same high-pressure scenario.
- **Dynamic Visuals**: Features a pulsing pressure meter, an animated news ticker, dynamic CSS "glitch" elements, and a confetti explosion upon the final commentary verdict.
- **Resilient Fallbacks**: If the API rate limit is hit, the application automatically falls back to a high-fidelity mock simulation, ensuring zero downtime.

## Technical Architecture
- **Frontend**: Pure HTML, Vanilla CSS, and JavaScript (ESM). No heavy frameworks, ensuring a lightweight and lightning-fast HUD.
- **AI Integration**: Uses the `@google/genai` SDK to communicate with Gemini models.
- **Prompt Engineering**: The application uses a "Mega-Prompt" schema, consolidating the debate into a single structured JSON response to minimize latency and API calls.

## How to Run
1. Open `index.html` in any modern web browser (or serve locally using Python).
2. Click the settings icon to input your Google Gemini API Key.
3. Select a captain and enter a match scenario.
4. Click "EXECUTE" and watch the debate unfold!
