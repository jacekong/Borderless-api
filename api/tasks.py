import os
import subprocess
import json
from celery import shared_task
from django.conf import settings
from .models import PostVideos

@shared_task
def transcode_video(video_id):
    video = PostVideos.objects.get(video_id=video_id)
    input_path = video.video.path
    output_dir = os.path.join(settings.MEDIA_ROOT, f'videos/{video_id}')
    os.makedirs(output_dir, exist_ok=True)
    print(f'--- Transcoding with Apple GPU (VideoToolbox): {input_path} ---')
    
    # Get input video metadata
    ffprobe_cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'stream=width,height:format=bit_rate,duration',
        '-of', 'json', input_path
    ]
    probe_result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
    video_info = json.loads(probe_result.stdout)
    width = video_info['streams'][0]['width']
    height = video_info['streams'][0]['height']
    input_bitrate = int(video_info['format'].get('bit_rate', '1000000')) // 1000  # kbps, default 1000
    duration = float(video_info['format'].get('duration', '60'))
    aspect_ratio = width / height
    print(f'Input: {width}x{height}, Bitrate: {input_bitrate} kbps, Duration: {duration} s')

    # Define bitrate tiers based on input bitrate
    streams = [
        {'bitrate': f'{max(50, int(input_bitrate * 0.25))}k', 'scale_factor': 0.25, 'index': '0'},  # 240p, 25%
        {'bitrate': f'{max(100, int(input_bitrate * 0.5))}k', 'scale_factor': 0.5, 'index': '1'},   # 720p, 50%
        {'bitrate': f'{input_bitrate}k', 'scale_factor': 1.0, 'index': '2'},                        # 1080p, original
    ]

    # Transcode each stream
    for stream in streams:
        scaled_width = int(width * stream['scale_factor']) - (int(width * stream['scale_factor']) % 2)
        scaled_height = int(height * stream['scale_factor']) - (int(height * stream['scale_factor']) % 2)
        output_path = f'{output_dir}/{stream["index"]}/playlist.m3u8'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        ffmpeg_cmd = [
            'ffmpeg',
            '-hwaccel', 'videotoolbox',
            '-i', input_path,
            '-c:v', 'h264_videotoolbox',
            '-b:v', stream['bitrate'],
            '-vf', f'scale={scaled_width}:{scaled_height}',
            '-c:a', 'copy',
            '-f', 'hls', '-hls_time', '6', '-hls_list_size', '0',  # Small segments
            '-v', 'verbose',
            output_path
        ]
        try:
            result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
            print(f'Stream {stream["index"]} ({scaled_width}x{scaled_height}) Output: {result.stdout}')
        except subprocess.CalledProcessError as e:
            print(f'FFmpeg Error for Stream {stream["index"]}: {e.stderr}')
            video.processed = False
            video.save()
            raise

    # Generate master.m3u8
    master_m3u8 = "#EXTM3U\n#EXT-X-VERSION:3\n"
    for stream in streams:
        scaled_width = int(width * stream['scale_factor']) - (int(width * stream['scale_factor']) % 2)
        scaled_height = int(height * stream['scale_factor']) - (int(height * stream['scale_factor']) % 2)
        master_m3u8 += f"#EXT-X-STREAM-INF:BANDWIDTH={stream['bitrate'][:-1]}000,RESOLUTION={scaled_width}x{scaled_height}\n{stream['index']}/playlist.m3u8\n"
    with open(os.path.join(output_dir, 'master.m3u8'), 'w') as f:
        f.write(master_m3u8)

    video.hls_path = f'media/videos/{video_id}/master.m3u8'
    video.processed = True
    video.save()
    print(f'Transcoding completed: {video.hls_path}')