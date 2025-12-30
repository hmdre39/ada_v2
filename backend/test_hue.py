"""
Simple test script for Hue Bridge discovery
Run with: python test_hue.py
"""
import asyncio
import sys

# First check if aiohttp is installed
try:
    import aiohttp
    print("✓ aiohttp is installed")
except ImportError:
    print("✗ aiohttp is NOT installed")
    print("\nPlease install it with:")
    print("  pip install aiohttp")
    sys.exit(1)

from hue_agent import HueAgent

async def test_discovery():
    print("=" * 50)
    print("HUE BRIDGE DISCOVERY TEST")
    print("=" * 50)
    
    hue = HueAgent()
    
    # Try discovery
    print("\n1. Attempting to discover Hue Bridge...")
    bridge_ip = await hue.discover_bridge("192.168.86.0/24")
    
    if not bridge_ip:
        print("\n✗ No Hue Bridge found automatically")
        print("\nManual options:")
        print("1. Make sure your Hue Bridge is powered on")
        print("2. Make sure it's connected to 192.168.86.x network")
        print("3. Try entering the bridge IP manually:")
        manual_ip = input("\nEnter Hue Bridge IP (or press Enter to skip): ").strip()
        if manual_ip:
            hue.bridge_ip = manual_ip
            print(f"✓ Using manual IP: {manual_ip}")
        else:
            print("Exiting...")
            return
    else:
        print(f"\n✓ Found Hue Bridge at: {bridge_ip}")
    
    # Try to register
    print("\n2. Attempting to register with bridge...")
    print("   → Please press the BUTTON on your Hue Bridge NOW")
    print("   → You have 30 seconds...")
    
    await asyncio.sleep(2)  # Give user time to read
    
    success = await hue.register()
    
    if not success:
        print("\n✗ Registration failed!")
        print("   Did you press the button on the bridge?")
        
        # Try one more time
        print("\nTrying again... Press the button NOW:")
        await asyncio.sleep(3)
        success = await hue.register()
        
        if not success:
            print("✗ Still failed. Exiting...")
            return
    
    print(f"\n✓ Registration successful!")
    print(f"   Username: {hue.username}")
    print(f"\nSave these for Ada integration:")
    print(f"   Bridge IP: {hue.bridge_ip}")
    print(f"   Username: {hue.username}")
    
    # Get lights
    print("\n3. Getting lights...")
    await hue.get_lights()
    
    if hue.lights:
        print(f"\n✓ Found {len(hue.lights)} lights:")
        for light_id, light in hue.lights.items():
            name = light.get('name', 'Unknown')
            state = light.get('state', {})
            on = state.get('on', False)
            bri = state.get('bri', 0)
            reachable = state.get('reachable', False)
            
            status = "ON" if on else "OFF"
            reach_status = "✓" if reachable else "✗"
            
            print(f"   [{light_id}] {name}: {status} (brightness: {bri}) {reach_status}")
    else:
        print("✗ No lights found")

if __name__ == "__main__":
    try:
        # Check if IP was provided as command line argument
        if len(sys.argv) > 1:
            manual_ip = sys.argv[1]
            print(f"Using provided IP: {manual_ip}")
            
            async def test_with_ip():
                hue = HueAgent(bridge_ip=manual_ip)
                
                # Skip discovery, go straight to registration
                print("\n2. Attempting to register with bridge...")
                print("   → Please press the BUTTON on your Hue Bridge NOW")
                print("   → You have 30 seconds...")
                
                await asyncio.sleep(2)
                success = await hue.register()
                
                if not success:
                    print("\n✗ Registration failed!")
                    print("   Did you press the button on the bridge?")
                    print("\nTrying again... Press the button NOW:")
                    await asyncio.sleep(3)
                    success = await hue.register()
                    
                    if not success:
                        print("✗ Still failed. Exiting...")
                        return
                
                print(f"\n✓ Registration successful!")
                print(f"   Username: {hue.username}")
                print(f"\nSave these for Ada integration:")
                print(f"   Bridge IP: {hue.bridge_ip}")
                print(f"   Username: {hue.username}")
                
                # Get lights
                print("\n3. Getting lights...")
                await hue.get_lights()
                
                if hue.lights:
                    print(f"\n✓ Found {len(hue.lights)} lights:")
                    for light_id, light in hue.lights.items():
                        name = light.get('name', 'Unknown')
                        state = light.get('state', {})
                        on = state.get('on', False)
                        bri = state.get('bri', 0)
                        reachable = state.get('reachable', False)
                        
                        status = "ON" if on else "OFF"
                        reach_status = "✓" if reachable else "✗"
                        
                        print(f"   [{light_id}] {name}: {status} (brightness: {bri}) {reach_status}")
                else:
                    print("✗ No lights found")
            
            asyncio.run(test_with_ip())
        else:
            asyncio.run(test_discovery())
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
