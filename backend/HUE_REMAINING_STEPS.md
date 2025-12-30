# Hue Integration - Remaining Steps

## ✅ Completed:
1. Settings updated with Hue credentials
2. HueAgent imported in server.py and ada.py
3. HueAgent initialized in server.py
4. Hue Socket.IO endpoints added (discover_hue, control_hue)
5. Hue tool definitions added to ada.py (list_hue_lights_tool, control_hue_light_tool)
6. Tools added to tools array
7. HueAgent parameter added to AudioLoop
8. HueAgent instance assigned in AudioLoop.__init__

## ⏳ TODO - Add Hue Tool Handlers:

In `ada.py`, find the section where tool calls are handled (`if fc.name == "control_light":`) around line 1100-1200.

Add these two handlers AFTER the `control_light` handler and BEFORE `discover_printers`:

```python
elif fc.name == "list_hue_lights":
    print(f"[ADA DEBUG] [TOOL] Tool Call: 'list_hue_lights'")
    try:
        await self.hue_agent.get_lights()
        lights = self.hue_agent.lights
        
        # Format for model
        light_summaries = []
        for light_id, light_data in lights.items():
            name = light_data.get('name', f'Light {light_id}')
            state = light_data.get('state', {})
            on = state.get('on', False)
            bri = state.get('bri', 0)
            reachable = state.get('reachable', False)
            
            status = "ON" if on else "OFF"
            reach_status = "reachable" if reachable else "unreachable"
            
            light_summaries.append(f"{name} (ID: {light_id}): {status}, Brightness: {bri}/254, {reach_status}")
        
        result_str = f"Found {len(lights)} Hue lights:\n" + "\n".join(light_summaries) if light_summaries else "No Hue lights found."
        
        function_response = types.FunctionResponse(
            id=fc.id, name=fc.name, response={"result": result_str}
        )
        function_responses.append(function_response)
    except Exception as e:
        print(f"[ADA DEBUG] [ERR] list_hue_lights error: {e}")
        function_response = types.FunctionResponse(
            id=fc.id, name=fc.name, response={"result": f"Error listing Hue lights: {str(e)}"}
        )
        function_responses.append(function_response)

elif fc.name == "control_hue_light":
    light_name = fc.args["light_name"]
    action = fc.args["action"]
    brightness = fc.args.get("brightness")
    color = fc.args.get("color")
    
    print(f"[ADA DEBUG] [TOOL] Tool Call: 'control_hue_light' Light='{light_name}' Action='{action}'")
    
    try:
        # First, get lights to find the ID
        await self.hue_agent.get_lights()
        
        # Find light by name or ID
        light_id = None
        for lid, light_data in self.hue_agent.lights.items():
            if lid == light_name or light_data.get('name', '').lower() == light_name.lower():
                light_id = lid
                break
        
        if not light_id:
            result_msg = f"Light '{light_name}' not found. Available lights: {', '.join([f\"{l.get('name')} (ID: {lid})\" for lid, l in self.hue_agent.lights.items()])}"
        else:
            result_msg = f"Action '{action}' on light '{light_name}' failed."
            success = False
            
            if action == "turn_on":
                success = await self.hue_agent.turn_on(light_id)
                if success:
                    result_msg = f"Turned ON '{light_name}'."
            elif action == "turn_off":
                success = await self.hue_agent.turn_off(light_id)
                if success:
                    result_msg = f"Turned OFF '{light_name}'."
            elif action == "set_brightness":
                if brightness is not None:
                    # Convert 0-100 to 0-254
                    bri_value = int(brightness * 2.54)
                    success = await self.hue_agent.set_brightness(light_id, bri_value)
                    if success:
                        result_msg = f"Set brightness of '{light_name}' to {brightness}%."
                else:
                    result_msg = "Brightness value required for set_brightness action."
            elif action == "set_color":
                if color:
                    # Map color names to hue/sat values
                    color_map = {
                        "red": (0, 254),
                        "green": (21845, 254),
                        "blue": (43690, 254),
                        "yellow": (10922, 254),
                        "orange": (5461, 254),
                        "purple": (49151, 254),
                        "pink": (56100, 254),
                        "warm white": (8000, 200),
                        "cool white": (33000, 100),
                        "white": (33000, 0)
                    }
                    
                    hue_sat = color_map.get(color.lower())
                    if hue_sat:
                        success = await self.hue_agent.set_color(light_id, hue_sat[0], hue_sat[1])
                        if success:
                            result_msg = f"Set color of '{light_name}' to {color}."
                    else:
                        result_msg = f"Unknown color '{color}'. Available colors: {', '.join(color_map.keys())}"
                else:
                    result_msg = "Color name required for set_color action."
        
        function_response = types.FunctionResponse(
            id=fc.id, name=fc.name, response={"result": result_msg}
        )
        function_responses.append(function_response)
    except Exception as e:
        print(f"[ADA DEBUG] [ERR] control_hue_light error: {e}")
        function_response = types.FunctionResponse(
            id=fc.id, name=fc.name, response={"result": f"Error controlling Hue light: {str(e)}"}
        )
        function_responses.append(function_response)
```

## Then update server.py start_audio to pass hue_agent:

Find this section around line 300:
```python
audio_loop = ada.AudioLoop(
    video_mode="none",
    ...
    kasa_agent=kasa_agent,
```

Add after `kasa_agent=kasa_agent,`:
```python
    hue_agent=hue_agent,
```

## Test Commands:

Once integrated, you can say:
- "List my Hue lights"
- "Turn on the office lights"
- "Set bedroom to 50% brightness"
- "Make the living room blue"

This will complete the full voice control integration!
