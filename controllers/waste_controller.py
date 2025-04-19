import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def get_ward_cleanliness_scores():
    """
    Generate ward-level cleanliness scores with realistic BBMP ward names
    """
    bengaluru_wards = [
        "Koramangala", "Indiranagar", "Jayanagar", "JP Nagar", "HSR Layout", 
        "Malleswaram", "Shivajinagar", "Hebbal", "Yelahanka", "Mahadevpura",
        "Whitefield", "Electronic City"
    ]
    
    # Seed random to get consistent results between refreshes
    random.seed(42)
    
    ward_scores = []
    for i, ward in enumerate(bengaluru_wards):
        # Generate a realistic score between 40-95
        score = random.randint(40, 95)
        
        # Determine category based on score
        if score >= 80:
            category = "Excellent"
        elif score >= 60:
            category = "Good"
        elif score >= 40:
            category = "Average"
        else:
            category = "Needs Improvement"
            
        # Generate recent change (improvement or deterioration)
        change = round(random.uniform(-5, 8), 1)
        
        # Get rank (1-12)
        rank = i + 1
        
        ward_scores.append({
            "ward": ward,
            "score": score,
            "category": category,
            "change": change,
            "rank": rank
        })
    
    # Sort by score to get actual rankings
    ward_scores.sort(key=lambda x: x["score"], reverse=True)
    for i, ward in enumerate(ward_scores):
        ward["rank"] = i + 1
    
    return ward_scores

def get_waste_stats(user_id=None, ward_name="Koramangala"):
    """
    Generate or retrieve waste statistics for a specific ward or user
    """
    # In a real app, this would query a database
    # For demo purposes, generate realistic data
    
    # Generate daily data for the last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    # Seed with ward name and user_id to get consistent but different results
    random.seed(hash(ward_name + str(user_id if user_id else 0)) % 2**32)
    
    daily_data = []
    time_series = []
    total_waste = 0
    
    # Create waste by type data - This adds the missing 'by_type' key
    waste_types = {
        'Wet': {'amount_kg': random.uniform(15, 25), 'segregated': random.uniform(0.7, 0.95)},
        'Dry': {'amount_kg': random.uniform(10, 20), 'segregated': random.uniform(0.8, 0.98)},
        'Hazardous': {'amount_kg': random.uniform(1, 5), 'segregated': random.uniform(0.6, 0.9)},
        'E-waste': {'amount_kg': random.uniform(0.5, 3), 'segregated': random.uniform(0.7, 1.0)},
        'Garden': {'amount_kg': random.uniform(3, 8), 'segregated': random.uniform(0.8, 1.0)}
    }
    
    for date in date_range:
        # Generate values with weekend patterns
        is_weekend = date.weekday() >= 5
        
        # More waste on weekends
        waste_generated = random.uniform(
            5.0 if is_weekend else 3.0,  # Min
            9.0 if is_weekend else 6.0   # Max
        )
        
        # Convert to tonnes for the ward (assuming around 5-9 tonnes per ward)
        waste_generated = round(waste_generated, 1)
        total_waste += waste_generated
        
        # Better segregation on weekdays
        segregation_rate = random.uniform(
            70 if is_weekend else 80,  # Min
            85 if is_weekend else 95   # Max
        )
        segregation_rate = round(segregation_rate, 1)
        
        # Collection efficiency (generally high due to BBMP mandates)
        collection_efficiency = random.uniform(85, 98)
        collection_efficiency = round(collection_efficiency, 1)
        
        # Processing and recycling rates
        processing_rate = random.uniform(70, 85)
        recycling_rate = random.uniform(30, 50)
        
        daily_data.append({
            "date": date,
            "waste_generated": waste_generated,
            "segregation_rate": segregation_rate,
            "collection_efficiency": collection_efficiency,
            "processing_rate": processing_rate,
            "recycling_rate": recycling_rate
        })
        
        # Generate time series data for individual waste entries
        for waste_type in ['Wet', 'Dry', 'Hazardous', 'E-waste', 'Garden']:
            # Weight by the overall waste distribution
            fraction = waste_types[waste_type]['amount_kg'] / sum(t['amount_kg'] for t in waste_types.values())
            amount = waste_generated * fraction * random.uniform(0.8, 1.2)  # Add some daily variation
            
            time_series.append({
                "date": date,
                "type": waste_type,
                "amount_kg": round(amount, 2),
                "segregated": random.random() < waste_types[waste_type]['segregated']
            })
    
    # Create DataFrame
    df = pd.DataFrame(daily_data)
    
    # Calculate summary statistics
    summary = {
        "total_waste_kg": round(total_waste, 1),
        "avg_daily_waste": round(df["waste_generated"].mean(), 1),
        "daily_average_kg": round(df["waste_generated"].mean(), 1),
        "total_monthly_waste": round(df["waste_generated"].sum(), 1),
        "avg_segregation": round(df["segregation_rate"].mean(), 1),
        "segregation_rate": round(df["segregation_rate"].mean(), 1),
        "avg_collection": round(df["collection_efficiency"].mean(), 1),
        "avg_processing": round(df["processing_rate"].mean(), 1),
        "avg_recycling": round(df["recycling_rate"].mean(), 1),
        "recent_trend": "improving" if random.random() > 0.3 else "stable",
        "by_type": waste_types,  # Add the missing 'by_type' key here
        "time_series": time_series  # Add time series data for charts
    }
    
    return summary, df

