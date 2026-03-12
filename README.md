# DEEP DRIFT

A first-person atmospheric drill-navigation game built in Godot with Python via py4godot.

The player operates a salvage drill in a hazardous collapsed zone, follows terminal coordinates, reaches airport-linked signal points, establishes connections, and uncovers the fate of missing evacuation flights.

## Backend Repository

https://github.com/v1to2006/project-underlink-backend

## What the game is

DEEP DRIFT is a mission-based exploration game where the player pilots a drill through a dangerous underground environment. The world is navigated through cockpit controls, a terminal console, and route-based progression tied to airport data loaded from a Flask + MariaDB backend.

The core loop is:

1. Log in with a username
2. Start or continue an expedition
3. Read the mission briefing
4. Travel to the currently active airport marker
5. Establish a terminal connection
6. Scan for the next airport
7. Avoid terrain, walls, and hazards
8. Reach the final airport and complete the expedition

## Tech Stack

### Game Client

* Godot 4.4
* Python scripting with py4godot
* 3D world with in-world cockpit interaction
* Menu flow, pause flow, intro, ending, and mission state handled in Python

### Backend

* Flask
* MariaDB
* REST API for player progress and airport data

## How the game works

### Login and save flow

The game starts from the username screen. After the player enters a username, the game sends a `/login` request to the backend.

The backend responds with the player's saved expedition state:

* player id
* username
* current route
* opened airports
* current progress index
* completion state

If the player starts a new expedition, the game calls `/start`, which resets the current expedition and generates a fresh route.

### Expedition flow

Each expedition consists of a route of airport targets.

Only one airport is active at a time.
The world contains five airport points, and the active route data is assigned to them dynamically.

The player must:

* navigate the drill to the active airport marker
* enter the airport trigger zone
* use the cockpit terminal to establish a connection
* receive airport data from the backend
* scan for the next airport

When a connection is established successfully, the game sends `/update` to the backend. The backend updates progress and unlocks the next airport.

### Terminal system

The cockpit terminal is a 3D in-world interface. It displays:

* the next airport name
* coordinates for navigation
* airport information after connection
* mission scanning messages
* route progression state

The terminal changes state depending on where the player is and what stage of the expedition they are in.

### Checkpoints

Completed airports act like checkpoints.
When the player loads back into an expedition, the drill is repositioned to the last opened airport location.

### Failure state

If the drill collides with terrain or lethal geometry, the current run is lost and the player is redirected back to the menu.

### Ending

When the final airport connection is completed, the backend marks the expedition as completed and the game transitions to a separate ending scene.

## Backend integration

The Godot client talks to the backend through HTTP requests.

### Endpoints used

* `POST /login`
* `POST /start`
* `POST /update`
* `GET /airport?icao_code=...`

### What each endpoint does

#### `POST /login`

Loads an existing player and their current expedition state.

#### `POST /start`

Starts a fresh expedition for the current player and creates a new airport route.

#### `POST /update`

Marks an airport as completed for the current player and advances expedition progress.

#### `GET /airport`

Returns detailed information for a specific airport by ICAO code.

## Project structure overview

A simplified overview of the client-side structure:

* `GameData` autoload manages player session, route data, checkpoint movement, and backend communication
* `WorldAirportsController` assigns route data to airport points in the world
* `AirportPoint` handles airport trigger logic and visibility
* `OldPcConsole` controls the in-world terminal display and interaction flow
* `DrillProxy` handles drill movement and collision/death behavior
* `PlayMenu`, `EnterYourUsername`, `PauseMenu`, `Intro`, and `Ending` manage scene flow

## Main gameplay scenes

### Main Menu

The player can:

* log in
* start a new expedition
* continue an existing one
* log out
* quit the game

### Intro

Before entering the expedition, the player receives a short lore briefing and gameplay instructions.

### Expedition

This is the main gameplay scene containing:

* the drill
* cockpit controls
* terminal console
* airport route points
* map display
* hazard/collision systems

### Ending

After the final airport is completed, the player receives the final mission result and survivor confirmation.

## Requirements

* Godot 4.4
* py4godot installed and enabled
* Python environment compatible with the py4godot setup
* Running backend server

## Running the project

1. Start the backend project first
2. Open the Godot project
3. Make sure py4godot is installed and enabled
4. Run the game from the Godot editor
5. Log in with a username
6. Start or continue an expedition

## Backend configuration

The client currently uses a backend URL in the `GameData` script.

Example:

`http://127.0.0.1:5000`

If your backend runs elsewhere, update the backend base URL in the game scripts.

## Notes

This project uses py4godot, so gameplay logic is written in Python instead of GDScript.
Because of that, exporting and distribution may require extra care depending on the py4godot setup used in the project.
