# 🅿️ PROBLEM 5: PARKING LOT SYSTEM

### ⭐⭐⭐ **Design Multi-Level Parking Lot**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium
**Focus:** OOP, Strategy Pattern, Resource Allocation

---

## 📋 Problem Statement

Design a parking lot system with:
- Multiple levels
- Different spot sizes (Compact, Large, Handicapped)
- Vehicle types (Motorcycle, Car, Bus)
- Park/unpark operations
- Find available spots
- Calculate parking fees

**Core Requirements:**
- Efficiently find available spots matching vehicle size
- Track vehicle locations for quick unparking
- Support multiple pricing strategies
- Thread-safe for concurrent operations

---

## 🎤 How to Explain in Interview

### **Opening Statement (30 seconds)**
> "I'll design a multi-level parking lot using **OOP principles** with Python. I'll use the **Strategy Pattern** for flexible pricing, **Enums** for vehicle/spot types, and a **dictionary** for O(1) vehicle lookup. The design allows easy extension for features like reservations or EV charging."

### **Key Points to Mention:**
1. "Using **Strategy Pattern** for pricing - can swap hourly/flat/surge pricing"
2. "Using **Enums** for type safety (VehicleType, SpotType)"
3. "**Dictionary** for O(1) vehicle location lookup"
4. "**Dataclasses** for clean entity modeling"
5. "Easy to extend with **EV charging, reservations, valet service**"

---

## 🎨 Visual Example

```text
Level 1:
[C1: Car  ] [C2: ____] [L1: Bus ] [H1: ____]

Level 2:
[C3: Moto ] [C4: ____] [L2: ____] [H2: Car ]

Legend:
C = Compact spot    L = Large spot    H = Handicapped spot
____ = Empty

Spot Compatibility:
- Motorcycle → Compact, Large, Handicapped
- Car → Compact (if fits), Large, Handicapped
- Bus → Large only (may need multiple spots)
```

---

## 🎯 Design Patterns Used

### **1. Strategy Pattern** ⭐⭐⭐
Flexible pricing algorithms without changing parking lot code.

```python
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Strategy interface for pricing."""
    
    @abstractmethod
    def calculate_fee(self, hours: float) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: float = 5.0):
        self.rate = rate_per_hour
    
    def calculate_fee(self, hours: float) -> float:
        return hours * self.rate

class FlatRatePricing(PricingStrategy):
    def __init__(self, daily_rate: float = 20.0):
        self.rate = daily_rate
    
    def calculate_fee(self, hours: float) -> float:
        days = (hours // 24) + 1
        return days * self.rate
```

### **2. Factory Pattern** (Optional)
Create vehicles/spots through factory methods.

```python
class VehicleFactory:
    @staticmethod
    def create(vehicle_type: VehicleType, license_plate: str) -> Vehicle:
        # Could add validation, logging, etc.
        return Vehicle(license_plate, vehicle_type)
```

### **3. Singleton Pattern** (Optional)
Single parking lot instance.

```python
class ParkingLot:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(levels=3, spots_per_level=20)
        return cls._instance
```

---

## 🏗️ Class Design

```text
┌─────────────────────────┐
│      ParkingLot         │  ← Main facade
├─────────────────────────┤
│ - levels: List[Level]   │
│ - vehicle_spots: Dict   │  ← O(1) lookup
│ - pricing: Strategy     │
├─────────────────────────┤
│ + park_vehicle()        │
│ + unpark_vehicle()      │
│ + get_available_count() │
└─────────────────────────┘
            │
            │ contains
            ▼
┌─────────────────────────┐
│     ParkingLevel        │
├─────────────────────────┤
│ - level_number: int     │
│ - spots: List[Spot]     │
├─────────────────────────┤
│ + find_available_spot() │
│ + get_available_count() │
└─────────────────────────┘
            │
            │ contains
            ▼
┌─────────────────────────┐
│     ParkingSpot         │
├─────────────────────────┤
│ - spot_number: int      │
│ - spot_type: SpotType   │
│ - vehicle: Vehicle      │
├─────────────────────────┤
│ + can_fit(vehicle)      │
│ + park(vehicle)         │
│ + unpark()              │
└─────────────────────────┘
```

