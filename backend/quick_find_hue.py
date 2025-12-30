"""
Fast Hue Bridge finder - checks common IPs first
"""
import asyncio
import aiohttp

async def quick_find_bridge():
    print("Quick scanning common IPs on 192.168.86.x...")
    
    # Common router DHCP ranges
    common_ranges = [
        range(2, 50),    # 192.168.86.2-49 (common DHCP start)
        range(100, 150), # 192.168.86.100-149 (common static range)
    ]
    
    async def check_ip(ip):
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1)) as session:
                async with session.get(f"http://192.168.86.{ip}/api/config") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "bridgeid" in data or "name" in data:
                            return f"192.168.86.{ip}"
        except:
            pass
        return None
    
    # Check all common IPs in parallel
    tasks = []
    for ip_range in common_ranges:
        for ip in ip_range:
            tasks.append(check_ip(ip))
            print(f"Checking 192.168.86.{ip}...", end='\r')
    
    results = await asyncio.gather(*tasks)
    found = [r for r in results if r]
    
    if found:
        print(f"\n✓ Found Hue Bridge at: {found[0]}")
        return found[0]
    else:
        print("\n✗ No bridge found in common IP ranges")
        return None

if __name__ == "__main__":
    bridge = asyncio.run(quick_find_bridge())
    if bridge:
        print(f"\nUse this IP: {bridge}")
        print(f"\nNow run: python test_hue.py")
        print(f"And when it asks, enter: {bridge}")
