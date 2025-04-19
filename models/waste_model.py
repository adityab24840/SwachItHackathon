from datetime import datetime

class Waste:
    def __init__(self, id=None, type=None, weight=None, location=None, 
                 segregated=True, timestamp=None, user_id=None, ward=None):
        self.id = id
        self.type = type  # 'wet', 'dry', 'hazardous', etc.
        self.weight = weight  # in kg
        self.location = location  # GPS coordinates or address
        self.segregated = segregated  # boolean
        self.timestamp = timestamp or datetime.now()
        self.user_id = user_id
        self.ward = ward
    
    @staticmethod
    def get_waste_types():
        """Return valid waste types for segregation"""
        return {
            'wet': "Wet/Organic Waste",
            'dry': "Dry/Recyclable Waste",
            'hazardous': "Household Hazardous Waste",
            'sanitary': "Sanitary Waste",
            'ewaste': "Electronic Waste",
            'construction': "Construction & Demolition Waste"
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Waste object from dictionary data"""
        return Waste(
            id=data.get('id'),
            type=data.get('type'),
            weight=data.get('weight'),
            location=data.get('location'),
            segregated=data.get('segregated', True),
            timestamp=data.get('timestamp'),
            user_id=data.get('user_id'),
            ward=data.get('ward')
        )
    
    def to_dict(self):
        """Convert Waste object to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'weight': self.weight,
            'location': self.location,
            'segregated': self.segregated,
            'timestamp': self.timestamp,
            'user_id': self.user_id,
            'ward': self.ward
        }
    
    def __repr__(self):
        return f"Waste(id={self.id}, type={self.type}, weight={self.weight}kg, ward={self.ward})"