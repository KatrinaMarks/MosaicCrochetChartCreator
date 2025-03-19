# MosaicCrochetChartCreator
This is a simple app with the sole function of creating mosaic crochet charts!

## How To Get The App
You can download ChartApp.py or copy and paste the code from ChartApp.py into your own .py file.

## How To Run The App
- Type "python ChartApp.py" or "python YourFileName.py" into your command line and press enter to run the app with its default chart width, heigh, and block size.

- Type "python ChartApp.py width height block_size" to run the app with your specified parameters.
  Example: "python ChartApp.py 20 40 15" makes an app 20 blocks wide and 40  blocks high with a block size of 15.

### 📦 Dependencies

This app uses:

- **tkinter** (for the GUI) → Usually pre-installed with Python.
- **Pillow** (for saving images) → Install it if you want to export your charts as images.

To install Pillow:

```bash
pip install pillow
```

## How To Use The App
- Left-click any block to turn it blue; left-click it again to turn it back to white.
- Right-click any block to put an "X" on it; right-click again to take the "X" off.

## Rules To Make A Mosaic Crochet Chart
- Rows alternate color so that every odd row is the same color, and every even row is the same color.
- Every column of a color must begin on its own color row.
- All columns of color must have an odd number of cells.
- X's mark double crochets; place X's starting on the the 3rd block of every column and then every other block going up the column.