---

## 💻 Python Implementation (Production-Ready)

```python
"""
Multi-Level Parking Lot System
==============================
OOP design with Strategy Pattern for pricing.

Design Patterns:
- Strategy Pattern: Flexible pricing algorithms
- Factory Pattern: Vehicle creation (optional)

Features:
- Multiple levels with different spot types
- Vehicle type compatibility checking
- O(1) vehicle lookup for unparking
- Flexible pricing strategies
- Ticket generation with entry/exit times
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from datetime import datetime
from abc import ABC, abstractmethod
import uuid


# ============ Enums ============

class VehicleType(Enum):
    """Types of vehicles with size ordering."""
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotType(Enum):
    """Types of parking spots."""
    COMPACT = auto()
    LARGE = auto()
    HANDICAPPED = auto()


# ============ Pricing Strategy ============

class PricingStrategy(ABC):
    """Abstract pricing strategy (Strategy Pattern)."""
    
    @abstractmethod
    def calculate_fee(self, duration_hours: float) -> float:
        """Calculate parking fee based on duration."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Strategy name for display."""
        pass


class HourlyPricing(PricingStrategy):
    """Hourly rate pricing."""
    
    def __init__(self, rate_per_hour: float = 5.0):
        self.rate = rate_per_hour
    
    def calculate_fee(self, duration_hours: float) -> float:
        # Round up to nearest hour
        hours = max(1, int(duration_hours) + (1 if duration_hours % 1 > 0 else 0))
        return hours * self.rate
    
    @property
    def name(self) -> str:
        return f"Hourly (${self.rate}/hr)"


class FlatRatePricing(PricingStrategy):
    """Flat daily rate pricing."""
    
    def __init__(self, daily_rate: float = 20.0):
        self.rate = daily_rate
    
    def calculate_fee(self, duration_hours: float) -> float:
        days = max(1, int(duration_hours / 24) + (1 if duration_hours % 24 > 0 else 0))
        return days * self.rate
    
    @property
    def name(self) -> str:
        return f"Flat Rate (${self.rate}/day)"


class SurgePricing(PricingStrategy):
    """Surge pricing during peak hours."""
    
    def __init__(self, base_rate: float = 5.0, surge_multiplier: float = 2.0):
        self.base_rate = base_rate
        self.surge_multiplier = surge_multiplier
    
    def calculate_fee(self, duration_hours: float) -> float:
        # Simplified: check if current hour is peak (9-17)
        current_hour = datetime.now().hour
        multiplier = self.surge_multiplier if 9 <= current_hour <= 17 else 1.0
        hours = max(1, int(duration_hours) + 1)
        return hours * self.base_rate * multiplier
    
    @property
    def name(self) -> str:
        return f"Surge (${self.base_rate}/hr, {self.surge_multiplier}x peak)"


# ============ Core Entities ============

@dataclass
class Vehicle:
    """
    Vehicle entity.
    
    Attributes:
        license_plate: Unique identifier
        vehicle_type: Type of vehicle (affects spot compatibility)
    """
    license_plate: str
    vehicle_type: VehicleType
    
    def __hash__(self):
        return hash(self.license_plate)
    
    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False
        return self.license_plate == other.license_plate


@dataclass
class Ticket:
    """
    Parking ticket issued on entry.
    
    Attributes:
        ticket_id: Unique ticket identifier
        vehicle: Vehicle being parked
        spot: Assigned parking spot
        entry_time: When vehicle entered
        exit_time: When vehicle exited (set on unpark)
    """
    vehicle: Vehicle
    spot: 'ParkingSpot'
    ticket_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    entry_time: datetime = field(default_factory=datetime.now)
    exit_time: Optional[datetime] = None
    
    def get_duration_hours(self) -> float:
        """Get parking duration in hours."""
        end = self.exit_time or datetime.now()
        delta = end - self.entry_time
        return delta.total_seconds() / 3600
    
    def __str__(self):
        duration = f"{self.get_duration_hours():.1f} hrs"
        return f"Ticket[{self.ticket_id}]: {self.vehicle.license_plate} | Spot: {self.spot} | Duration: {duration}"


@dataclass
class ParkingSpot:
    """
    Individual parking spot.
    
    Attributes:
        spot_number: Spot identifier within level
        spot_type: Type of spot (Compact, Large, Handicapped)
        vehicle: Currently parked vehicle (None if empty)
        level: Level number (for display)
    """
    spot_number: int
    spot_type: SpotType
    level: int = 0
    vehicle: Optional[Vehicle] = None
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        """
        Check if vehicle can fit in this spot.
        
        Rules:
        - Motorcycle: Can fit in any spot
        - Car: Can fit in Compact (if available), Large, Handicapped
        - Bus: Can only fit in Large spots
        """
        if self.vehicle is not None:
            return False  # Already occupied
        
        if self.spot_type == SpotType.LARGE:
            return True  # Large fits all
        
        if self.spot_type == SpotType.HANDICAPPED:
            return vehicle.vehicle_type != VehicleType.BUS
        
        if self.spot_type == SpotType.COMPACT:
            return vehicle.vehicle_type in (VehicleType.MOTORCYCLE, VehicleType.CAR)
        
        return False
    
    def park(self, vehicle: Vehicle) -> bool:
        """Park vehicle in spot. Returns True if successful."""
        if not self.can_fit(vehicle):
            return False
        self.vehicle = vehicle
        return True
    
    def unpark(self) -> Optional[Vehicle]:
        """Remove and return vehicle from spot."""
        vehicle = self.vehicle
        self.vehicle = None
        return vehicle
    
    def is_available(self) -> bool:
        """Check if spot is empty."""
        return self.vehicle is None
    
    def __str__(self):
        return f"L{self.level}-{self.spot_type.name[0]}{self.spot_number}"


@dataclass
class ParkingLevel:
    """
    Single level/floor of parking lot.
    
    Attributes:
        level_number: Floor number
        spots: List of parking spots on this level
    """
    level_number: int
    spots: List[ParkingSpot] = field(default_factory=list)
    
    def __post_init__(self):
        """Set level number on all spots."""
        for spot in self.spots:
            spot.level = self.level_number
    
    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Find first available spot for vehicle.
        Uses first-fit strategy.
        """
        for spot in self.spots:
            if spot.can_fit(vehicle):
                return spot
        return None
    
    def get_available_count(self, spot_type: Optional[SpotType] = None) -> int:
        """Get count of available spots, optionally filtered by type."""
        return sum(
            1 for spot in self.spots 
            if spot.is_available() and (spot_type is None or spot.spot_type == spot_type)
        )
    
    def get_total_count(self, spot_type: Optional[SpotType] = None) -> int:
        """Get total spot count, optionally filtered by type."""
        return sum(
            1 for spot in self.spots 
            if spot_type is None or spot.spot_type == spot_type
        )


class ParkingLot:
    """
    Multi-level parking lot system.
    
    Features:
    - Multiple levels with mixed spot types
    - O(1) vehicle lookup for unparking
    - Configurable pricing strategy
    - Ticket generation and fee calculation
    
    Example:
        >>> lot = ParkingLot(levels=3, spots_per_level=10)
        >>> car = Vehicle("ABC123", VehicleType.CAR)
        >>> ticket = lot.park_vehicle(car)
        >>> lot.unpark_vehicle("ABC123")  # Returns fee
    """
    
    def __init__(self, levels: int = 3, spots_per_level: int = 20,
                 pricing_strategy: PricingStrategy = None):
        """
        Initialize parking lot.
        
        Args:
            levels: Number of parking levels
            spots_per_level: Spots per level (mix of types)
            pricing_strategy: Pricing algorithm (default: hourly)
        """
        self.levels: List[ParkingLevel] = []
        self.vehicle_tickets: Dict[str, Ticket] = {}  # license_plate -> ticket
        self.pricing = pricing_strategy or HourlyPricing()
        
        # Initialize levels with mixed spot types
        self._initialize_levels(levels, spots_per_level)
    
    def _initialize_levels(self, num_levels: int, spots_per_level: int) -> None:
        """Create levels with balanced spot types."""
        for level_num in range(1, num_levels + 1):
            spots = []
            spot_num = 1
            
            # Distribution: 60% Compact, 30% Large, 10% Handicapped
            num_compact = int(spots_per_level * 0.6)
            num_large = int(spots_per_level * 0.3)
            num_handicapped = spots_per_level - num_compact - num_large
            
            for _ in range(num_compact):
                spots.append(ParkingSpot(spot_num, SpotType.COMPACT, level_num))
                spot_num += 1
            
            for _ in range(num_large):
                spots.append(ParkingSpot(spot_num, SpotType.LARGE, level_num))
                spot_num += 1
            
            for _ in range(num_handicapped):
                spots.append(ParkingSpot(spot_num, SpotType.HANDICAPPED, level_num))
                spot_num += 1
            
            self.levels.append(ParkingLevel(level_num, spots))
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        """
        Park vehicle in first available spot.
        
        Args:
            vehicle: Vehicle to park
            
        Returns:
            Ticket if parked successfully, None if no spot available
            
        Raises:
            ValueError: If vehicle is already parked
        """
        if vehicle.license_plate in self.vehicle_tickets:
            raise ValueError(f"Vehicle {vehicle.license_plate} is already parked")
        
        # Find available spot across all levels
        for level in self.levels:
            spot = level.find_available_spot(vehicle)
            if spot:
                spot.park(vehicle)
                ticket = Ticket(vehicle=vehicle, spot=spot)
                self.vehicle_tickets[vehicle.license_plate] = ticket
                return ticket
        
        return None  # Parking full
    
    def unpark_vehicle(self, license_plate: str) -> Tuple[Optional[Ticket], float]:
        """
        Unpark vehicle and calculate fee.
        
        Args:
            license_plate: Vehicle's license plate
            
        Returns:
            Tuple of (ticket, fee) or (None, 0) if not found
        """
        if license_plate not in self.vehicle_tickets:
            return None, 0.0
        
        ticket = self.vehicle_tickets.pop(license_plate)
        ticket.exit_time = datetime.now()
        ticket.spot.unpark()
        
        fee = self.pricing.calculate_fee(ticket.get_duration_hours())
        return ticket, fee
    
    def get_vehicle_location(self, license_plate: str) -> Optional[ParkingSpot]:
        """Find where a vehicle is parked."""
        ticket = self.vehicle_tickets.get(license_plate)
        return ticket.spot if ticket else None
    
    def is_full(self) -> bool:
        """Check if parking lot is completely full."""
        return self.get_available_count() == 0
    
    def get_available_count(self, spot_type: Optional[SpotType] = None) -> int:
        """Get total available spots across all levels."""
        return sum(level.get_available_count(spot_type) for level in self.levels)
    
    def get_total_count(self, spot_type: Optional[SpotType] = None) -> int:
        """Get total spot count across all levels."""
        return sum(level.get_total_count(spot_type) for level in self.levels)
    
    def get_occupancy_rate(self) -> float:
        """Get current occupancy percentage."""
        total = self.get_total_count()
        occupied = total - self.get_available_count()
        return (occupied / total) * 100 if total > 0 else 0
    
    def set_pricing_strategy(self, strategy: PricingStrategy) -> None:
        """Change pricing strategy (Strategy Pattern)."""
        self.pricing = strategy
    
    def display_status(self) -> None:
        """Print parking lot status."""
        print(f"\n{'='*50}")
        print(f"PARKING LOT STATUS")
        print(f"{'='*50}")
        print(f"Pricing: {self.pricing.name}")
        print(f"Occupancy: {self.get_occupancy_rate():.1f}%")
        print(f"\nAvailable spots by type:")
        for spot_type in SpotType:
            avail = self.get_available_count(spot_type)
            total = self.get_total_count(spot_type)
            print(f"  {spot_type.name}: {avail}/{total}")
        
        print(f"\nBy Level:")
        for level in self.levels:
            avail = level.get_available_count()
            total = level.get_total_count()
            print(f"  Level {level.level_number}: {avail}/{total} available")


# ============ Demo / Usage ============
if __name__ == "__main__":
    print("=== Multi-Level Parking Lot Demo ===")
    
    # Create parking lot
    lot = ParkingLot(levels=3, spots_per_level=10, pricing_strategy=HourlyPricing(5.0))
    lot.display_status()
    
    # Create vehicles
    vehicles = [
        Vehicle("CAR-001", VehicleType.CAR),
        Vehicle("CAR-002", VehicleType.CAR),
        Vehicle("MOTO-001", VehicleType.MOTORCYCLE),
        Vehicle("BUS-001", VehicleType.BUS),
    ]
    
    # Park vehicles
    print("\n" + "=" * 50)
    print("PARKING VEHICLES")
    print("=" * 50)
    
    tickets = []
    for vehicle in vehicles:
        ticket = lot.park_vehicle(vehicle)
        if ticket:
            tickets.append(ticket)
            print(f"✓ Parked {vehicle.license_plate} ({vehicle.vehicle_type.name}) at {ticket.spot}")
        else:
            print(f"✗ Could not park {vehicle.license_plate} - lot full")
    
    lot.display_status()
    
    # Find vehicle
    print("\n" + "=" * 50)
    print("FIND VEHICLE")
    print("=" * 50)
    spot = lot.get_vehicle_location("CAR-001")
    print(f"CAR-001 is at: {spot}")
    
    # Unpark and calculate fee
    print("\n" + "=" * 50)
    print("UNPARK VEHICLE")
    print("=" * 50)
    
    import time
    time.sleep(1)  # Simulate some parking time
    
    ticket, fee = lot.unpark_vehicle("CAR-001")
    if ticket:
        print(f"Unparked: {ticket}")
        print(f"Fee: ${fee:.2f} ({lot.pricing.name})")
    
    # Change pricing strategy
    print("\n" + "=" * 50)
    print("CHANGE PRICING STRATEGY")
    print("=" * 50)
    lot.set_pricing_strategy(FlatRatePricing(20.0))
    print(f"New pricing: {lot.pricing.name}")
    
    ticket, fee = lot.unpark_vehicle("CAR-002")
    if ticket:
        print(f"Fee with flat rate: ${fee:.2f}")
    
    lot.display_status()
```

