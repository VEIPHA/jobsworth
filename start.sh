#!/bin/bash

echo "[start.sh] Running Python scraper..."
python3 -m src.scraper

echo "[start.sh] Enriching descriptions..."
python3 -m src.grabbers.description_grabber
