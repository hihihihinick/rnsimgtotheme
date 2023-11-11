# Renoise Theme Generator

The `generate_theme.py` script dynamically generates a Renoise theme (.xrnc file) based on the most prevalent colors found in an image. This allows users to create custom Renoise themes that match their favorite images or album art.

## Features

- Analyzes an image to determine its top colors.
- Generates a theme with color variants based on the image's palette.
- Supports different theme styles (light, dark, and base).
- Outputs a .xrnc file that can be loaded into Renoise.

## Dependencies

- Python 3
- Pillow (PIL Fork)
- NumPy
- Scikit-learn

To install the required Python packages, you can use pip:

```bash
pip install pillow numpy scikit-learn
```

## Setting Up a Virtual Environment

To avoid conflicts with other Python projects, it's a good idea to set up a virtual environment. Here's how you can set it up in the directory where you've saved the `generate_theme.py` script:

1. Navigate to the directory containing `generate_theme.py`.
2. Run the following command to create a virtual environment named `venv`:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```

4. Once the virtual environment is activated, install the dependencies:

    ```bash
    pip install pillow numpy scikit-learn
    ```
## Usage Instructions

To generate a Renoise theme using the `generate_theme.py` script, follow these steps:

1. **Prepare Your Image**:
   - Choose an image that you want to base your Renoise theme on.
   - For faster processing, consider resizing large images. The color analysis doesn't require high resolution.

2. **Run the Script**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing the `generate_theme.py` script.
   - Run the script with the path to your image as an argument. For example:
     ```bash
     python generate_theme.py path/to/your_image.jpg
     ```

3. **Apply the Theme in Renoise**:
   - Once the script has finished running, it will output a `.xrnc` file in the same directory.
   - Open Renoise.
   - Go to `Edit` > `Preferences` in the menu bar.
   - In the Preferences window, navigate to the `Theme` tab.
   - Click on `Load Theme...` and select the generated `.xrnc` file.
   - Your new theme based on your image's color palette will now be applied to Renoise.

### Tips for Best Results:
- Images with distinct and contrasting colors will produce more vibrant themes.
- Themes generated from images with muted or similar colors may not provide enough contrast for comfortable use.

### Troubleshooting:
- If the theme doesn't load correctly, ensure that the `.xrnc` file is not corrupted and that it was generated without errors.
- If you encounter an error during the theme generation process, check that you have all the required dependencies installed in your virtual environment.

For any issues or questions, please [open an issue](link-to-your-github-repo-issues) on the GitHub repository.



3. The script will generate a `.xrnc` file in the same directory. You can load this file into Renoise by going to `Preferences` > `Theme` > `Load Theme`.

## Notes

- For best results, use images with a clear color palette.
- Large images may take longer to process. You can resize your image for quicker results without significantly affecting the theme colors generated.

## License

Feel free to fill in any additional details, specify the license, and provide any other necessary information.
