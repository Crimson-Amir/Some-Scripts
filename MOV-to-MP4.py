import os
import subprocess
import sys

def convert_mov_to_mp4(folder_path):
    # Check if directory exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Get all files in the directory
    files = os.listdir(folder_path)
    mov_files = [f for f in files if f.lower().endswith('.mov')]

    if not mov_files:
        print("No .MOV files found in the specified folder.")
        return

    print(f"Found {len(mov_files)} MOV files. Starting conversion...")

    for filename in mov_files:
        input_path = os.path.join(folder_path, filename)
        
        # Create output filename (change extension to .mp4)
        output_filename = os.path.splitext(filename)[0] + ".mp4"
        output_path = os.path.join(folder_path, output_filename)

        # Skip if output already exists to avoid overwriting
        if os.path.exists(output_path):
            print(f"Skipping {filename}: {output_filename} already exists.")
            continue

        print(f"Converting: {filename} -> {output_filename}")

        # FFmpeg command
        # -i: Input file
        # -c:v libx264: Use H.264 video codec (highly compatible for editing)
        # -crf 18: Quality setting (0-51). 18 is visually lossless. Lower is better quality/larger file.
        # -preset slow: Better compression efficiency (takes longer, looks better)
        # -c:a aac: AAC audio codec
        # -b:a 192k: Audio bitrate
        # -movflags +faststart: Moves metadata to front (better for web/previewing)
        # -vf format=yuv420p: Ensures compatibility with all players (iPhone sometimes uses different pixel formats)
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-crf', '18',
            '-preset', 'ultrafast',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-vf', 'format=yuv420p',
            '-movflags', '+faststart',
            output_path
        ]

        try:
            # Run the command and suppress detailed output (remove stderr=subprocess.DEVNULL to see logs)
            subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
            print(f"Success: {output_filename}")
        except subprocess.CalledProcessError:
            print(f"Error converting {filename}. Ensure FFmpeg is installed correctly.")
        except FileNotFoundError:
            print("Error: FFmpeg not found. Please install FFmpeg and add it to your system PATH.")
            sys.exit(1)

    print("\nBatch conversion complete!")

if __name__ == "__main__":
    # Use current directory where the script is running
    current_folder = os.getcwd()
    
    # OR replace 'current_folder' below with a specific path like r"C:\Users\Name\Videos\iPhoneClips"
    convert_mov_to_mp4(current_folder)
