from rgbmatrix import RGBMatrix, RGBMatrixOptions

def setupPanelOptions():
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.parallel = 1
    options.gpio_slowdown = 4
    options.drop_privileges=False
    return options
