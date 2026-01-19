# CLAUDE.MD - AI Assistant Guide for JARVIS V2

> **Purpose**: This document helps AI assistants (like Claude) understand the JARVIS V2 codebase architecture, conventions, and best practices for making changes.

---

## 📋 Project Overview

**JARVIS V2** (Just A Rather Very Intelligent System) is a sophisticated multimodal AI assistant combining:
- **Voice AI**: Google Gemini 2.5 Native Audio for real-time conversation
- **Computer Vision**: MediaPipe for face authentication and gesture control
- **3D CAD Generation**: build123d for parametric modeling from voice commands
- **3D Printing**: OrcaSlicer integration with wireless printer control
- **Web Automation**: Playwright-based browser agent
- **Smart Home**: TP-Link Kasa and Philips Hue integration
- **Project Memory**: Persistent context management across sessions

**Tech Stack**:
- Frontend: React 18 + Electron + Three.js + Tailwind CSS
- Backend: Python 3.11 + FastAPI + Socket.IO
- AI: Google Gemini 2.5 Flash with Native Audio
- Build: Vite + Node.js 18+

---

## 🏗️ Architecture

### High-Level Flow
```
User Voice/Input → React UI → Socket.IO → Python Backend → Gemini API
                                                ↓
                          Tool Execution (CAD/Web/SmartHome/etc.)
                                                ↓
                          Results → Socket.IO → React UI → User
```

### Key Components

