import re

def extract_video_id(url):
    # Regular expression pattern to match the video ID
    pattern = r"(?:youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=|vi\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    
    # Find the video ID using regular expression
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None