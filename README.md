# Website Screenshot Taker

Automated Python CLI tool for capturing full-height screenshots of complex web pages with animations, progressive loading, and dynamic content.

## Features

- Full-page screenshots with automatic height detection
- Handles scroll animations by freezing page elements
- Removes scroll event listeners to prevent interference
- High-DPI support with configurable scale factors
- Batch processing from URL list
- Cookie banner removal
- Timeout management for slow pages

## How It Works

### Core Components

- **`main.py`** - Entry point that processes URLs from `links.txt`, handles errors, and saves screenshots to `images/` directory.

- **`screenshot.py`** - Main Screenshot class using headless Chrome with optimized settings for capture.

- **`freeze_units.js`** - JavaScript that locks all DOM elements to current dimensions and hides cookie banners.

- **`remove_scroll_listeners.js`** - Removes scroll and wheel event listeners to prevent animations during capture.

### Process Flow

1. Load URL and wait for complete document readiness
2. Set browser window to specified dimensions  
3. Wait for animations to settle
4. Hide scrollbars via CSS injection
5. Scroll to bottom to trigger lazy-loading
6. Remove scroll event listeners
7. Freeze all elements to current dimensions
8. Adjust window height to full page height
9. Capture screenshot

## Usage

1. Add URLs to `links.txt` (one per line)
2. Run: `python main.py`
3. Screenshots saved to `images/` directory
4. Check `errors.txt` for failed URLs

## Configuration

Default settings in Screenshot class:
- Size: 1920x1200px
- Scale factor: 2x (high-DPI)
- Timeout: 60 seconds
- Page freezing: enabled

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome browser
- chromedriver-autoinstaller

Install dependencies:
```bash
pip install selenium chromedriver-autoinstaller
```

## File Structure

- `main.py` - Main execution script
- `screenshot.py` - Screenshot capture class
- `freeze_units.js` - DOM element freezing
- `remove_scroll_listeners.js` - Event listener removal
- `links.txt` - Input URLs
- `errors.txt` - Failed URL log
- `images/` - Output directory

Designed for modern websites with complex animations and dynamic content that traditional screenshot tools can't handle effectively.