#### Frontend (`src/`)
- **App.jsx**: Main application orchestrator, manages socket connections and global state
- **components/**:
  - `AudioControls.jsx`: Microphone, recording, noise suppression controls
  - `CADViewer.jsx`: Three.js-based STL model viewer with orbit controls
  - `Authenticator.jsx`: Face authentication using MediaPipe
  - `GestureController.jsx`: Hand tracking for Minority Report-style gestures
  - `PrinterWindow.jsx`: 3D printer management UI
  - `ProjectSelector.jsx`: Project context switching
  - `WebAgentWindow.jsx`: Browser automation interface
  - `ConnectionStatus.jsx`, `VUMeter.jsx`, `ToastNotifications.jsx`: UI enhancements

#### Backend (`backend/`)
- **server.py**: FastAPI + Socket.IO server, routes all client requests
- **ada.py**: Core Gemini Live API integration (77KB, most complex file)
  - Handles WebSocket connections to Gemini
  - Manages audio streaming (input/output)
  - Tool calling orchestration
  - Session state management
- **cad_agent.py**: 3D model generation using build123d
- **printer_agent.py**: Printer discovery (mDNS), slicing (OrcaSlicer), print job submission
- **web_agent.py**: Playwright browser automation with intelligent action selection
- **kasa_agent.py**: TP-Link Kasa smart home device control
- **hue_agent.py**: Philips Hue light control (NEW - recent integration)
- **authenticator.py**: MediaPipe face landmarker for biometric auth
- **project_manager.py**: Persistent project context storage (JSON-based)
- **audio_processor.py**: WebRTC VAD, noise gating, audio buffering
- **tools.py**: Tool definitions passed to Gemini for function calling

---

## 📂 Critical Files & Their Responsibilities

| File | Lines | Purpose | Modify With Care |
|------|-------|---------|------------------|
| `backend/ada.py` | ~1900 | Gemini WebSocket, audio streaming, tool orchestration | ⚠️ HIGH |
| `backend/server.py` | ~1050 | Socket.IO server, client event handlers | ⚠️ HIGH |
| `backend/cad_agent.py` | ~480 | CAD generation, LLM-to-Python code translation | ⚠️ MEDIUM |
| `backend/printer_agent.py` | ~1080 | Printer discovery, slicing, job submission | ⚠️ MEDIUM |
| `backend/web_agent.py` | ~330 | Browser automation logic | ⚠️ MEDIUM |
| `src/App.jsx` | ~650 | React app root, socket event handlers | ⚠️ HIGH |
| `src/components/AudioControls.jsx` | ~250 | Microphone controls, audio settings | ⚠️ LOW |
| `backend/settings.json` | ~20 | User preferences, tool permissions | ⚠️ LOW |

---

## 🔧 Development Workflow

### Making Changes

1. **Always check current branch**: `git status` (should be `claude/update-claude-md-Xbuas`)
2. **Understand before modifying**: Read files completely before suggesting changes
3. **Test locally**: Run the app to verify changes work
4. **Commit with clear messages**: Use descriptive commit messages
5. **Push to correct branch**: Use `git push -u origin claude/update-claude-md-Xbuas`

### Running the Application

**Two-Terminal Setup (Recommended for Development)**:
```bash
# Terminal 1 - Backend
conda activate ada_v2
python backend/server.py

# Terminal 2 - Frontend
npm run dev
```

**Single Command** (Production-like):
```bash
conda activate ada_v2
npm run dev  # Starts both backend and Electron
```

---

## ⚙️ Configuration Files

### `.env` (Root Level)
```
GEMINI_API_KEY=your_api_key_here
PORCUPINE_ACCESS_KEY=optional_wake_word_key
```

### `backend/settings.json`
```json
{
  "face_auth_enabled": true,
  "tool_permissions": {
    "generate_cad": false,
    "run_web_agent": false,
    "write_file": true,
    "control_hue": false
  }
}
```

---

## 🎯 Common Tasks & How to Approach Them

### Adding a New Voice Command
1. **Define Tool**: Add function definition to `backend/tools.py`
2. **Implement Handler**: Create handler in appropriate agent file (e.g., `kasa_agent.py`)
3. **Register in ada.py**: Add tool to `self.tools` list and handle in tool execution block
4. **Test**: Use voice command and verify execution

### Adding a New UI Component
1. **Create Component**: Add file to `src/components/`
2. **Import in App.jsx**: Add import and state management
3. **Style with Tailwind**: Use existing design system (dark mode, glassmorphism)
4. **Socket Events**: If backend communication needed, add socket listeners

### Fixing Audio Issues
- **Check**: `backend/audio_processor.py` for WebRTC VAD and noise gate
- **Buffer Size**: `ada.py` manages audio chunks (480 samples @ 16kHz = 30ms)
- **Latency**: Look at `AudioControls.jsx` for real-time metrics

### Adding Smart Home Support
- **Template**: Copy structure from `kasa_agent.py` or `hue_agent.py`
- **Discovery**: Use mDNS (zeroconf) for network device discovery
- **Tools**: Define clear tool schemas in `tools.py`
- **Permissions**: Add to `settings.json` tool_permissions

---

## 🚨 Critical Considerations

### Security
- **API Keys**: Never commit `.env` file
- **Face Data**: `backend/reference.jpg` contains biometric data - never upload
- **Tool Permissions**: Respect `settings.json` - especially `write_file`
- **Code Execution**: CAD agent executes generated Python - validate carefully

### Performance
- **Audio Latency**: Keep audio processing under 30ms (ada.py:480 sample chunks)
- **WebSocket**: Gemini connection drops if silent >60s (ada.py sends keepalive)
- **Memory**: Project memory limited to 100 messages (project_manager.py)
- **3D Rendering**: Large STL files (>10MB) may lag Three.js viewer

### Compatibility
- **Python**: Requires 3.11 (build123d dependency)
- **MediaPipe**: Face landmarker model is 3.7MB binary (`face_landmarker.task`)
- **Windows**: Face auth path handling differs (authenticator.py uses platform-specific logic)
- **Printers**: Moonraker/OctoPrint API differences handled in printer_agent.py

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Voice: Say "Hello Jarvis" - should respond
- [ ] Face Auth: Look at camera - should unlock if enabled
- [ ] CAD: "Create a cube" - should generate and display STL
- [ ] Web Agent: "Go to Google" - should open browser
- [ ] Smart Home: "Turn on lights" - should control devices
- [ ] Recording: Start/stop recording - should save WAV file
- [ ] Gestures: Enable video feed - hand tracking should work

### Key Log Locations
- **Backend**: Python stdout (Terminal 1)
- **Frontend**: Browser DevTools Console (Ctrl+Shift+I in Electron)
- **Socket.IO**: Look for `Connected to server` / `Disconnected` messages

---

## 📦 Dependencies

### Python (requirements.txt)
- `google-genai`: Gemini SDK (Live API)
- `fastapi`, `python-socketio`: Server
- `build123d`: CAD generation
- `playwright`: Browser automation
- `python-kasa`, `phue`: Smart home
- `mediapipe`: Computer vision
- `pyaudio`: Audio I/O (macOS requires `brew install portaudio`)

### Node.js (package.json)
- `react`, `react-dom`: UI framework
- `three`, `@react-three/fiber`: 3D rendering
- `electron`: Desktop app wrapper
- `socket.io-client`: Real-time communication
- `tailwindcss`: Styling

---

## 🐛 Known Issues & Workarounds

### Issue: WebSocket 1011 Internal Error
**Symptom**: Gemini connection drops randomly
**Cause**: Google backend issue or rate limiting
**Fix**: Reconnect automatically (ada.py has retry logic)

### Issue: Camera Permission Denied (macOS)
**Symptom**: Black video feed, permission error
**Cause**: Terminal app lacks camera access
**Fix**: System Preferences → Privacy → Camera → Enable for Terminal/VS Code

### Issue: Face Auth Not Working on Windows
**Symptom**: authenticator.py crashes on Windows
**Cause**: Path handling for `reference.jpg`
**Fix**: Use `os.path.join()` for cross-platform paths (FIXED in recent commit)

### Issue: Audio Skipping/Crackling
**Symptom**: Voice output cuts out or skips
**Cause**: Buffer underruns in audio playback
**Fix**: Improved buffering in audio_processor.py (FIXED - see AUDIO_SKIP_FIX_COMPLETE.md)

---

## 📚 Additional Documentation

- **README.md**: User-facing installation and usage guide
- **VOICE_FEATURES.md**: Voice command reference, audio settings
- **UI_ENHANCEMENTS.md**: UI component documentation
- **backend/HUE_INTEGRATION_GUIDE.md**: Philips Hue setup guide
- **backend/AUDIO_FIX_COMPLETE.md**: Audio bug fix history

---

## 🔄 Recent Major Changes (Last 5 Commits)

1. **Enhanced Memory System**: Increased from 20 to 100 messages
2. **Face Auth Windows Fix**: Cross-platform path handling
3. **Hue Integration Complete**: Full Philips Hue support with discovery
4. **Audio Skip Fix**: Improved buffering eliminates voice skipping
5. **JARVIS Transformation**: Switched from female (Ada) to male voice (Fenrir)

---

## 💡 Tips for AI Assistants

1. **Read First**: Always read files before suggesting modifications
2. **Respect Architecture**: Don't bypass socket.io communication layer
3. **Test Tool Permissions**: Check `settings.json` before enabling dangerous tools
4. **Preserve Comments**: Code has inline docs explaining Gemini API quirks
5. **Branch Naming**: Must start with `claude/` and end with session ID
6. **No Backwards Compat Hacks**: Delete unused code cleanly, no `_vars` or `// removed`
7. **Simple Solutions**: Don't over-engineer - add only what's requested
8. **Security First**: Validate user inputs, especially in CAD/web agents

---

## 🤝 Contributing Guidelines

When making changes:
1. **Understand the "why"**: Read relevant docs and code context
2. **Make focused changes**: One feature/fix per commit
3. **Update documentation**: If adding features, update README.md or relevant docs
4. **Test thoroughly**: Manually verify changes work end-to-end
5. **Clear commit messages**: Describe what changed and why
6. **Push to correct branch**: `claude/update-claude-md-Xbuas` for this session

---

## 📞 Getting Help

- **Issues**: Check `backend/*.md` files for known issue documentation
- **API Docs**: [Gemini Live API](https://ai.google.dev/api/multimodal-live)
- **build123d**: [Documentation](https://build123d.readthedocs.io/)
- **MediaPipe**: [Hand Tracking](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)

---

**Last Updated**: 2026-01-19
**Project Version**: 1.0.0
**Python**: 3.11
**Node**: 18+
**Primary Branch**: `claude/update-claude-md-Xbuas`

---

<p align="center">
<em>This document is maintained for AI assistants working on the JARVIS V2 codebase.</em><br>
<strong>Built with 🤖 by Nazir Louis</strong>
</p>
