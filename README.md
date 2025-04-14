# Fourier Graphics Renderer

This project visualizes 2D graphics using Fourier transforms. It animates a series of rotating vectors (arrows) that combine to draw a specified shape or pattern. The input for the shapes is derived from an SVG file, and the output showcases the beauty of Fourier-based rendering.

> **Inspired by:** [3Blue1Brown's mesmerizing video on Fourier series](https://www.youtube.com/watch?v=r6sGWTCMz2k&t=998s), which illustrates how rotating vectors can represent complex drawings through epicycles.

---

## Demo

Watch the GitHub logo being rendered using Fourier transforms:

[![GitHub Logo Render](https://img.youtube.com/vi/NyPIr30Dy0A/0.jpg)](https://www.youtube.com/shorts/NyPIr30Dy0A)

## Features

- **Fourier Transformation:** Decomposes 2D points into Fourier coefficients and uses them to animate graphics.
- **Dynamic Visualization:** Displays rotating vectors and the resulting composite figure in real-time.
- **SVG Path Input:** Supports importing 2D shapes from SVG files for Fourier decomposition.
- **Interactive Animation:** Visualizes the reconstruction of the shape step-by-step using Fourier components.
- **Customizable Settings:** Configure the number of coefficients, canvas size, and frame rate.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)
4. [Project Structure](#project-structure)
5. [Dependencies](#dependencies)
6. [Future Improvements](#future-improvements)

---

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:akashdeeep/Fourier-Graphics-Renderer.git
   cd fourier-graphics-renderer
   ```

2. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have a valid SVG file for input (example: `input.svg`).

---

## Usage

1. Place your SVG file in the project directory.

2. Run the script:

   ```bash
   python main.py
   ```

3. Watch the Fourier-based rendering animation in a `pygame` window.

4. Modify settings in `conf` for custom behavior (e.g., number of coefficients, SVG file path).

---

## Configuration

```python
size = 10 #multiply the size of rendered animation
width = 990 #width of pygame window
height = 1320 #height of pygame window
grid_size = 400 #grid size
```

---

## Project Structure

```
.
├── main.py                # Entry point for the application
├── read_svg.py            # Utility to read the svg file
├── cal_coefficients.py    # Functions for parsing and sampling SVG paths
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
└── input.svg              # Example SVG file
```

---

## Dependencies

This project requires Python 3.7+ and the following libraries:

- `pygame`: For rendering and animation.
- `numpy`: For numerical computations.
- `svgpathtools`: For parsing SVG files.

Install them using:

```bash
pip install pygame numpy svgpathtools
```

---

## Future Improvements

- **Adaptive Sampling:** Automatically adjust the sampling density based on SVG path complexity.
- **Performance Optimization:** Cache Fourier coefficients and enable multi-threaded rendering.
- **GUI Integration:** Add a user interface for loading SVG files and adjusting settings dynamically.

---

Enjoy creating beautiful graphics with Fourier transforms!
