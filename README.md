# Game Hub & Mini-games

This repository hosts a Flask‑based game hub and a collection of Pygame mini‑games: Chess, Rotating Box, and Pong.

## Requirements

- Python 3.8+
- Pygame 2.1.2

## Installation

Install dependencies:

```
pip install -r requirements.txt
```

## Usage

### Run the game hub (Flask site)
```bash
pip install -r requirements.txt
python app.py
```

### Run the individual games
From the project root:
```bash
python -m chess.main       # launch the chess Pygame app
python rotating_box/rotating_box_simulation.py  # launch the rotating box Pygame app
python pong/pong.py        # launch the Pong Pygame app
```

## Features

- Move generation for all standard pieces, including pawn promotion.
- Basic AI using negamax (minimax) with alpha-beta pruning.
- Highlights selected square and shows simple board UI.

## Limitations

- Castling and en passant are not supported.
