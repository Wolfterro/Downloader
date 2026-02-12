from yt_dlp.extractor import gen_extractors

def isValidUrl(url: str) -> bool:
    extractors = gen_extractors()
    for ext in extractors:
        if ext.suitable(url) and ext.IE_NAME != "generic":
            return True
    
    return False