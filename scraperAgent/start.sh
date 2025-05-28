#!/bin/bash

echo "[start.sh] Scraping all job listings...."
python3 -m src.scraper

echo "[start.sh] Grabbing descriptions from URLs...."
python3 -m src.description_grabber
