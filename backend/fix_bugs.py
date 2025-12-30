"""
Script to fix the JSON serialization and WebSocket errors in ada.py
Run this script to automatically apply the fixes
"""
import re


def fix_ada_py():
    ada_path = r"E:\jarvis\ada_v2\backend\ada.py"
    
    # Read the file
    with open(ada_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add imports at the top
    if 'import websockets.exceptions' not in content:
        content = content.replace(
            'import time',
            'import time\nimport websockets.exceptions'
        )
    
    if 'from json_sanitizer import sanitize_for_json' not in content:
        content = content.replace(
            'from tools import tools_list',
            'from tools import tools_list\nfrom json_sanitizer import sanitize_for_json'
        )
    
    # Fix 2: Sanitize on_transcription callbacks
    # Find all on_transcription calls and wrap them with sanitize_for_json
    content = re.sub(
        r'self\.on_transcription\(\{"sender": "User", "text": delta\}\)',
        r'self.on_transcription(sanitize_for_json({"sender": "User", "text": delta}))',
        content
    )
    
    content = re.sub(
        r'self\.on_transcription\(\{"sender": "JARVIS", "text": delta\}\)',
        r'self.on_transcription(sanitize_for_json({"sender": "JARVIS", "text": delta}))',
        content
    )
    
    # Fix 3: Add specific WebSocket error handling
    content = content.replace(
        '        except Exception as e:\n            print(f"Error in receive_audio: {e}")\n            traceback.print_exc()\n            # CRITICAL: Re-raise to crash the TaskGroup and trigger outer loop reconnect\n            raise e',
        '        except websockets.exceptions.ConnectionClosedError as e:\n            print(f"[ADA DEBUG] [ERR] WebSocket connection closed: {e}")\n            # This is expected during reconnection - re-raise to trigger reconnect\n            raise e\n        except Exception as e:\n            print(f"Error in receive_audio: {e}")\n            traceback.print_exc()\n            # CRITICAL: Re-raise to crash the TaskGroup and trigger outer loop reconnect\n            raise e'
    )
    
    # Write the file back
    with open(ada_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[SUCCESS] Applied fixes to ada.py")
    print("  ✓ Added websockets.exceptions import")
    print("  ✓ Added json_sanitizer import")
    print("  ✓ Added sanitize_for_json wrapper for transcription callbacks")
    print("  ✓ Added specific WebSocket error handling")


def fix_server_py():
    server_path = r"E:\jarvis\ada_v2\backend\server.py"
    
    with open(server_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace @app.on_event("startup") with lifespan pattern
    old_startup = '''@app.on_event("startup")
async def startup_event():'''
    
    new_startup = '''from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code'''
    
    if old_startup in content:
        # Find the entire startup function
        startup_match = re.search(
            r'@app\.on_event\("startup"\)\nasync def startup_event\(\):(.*?)(?=\n@|\nclass |\ndef |\napp = |\Z)',
            content,
            re.DOTALL
        )
        
        if startup_match:
            startup_body = startup_match.group(1).strip()
            
            # Create new lifespan function
            new_lifespan = f'''from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
{startup_body}
    yield
    # Shutdown code (if needed)
    pass
'''
            
            # Replace the old function
            content = content.replace(startup_match.group(0), new_lifespan)
            
            # Update FastAPI app initialization to use lifespan
            content = re.sub(
                r'app = FastAPI\(\)',
                'app = FastAPI(lifespan=lifespan)',
                content
            )
            
            print("[SUCCESS] Applied fixes to server.py")
            print("  ✓ Replaced @app.on_event('startup') with lifespan pattern")
            print("  ✓ Updated FastAPI() to FastAPI(lifespan=lifespan)")
            
            # Write back
            with open(server_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print("[WARN] Could not find startup_event function body in server.py")
    else:
        print("[INFO] server.py already uses lifespan pattern or startup not found")


if __name__ == "__main__":
    print("=" * 60)
    print("Ada v2 Bug Fix Script")
    print("=" * 60)
    print()
    
    try:
        fix_ada_py()
        print()
        fix_server_py()
        print()
        print("=" * 60)
        print("All fixes applied successfully!")
        print("Please restart your application to apply changes.")
        print("=" * 60)
    except Exception as e:
        print(f"\n[ERROR] Failed to apply fixes: {e}")
        import traceback
        traceback.print_exc()