---

## 🚀 Extensions & Follow-ups

### **Extension 1: Reserved Spots**
```python
@dataclass
class ParkingSpot:
    reserved_for: Optional[str] = None  # license plate
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        if self.reserved_for and self.reserved_for != vehicle.license_plate:
            return False
        # ... rest of logic

class ParkingLot:
    def reserve_spot(self, spot: ParkingSpot, license_plate: str):
        spot.reserved_for = license_plate
```

### **Extension 2: EV Charging**
```python
class SpotType(Enum):
    COMPACT = auto()
    LARGE = auto()
    HANDICAPPED = auto()
    EV_CHARGING = auto()  # New type

class EVChargingSpot(ParkingSpot):
    charging_rate_kw: float = 7.2
    
    def start_charging(self) -> None:
        pass
    
    def stop_charging(self) -> float:
        # Return kWh consumed
        pass
```

### **Extension 3: Display Board**
```python
class DisplayBoard:
    """Real-time availability display."""
    
    def __init__(self, parking_lot: ParkingLot):
        self.lot = parking_lot
    
    def show(self) -> str:
        lines = ["=== PARKING AVAILABILITY ==="]
        for level in self.lot.levels:
            avail = level.get_available_count()
            lines.append(f"Level {level.level_number}: {avail} spots")
        return "\n".join(lines)
```

