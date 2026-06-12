# DaVinci Resolve Python Scripting

## When to use
- Color grade with scopes-accurate primary + secondary nodes (FFmpeg can't replicate)
- Automate render queue across N projects
- Apply LUT to specific timeline nodes (vs whole clip)
- Color-page batch operations (e.g., apply same grade to a series)

Skip when: a simple `ffmpeg lut3d` does the job; the user lacks DaVinci installed.

## Setup
Requires DaVinci Resolve (free or Studio) installed locally.

```bash
# Python path: bundled in Resolve install
# Windows: C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\
# macOS:   /Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/
# Linux:   /opt/resolve/Developer/Scripting/

export RESOLVE_SCRIPT_API="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
```

DaVinci must be running. Python script connects via local TCP.

## Common recipes

### 1. Connect to Resolve
```python
import DaVinciResolveScript as dvr_script
resolve = dvr_script.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()
timeline = project.GetCurrentTimeline()
```

### 2. Create / load project
```python
# Create
new_proj = project_manager.CreateProject("MyAutoProject")

# Load existing
project_manager.LoadProject("Existing Project Name")
```

### 3. Import media
```python
folder = media_pool.GetCurrentFolder()
items = media_pool.ImportMedia(["/abs/path/clip1.mp4", "/abs/path/clip2.mp4"])
# items: list of MediaPoolItem
```

### 4. Create timeline from media pool items
```python
timeline = media_pool.CreateTimelineFromClips("Auto Timeline", items)
project.SetCurrentTimeline(timeline)
```

### 5. Apply LUT to a clip on the color page
```python
resolve.OpenPage("color")
clip = timeline.GetCurrentVideoItem()
# Get current node
clip.SetLUT(1, "/path/to/cinematic.cube")  # 1 = node index
```

### 6. Add a new color correction node
```python
# Requires accessing the color page programmatically; limited surface
# Use Resolve's Fusion-style API for nodes
graph = clip.GetNodeGraph()
graph.AddNode(node_type="ColorCorrector", label="Primary")
```
(Note: Node-graph API is more limited than Fusion; for complex graphs, save a preset in GUI and apply via `ApplyGradeFromDRX`.)

### 7. Apply a `.drx` color preset
```python
# Save a grade in the GUI as MyLook.drx via File > Save Color Preset
clip = timeline.GetCurrentVideoItem()
clip.ApplyArriCdlLut("/path/to/grade.drx")
# OR via project_manager: project.ImportDrx(...)
```

### 8. Iterate all timeline clips and apply same LUT
```python
items = timeline.GetItemListInTrack("video", 1)
for item in items:
    item.SetLUT(1, "/path/cinematic.cube")
```

### 9. Render queue automation
```python
# Configure render
project.SetCurrentRenderMode(0)  # 0 = individual clips, 1 = single clip
project.SetRenderSettings({
    "SelectAllFrames": True,
    "TargetDir": "/abs/path/renders",
    "CustomName": "myrender",
    "FormatWidth": 1920,
    "FormatHeight": 1080,
    "FrameRate": "30",
    "VideoQuality": 0,   # 0 = Automatic
})
job_id = project.AddRenderJob()
project.StartRendering([job_id])
# Poll
while project.IsRenderingInProgress():
    time.sleep(2)
status = project.GetRenderJobStatus(job_id)
```

### 10. List available render presets
```python
presets = project.GetRenderPresetList()
project.LoadRenderPreset("YouTube 1080p")
```

### 11. Batch project processing
```python
projects = ["ep01", "ep02", "ep03"]
for name in projects:
    project_manager.LoadProject(name)
    p = project_manager.GetCurrentProject()
    # ...apply same grade, then render
    p.AddRenderJob()
    p.StartRendering()
```

### 12. Smart Reframe (auto-vertical from horizontal)
```python
# Resolve 18+ has "Smart Reframe" — drives via the API:
# Not directly callable; trigger via Fusion macro or AppleScript wrapper.
# Workaround: apply during a "Color page" effect chain.
```

### 13. Apply Fairlight audio settings
```python
# Limited API surface; mostly export via render with audio bitrate set
project.SetRenderSettings({
    "AudioCodec": "aac",
    "AudioBitDepth": "16",
    "AudioSampleRate": "48000",
    "ExportAudio": True
})
```

### 14. Headless rendering wrapper
```bash
# resolve_render.py
python3 resolve_render.py --project EP01 --preset "YouTube 1080p" --output renders/
```
Wraps the above pattern; can be triggered from `cli-anything`.

### 15. Save / restore color preset (DRX)
```python
# Save current clip's grade
clip = timeline.GetCurrentVideoItem()
clip.SaveColorPreset("My Look")  # saves to ~/Library/.../ColorPresets/

# Apply to another clip
other_clip.ApplyColorPreset("My Look")
```

## Examples

### A. Apply LUT across a 50-clip timeline
1. Open project → get timeline → list items.
2. Loop `item.SetLUT(1, "cinematic.cube")` for each.
3. Render to YouTube 1080p preset.

### B. Batch-render 10 episodes with same grade
1. Save grade as DRX in episode 1 (manually).
2. Python: loop EP01–EP10, load project, apply DRX, add render job, start.
3. Total: ~3 hrs unattended vs ~6 hrs manual.

### C. Vertical reframe for short-form
1. Open horizontal project.
2. Use Resolve's Smart Reframe (manual click) → save as `_vertical` timeline.
3. Render the vertical timeline programmatically.

### D. Color-match cross-camera shoot
1. Identify hero camera grade in GUI → save DRX.
2. Python: apply DRX to all clips from other cameras.
3. Manual tweak per-clip → final.

## Edge cases / gotchas

1. **Resolve must be running.** No headless mode; script connects to live app.
2. **Node-graph API is limited.** Save complex grades as DRX presets in the GUI, then apply via Python.
3. **`SetLUT(node, path)`** silently no-ops on invalid paths; verify file exists first.
4. **Render preset names are case-sensitive.**
5. **`StartRendering` is non-blocking.** Use `IsRenderingInProgress()` loop to wait.
6. **Render fails silently** on disk-full / permission errors; check `GetRenderJobStatus`.
7. **Free vs Studio differences.** Smart Reframe + some neural-engine features Studio-only.
8. **PYTHONPATH** must include Resolve's Scripting/Modules directory.
9. **macOS Gatekeeper** can block fusionscript.so; allow once in Security & Privacy.
10. **Project locks** — only one Python script attached at a time. Multiple attempts conflict.
11. **`ImportMedia` returns clip objects only if successful.** Defensive: `items if items else handle_error()`.
12. **Drx files are GUI-saved, not Python-creatable.** API consumes them; doesn't author them.

## Sources
- https://www.blackmagicdesign.com/products/davinciresolve (download)
- Resolve docs ship at: `Support/Developer/Scripting/README.txt` after install
- Community wiki: https://www.steakunderwater.com/wesuckless/viewtopic.php?p=29483
- https://documents.blackmagicdesign.com/UserManuals/DaVinciResolve19-Documentation.pdf
