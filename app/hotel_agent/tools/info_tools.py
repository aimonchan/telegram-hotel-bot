def get_attractions(location: str) -> dict:
    """Provides a list of nearby attractions."""
    # This could be a static list or use a real API like Google Places
    attractions = {
        "downtown": ["City Museum", "Grand Park", "Central Library"],
        "beach": ["Sunny Beach Pier", "Boardwalk", "Marine Life Aquarium"]
    }
    return {"attractions": attractions.get(location.lower(), ["No specific attractions found for that area."])}