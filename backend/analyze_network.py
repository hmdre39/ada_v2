"""
Network diagnostic tool - identify your network setup
"""
import subprocess
import re

def get_network_info():
    print("=" * 60)
    print("NETWORK CONFIGURATION ANALYZER")
    print("=" * 60)
    
    try:
        # Run ipconfig
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
        output = result.stdout
        
        print("\nActive Network Adapters:\n")
        
        # Parse each adapter
        adapters = []
        current_adapter = None
        
        for line in output.split('\n'):
            # New adapter section
            if 'adapter' in line.lower() and ':' in line:
                if current_adapter:
                    adapters.append(current_adapter)
                current_adapter = {'name': line.strip(), 'ip': None, 'gateway': None, 'subnet': None}
            
            # IPv4 Address
            elif current_adapter and 'IPv4 Address' in line:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    current_adapter['ip'] = match.group(1)
            
            # Default Gateway
            elif current_adapter and 'Default Gateway' in line:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    current_adapter['gateway'] = match.group(1)
            
            # Subnet Mask
            elif current_adapter and 'Subnet Mask' in line:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    current_adapter['subnet'] = match.group(1)
        
        if current_adapter:
            adapters.append(current_adapter)
        
        # Filter and display active adapters with IP addresses
        active_adapters = [a for a in adapters if a.get('ip') and not a['ip'].startswith('169.254')]
        
        if not active_adapters:
            print("No active network adapters found!")
            return
        
        for i, adapter in enumerate(active_adapters, 1):
            print(f"{i}. {adapter['name']}")
            print(f"   IP Address:      {adapter.get('ip', 'N/A')}")
            print(f"   Default Gateway: {adapter.get('gateway', 'N/A')}")
            print(f"   Subnet Mask:     {adapter.get('subnet', 'N/A')}")
            print()
        
        # Identify which network can reach Hue
        print("=" * 60)
        print("ANALYSIS:")
        print("=" * 60)
        
        can_reach_192_1 = any(a.get('ip', '').startswith('192.168.1.') for a in active_adapters)
        can_reach_192_86 = any(a.get('ip', '').startswith('192.168.86.') for a in active_adapters)
        
        print(f"\n✓ Your PC is on network: {[a['ip'] for a in active_adapters if a.get('ip')]}")
        print(f"✓ Hue Bridge is on: 192.168.86.68")
        
        if can_reach_192_86:
            print("\n✓ Your PC is ALREADY on the same network as Hue!")
            print("  The connection issue might be something else.")
        elif can_reach_192_1:
            print("\n✗ Your PC is on 192.168.1.x network")
            print("✗ Hue Bridge is on 192.168.86.x network")
            print("\nYou need to set up routing. Here's how:")
            
            # Find the gateway
            gateway = next((a['gateway'] for a in active_adapters if a.get('gateway')), None)
            
            if gateway:
                print(f"\n1. Open your router admin page:")
                print(f"   → Open browser and go to: http://{gateway}")
                print(f"   → Login (usually admin/admin or check router label)")
                
                print(f"\n2. Look for one of these settings:")
                print(f"   - 'Static Routes' or 'Routing Table'")
                print(f"   - 'Advanced Routing'")
                print(f"   - 'LAN Settings' → 'Static Routes'")
                
                print(f"\n3. Add a static route:")
                print(f"   Destination Network: 192.168.86.0")
                print(f"   Subnet Mask:         255.255.255.0")
                print(f"   Gateway:             {gateway}")
                print(f"   Interface:           LAN")
                
                print(f"\n4. OR try adding from Windows command line:")
                print(f"   Open PowerShell as Administrator and run:")
                print(f"   route ADD 192.168.86.0 MASK 255.255.255.0 {gateway}")
        else:
            print("\n? Unknown network configuration")
            print("  Please check your network settings")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error analyzing network: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_network_info()
