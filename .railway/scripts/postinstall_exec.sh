#!/bin/bash
echo "Installing Playwright browsers..."
playwright install --with-deps
python3 -m src.scraper
