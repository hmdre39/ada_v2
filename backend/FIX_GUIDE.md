# Ada v2 Bug Fixes - Manual Application Guide

## Summary
Your Ada voice assistant has two main issues:
1. **JSON Serialization Error**: `TypeError: Object of type float32 is not JSON serializable`
2. **WebSocket Timeout**: `ConnectionClosedError: Deadline expired before operation could complete`

## Files Created

### 1. `E:\jarvis\ada_v2\backend\json_sanitizer.py` (NEW FILE - Already Created)
This helper module converts numpy float32 values to Python floats for JSON serialization.

### 2. `E:\jarvis\ada_v2\backend\fix_bugs.py` (NEW FILE - Already Created)
Automated fix script (run this if you want automatic fixes).

## Manual Fixes Required

### Fix 1: Update ada.py

#### A. Add imports (near line 17-19, after existing imports)
Find this line:
```python
import time
```

Add after it:
```python
import websockets.exceptions
```

Find this line:
```python
from tools import tools_list
```

Add after it:
```python
from json_sanitizer import sanitize_for_json
```

#### B. Fix JSON serialization in transcription callbacks
Find these two locations (around lines 730-740 and 760-770):

**Location 1** - User transcription:
```python
# Send to frontend (Streaming)
if self.on_transcription:
    self.on_transcription({"sender": "User", "text": delta})
```

Replace with:
```python
# Send to frontend (Streaming) - sanitize for JSON
if self.on_transcription:
    self.on_transcription(sanitize_for_json({"sender": "User", "text": delta}))
```

**Location 2** - JARVIS transcription:
```python
# Send to frontend (Streaming)
if self.on_transcription:
    self.on_transcription({"sender": "JARVIS", "text": delta})
```

Replace with:
```python
# Send to frontend (Streaming) - sanitize for JSON
if self.on_transcription:
    self.on_transcription(sanitize_for_json({"sender": "JARVIS", "text": delta}))
```

#### C. Improve WebSocket error handling
Find this code (around line 1050):
```python
        except Exception as e:
            print(f"Error in receive_audio: {e}")
            traceback.print_exc()
            # CRITICAL: Re-raise to crash the TaskGroup and trigger outer loop reconnect
            raise e
```

Replace with:
```python
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"[ADA DEBUG] [ERR] WebSocket connection closed: {e}")
            # This is expected during reconnection - re-raise to trigger reconnect
            raise e
        except Exception as e:
            print(f"Error in receive_audio: {e}")
            traceback.print_exc()
            # CRITICAL: Re-raise to crash the TaskGroup and trigger outer loop reconnect
            raise e
```

### Fix 2: Update server.py (Optional - Fixes deprecation warning)

Find this code (around line 117):
```python
@app.on_event("startup")
async def startup_event():
    import sys
    print(f"[SERVER DEBUG] Startup Event Triggered")
    # ... rest of startup code ...
    print("[SERVER] Startup: Initializing Kasa Agent...")
    await kasa_agent.initialize()
```

Add this import at the top of the file:
```python
from contextlib import asynccontextmanager
```

Replace the entire @app.on_event block with:
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    import sys
    print(f"[SERVER DEBUG] Startup Event Triggered")
    print(f"[SERVER DEBUG] Python Version: {sys.version}")
    try:
        loop = asyncio.get_running_loop()
        print(f"[SERVER DEBUG] Running Loop: {type(loop)}")
        policy = asyncio.get_event_loop_policy()
        print(f"[SERVER DEBUG] Current Policy: {type(policy)}")
    except Exception as e:
        print(f"[SERVER DEBUG] Error checking loop: {e}")

    print("[SERVER] Startup: Initializing Kasa Agent...")
    await kasa_agent.initialize()
    
    yield
    
    # Shutdown code (if needed)
    pass
```

Then update your FastAPI app initialization (around line 26):
```python
app = FastAPI()
```

Change to:
```python
app = FastAPI(lifespan=lifespan)
```

## Automated Fix Option

Instead of manual fixes, you can run the automated script:

```bash
cd E:\jarvis\ada_v2\backend
python fix_bugs.py
```

This will apply all the fixes automatically.

## Testing

After applying fixes:
1. Stop the current Ada application
2. Restart it
3. Test voice interaction
4. The errors should no longer appear in the console

## What These Fixes Do

1. **json_sanitizer.py**: Converts numpy float32 values (from audio processing) to regular Python floats before sending via Socket.IO

2. **Transcription sanitization**: Wraps all transcription data with sanitize_for_json() to prevent float32 serialization errors

3. **WebSocket error handling**: Separates ConnectionClosedError handling (expected during timeout) from other exceptions for better error messages and reconnection

4. **FastAPI lifespan** (optional): Modernizes the startup event handler to use the new lifespan pattern, removing the deprecation warning

## Expected Results

After applying these fixes:
- ✅ No more "Object of type float32 is not JSON serializable" errors
- ✅ Better handling of Google API timeouts with automatic reconnection
- ✅ No more FastAPI deprecation warnings (if Fix 2 applied)
- ✅ Smoother voice interaction without crashes
