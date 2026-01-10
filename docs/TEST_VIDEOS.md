# Test Videos for Squirrel Detection

For development and testing on Windows, you can use video files instead of a live camera feed. This document provides information on where to find suitable test videos.

## Finding Test Videos

### Free Video Sources

1. **Pexels Videos** (https://www.pexels.com/videos/)
   - Search for "squirrel" or "squirrel in garden"
   - Free to use, no attribution required for testing
   - High quality videos available

2. **Pixabay Videos** (https://pixabay.com/videos/)
   - Search for "squirrel", "wildlife", "garden squirrel"
   - Free for commercial use
   - Various resolutions available

3. **YouTube** (with proper permissions)
   - Search for "squirrel videos"
   - Use tools like `yt-dlp` to download videos for testing:
     ```bash
     yt-dlp -f "best[height<=1080]" "YOUTUBE_URL" -o test_videos/squirrel.mp4
     ```
   - **Note**: Ensure you have permission to download and use the video

4. **Internet Archive** (https://archive.org/details/movies)
   - Search for wildlife or nature videos
   - Many are in public domain

## Creating Test Videos

You can also create your own test videos:

1. **Record your own**: If you have access to squirrels, record videos with your phone or camera
2. **Generate synthetic**: Use image sequences with brown objects to simulate squirrels
3. **Use test fixtures**: The test suite creates temporary videos programmatically

## Recommended Video Specifications

- **Resolution**: 640x480 minimum, 1920x1080 preferred
- **Format**: MP4 (H.264 codec) works best
- **Frame rate**: 20-30 FPS
- **Duration**: 10-60 seconds for testing, longer for extended testing
- **Content**: Videos with squirrels in various positions (center, edge, multiple squirrels)

## Using Test Videos

Once you have a video file, use it with the application:

```bash
squirrel-detector --video-path path/to/squirrel_video.mp4 --gpio-pin 18 --debug
```

The `--debug` flag will show you the detection in real-time so you can see how well the detector is working.

## Example Video Downloads

Here are some example commands to download test videos (requires `yt-dlp`):

```bash
# Create test videos directory
mkdir -p test_videos

# Example: Download a squirrel video (replace URL with actual video)
# yt-dlp "https://www.youtube.com/watch?v=EXAMPLE" -o test_videos/squirrel1.mp4

# For Pexels/Pixabay, download directly from their websites
```

## Legal Note

Always ensure you have the right to download and use videos for testing purposes. Many sites like Pexels and Pixabay provide videos under licenses that allow free use for testing and development.
