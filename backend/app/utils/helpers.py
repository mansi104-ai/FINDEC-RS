def format_response(data: any, status: str = "success") -> dict:
    """Format API response"""
    return {
        "status": status,
        "data": data
    }

def parse_request(request_data: dict) -> dict:
    """Parse and validate request data"""
    return {
        "parsed": True,
        "data": request_data
    }

def calculate_bias_score(factors: list) -> float:
    """Calculate bias score from factors"""
    return min(100.0, len(factors) * 15.0)