---

## 🧪 Testing Strategy

```python
import pytest
from datetime import datetime, timedelta

class TestParkingLot:
    
    def test_park_vehicle(self):
        """Vehicle parks successfully."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        car = Vehicle("ABC123", VehicleType.CAR)
        
        ticket = lot.park_vehicle(car)
        
        assert ticket is not None
        assert ticket.vehicle == car
        assert lot.get_available_count() == 4
    
    def test_park_vehicle_full(self):
        """Returns None when lot is full."""
        lot = ParkingLot(levels=1, spots_per_level=1)
        lot.park_vehicle(Vehicle("A", VehicleType.MOTORCYCLE))
        
        result = lot.park_vehicle(Vehicle("B", VehicleType.MOTORCYCLE))
        
        assert result is None
    
    def test_unpark_vehicle(self):
        """Unpark returns ticket and fee."""
        lot = ParkingLot(levels=1, spots_per_level=5, 
                        pricing_strategy=HourlyPricing(10.0))
        car = Vehicle("ABC123", VehicleType.CAR)
        lot.park_vehicle(car)
        
        ticket, fee = lot.unpark_vehicle("ABC123")
        
        assert ticket is not None
        assert fee >= 10.0  # At least 1 hour
        assert lot.get_available_count() == 5
    
    def test_vehicle_already_parked(self):
        """Cannot park same vehicle twice."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        car = Vehicle("ABC123", VehicleType.CAR)
        lot.park_vehicle(car)
        
        with pytest.raises(ValueError):
            lot.park_vehicle(car)
    
    def test_spot_compatibility(self):
        """Vehicles only fit in compatible spots."""
        # Bus should only fit in Large spots
        large_spot = ParkingSpot(1, SpotType.LARGE)
        compact_spot = ParkingSpot(2, SpotType.COMPACT)
        bus = Vehicle("BUS1", VehicleType.BUS)
        
        assert large_spot.can_fit(bus) == True
        assert compact_spot.can_fit(bus) == False
    
    def test_pricing_strategy(self):
        """Different strategies calculate different fees."""
        hourly = HourlyPricing(5.0)
        flat = FlatRatePricing(20.0)
        
        # 2 hours
        assert hourly.calculate_fee(2.0) == 10.0
        assert flat.calculate_fee(2.0) == 20.0
        
        # 25 hours (> 1 day)
        assert hourly.calculate_fee(25.0) == 130.0  # 26 hours rounded
        assert flat.calculate_fee(25.0) == 40.0     # 2 days
```

---

## 📊 Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| `park_vehicle` | O(L × S) | O(1) |
| `unpark_vehicle` | O(1) | O(1) |
| `get_vehicle_location` | O(1) | O(1) |
| `get_available_count` | O(L × S) | O(1) |
| `is_full` | O(L × S) | O(1) |

**Where:** L = levels, S = spots per level

**Optimization:** Could maintain available count to make `is_full` O(1)

---

## 💯 Interview Checklist

Before finishing, ensure you've mentioned:
- [ ] ✅ **Strategy Pattern** for pricing
- [ ] ✅ **Enums** for vehicle/spot types
- [ ] ✅ **Dictionary** for O(1) vehicle lookup
- [ ] ✅ **Spot compatibility** logic
- [ ] ✅ **Ticket system** for tracking
- [ ] ✅ **Thread safety** mention (locks for concurrent access)
- [ ] ✅ **Extensions** (reservations, EV charging, display board)
- [ ] ✅ **Testing strategy**

---

**Design Patterns Used:**
- Strategy Pattern (Pricing)
- Factory Pattern (Vehicle creation)
- Singleton Pattern (Single lot instance)

**Related Problems:**
- Design Parking Garage
- Design Valet Parking System
