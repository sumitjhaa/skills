"""Music player — now playing display with formatted strings"""

song = "Bohemian Rhapsody"
artist = "Queen"
album = "A Night at the Opera"
duration_sec = 354
progress_sec = 127
rating = 4.8

print(f"Now Playing: {song} by {artist}")
print(f"   Album: {album}")
print(f"   Duration: {duration_sec // 60}:{duration_sec % 60:02d}")
print(f"   Progress: {progress_sec // 60}:{progress_sec % 60:02d}")
print(f"   Rating: {rating}/5.0")

print(f"\nProgress percentage: {progress_sec / duration_sec * 100:.1f}%")

print("\n--- Library Entry ---")
print("Track: {} by {} ({})".format(song, artist, album))

print("\n--- Playlist ---")
print("1. Come Together\t2. Dream On\t3. Stairway")
print("Lyrics preview:\nIs this the real life?\nIs this just fantasy?")

music_path = r"C:\Users\DJ\Music\Classic Rock"
print(f"\nMusic folder: {music_path}")
