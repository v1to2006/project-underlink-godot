# DEEP DRIFT

A first-year project at Metropolia University of Applied Sciences.

A first-person atmospheric drill-navigation game built in Godot with Python via py4godot.

## Backend Repository

[https://github.com/v1to2006/project-underlink-backend](https://github.com/v1to2006/project-underlink-backend)

## Overview

DEEP DRIFT is a mission-based exploration game where the player pilots a drill through a hazardous underground zone. Progression is tied to airport-based route points loaded from a Flask + MariaDB backend.

Core flow:

1. Log in with a username
2. Start or continue an expedition
3. Travel to the active airport marker
4. Establish a terminal connection
5. Unlock the next airport
6. Complete the route

## Tech Stack

### Game Client

* Godot 4.4
* Python scripting with py4godot
* 3D world with cockpit interaction
* Python-driven menu flow, mission state, intro, pause, and ending

### Backend

* Flask
* MariaDB
* REST API for player progress and airport data

## How it works

### Login and save flow

The game starts from a username screen and sends a `POST /login` request to the backend.

The backend returns the player's current expedition state, including:

* player id
* username
* current route
* opened airports
* progress index
* completion state

Starting a new expedition calls `POST /start`, which resets progress and generates a new route.

### Expedition flow

Each expedition is a route of airport targets. Only one airport is active at a time, and route data is assigned dynamically to five airport points in the world.

When the player reaches the active point and connects through the cockpit terminal, the game sends `POST /update` to advance progress and unlock the next airport.

### Terminal system

The cockpit terminal is a 3D in-world interface that shows:

* active airport name
* coordinates
* airport information after connection
* scanning messages
* route progression state

### Checkpoints and failure

Completed airports work as checkpoints. On load, the drill is repositioned to the last opened airport.

If the drill collides with terrain or lethal geometry, the run ends and the player returns to the menu.

### Ending

After the final airport is completed, the backend marks the expedition as complete and the game switches to an ending scene.

## Backend integration

The Godot client communicates with the backend through HTTP requests.

### Endpoints used

* `POST /login`
* `POST /start`
* `POST /update`
* `GET /airport?icao_code=...`

## Requirements

* Godot 4.4
* py4godot installed and enabled
* Python environment compatible with py4godot
* Running backend server

## Running the project

1. Start the backend project
2. Open the Godot project
3. Make sure py4godot is installed and enabled
4. Run the game from the Godot editor
5. Log in with a username
6. Start or continue an expedition

## Backend configuration

The client uses a backend URL in the `GameData` script, for example:

`http://127.0.0.1:5000`

If the backend runs elsewhere, update the base URL in the game scripts.

## Notes

This project uses py4godot, so gameplay logic is written in Python instead of GDScript. Exporting and distribution may require extra care depending on the py4godot setup used.
