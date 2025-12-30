"""
Test basic network connectivity to Hue Bridge
"""
import socket
import requests

def test_connection(ip):
    print(f"Testing connection to {ip}...")
    print("=" * 50)
    
    # Test 1: Ping check (ICMP)
    print(f"\n1. Testing if {ip} is reachable...")
    import subprocess
    try:
        result = subprocess.run(
            ["ping", "-n", "1", ip] if __import__('sys').platform == 'win32' else ["ping", "-c", "1", ip],
            capture_output=True,
            timeout=3
        )
        if result.returncode == 0:
            print(f"   ✓ {ip} is reachable (ping successful)")
        else:
            print(f"   ✗ {ip} did not respond to ping")
            print("   This might be normal if the device blocks ping")
    except Exception as e:
        print(f"   ✗ Ping test failed: {e}")
    
    # Test 2: HTTP connection
    print(f"\n2. Testing HTTP connection to {ip}:80...")
    try:
        response = requests.get(f"http://{ip}/api/config", timeout=5)
        print(f"   ✓ HTTP connection successful!")
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Bridge ID: {data.get('bridgeid', 'unknown')}")
            print(f"   Name: {data.get('name', 'unknown')}")
            print(f"   API Version: {data.get('apiversion', 'unknown')}")
            print(f"\n   ✓ This IS a Hue Bridge!")
            return True
        else:
            print(f"   ✗ Unexpected response")
            
    except requests.exceptions.Timeout:
        print(f"   ✗ Connection timed out")
        print(f"   The IP might be wrong or the device is unreachable")
    except requests.exceptions.ConnectionError as e:
        print(f"   ✗ Connection refused or failed")
        print(f"   Error: {e}")
    except Exception as e:
        print(f"   ✗ HTTP test failed: {e}")
    
    # Test 3: Port check
    print(f"\n3. Testing if port 80 is open on {ip}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        result = sock.connect_ex((ip, 80))
        if result == 0:
            print(f"   ✓ Port 80 is open")
        else:
            print(f"   ✗ Port 80 is closed or filtered")
    except Exception as e:
        print(f"   ✗ Port test failed: {e}")
    finally:
        sock.close()
    
    return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_connection.py <IP>")
        print("Example: python test_connection.py 192.168.86.68")
        sys.exit(1)
    
    ip = sys.argv[1]
    
    success = test_connection(ip)
    
    if success:
        print("\n" + "=" * 50)
        print("✓ Connection test PASSED")
        print("You can now run: python test_hue.py " + ip)
    else:
        print("\n" + "=" * 50)
        print("✗ Connection test FAILED")
        print("\nTroubleshooting:")
        print("1. Verify the IP address is correct")
        print("2. Make sure your PC and Hue Bridge are on the same network")
        print("3. Check if there's a firewall blocking port 80")
        print("4. Try finding the bridge IP in your router's device list")
