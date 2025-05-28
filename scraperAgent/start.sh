#!/bin/bash

echo "[start.sh] Scraping all job listings..."
python3 -m scraperAgent.src.scraper

echo "[start.sh] Grabbing descriptions from URLs..."
python3 -m scraperAgent.src.description_grabber
