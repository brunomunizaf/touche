# Touché - Box Design Tool

A Streamlit application for generating cutting and folding lines for various box types with internal and external linings.

## Features

- **Box Types**: Loose Top, Book Top, Magnet Top, Sleeve Top, Half Spine, Circular
- **Slot Types**: None, Square, Circular, Cylindrical
- **Materials**: Cardboard, Internal Lining, External Lining
- **Export**: SVG format for cutting and folding lines
- **Multi-instance**: Optimize layouts for multiple boxes

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Troubleshooting

### Python Environment Mismatch Error

If you encounter the error:
```
TypeError: ImageMixin.image() got an unexpected keyword argument 'use_container_width'
```

This is typically caused by a **Python environment mismatch** where your Python and pip are pointing to different environments.

#### Symptoms:
- `which python` and `which pip` show different paths
- You have conda installed but pip is using system Python
- Streamlit version mismatch between environments

#### Solutions:

**Option 1: Use conda (Recommended for conda users)**
```bash
conda install streamlit svgwrite
```

**Option 2: Use the correct pip path**
```bash
# Find your conda pip path
which python
# Use the corresponding pip (replace with your actual path)
/Users/yourusername/anaconda3/bin/pip install -r requirements.txt
```

**Option 3: Activate conda environment properly**
```bash
conda activate base
pip install -r requirements.txt
```

#### Prevention:
- Always check `which python` and `which pip` before installing packages
- Use `conda install` in conda environments instead of `pip install`
- Ensure both Python and pip are from the same environment

## Project Structure

```
touche/
├── app.py                 # Main Streamlit application
├── models.py             # Box model definitions
├── requirements.txt      # Python dependencies
├── images/              # Box type preview images
└── export/              # SVG export components
    ├── components/       # Box component definitions
    ├── layout.py         # Layout management
    └── svg_exporter.py  # SVG generation
```

## Dependencies

- streamlit >= 1.28.0
- svgwrite

## License

[Add your license information here]
