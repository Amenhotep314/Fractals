# Fractals
This project was born from my curiosity about fractals in the complex plane after encountering them briefly in a geometry class. It is capable of generating arbitrarily high-definition descriptions of these fractals as XML data, and then rendering that data to PNG images per coloring choices of the user. Aside from their mathematical appeal, these images tend to contain very visually appealing structures.

## Capabilities
Currently, the software can generate the following fractals:
- Julia sets
- Mandelbrot sets
- Multibrot sets, forms of Mandelbrot sets that are general in degree
- Burning ship sets
- Tricorns

## Use
This software is written in Python 3 and has minimal dependency requirements: only the Python Image Library.
However, computational resources should be considered for more ambitions uses. Set generation is CPU-intensive and time-consuming, and image rendering places high demands on memory. Even with optimizations for large renders, adjustments may be needed for machines with 8GB RAM or less.
