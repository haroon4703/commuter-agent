from typing import Dict, Any, List, Optional, Tuple
import random
import re
import googlemaps
from config import Config
from utils import logger

class CommuterAgentLogic:
    def __init__(self):
        """Initialize the commuter agent with Google Maps API client if available."""
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        self.gmaps = None
        if self.api_key:
            try:
                self.gmaps = googlemaps.Client(key=self.api_key)
                logger.info("Google Maps API client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Maps client: {e}")
                self.gmaps = None
        else:
            logger.info("Google Maps API key not provided, using mock data")
    
    def _extract_locations(self, query: str) -> Optional[Tuple[str, str]]:
        """
        Extract origin and destination from query.
        Simple extraction - looks for patterns like "to [location]" or "from [origin] to [destination]"
        """
        query_lower = query.lower()
        
        # Pattern: "to [destination]" or "go to [destination]"
        to_match = re.search(r'(?:to|go to|going to)\s+([^?.,!]+)', query_lower)
        if to_match:
            destination = to_match.group(1).strip()
            # Try to find origin
            from_match = re.search(r'from\s+([^?.,!]+?)\s+(?:to|go)', query_lower)
            origin = from_match.group(1).strip() if from_match else "Current Location"
            return (origin, destination)
        
        # Pattern: "from [origin] to [destination]"
        from_to_match = re.search(r'from\s+([^?.,!]+?)\s+to\s+([^?.,!]+)', query_lower)
        if from_to_match:
            return (from_to_match.group(1).strip(), from_to_match.group(2).strip())
        
        return None
    
    def _format_duration(self, seconds: int) -> str:
        """Convert seconds to human-readable duration."""
        if seconds < 60:
            return f"{seconds} secs"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} mins"
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours} hr {mins} mins" if mins > 0 else f"{hours} hr"
    
    def _format_distance(self, meters: int) -> str:
        """Convert meters to human-readable distance."""
        if meters < 1000:
            return f"{meters} m"
        km = meters / 1000
        return f"{km:.1f} km"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process the user query and return a structured response.
        """
        query = query.lower()
        
        if "route" in query or "go to" in query:
            return self.get_route_recommendation(query)
        elif "traffic" in query:
            return self.get_traffic_conditions(query)
        elif "mode" in query or "how" in query:
            return self.suggest_travel_mode(query)
        else:
            return {
                "type": "general_response",
                "message": "I can help you with route planning, traffic updates, and travel mode suggestions. Please ask specifically about these topics."
            }

    def get_route_recommendation(self, query: str) -> Dict[str, Any]:
        """
        Get route recommendations using Google Maps Directions API.
        Returns 3 route options with duration, distance, and traffic info.
        Falls back to mock data if API is unavailable.
        """
        if not self.gmaps:
            logger.info("Using mock data for route recommendation")
            return self._get_mock_route_recommendation()
        
        locations = self._extract_locations(query)
        if not locations:
            logger.warning("Could not extract locations from query, using mock data")
            return self._get_mock_route_recommendation()
        
        origin, destination = locations
        
        try:
            # Get directions with alternatives
            directions_result = self.gmaps.directions(
                origin=origin,
                destination=destination,
                alternatives=True,
                mode="driving",
                traffic_model="best_guess",
                departure_time="now"
            )
            
            if not directions_result:
                logger.warning("No routes found, using mock data")
                return self._get_mock_route_recommendation()
            
            routes = []
            # Get up to 3 routes
            for idx, route in enumerate(directions_result[:3], 1):
                leg = route['legs'][0]
                duration = leg['duration']['value']  # in seconds
                duration_in_traffic = leg.get('duration_in_traffic', {}).get('value', duration)
                distance = leg['distance']['value']  # in meters
                
                # Determine traffic level based on duration difference
                traffic_delay = duration_in_traffic - duration
                if traffic_delay > 600:  # > 10 minutes delay
                    traffic = "Heavy"
                elif traffic_delay > 300:  # > 5 minutes delay
                    traffic = "Moderate"
                else:
                    traffic = "Light"
                
                # Get route summary/description
                summary = route.get('summary', f"Route {idx}")
                steps = leg.get('steps', [])
                if steps:
                    first_road = steps[0].get('html_instructions', '')
                    # Extract road name if possible
                    road_match = re.search(r'<b>([^<]+)</b>', first_road)
                    if road_match:
                        summary = f"Via {road_match.group(1)}"
                
                routes.append({
                    "id": idx,
                    "description": summary,
                    "duration": self._format_duration(duration_in_traffic),
                    "distance": self._format_distance(distance),
                    "traffic": traffic
                })
            
            # Ensure we have at least 3 routes (duplicate if needed for demo)
            while len(routes) < 3:
                routes.append(routes[-1].copy() if routes else {
                    "id": len(routes) + 1,
                    "description": "Alternative route",
                    "duration": "50 mins",
                    "distance": "16 km",
                    "traffic": "Moderate"
                })
            
            return {
                "type": "route_recommendation",
                "routes": routes[:3]
            }
            
        except Exception as e:
            logger.error(f"Error calling Google Maps API: {e}")
            return self._get_mock_route_recommendation()
    
    def _get_mock_route_recommendation(self) -> Dict[str, Any]:
        """Fallback mock route recommendation."""
        return {
            "type": "route_recommendation",
            "routes": [
                {
                    "id": 1,
                    "description": "Fastest route via Highway A",
                    "duration": "45 mins",
                    "distance": "15 km",
                    "traffic": "Moderate"
                },
                {
                    "id": 2,
                    "description": "Scenic route via Coastal Road",
                    "duration": "60 mins",
                    "distance": "18 km",
                    "traffic": "Light"
                },
                {
                    "id": 3,
                    "description": "Alternative route via Main Street",
                    "duration": "55 mins",
                    "distance": "16 km",
                    "traffic": "Heavy"
                }
            ]
        }

    def get_traffic_conditions(self, query: str) -> Dict[str, Any]:
        """
        Get traffic conditions using Google Maps Directions API.
        Returns current status, incidents, and peak hours.
        Falls back to mock data if API is unavailable.
        """
        if not self.gmaps:
            logger.info("Using mock data for traffic conditions")
            return self._get_mock_traffic_conditions()
        
        # Extract location from query
        location_match = re.search(r'(?:on|at|in|for)\s+([^?.,!]+)', query.lower())
        location = location_match.group(1).strip() if location_match else "Downtown"
        
        # Try to extract a route if available
        locations = self._extract_locations(query)
        origin = location
        destination = f"{location} city center"
        
        if locations:
            origin, destination = locations
        
        try:
            # Get directions to check traffic conditions
            directions_result = self.gmaps.directions(
                origin=origin,
                destination=destination,
                mode="driving",
                traffic_model="best_guess",
                departure_time="now"
            )
            
            if directions_result:
                route = directions_result[0]
                leg = route['legs'][0]
                duration = leg['duration']['value']
                duration_in_traffic = leg.get('duration_in_traffic', {}).get('value', duration)
                
                traffic_delay = duration_in_traffic - duration
                if traffic_delay > 600:
                    status = "Heavy"
                elif traffic_delay > 300:
                    status = "Moderate"
                else:
                    status = "Light"
                
                # Extract incidents/warnings from steps
                incidents = []
                for step in leg.get('steps', []):
                    warnings = step.get('warnings', [])
                    for warning in warnings:
                        if 'accident' in warning.lower() or 'construction' in warning.lower():
                            incidents.append(warning)
                
                if not incidents:
                    incidents = [
                        "No major incidents reported",
                        "Normal traffic flow expected"
                    ]
                
                return {
                    "type": "traffic_update",
                    "location": location.title(),
                    "current_status": status,
                    "incidents": incidents[:2],  # Limit to 2 incidents
                    "peak_hours": {
                        "morning": "7:00 AM - 9:00 AM",
                        "evening": "5:00 PM - 7:00 PM"
                    }
                }
            else:
                return self._get_mock_traffic_conditions()
                
        except Exception as e:
            logger.error(f"Error calling Google Maps API for traffic: {e}")
            return self._get_mock_traffic_conditions()
    
    def _get_mock_traffic_conditions(self) -> Dict[str, Any]:
        """Fallback mock traffic conditions."""
        conditions = ["Heavy", "Moderate", "Light"]
        status = random.choice(conditions)
        return {
            "type": "traffic_update",
            "location": "Downtown",
            "current_status": status,
            "incidents": [
                "Road work on Main Street causing delays",
                "Accident on Highway A - cleared"
            ],
            "peak_hours": {
                "morning": "7:00 AM - 9:00 AM",
                "evening": "5:00 PM - 7:00 PM"
            }
        }

    def suggest_travel_mode(self, query: str) -> Dict[str, Any]:
        """
        Suggest travel modes using Google Maps Distance Matrix and Directions API.
        Returns 4 modes (Car, Public Transit, Bike, Rideshare) with cost, time, pros/cons.
        Falls back to mock data if API is unavailable.
        """
        if not self.gmaps:
            logger.info("Using mock data for travel mode suggestion")
            return self._get_mock_travel_mode()
        
        locations = self._extract_locations(query)
        if not locations:
            logger.warning("Could not extract locations from query, using mock data")
            return self._get_mock_travel_mode()
        
        origin, destination = locations
        
        try:
            modes_data = []
            
            # 1. Car (driving)
            try:
                car_result = self.gmaps.directions(
                    origin=origin,
                    destination=destination,
                    mode="driving",
                    traffic_model="best_guess",
                    departure_time="now"
                )
                if car_result:
                    leg = car_result[0]['legs'][0]
                    car_time = leg.get('duration_in_traffic', leg['duration'])['value']
                    car_distance = leg['distance']['value']
                    # Estimate cost: $0.50 per km + parking
                    car_cost = (car_distance / 1000) * 0.5 + 3
                    modes_data.append({
                        "mode": "Car",
                        "cost": f"${car_cost:.2f}",
                        "time": self._format_duration(car_time),
                        "pros": ["Fastest option", "Door-to-door convenience", "Privacy"],
                        "cons": ["Parking costs", "Traffic delays", "Environmental impact"]
                    })
            except Exception as e:
                logger.warning(f"Error getting car directions: {e}")
            
            # 2. Public Transit
            try:
                transit_result = self.gmaps.directions(
                    origin=origin,
                    destination=destination,
                    mode="transit",
                    departure_time="now"
                )
                if transit_result:
                    leg = transit_result[0]['legs'][0]
                    transit_time = leg['duration']['value']
                    # Standard transit fare
                    transit_cost = 2.5
                    modes_data.append({
                        "mode": "Public Transit",
                        "cost": f"${transit_cost:.2f}",
                        "time": self._format_duration(transit_time),
                        "pros": ["Cost-effective", "No parking needed", "Eco-friendly"],
                        "cons": ["Fixed schedules", "Possible delays", "Less privacy"]
                    })
            except Exception as e:
                logger.warning(f"Error getting transit directions: {e}")
            
            # 3. Bike
            try:
                bike_result = self.gmaps.directions(
                    origin=origin,
                    destination=destination,
                    mode="bicycling"
                )
                if bike_result:
                    leg = bike_result[0]['legs'][0]
                    bike_time = leg['duration']['value']
                    modes_data.append({
                        "mode": "Bike",
                        "cost": "$0",
                        "time": self._format_duration(bike_time),
                        "pros": ["Free", "Healthy exercise", "No emissions"],
                        "cons": ["Weather dependent", "Physical effort", "Limited range"]
                    })
            except Exception as e:
                logger.warning(f"Error getting bike directions: {e}")
            
            # 4. Rideshare (use driving time + 20% cost premium)
            if modes_data and modes_data[0]["mode"] == "Car":
                car_cost_val = float(modes_data[0]["cost"].replace("$", ""))
                rideshare_cost = car_cost_val * 1.6  # 60% premium
                car_time_str = modes_data[0]["time"]
                modes_data.append({
                    "mode": "Rideshare",
                    "cost": f"${rideshare_cost:.2f}",
                    "time": car_time_str,
                    "pros": ["Convenient", "No parking", "Can work during ride"],
                    "cons": ["Higher cost", "Surge pricing", "Less reliable"]
                })
            
            # If we got some real data, use it; otherwise fall back to mock
            if len(modes_data) >= 2:
                # Ensure we have all 4 modes
                while len(modes_data) < 4:
                    # Add missing modes from mock data
                    mock_modes = self._get_mock_travel_mode()["modes"]
                    for mock_mode in mock_modes:
                        if not any(m["mode"] == mock_mode["mode"] for m in modes_data):
                            modes_data.append(mock_mode)
                            break
                
                # Sort by time (convert time strings to comparable values)
                def time_to_minutes(time_str):
                    if "hr" in time_str:
                        parts = time_str.split()
                        hours = int(parts[0])
                        mins = int(parts[2]) if len(parts) > 2 else 0
                        return hours * 60 + mins
                    return int(time_str.split()[0])
                
                modes_data.sort(key=lambda x: time_to_minutes(x["time"]))
                
                # Generate recommendation
                fastest = modes_data[0]
                cheapest = min(modes_data, key=lambda x: float(x["cost"].replace("$", "")))
                recommendation = f"{fastest['mode']} for speed ({fastest['time']}), or {cheapest['mode']} for cost efficiency ({cheapest['cost']})."
                
                return {
                    "type": "travel_mode_suggestion",
                    "modes": modes_data[:4],
                    "recommendation": recommendation
                }
            else:
                return self._get_mock_travel_mode()
                
        except Exception as e:
            logger.error(f"Error calling Google Maps API for travel modes: {e}")
            return self._get_mock_travel_mode()
    
    def _get_mock_travel_mode(self) -> Dict[str, Any]:
        """Fallback mock travel mode suggestion."""
        return {
            "type": "travel_mode_suggestion",
            "modes": [
                {
                    "mode": "Car",
                    "cost": "$5",
                    "time": "30 mins",
                    "pros": ["Fastest option", "Door-to-door convenience", "Privacy"],
                    "cons": ["Parking costs", "Traffic delays", "Environmental impact"]
                },
                {
                    "mode": "Public Transit",
                    "cost": "$2",
                    "time": "45 mins",
                    "pros": ["Cost-effective", "No parking needed", "Eco-friendly"],
                    "cons": ["Fixed schedules", "Possible delays", "Less privacy"]
                },
                {
                    "mode": "Bike",
                    "cost": "$0",
                    "time": "40 mins",
                    "pros": ["Free", "Healthy exercise", "No emissions"],
                    "cons": ["Weather dependent", "Physical effort", "Limited range"]
                },
                {
                    "mode": "Rideshare",
                    "cost": "$8",
                    "time": "35 mins",
                    "pros": ["Convenient", "No parking", "Can work during ride"],
                    "cons": ["Higher cost", "Surge pricing", "Less reliable"]
                }
            ],
            "recommendation": "Public Transit for cost efficiency, or Car for speed."
        }
