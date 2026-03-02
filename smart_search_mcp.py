"""
Smart Search MCP Server for Employee Lookup Agent
=================================================
This MCP server provides intelligent search capabilities similar to Perplexity,
allowing Gemini to search through employees, assets, policies, and provide contextual suggestions.
"""

import json
import re
from typing import List, Dict, Any
from fuzzywuzzy import fuzz
import pandas as pd
from mcp.server import Server
from mcp.types import Tool
import asyncio

class SmartSearchMCP:
    def __init__(self, employee_data_path: str = "Employee_Data.csv", 
                 policy_path: str = "asset_purchase_policy.json"):
        """Initialize the Smart Search MCP with data sources"""
        
        # Load employee data
        self.employees_df = pd.read_csv(employee_data_path)
        self.employees = self.employees_df.to_dict('records')
        
        # Load policy data
        with open(policy_path, 'r') as f:
            self.policy_data = json.load(f)
        
        # Asset database with product links (expandable)
        self.assets_db = {
            "laptops": [
                {"name": "MacBook Pro 16-inch", "category": "laptop", "price": 2999, "specs": "M3 Max, 32GB RAM, 1TB SSD", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.apple.com/macbook-pro/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "MacBook Pro 14-inch", "category": "laptop", "price": 2399, "specs": "M3 Pro, 16GB RAM, 512GB SSD", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.apple.com/macbook-pro/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "MacBook Air 15-inch", "category": "laptop", "price": 1699, "specs": "M3, 16GB RAM, 512GB SSD", "suitable_for": ["IC", "Senior IC"], "url": "https://www.apple.com/macbook-air/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "MacBook Air 13-inch", "category": "laptop", "price": 1299, "specs": "M3, 8GB RAM, 256GB SSD", "suitable_for": ["IC"], "url": "https://www.apple.com/macbook-air/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "ThinkPad X1 Carbon", "category": "laptop", "price": 1899, "specs": "Intel i7, 16GB RAM, 512GB SSD", "suitable_for": ["IC", "Senior IC"], "url": "https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadx1/thinkpad-x1-carbon-gen-12", "vendor": "Lenovo", "availability": "In Stock"},
                {"name": "Dell XPS 15", "category": "laptop", "price": 2199, "specs": "Intel i9, 32GB RAM, 1TB SSD", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.dell.com/en-us/shop/dell-laptops/xps-15-laptop/spd/xps-15-9530-laptop", "vendor": "Dell", "availability": "In Stock"},
            ],
            "cars": [
                {"name": "Tesla Model 3", "category": "car", "price": 38990, "specs": "Long Range, Autopilot", "suitable_for": ["Manager"], "url": "https://www.tesla.com/model3/", "vendor": "Tesla", "availability": "Available"},
                {"name": "Toyota Camry Hybrid", "category": "car", "price": 32950, "specs": "Hybrid, Fuel Efficient", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.toyota.com/camry/", "vendor": "Toyota", "availability": "Available"},
                {"name": "Honda Accord", "category": "car", "price": 28500, "specs": "Reliable, Good MPG", "suitable_for": ["Senior IC", "Manager"], "url": "https://automobiles.honda.com/accord", "vendor": "Honda", "availability": "Available"},
                {"name": "BMW 3 Series", "category": "car", "price": 45900, "specs": "Luxury, Performance", "suitable_for": ["Manager"], "url": "https://www.bmwusa.com/vehicles/3-series/sedan/overview.html", "vendor": "BMW", "availability": "Available"},
            ],
            "accessories": [
                {"name": "iPad Pro 12.9", "category": "tablet", "price": 1299, "specs": "M2 chip, 128GB", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.apple.com/ipad-pro/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "Apple Studio Display", "category": "monitor", "price": 1599, "specs": "27-inch 5K Retina", "suitable_for": ["Senior IC", "Manager"], "url": "https://www.apple.com/studio-display/", "vendor": "Apple", "availability": "In Stock"},
                {"name": "Dell UltraSharp Monitor", "category": "monitor", "price": 899, "specs": "32-inch 4K USB-C", "suitable_for": ["IC", "Senior IC"], "url": "https://www.dell.com/en-us/shop/dell-32-4k-usb-c-hub-monitor-s3221qs/apd/210-axcu", "vendor": "Dell", "availability": "In Stock"},
                {"name": "Logitech MX Master 3S", "category": "mouse", "price": 99, "specs": "Wireless, Ergonomic", "suitable_for": ["IC", "Senior IC", "Manager"], "url": "https://www.logitech.com/en-us/products/mice/mx-master-3s.910-006556.html", "vendor": "Logitech", "availability": "In Stock"},
                {"name": "Apple Magic Keyboard", "category": "keyboard", "price": 179, "specs": "Wireless, Touch ID", "suitable_for": ["IC", "Senior IC", "Manager"], "url": "https://www.apple.com/shop/product/MK2A3LL/A/magic-keyboard-us-english", "vendor": "Apple", "availability": "In Stock"},
            ]
        }
        
        # Flatten assets for easier searching
        self.all_assets = []
        for category, items in self.assets_db.items():
            self.all_assets.extend(items)
    
    def search_employees(self, query: str, limit: int = 10) -> List[Dict]:
        """Smart employee search with fuzzy matching"""
        results = []
        query_lower = query.lower()
        
        for emp in self.employees:
            scores = []
            
            # Search in different fields
            fields_to_search = [
                ('name', emp['name']),
                ('email', emp['email_id']),
                ('department', emp['department']),
                ('designation', emp['designation']),
                ('level', emp['employee_level']),
                ('id', emp['employee_id'])
            ]
            
            for field_name, field_value in fields_to_search:
                if field_value:
                    score = fuzz.partial_ratio(query_lower, str(field_value).lower())
                    if score > 60:  # Minimum threshold
                        scores.append({
                            'score': score,
                            'field': field_name,
                            'match': field_value
                        })
            
            if scores:
                best_match = max(scores, key=lambda x: x['score'])
                results.append({
                    'employee': emp,
                    'relevance_score': best_match['score'],
                    'matched_field': best_match['field'],
                    'matched_value': best_match['match']
                })
        
        # Sort by relevance and limit results
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:limit]
    
    def search_assets(self, query: str, employee_level: str = None, budget_limit: float = None) -> List[Dict]:
        """Search assets with contextual filtering"""
        results = []
        query_lower = query.lower()
        
        for asset in self.all_assets:
            # Calculate relevance score
            name_score = fuzz.partial_ratio(query_lower, asset['name'].lower())
            category_score = fuzz.partial_ratio(query_lower, asset['category'].lower())
            specs_score = fuzz.partial_ratio(query_lower, asset['specs'].lower())
            
            max_score = max(name_score, category_score, specs_score)
            
            # Filter by budget if provided
            if budget_limit and asset['price'] > budget_limit:
                continue
            
            # Filter by employee level if provided
            if employee_level and employee_level not in asset['suitable_for']:
                max_score = max_score * 0.7  # Reduce score but don't eliminate
            
            if max_score > 50:  # Minimum threshold
                results.append({
                    'asset': asset,
                    'relevance_score': max_score,
                    'affordable': budget_limit is None or asset['price'] <= budget_limit,
                    'level_appropriate': employee_level is None or employee_level in asset['suitable_for']
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
    
    def get_purchase_suggestions(self, employee_email: str, query: str = "") -> Dict:
        """Get personalized purchase suggestions for an employee"""
        
        # Find employee
        employee = None
        for emp in self.employees:
            if emp['email_id'].lower() == employee_email.lower():
                employee = emp
                break
        
        if not employee:
            return {"error": "Employee not found"}
        
        # Get employee's policy
        level = employee['employee_level']
        policy = self.policy_data.get('policy_rules', {}).get(level, {})
        budget_limit = policy.get('purchase_limit', 0)
        
        # Search assets based on query and employee context
        asset_results = self.search_assets(query, level, budget_limit)
        
        # Generate contextual suggestions
        suggestions = {
            'employee': employee,
            'budget_limit': budget_limit,
            'currency': policy.get('currency', 'USD'),
            'matching_assets': asset_results[:10],
            'recommendations': self._generate_recommendations(employee, asset_results),
            'budget_breakdown': self._calculate_budget_breakdown(asset_results, budget_limit)
        }
        
        return suggestions
    
    def _generate_recommendations(self, employee: Dict, asset_results: List[Dict]) -> List[str]:
        """Generate smart recommendations based on employee and assets"""
        recommendations = []
        level = employee['employee_level']
        department = employee['department']
        
        # Role-based recommendations
        if department == 'IT' or department == 'Engineering':
            recommendations.append("💻 Consider high-performance laptops for development work")
            recommendations.append("🖥️ External monitors can boost productivity")
        
        if level == 'Manager':
            recommendations.append("🚗 Company car options available for your level")
            recommendations.append("📱 Premium devices for client meetings")
        
        # Budget-based recommendations
        affordable_assets = [r for r in asset_results if r['affordable']]
        if affordable_assets:
            recommendations.append(f"✅ {len(affordable_assets)} items within your budget")
        
        over_budget = [r for r in asset_results if not r['affordable']]
        if over_budget:
            recommendations.append(f"⚠️ {len(over_budget)} items require manager approval")
        
        return recommendations
    
    def _calculate_budget_breakdown(self, asset_results: List[Dict], budget_limit: float) -> Dict:
        """Calculate budget utilization breakdown"""
        affordable = [r for r in asset_results if r['affordable']]
        over_budget = [r for r in asset_results if not r['affordable']]
        
        return {
            'total_budget': budget_limit,
            'affordable_count': len(affordable),
            'over_budget_count': len(over_budget),
            'cheapest_option': min([r['asset']['price'] for r in asset_results]) if asset_results else 0,
            'most_expensive': max([r['asset']['price'] for r in asset_results]) if asset_results else 0,
            'average_price': sum([r['asset']['price'] for r in asset_results]) / len(asset_results) if asset_results else 0
        }
    
    def smart_query_understanding(self, query: str) -> Dict:
        """Understand user intent and provide comprehensive response"""
        query_lower = query.lower()
        
        # Detect query type
        query_types = {
            'employee_search': ['employee', 'person', 'who is', 'find user', '@'],
            'asset_search': ['laptop', 'macbook', 'car', 'device', 'equipment', 'buy', 'purchase'],
            'budget_query': ['budget', 'limit', 'spend', 'cost', 'price', 'how much'],
            'policy_query': ['policy', 'rules', 'allowed', 'can i', 'eligible'],
            'comparison': ['vs', 'versus', 'compare', 'difference', 'better'],
            'recommendation': ['suggest', 'recommend', 'best', 'should i', 'what']
        }
        
        detected_types = []
        for query_type, keywords in query_types.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_types.append(query_type)
        
        # Extract entities
        entities = {
            'employee_mentioned': self._extract_employee_mentions(query),
            'assets_mentioned': self._extract_asset_mentions(query),
            'departments_mentioned': self._extract_department_mentions(query),
            'levels_mentioned': self._extract_level_mentions(query)
        }
        
        return {
            'query': query,
            'detected_types': detected_types,
            'entities': entities,
            'confidence': len(detected_types) / len(query_types),
            'suggested_searches': self._generate_search_suggestions(detected_types, entities)
        }
    
    def _extract_employee_mentions(self, query: str) -> List[str]:
        """Extract employee names or emails from query"""
        mentions = []
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, query)
        mentions.extend(emails)
        
        # Name pattern (fuzzy match against employee names)
        for emp in self.employees:
            name_parts = emp['name'].lower().split()
            for part in name_parts:
                if len(part) > 2 and part in query.lower():
                    mentions.append(emp['name'])
                    break
        
        return list(set(mentions))
    
    def _extract_asset_mentions(self, query: str) -> List[str]:
        """Extract asset names from query"""
        mentions = []
        query_lower = query.lower()
        
        for asset in self.all_assets:
            asset_name_lower = asset['name'].lower()
            if asset_name_lower in query_lower or fuzz.partial_ratio(query_lower, asset_name_lower) > 80:
                mentions.append(asset['name'])
        
        return list(set(mentions))
    
    def _extract_department_mentions(self, query: str) -> List[str]:
        """Extract department names from query"""
        departments = list(set(emp['department'] for emp in self.employees))
        mentions = []
        
        for dept in departments:
            if dept.lower() in query.lower():
                mentions.append(dept)
        
        return mentions
    
    def _extract_level_mentions(self, query: str) -> List[str]:
        """Extract employee levels from query"""
        levels = list(set(emp['employee_level'] for emp in self.employees))
        mentions = []
        
        for level in levels:
            if level.lower() in query.lower():
                mentions.append(level)
        
        return mentions
    
    def _generate_search_suggestions(self, detected_types: List[str], entities: Dict) -> List[str]:
        """Generate helpful search suggestions"""
        suggestions = []
        
        if 'employee_search' in detected_types:
            suggestions.extend([
                "🔍 Try: 'john.doe@abc-company.com'",
                "🏢 Try: 'IT department employees'",
                "👨‍💼 Try: 'all managers'"
            ])
        
        if 'asset_search' in detected_types:
            suggestions.extend([
                "💻 Try: 'MacBook Pro for developers'",
                "🚗 Try: 'company cars under $40k'",
                "📱 Try: 'tablets for presentations'"
            ])
        
        if 'budget_query' in detected_types:
            suggestions.extend([
                "💰 Try: 'budget for Senior IC'",
                "📊 Try: 'spending limits by department'"
            ])
        
        if not suggestions:
            suggestions = [
                "💡 Try searching for employees: 'John Doe'",
                "🛒 Try searching for assets: 'MacBook'",
                "📈 Try asking about budgets: 'Manager spending limit'"
            ]
        
        return suggestions[:5]  # Limit to 5 suggestions


# MCP Server Setup
app = Server("smart-search-mcp")
search_engine = SmartSearchMCP()

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available search tools"""
    return [
        Tool(
            name="search_employees",
            description="Search for employees by name, email, department, or role",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 10, "description": "Max results"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_assets",
            description="Search for company assets (laptops, cars, etc.) with budget filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Asset search query"},
                    "employee_level": {"type": "string", "description": "Employee level for filtering"},
                    "budget_limit": {"type": "number", "description": "Budget limit for filtering"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_purchase_suggestions",
            description="Get personalized purchase suggestions for an employee",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_email": {"type": "string", "description": "Employee email"},
                    "query": {"type": "string", "description": "What they're looking for"}
                },
                "required": ["employee_email"]
            }
        ),
        Tool(
            name="smart_query_understanding",
            description="Understand user intent and provide comprehensive search guidance",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "User's natural language query"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Handle tool calls"""
    
    if name == "search_employees":
        results = search_engine.search_employees(
            arguments["query"], 
            arguments.get("limit", 10)
        )
        return [{"type": "text", "text": json.dumps(results, indent=2)}]
    
    elif name == "search_assets":
        results = search_engine.search_assets(
            arguments["query"],
            arguments.get("employee_level"),
            arguments.get("budget_limit")
        )
        return [{"type": "text", "text": json.dumps(results, indent=2)}]
    
    elif name == "get_purchase_suggestions":
        results = search_engine.get_purchase_suggestions(
            arguments["employee_email"],
            arguments.get("query", "")
        )
        return [{"type": "text", "text": json.dumps(results, indent=2)}]
    
    elif name == "smart_query_understanding":
        results = search_engine.smart_query_understanding(arguments["query"])
        return [{"type": "text", "text": json.dumps(results, indent=2)}]
    
    else:
        return [{"type": "text", "text": f"Unknown tool: {name}"}]

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())