
major = "0"
minor = "1"
patch = "0"
release_type = "dev0"

if release_type:
    __version__ = f"{major}.{minor}.{patch}.{release_type}"
else:
    __version__ = f"{major}.{minor}.{patch}"
