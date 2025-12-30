# Philips Hue Integration for Ada

## Your Hue Credentials (SAVE THESE!)

```
Bridge IP: 192.168.86.68
Username: P82u7Cds2TuL7av95ij6dqsCzcVj5Ffxa4d107K3
```

## Integration Steps

### 1. Add Hue credentials to `settings.json`:

Add this to your `DEFAULT_SETTINGS` in `server.py`:

```python
"hue_bridge_ip": "192.168.86.68",
"hue_username": "P82u7Cds2TuL7av95ij6dqsCzcVj5Ffxa4d107K3",
```

### 2. Import HueAgent in `server.py`:

```python
from hue_agent import HueAgent
```

### 3. Initialize HueAgent in `server.py`:

```python
hue_agent = HueAgent(
    bridge_ip=SETTINGS.get("hue_bridge_ip"),
    username=SETTINGS.get("hue_username")
)
```

### 4. Add Socket.IO endpoints for Hue control:

```python
@sio.event
async def discover_hue(sid):
    """Discover and list all Hue lights"""
    if not hue_agent.bridge_ip or not hue_agent.username:
        await sio.emit('error', {'msg': "Hue not configured"})
        return
    
    try:
        await hue_agent.get_lights()
        lights = hue_agent.format_lights_for_frontend()
        await sio.emit('hue_lights', lights)
        await sio.emit('status', {'msg': f"Found {len(lights)} Hue lights"})
    except Exception as e:
        await sio.emit('error', {'msg': f"Hue Discovery Failed: {str(e)}"})

@sio.event  
async def control_hue(sid, data):
    """Control a Hue light"""
    # data: { light_id, action: "on"|"off"|"brightness"|"color", value: ... }
    light_id = data.get('light_id')
    action = data.get('action')
    
    try:
        success = False
        if action == "on":
            success = await hue_agent.turn_on(light_id)
        elif action == "off":
            success = await hue_agent.turn_off(light_id)
        elif action == "brightness":
            val = data.get('value')  # 0-100
            success = await hue_agent.set_brightness(light_id, val)
        elif action == "color":
            hue_val = data.get('hue', 0)
            sat_val = data.get('sat', 254)
            success = await hue_agent.set_color(light_id, hue_val, sat_val)
        
        if success:
            # Refresh lights
            await hue_agent.get_lights()
            lights = hue_agent.format_lights_for_frontend()
            await sio.emit('hue_lights', lights)
        else:
            await sio.emit('error', {'msg': f"Failed to control light {light_id}"})
    except Exception as e:
        await sio.emit('error', {'msg': f"Hue Control Error: {str(e)}"})
```

### 5. Voice Commands - Add Hue tools to `ada.py`:

```python
list_hue_lights_tool = {
    "name": "list_hue_lights",
    "description": "Lists all Philips Hue lights and their current state.",
    "parameters": {
        "type": "OBJECT",
        "properties": {},
    }
}

control_hue_light_tool = {
    "name": "control_hue_light",
    "description": "Controls a Philips Hue light.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "light_id": {
                "type": "STRING",
                "description": "The ID or name of the light to control."
            },
            "action": {
                "type": "STRING",
                "description": "The action: 'turn_on', 'turn_off', 'set_brightness', 'set_color'."
            },
            "brightness": {
                "type": "INTEGER",
                "description": "Optional brightness (0-100)."
            },
            "color": {
                "type": "STRING",
                "description": "Optional color name (e.g., 'red', 'blue', 'warm white')."
            }
        },
        "required": ["light_id", "action"]
    }
}
```

Add to tools array:
```python
tools = [
    {'google_search': {}}, 
    {"function_declarations": [
        generate_cad, 
        run_web_agent, 
        # ... existing tools ...
        list_hue_lights_tool,
        control_hue_light_tool,
        # ... rest of tools ...
    ]}
]
```

## Quick Start

For now, to test Hue control manually:

1. **Save these credentials** somewhere safe
2. I'll create a simple integration that you can trigger from Ada

Would you like me to:
- A) Do a full integration now (adds voice control to Ada)
- B) Just add manual control buttons to the frontend first
- C) Create a simple test script to control your lights from command line

Which would you prefer? 🤔
