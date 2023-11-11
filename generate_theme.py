import argparse
import os
import time
from colorsys import rgb_to_hls, hls_to_rgb
from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans
import numpy as np

def get_top_colors(image_path, num_colors=7, sample_size=5000):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        pixels = np.array(img).reshape(-1, 3)  # Flatten the image pixels

        # If the image is large, sample the pixels to speed up KMeans
        if pixels.shape[0] > sample_size:
            pixels = pixels[np.random.choice(pixels.shape[0], sample_size, replace=False), :]

        # Use k-means clustering to find the most common colors
        kmeans = KMeans(n_clusters=num_colors, n_init=10)
        kmeans.fit(pixels)
        
        # Get the RGB values of the cluster centers (rounded and converted to integers)
        top_colors = [tuple(int(value) for value in color) for color in kmeans.cluster_centers_]
        
        return top_colors


# Function to convert RGB to HLS and back, enhancing the saturation
def enhance_saturation(rgb, enhancement_factor):
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])
    s = min(max(s * enhancement_factor, 0), 1)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)
# Function to adjust the lightness of an RGB color
def adjust_color_lightness(rgb, factor):
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])
    l = max(min(l * factor, 1), 0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

# Function to ensure minimum brightness
def ensure_minimum_brightness(rgb, min_brightness=60):
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])
    l = max(l, min_brightness / 255.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

# Function to create color variants with ensured minimum brightness
def create_color_variants(top_colors, theme_style):
    if theme_style == 'light':
        base_lightness_factor = 3.2
        saturation_factor = 2.6
    elif theme_style == 'dark':
        base_lightness_factor = 0.5
        saturation_factor = 0.4
    else:
        base_lightness_factor = 1.0
        saturation_factor = 1.0

    # Ensure that top_colors has 7 elements
    if len(top_colors) < 7:
        raise ValueError("Not enough colors found in image to create variants.")

    # Use the top 7 colors for the variants
    variants = {
        'color_one': top_colors[0],
        'color_two': top_colors[1],
        'color_three': top_colors[2],
        'color_four': top_colors[3],
        'color_five': top_colors[4],
        'color_six': top_colors[5],
        'color_seven': top_colors[6],
    }
    return variants



def create_xrns_theme(color_variants):
    print(color_variants)
    # XML structure with dynamic color values based on color_variants
    xrns_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<SkinColors doc_version="12">
  <Main_Back>{','.join(map(str, color_variants['color_one']))}</Main_Back>
  <Main_Font>{','.join(map(str, color_variants['color_two']))}</Main_Font>
  <Alternate_Main_Back>{','.join(map(str, color_variants['color_three']))}</Alternate_Main_Back>
  <Alternate_Main_Font>{','.join(map(str, color_variants['color_four']))}</Alternate_Main_Font>
  <Body_Back>{','.join(map(str, color_variants['color_five']))}</Body_Back>
  <Body_Font>{','.join(map(str, color_variants['color_six']))}</Body_Font>
  <Strong_Body_Font>{','.join(map(str, color_variants['color_seven']))}</Strong_Body_Font>
  <Button_Back>{','.join(map(str, color_variants['color_three']))}</Button_Back>
  <Button_Font>{','.join(map(str, color_variants['color_four']))}</Button_Font>
  <Button_Highlight_Font>{','.join(map(str, color_variants['color_two']))}</Button_Highlight_Font>
  <Selected_Button_Back>{','.join(map(str, color_variants['color_five']))}</Selected_Button_Back>
  <Selected_Button_Font>{','.join(map(str, color_variants['color_six']))}</Selected_Button_Font>
  <Selection_Back>{','.join(map(str, color_variants['color_seven']))}</Selection_Back>
  <Selection_Font>{','.join(map(str, color_variants['color_two']))}</Selection_Font>
  <StandBy_Selection_Back>{','.join(map(str, color_variants['color_three']))}</StandBy_Selection_Back>
  <StandBy_Selection_Font>{','.join(map(str, color_variants['color_four']))}</StandBy_Selection_Font>
  <Midi_Mapping_Back>{','.join(map(str, color_variants['color_five']))}</Midi_Mapping_Back>
  <Midi_Mapping_Font>{','.join(map(str, color_variants['color_six']))}</Midi_Mapping_Font>
  <ToolTip_Back>{','.join(map(str, color_variants['color_seven']))}</ToolTip_Back>
  <ToolTip_Font>{','.join(map(str, color_variants['color_two']))}</ToolTip_Font>
  <ValueBox_Back>{','.join(map(str, color_variants['color_three']))}</ValueBox_Back>
  <ValueBox_Font>{','.join(map(str, color_variants['color_four']))}</ValueBox_Font>
  <ValueBox_Font_Icons>{','.join(map(str, color_variants['color_five']))}</ValueBox_Font_Icons>
  <Scrollbar>{','.join(map(str, color_variants['color_six']))}</Scrollbar>
  <Slider>{','.join(map(str, color_variants['color_seven']))}</Slider>
  <Folder>{','.join(map(str, color_variants['color_two']))}</Folder>
  <Pattern_Default_Back>{','.join(map(str, color_variants['color_three']))}</Pattern_Default_Back>
  <Pattern_Default_Font>{','.join(map(str, color_variants['color_four']))}</Pattern_Default_Font>
  <Pattern_Default_Font_Volume>{','.join(map(str, color_variants['color_five']))}</Pattern_Default_Font_Volume>
  <Pattern_Default_Font_Panning>{','.join(map(str, color_variants['color_six']))}</Pattern_Default_Font_Panning>
  <Pattern_Default_Font_Pitch>{','.join(map(str, color_variants['color_seven']))}</Pattern_Default_Font_Pitch>
  <Pattern_Default_Font_Delay>{','.join(map(str, color_variants['color_two']))}</Pattern_Default_Font_Delay>
  <Pattern_Default_Font_Global>{','.join(map(str, color_variants['color_three']))}</Pattern_Default_Font_Global>
  <Pattern_Default_Font_Other>{','.join(map(str, color_variants['color_four']))}</Pattern_Default_Font_Other>
  <Pattern_Default_Font_DspFx>{','.join(map(str, color_variants['color_five']))}</Pattern_Default_Font_DspFx>
  <Pattern_Default_Font_Unused>{','.join(map(str, color_variants['color_six']))}</Pattern_Default_Font_Unused>
  <Pattern_Highlighted_Back>{','.join(map(str, color_variants['color_seven']))}</Pattern_Highlighted_Back>
  <Pattern_Highlighted_Font>{','.join(map(str, color_variants['color_two']))}</Pattern_Highlighted_Font>
  <Pattern_Highlighted_Font_Volume>{','.join(map(str, color_variants['color_three']))}</Pattern_Highlighted_Font_Volume>
  <Pattern_Highlighted_Font_Panning>{','.join(map(str, color_variants['color_four']))}</Pattern_Highlighted_Font_Panning>
  <Pattern_Highlighted_Font_Pitch>{','.join(map(str, color_variants['color_five']))}</Pattern_Highlighted_Font_Pitch>
  <Pattern_Highlighted_Font_Delay>{','.join(map(str, color_variants['color_six']))}</Pattern_Highlighted_Font_Delay>
  <Pattern_Highlighted_Font_Global>{','.join(map(str, color_variants['color_seven']))}</Pattern_Highlighted_Font_Global>
  <Pattern_Highlighted_Font_Other>{','.join(map(str, color_variants['color_two']))}</Pattern_Highlighted_Font_Other>
  <Pattern_Highlighted_Font_DspFx>{','.join(map(str, color_variants['color_three']))}</Pattern_Highlighted_Font_DspFx>
  <Pattern_Highlighted_Font_Unused>{','.join(map(str, color_variants['color_four']))}</Pattern_Highlighted_Font_Unused>
  <Pattern_PlayPosition_Back>{','.join(map(str, color_variants['color_five']))}</Pattern_PlayPosition_Back>
  <Pattern_PlayPosition_Font>{','.join(map(str, color_variants['color_six']))}</Pattern_PlayPosition_Font>
  <Pattern_CenterBar_Back>{','.join(map(str, color_variants['color_seven']))}</Pattern_CenterBar_Back>
  <Pattern_CenterBar_Font>{','.join(map(str, color_variants['color_two']))}</Pattern_CenterBar_Font>
  <Pattern_CenterBar_Back_StandBy>{','.join(map(str, color_variants['color_three']))}</Pattern_CenterBar_Back_StandBy>
  <Pattern_CenterBar_Font_StandBy>{','.join(map(str, color_variants['color_four']))}</Pattern_CenterBar_Font_StandBy>
  <Pattern_Selection>{','.join(map(str, color_variants['color_five']))}</Pattern_Selection>
  <Pattern_StandBy_Selection>{','.join(map(str, color_variants['color_six']))}</Pattern_StandBy_Selection>
  <Pattern_Mute_State>{','.join(map(str, color_variants['color_seven']))}</Pattern_Mute_State>
  <Automation_Grid>{','.join(map(str, color_variants['color_two']))}</Automation_Grid>
  <Automation_Line_Edge>{','.join(map(str, color_variants['color_three']))}</Automation_Line_Edge>
  <Automation_Line_Fill>{','.join(map(str, color_variants['color_four']))}</Automation_Line_Fill>
  <Automation_Point>{','.join(map(str, color_variants['color_five']))}</Automation_Point>
  <Automation_Marker_Play>{','.join(map(str, color_variants['color_six']))}</Automation_Marker_Play>
  <Automation_Marker_Single>{','.join(map(str, color_variants['color_seven']))}</Automation_Marker_Single>
  <Automation_Marker_Pair>{','.join(map(str, color_variants['color_two']))}</Automation_Marker_Pair>
  <Automation_Marker_Diamond>{','.join(map(str, color_variants['color_three']))}</Automation_Marker_Diamond>
  <VuMeter_Meter>{','.join(map(str, color_variants['color_four']))}</VuMeter_Meter>
  <VuMeter_Meter_Low>{','.join(map(str, color_variants['color_five']))}</VuMeter_Meter_Low>
  <VuMeter_Meter_Middle>{','.join(map(str, color_variants['color_six']))}</VuMeter_Meter_Middle>
  <VuMeter_Meter_High>{','.join(map(str, color_variants['color_seven']))}</VuMeter_Meter_High>
  <VuMeter_Peak>{','.join(map(str, color_variants['color_two']))}</VuMeter_Peak>
  <VuMeter_Back_Normal>{','.join(map(str, color_variants['color_three']))}</VuMeter_Back_Normal>
  <VuMeter_Back_Clipped>{','.join(map(str, color_variants['color_four']))}</VuMeter_Back_Clipped>  <Default_Color_01>{','.join(map(str, color_variants['color_one']))}</Default_Color_01>
  <Default_Color_02>{','.join(map(str, color_variants['color_one']))}</Default_Color_02>
  <Default_Color_03>{','.join(map(str, color_variants['color_one']))}</Default_Color_03>
  <Default_Color_04>{','.join(map(str, color_variants['color_one']))}</Default_Color_04>
  <Default_Color_05>{','.join(map(str, color_variants['color_one']))}</Default_Color_05>
  <Default_Color_06>{','.join(map(str, color_variants['color_one']))}</Default_Color_06>
  <Default_Color_07>{','.join(map(str, color_variants['color_one']))}</Default_Color_07>
  <Default_Color_08>{','.join(map(str, color_variants['color_one']))}</Default_Color_08>
  <Default_Color_09>{','.join(map(str, color_variants['color_one']))}</Default_Color_09>
  <Default_Color_10>{','.join(map(str, color_variants['color_one']))}</Default_Color_10>
  <Default_Color_11>{','.join(map(str, color_variants['color_one']))}</Default_Color_11>
  <Default_Color_12>{','.join(map(str, color_variants['color_one']))}</Default_Color_12>
  <Default_Color_13>{','.join(map(str, color_variants['color_one']))}</Default_Color_13>
  <Default_Color_14>{','.join(map(str, color_variants['color_one']))}</Default_Color_14>
  <Default_Color_15>{','.join(map(str, color_variants['color_one']))}</Default_Color_15>
  <Default_Color_16>{','.join(map(str, color_variants['color_one']))}</Default_Color_16>
  <ButtonBevalAmount>1.0</ButtonBevalAmount>
  <BodyBevalAmount>1.0</BodyBevalAmount>
  <ContrastAdjustment>-0.0</ContrastAdjustment>
  <TextureSet>Default</TextureSet>
</SkinColors>"""
    return xrns_content


# Function to load ASCII art frames from text files
def load_ascii_frames(num_frames, file_path_template):
    frames = []
    for i in range(1, num_frames + 1):
        with open(file_path_template.format(i), 'r') as file:
            frames.append(file.read())
    return frames

# Function to play ASCII animation frames
def play_ascii_animation(frames, duration=6):
    num_frames = len(frames)
    frame_duration = duration / num_frames
    for frame in frames:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
        print(frame, end="\r", flush=True)
        time.sleep(frame_duration)

# Main function to parse arguments and run the script
def main():
    parser = argparse.ArgumentParser(description='Generate a .xrns theme file from an image.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')
    parser.add_argument('--saturation', type=float, default=5.0, help='Saturation enhancement factor (1-10).')
    parser.add_argument('--theme_style', type=str, default='base', choices=['light', 'dark', 'base'], help='Theme style: light, dark, or base.')
    parser.add_argument('--output', type=str, default='output_theme.xrnc', help='Output file path for the theme.')
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print("The specified image file does not exist.")
        exit()

    # Confirm before overwriting an existing file
    if os.path.exists(args.output):
        confirm = input(f"The file {args.output} already exists. Overwrite? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

    start_time = time.time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Load the ASCII frames
    frames = load_ascii_frames(60, os.path.join(script_dir, 'resources', 'renoise_logo_frame_{:02d}.txt'))
    # Play the ASCII animation
    play_ascii_animation(frames, duration=6)

    # Inside the main function before calling enhance_saturation

    img = Image.open(args.image_path).convert('RGB')  # Ensure image is in RGB mode
    pixels = img.getdata()  # Get all pixels in the image
    color_counts = {}

    # Count the frequency of each color
    for color in pixels:
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1

    # Find the most frequent color
    most_frequent_color = max(color_counts, key=color_counts.get)

    # Print out the most frequent color
    print("Most frequent color:", most_frequent_color)

    # Ensure that we have a tuple of three integers for the RGB color
    if not isinstance(most_frequent_color, tuple) or len(most_frequent_color) != 3:
        raise ValueError("The most frequent color must be a tuple of three integers.")

    enhanced_base_color = enhance_saturation(most_frequent_color, args.saturation)
    # Create color variants using the enhanced base color
    top_colors = get_top_colors(args.image_path)
    color_variants = create_color_variants(top_colors, args.theme_style)
    # Now, pass color_variants to create_xrns_theme
    theme_content = create_xrns_theme(color_variants)

    # Save the theme content to a file
    with open(args.output, 'w') as theme_file:
        theme_file.write(theme_content)
    
    elapsed_time = time.time() - start_time
    print(f"\nTheme generated in {elapsed_time:.2f} seconds and saved as {args.output}.")

if __name__ == "__main__":
    main()

