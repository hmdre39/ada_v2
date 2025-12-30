import asyncio
import aiohttp
from typing import Dict, List, Optional

class HueAgent:
    """Agent for controlling Philips Hue lights via the Hue Bridge."""
    
    def __init__(self, bridge_ip: Optional[str] = None, username: Optional[str] = None):
        self.bridge_ip = bridge_ip
        self.username = username
        self.lights = {}
        self.groups = {}
        
    async def discover_bridge(self, network: str = "192.168.86.0/24") -> Optional[str]:
        """Discover Hue Bridge on the network using SSDP or N-UPnP."""
        print(f"[HueAgent] Discovering Hue Bridge on {network}...")
        
        # Method 1: Use Philips N-UPnP discovery service
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://discovery.meethue.com/") as resp:
                    if resp.status == 200:
                        bridges = await resp.json()
                        if bridges:
                            self.bridge_ip = bridges[0]["internalipaddress"]
                            print(f"[HueAgent] Found bridge at {self.bridge_ip}")
                            return self.bridge_ip
        except Exception as e:
            print(f"[HueAgent] N-UPnP discovery failed: {e}")
        
        # Method 2: Manual scan of subnet (fallback)
        if not self.bridge_ip:
            print(f"[HueAgent] Scanning {network} for Hue Bridge...")
            # Parse network CIDR
            import ipaddress
            net = ipaddress.ip_network(network, strict=False)
            
            # Scan common Hue bridge ports
            for ip in net.hosts():
                ip_str = str(ip)
                if await self._test_hue_bridge(ip_str):
                    self.bridge_ip = ip_str
                    print(f"[HueAgent] Found bridge at {self.bridge_ip}")
                    return self.bridge_ip
        
        print("[HueAgent] No Hue Bridge found")
        return None
    
    async def _test_hue_bridge(self, ip: str) -> bool:
        """Test if an IP is a Hue Bridge."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
                async with session.get(f"http://{ip}/api/config") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return "bridgeid" in data or "name" in data
        except:
            pass
        return False
    
    async def register(self) -> bool:
        """Register with the Hue Bridge to get a username (API key)."""
        if not self.bridge_ip:
            print("[HueAgent] No bridge IP set")
            return False
        
        print("[HueAgent] Initiating registration - user should press bridge button within 30s...")
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"devicetype": "ada_jarvis#user"}
                async with session.post(f"http://{self.bridge_ip}/api", json=payload) as resp:
                    result = await resp.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        if "success" in result[0]:
                            self.username = result[0]["success"]["username"]
                            print(f"[HueAgent] Registration successful! Username: {self.username}")
                            return True
                        elif "error" in result[0]:
                            error = result[0]["error"]
                            print(f"[HueAgent] Registration failed: {error.get('description')}")
        except Exception as e:
            print(f"[HueAgent] Registration error: {e}")
        
        return False
    
    async def get_lights(self) -> Dict:
        """Get all lights from the bridge."""
        if not self.bridge_ip or not self.username:
            print("[HueAgent] Not connected to bridge")
            return {}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{self.bridge_ip}/api/{self.username}/lights") as resp:
                    if resp.status == 200:
                        self.lights = await resp.json()
                        print(f"[HueAgent] Found {len(self.lights)} lights")
                        return self.lights
        except Exception as e:
            print(f"[HueAgent] Error getting lights: {e}")
        
        return {}
    
    async def turn_on(self, light_id: str) -> bool:
        """Turn on a light."""
        return await self._set_light_state(light_id, {"on": True})
    
    async def turn_off(self, light_id: str) -> bool:
        """Turn off a light."""
        return await self._set_light_state(light_id, {"on": False})
    
    async def set_brightness(self, light_id: str, brightness: int) -> bool:
        """Set brightness (0-254)."""
        # Convert 0-100 to 0-254 if needed
        if brightness <= 100:
            brightness = int(brightness * 2.54)
        return await self._set_light_state(light_id, {"bri": brightness})
    
    async def set_color(self, light_id: str, hue: int, sat: int) -> bool:
        """Set color using hue (0-65535) and saturation (0-254)."""
        return await self._set_light_state(light_id, {"hue": hue, "sat": sat})
    
    async def set_color_temp(self, light_id: str, ct: int) -> bool:
        """Set color temperature (153-500 mireds)."""
        return await self._set_light_state(light_id, {"ct": ct})
    
    async def _set_light_state(self, light_id: str, state: Dict) -> bool:
        """Internal method to set light state."""
        if not self.bridge_ip or not self.username:
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://{self.bridge_ip}/api/{self.username}/lights/{light_id}/state"
                async with session.put(url, json=state) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        # Check if all commands succeeded
                        success = all("success" in item for item in result if isinstance(result, list))
                        return success or resp.status == 200
        except Exception as e:
            print(f"[HueAgent] Error setting light state: {e}")
        
        return False
    
    def format_lights_for_frontend(self) -> List[Dict]:
        """Format lights for frontend display."""
        formatted = []
        for light_id, light_data in self.lights.items():
            formatted.append({
                "id": light_id,
                "name": light_data.get("name", f"Light {light_id}"),
                "type": light_data.get("type", "unknown"),
                "model": light_data.get("modelid", "unknown"),
                "manufacturer": light_data.get("manufacturername", "Philips"),
                "state": {
                    "on": light_data.get("state", {}).get("on", False),
                    "brightness": light_data.get("state", {}).get("bri", 0),
                    "hue": light_data.get("state", {}).get("hue"),
                    "sat": light_data.get("state", {}).get("sat"),
                    "ct": light_data.get("state", {}).get("ct"),
                    "reachable": light_data.get("state", {}).get("reachable", False)
                }
            })
        return formatted