def get_cleanliness_score(user_id=None):
    """
    Calculate overall cleanliness score based on waste management parameters
    """
    # In a real app, this would be based on actual metrics
    # For demo, generate a realistic score
    
    # Base score between 60-90
    base_score = random.randint(60, 90)
    
    # Component scores
    segregation_score = random.randint(60, 95)
    collection_score = random.randint(70, 95)
    black_spots_score = random.randint(50, 90)
    citizen_rating = random.randint(60, 90)
    
    # Calculate weighted average
    overall_score = (
        0.35 * segregation_score +
        0.25 * collection_score +
        0.25 * black_spots_score +
        0.15 * citizen_rating
    )
    
    result = {
        "overall_score": round(overall_score, 1),
        "components": {
            "segregation_score": segregation_score,
            "collection_score": collection_score,
            "black_spots_score": black_spots_score,
            "citizen_rating": citizen_rating
        },
        "trend": random.choice(["improving", "stable", "needs attention"])
    }
    
    return result

def get_active_complaints(ward=None):
    """
    Get active waste management complaints for a ward
    """
    complaint_types = [
        "Missed garbage collection",
        "Black spot not cleared",
        "Overflowing bin",
        "Improper segregation by neighbors",
        "Waste burning incident",
        "Littering in public space",
        "Commercial waste dumping",
        "Construction debris",
        "Drain blockage due to waste"
    ]
    
    # Generate random number of complaints
    num_complaints = random.randint(5, 15)
    
    complaints = []
    for i in range(num_complaints):
        # Random age of complaint (1-10 days)
        age = random.randint(1, 10)
        complaint_date = datetime.now() - timedelta(days=age)
        
        # Random status
        status = random.choice(["Pending", "In Progress", "Resolved", "Closed"])
        
        # Random location within the ward
        locations = [
            "Main Road", "Cross Road", "Park", "Market", "Bus Stop", 
            "Residential Layout", "Commercial Complex", "School Area"
        ]
        location = f"{random.choice(locations)}, {ward}" if ward else random.choice(locations)
        
        # Add random number of votes (0-15)
        votes = random.randint(0, 15)
        
        complaints.append({
            "id": f"BBMP-WM-{random.randint(10000, 99999)}",
            "type": random.choice(complaint_types),
            "location": location,
            "date_reported": complaint_date.strftime("%Y-%m-%d"),
            "age_days": age,
            "status": status,
            "priority": "High" if age > 7 else "Medium" if age > 3 else "Low",
            "votes": votes  # Add votes to each complaint
        })
    
    return complaints

def get_recycling_stats(ward=None):
    """
    Get statistics about recycling efforts in the ward
    """
    # Create statistics for different recyclable categories
    categories = [
        "Paper & Cardboard",
        "Plastic",
        "Glass",
        "Metal",
        "E-Waste",
        "Organic/Compost"
    ]
    
    stats = []
    for category in categories:
        # Different baseline quantities for different categories
        if category == "Paper & Cardboard":
            quantity = random.uniform(20, 35)
        elif category == "Plastic":
            quantity = random.uniform(15, 25)
        elif category == "Glass":
            quantity = random.uniform(5, 15)
        elif category == "Metal":
            quantity = random.uniform(3, 10)
        elif category == "E-Waste":
            quantity = random.uniform(1, 5)
        else:  # Organic/Compost
            quantity = random.uniform(30, 50)
            
        stats.append({
            "category": category,
            "quantity_tonnes": round(quantity, 1),
            "percentage": 0,  # Will calculate after
            "trend": random.choice(["increasing", "stable", "decreasing"])
        })
    
    # Calculate percentages
    total = sum(item["quantity_tonnes"] for item in stats)
    for item in stats:
        item["percentage"] = round((item["quantity_tonnes"] / total) * 100, 1)
    
    return stats

def get_daily_waste_stats(user_id=None):
    """
    Get waste statistics aggregated by day of week
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Generate different patterns for different days
    waste_by_day = []
    for i, day in enumerate(days):
        is_weekend = i >= 5
        
        # Weekend patterns
        waste_generated = random.uniform(
            5.0 if is_weekend else 3.0,  # Min
            9.0 if is_weekend else 6.0   # Max
        )
        
        segregation_rate = random.uniform(
            70 if is_weekend else 80,  # Min
            85 if is_weekend else 95   # Max
        )
        
        waste_by_day.append({
            "day": day,
            "waste_generated": round(waste_generated, 1),
            "segregation_rate": round(segregation_rate, 1)
        })
    
    return waste_by_day