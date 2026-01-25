import os
import httpx
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://xandria-eight.vercel.app/api/")

class XandriaAPI:
    def __init__(self):
        self.base_url = API_BASE_URL.rstrip('/')
        self.timeout = 10.0
    
    async def get_pnodes(self, network: str = "devnet") -> Optional[Dict]:
        """Fetch all pnodes for a given network"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/pnodes?network={network}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching pnodes for {network}: {str(e)}")
            return None
    
    async def get_node_info(self, pubkey: str) -> Optional[Dict]:
        """Fetch detailed info for a specific node"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/pnodes/{pubkey}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching node {pubkey}: {str(e)}")
            return None
    
    async def get_node_analytics(self, pubkey: str) -> Optional[Dict]:
        """Fetch analytics/history for a specific node"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/analytics/node/{pubkey}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching analytics for {pubkey}: {str(e)}")
            return None
    
    async def get_both_networks(self) -> Dict[str, Optional[Dict]]:
        """Fetch pnode data from both networks"""
        devnet = await self.get_pnodes("devnet")
        mainnet = await self.get_pnodes("mainnet")
        return {"devnet": devnet, "mainnet": mainnet}

xandria_api = XandriaAPI()