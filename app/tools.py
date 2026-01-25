import re
from typing import Dict, Optional, List
from xandria_pnodes_apis import xandria_api

class NetworkTools:
    """
    Analyzes user queries and fetches relevant network data when needed.
    Called before RAG search to provide live context.
    """
    
    def __init__(self):
        self.network_keywords = [
            'pnode', 'node', 'validator', 'network', 'devnet', 'mainnet',
            'storage', 'uptime', 'score', 'status', 'active', 'offline',
            'performance', 'analytics', 'metrics', 'stats'
        ]
        self.pubkey_pattern = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{43,44}\b')
    
    def should_fetch_network_data(self, query: str) -> bool:
        """Determine if query needs live network data"""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.network_keywords)
    
    def extract_pubkey(self, query: str) -> Optional[str]:
        """Extract node pubkey from query if present"""
        match = self.pubkey_pattern.search(query)
        return match.group(0) if match else None
    
    def extract_network(self, query: str) -> str:
        """Determine which network user is asking about"""
        query_lower = query.lower()
        if 'mainnet' in query_lower:
            return 'mainnet'
        return 'devnet'
    
    async def fetch_relevant_data(self, query: str) -> Dict:
        """
        Main method: analyzes query and fetches appropriate network data
        Returns dict with fetched data and metadata
        """
        result = {
            "fetched": False,
            "data": {},
            "context": ""
        }
        
        if not self.should_fetch_network_data(query):
            return result
        
        pubkey = self.extract_pubkey(query)
        
        if pubkey:
            node_info = await xandria_api.get_node_info(pubkey)
            if node_info and node_info.get('success'):
                result['fetched'] = True
                result['data']['node_info'] = node_info['data']
                result['context'] = self._format_node_context(node_info['data'])
            
            query_lower = query.lower()
            if any(word in query_lower for word in ['analytics', 'history', 'metrics', 'performance']):
                analytics = await xandria_api.get_node_analytics(pubkey)
                if analytics and analytics.get('success'):
                    result['data']['analytics'] = analytics['data']
                    result['context'] += "\n\n" + self._format_analytics_context(analytics['data'])
        
        else:
            query_lower = query.lower()
            if 'both' in query_lower or ('devnet' in query_lower and 'mainnet' in query_lower):
                networks = await xandria_api.get_both_networks()
                result['fetched'] = True
                result['data']['networks'] = networks
                result['context'] = self._format_networks_context(networks)
            else:
                network = self.extract_network(query)
                pnodes = await xandria_api.get_pnodes(network)
                if pnodes and pnodes.get('success'):
                    result['fetched'] = True
                    result['data'][f'{network}_pnodes'] = pnodes
                    result['context'] = self._format_pnodes_context(pnodes, network)
        
        return result
    
    def _format_node_context(self, node_data: Dict) -> str:
        """Format single node data for AI context"""
        return f"""Current Node Status:
Pubkey: {node_data.get('pubkey', 'N/A')}
Status: {node_data.get('status', 'unknown')}
Version: {node_data.get('version', 'N/A')}
Score: {node_data.get('score', 'N/A')}
Uptime: {node_data.get('uptime', 0)} seconds
Storage Committed: {node_data.get('storageCommitted', 0)} bytes
Storage Used: {node_data.get('storageUsed', 0)} bytes ({node_data.get('storageUsagePercent', 0):.4f}%)
Last Seen: {node_data.get('lastSeen', 'N/A')}
Grade: {node_data.get('scoreBreakdown', {}).get('grade', 'N/A')}
"""
    
    def _format_analytics_context(self, analytics_data: Dict) -> str:
        """Format analytics data for AI context"""
        stats = analytics_data.get('stats', {})
        metrics = stats.get('metrics', {})
        
        return f"""Node Analytics Summary:
Data Points: {stats.get('dataPoints', 0)}
Current Uptime: {metrics.get('uptime', {}).get('current', 'N/A')} seconds
Current Score: {metrics.get('score', {}).get('current', 'N/A')}
Score Range: {metrics.get('score', {}).get('min', 'N/A')} - {metrics.get('score', {}).get('max', 'N/A')}
"""
    
    def _format_pnodes_context(self, pnodes_data: Dict, network: str) -> str:
        """Format network pnodes list for AI context"""
        stats = pnodes_data.get('stats', {})
        return f"""Network Overview ({network.upper()}):
Total Nodes: {stats.get('total', 0)}
Active: {stats.get('active', 0)}
Syncing: {stats.get('syncing', 0)}
Offline: {stats.get('offline', 0)}
Average Score: {stats.get('avgScore', 0):.2f}
Total Storage: {stats.get('totalStorage', 0)} bytes
Used Storage: {stats.get('usedStorage', 0)} bytes
"""
    
    def _format_networks_context(self, networks_data: Dict) -> str:
        """Format both networks data for AI context"""
        contexts = []
        for network, data in networks_data.items():
            if data and data.get('success'):
                contexts.append(self._format_pnodes_context(data, network))
        return "\n\n".join(contexts)

network_tools = NetworkTools()