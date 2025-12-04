# 🅿️ PROBLEM 5: PARKING LOT SYSTEM

### ⭐⭐⭐ **Design Multi-Level Parking Lot**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium
**Time to Solve:** 35-45 minutes
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
- Thread-safe for concurrent operations (mention)

**Constraints:**
- 1 ≤ Levels ≤ 10
- 1 ≤ Spots per level ≤ 100
- Vehicle must fit in appropriate spot type
- Fees calculated based on duration

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What vehicle types? Motorcycle, Car, Bus, EV?"
2. "What spot types? Compact, Large, Handicapped, EV?"
3. "Can a motorcycle park in a large spot? (Spot compatibility rules)"
4. "How should pricing work? Hourly, daily, or different strategies?"
5. "Do we need reservations or valet service?"
6. "Should buses span multiple spots or just use one large spot?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Discuss Key Design Decisions (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the key design decisions."

#### **Spot Allocation Strategy**

```text
Option 1: First-Fit
- Search linearly, take first available spot
- Simple, O(L × S) where L = levels, S = spots
- Good for interviews

Option 2: Best-Fit
- Find smallest spot that fits the vehicle
- More efficient use of space
- More complex

Option 3: Level-Optimized
- Fill lower levels first
- Better for user convenience
```

**Explain:**
> "I'll use First-Fit for simplicity. In production, we might use Best-Fit or maintain separate lists per spot type."

---

#### **Vehicle Lookup for Unparking**

```text
Naive: Search all spots - O(L × S)
Optimal: Dictionary mapping - O(1) ✓

vehicle_tickets: Dict[str, Ticket]
- Key: license_plate
- Value: Ticket with spot reference
```

**Explain:**
> "I'll use a dictionary mapping license plate to ticket.
> This gives O(1) lookup when unparking instead of searching all spots."

---

### **PHASE 3: High-Level Design (2-3 minutes)**

**SAY THIS:**
> "Let me draw the class structure."

**Draw on whiteboard:**
```
┌─────────────────────────────────────────────────────────┐
│                     ParkingLot                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Main facade - entry point for operations       │   │
│  │                                                  │   │
│  │  - levels: List[ParkingLevel]                   │   │
│  │  - vehicle_tickets: Dict[str, Ticket] ← O(1)   │   │
│  │  - pricing_strategy: PricingStrategy            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  + park_vehicle(vehicle) → Ticket                      │
│  + unpark_vehicle(license_plate) → (Ticket, fee)       │
│  + get_available_count() → int                         │
└─────────────────────────────────────────────────────────┘
            │
            │ contains
            ▼
┌─────────────────────┐     ┌─────────────────────┐
│    ParkingLevel     │     │   ParkingSpot       │
├─────────────────────┤     ├─────────────────────┤
│ - level_number      │────▶│ - spot_number       │
│ - spots: List[Spot] │     │ - spot_type: Enum   │
│                     │     │ - vehicle: Vehicle  │
│ + find_spot(vehicle)│     │ + can_fit(vehicle)  │
└─────────────────────┘     │ + park(vehicle)     │
                            │ + unpark()          │
                            └─────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│      Vehicle        │     │  PricingStrategy    │
├─────────────────────┤     ├─────────────────────┤
│ - license_plate     │     │ + calculate_fee()   │
│ - vehicle_type      │     └─────────────────────┘
└─────────────────────┘              △
                                     │
                        ┌────────────┼────────────┐
                        │            │            │
                   HourlyPricing  FlatRate   SurgePricing
```

---

### **PHASE 4: Design Patterns & Principles (2 minutes)**

**SAY THIS:**
> "I'm using the Strategy Pattern for pricing flexibility."

#### **Strategy Pattern** ⭐⭐⭐⭐⭐

```python
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Strategy interface - encapsulates pricing algorithm."""
    
    @abstractmethod
    def calculate_fee(self, duration_hours: float) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def __init__(self, rate: float = 5.0):
        self.rate = rate
    
    def calculate_fee(self, duration_hours: float) -> float:
        return max(1, int(duration_hours) + 1) * self.rate

class FlatRatePricing(PricingStrategy):
    def __init__(self, daily_rate: float = 20.0):
        self.rate = daily_rate
    
    def calculate_fee(self, duration_hours: float) -> float:
        days = max(1, int(duration_hours / 24) + 1)
        return days * self.rate
```

**Why Strategy Pattern?**
> "We can change pricing at runtime without modifying ParkingLot.
> Add new pricing strategies without changing existing code (Open/Closed Principle).
> In production: surge pricing during events, weekend rates, loyalty discounts."

---

#### **Factory Pattern** (Optional) ⭐

```python
class VehicleFactory:
    @staticmethod
    def create(vehicle_type: VehicleType, license_plate: str) -> Vehicle:
        # Add validation, logging
        return Vehicle(license_plate, vehicle_type)
```

---

### **PHASE 5: Data Structures & Why (2 minutes)**

**SAY THIS:**
> "Let me explain my data structure choices."

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `Dict[str, Ticket]` | Vehicle lookup | O(1) find parked vehicle |
| `List[ParkingLevel]` | Level storage | Ordered by level number |
| `List[ParkingSpot]` | Spots per level | Ordered, allows iteration |
| `Enum` | VehicleType, SpotType | Type safety, clear values |
| `dataclass` | Vehicle, Ticket, Spot | Clean initialization |

**Key Insight:**
> "The dictionary `vehicle_tickets` is crucial:
> - Maps license_plate → Ticket
> - Ticket contains spot reference
> - O(1) lookup instead of O(L × S) search"

---

### **PHASE 6: Write the Code (15-20 minutes)**

**SAY THIS:**
> "Now let me implement this. I'll start with enums, then entities, then the ParkingLot."

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
    """Types of vehicles."""
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotType(Enum):
    """Types of parking spots."""
    COMPACT = auto()
    LARGE = auto()
    HANDICAPPED = auto()


# ============ Strategy Pattern: Pricing ============

class PricingStrategy(ABC):
    """
    Abstract pricing strategy (Strategy Pattern).
    
    Encapsulates pricing algorithm so it can be:
    - Changed at runtime (set_pricing_strategy)
    - Extended without modifying ParkingLot
    - Tested independently
    """
    
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
    """Hourly rate pricing - most common."""
    
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
    """Surge pricing during peak hours (9-17)."""
    
    def __init__(self, base_rate: float = 5.0, surge_multiplier: float = 2.0):
        self.base_rate = base_rate
        self.surge_multiplier = surge_multiplier
    
    def calculate_fee(self, duration_hours: float) -> float:
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
    """Vehicle entity."""
    license_plate: str
    vehicle_type: VehicleType
    
    def __hash__(self):
        return hash(self.license_plate)
    
    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False
        return self.license_plate == other.license_plate


@dataclass
class ParkingSpot:
    """
    Individual parking spot.
    
    Spot Compatibility Rules:
    - COMPACT: Motorcycle, Car
    - LARGE: Motorcycle, Car, Bus (all vehicles)
    - HANDICAPPED: Motorcycle, Car (not Bus)
    """
    spot_number: int
    spot_type: SpotType
    level: int = 0
    vehicle: Optional[Vehicle] = None
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        """
        Check if vehicle can fit in this spot.
        
        Rules:
        - Spot must be empty
        - LARGE fits all vehicles
        - HANDICAPPED fits all except Bus
        - COMPACT fits Motorcycle and Car
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
class Ticket:
    """
    Parking ticket issued on entry.
    
    Contains all information needed for:
    - Finding the parked vehicle (spot reference)
    - Calculating fee (entry_time)
    - Receipt generation (all details)
    """
    vehicle: Vehicle
    spot: ParkingSpot
    ticket_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    entry_time: datetime = field(default_factory=datetime.now)
    exit_time: Optional[datetime] = None
    
    def get_duration_hours(self) -> float:
        """Get parking duration in hours."""
        end = self.exit_time or datetime.now()
        delta = end - self.entry_time
        return delta.total_seconds() / 3600
    
    def __str__(self):
        duration = f"{self.get_duration_hours():.2f} hrs"
        return f"Ticket[{self.ticket_id}]: {self.vehicle.license_plate} | {self.spot} | {duration}"


@dataclass
class ParkingLevel:
    """
    Single level/floor of parking lot.
    
    Responsibilities:
    - Store and manage spots
    - Find available spot for vehicle
    - Track available counts
    """
    level_number: int
    spots: List[ParkingSpot] = field(default_factory=list)
    
    def __post_init__(self):
        """Set level number on all spots."""
        for spot in self.spots:
            spot.level = self.level_number
    
    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Find first available spot for vehicle (First-Fit strategy).
        
        Time: O(S) where S = spots on this level
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
    
    Key Design Decisions:
    1. Dict for O(1) vehicle lookup (vehicle_tickets)
    2. Strategy Pattern for flexible pricing
    3. First-Fit allocation strategy
    
    Example:
        >>> lot = ParkingLot(levels=3, spots_per_level=10)
        >>> car = Vehicle("ABC123", VehicleType.CAR)
        >>> ticket = lot.park_vehicle(car)
        >>> ticket, fee = lot.unpark_vehicle("ABC123")
    """
    
    def __init__(self, levels: int = 3, spots_per_level: int = 20,
                 pricing_strategy: PricingStrategy = None):
        """
        Initialize parking lot.
        
        Args:
            levels: Number of parking levels
            spots_per_level: Spots per level (mixed types)
            pricing_strategy: Pricing algorithm (default: hourly)
        """
        if levels <= 0 or spots_per_level <= 0:
            raise ValueError("Levels and spots must be positive")
        
        self.levels: List[ParkingLevel] = []
        self.vehicle_tickets: Dict[str, Ticket] = {}  # ★ O(1) lookup
        self.pricing = pricing_strategy or HourlyPricing()
        
        self._initialize_levels(levels, spots_per_level)
    
    def _initialize_levels(self, num_levels: int, spots_per_level: int) -> None:
        """Create levels with balanced spot types (60% Compact, 30% Large, 10% Handicapped)."""
        for level_num in range(1, num_levels + 1):
            spots = []
            spot_num = 1
            
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
        
        Time: O(L × S) to find spot, O(1) to store ticket
        
        Returns:
            Ticket if parked successfully, None if lot is full
        """
        if vehicle.license_plate in self.vehicle_tickets:
            raise ValueError(f"Vehicle {vehicle.license_plate} is already parked")
        
        # Find available spot across all levels
        for level in self.levels:
            spot = level.find_available_spot(vehicle)
            if spot:
                spot.park(vehicle)
                ticket = Ticket(vehicle=vehicle, spot=spot)
                self.vehicle_tickets[vehicle.license_plate] = ticket  # O(1) store
                return ticket
        
        return None  # Parking full
    
    def unpark_vehicle(self, license_plate: str) -> Tuple[Optional[Ticket], float]:
        """
        Unpark vehicle and calculate fee.
        
        Time: O(1) - dictionary lookup!
        
        Returns:
            Tuple of (ticket, fee) or (None, 0) if not found
        """
        if license_plate not in self.vehicle_tickets:
            return None, 0.0
        
        ticket = self.vehicle_tickets.pop(license_plate)  # O(1) remove
        ticket.exit_time = datetime.now()
        ticket.spot.unpark()
        
        fee = self.pricing.calculate_fee(ticket.get_duration_hours())
        return ticket, fee
    
    def get_vehicle_location(self, license_plate: str) -> Optional[ParkingSpot]:
        """Find where a vehicle is parked. O(1)"""
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
        """
        Change pricing strategy (Strategy Pattern).
        
        Can be changed at runtime without modifying ParkingLot.
        """
        self.pricing = strategy
    
    def display_status(self) -> None:
        """Print parking lot status."""
        print(f"\n{'='*50}")
        print("PARKING LOT STATUS")
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


# ============ Demo ============
def main():
    """Demonstrate parking lot functionality."""
    print("=" * 60)
    print("MULTI-LEVEL PARKING LOT DEMO")
    print("=" * 60)
    
    # Create parking lot with hourly pricing
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
    print("\n" + "=" * 60)
    print("PARKING VEHICLES")
    print("=" * 60)
    
    tickets = []
    for vehicle in vehicles:
        ticket = lot.park_vehicle(vehicle)
        if ticket:
            tickets.append(ticket)
            print(f"✓ Parked {vehicle.license_plate} ({vehicle.vehicle_type.name}) at {ticket.spot}")
        else:
            print(f"✗ Could not park {vehicle.license_plate}")
    
    lot.display_status()
    
    # Find vehicle location (O(1) lookup!)
    print("\n" + "=" * 60)
    print("FIND VEHICLE (O(1) Lookup)")
    print("=" * 60)
    spot = lot.get_vehicle_location("CAR-001")
    print(f"CAR-001 is at: {spot}")
    
    # Unpark and calculate fee
    print("\n" + "=" * 60)
    print("UNPARK VEHICLE")
    print("=" * 60)
    
    import time
    time.sleep(1)  # Simulate parking time
    
    ticket, fee = lot.unpark_vehicle("CAR-001")
    if ticket:
        print(f"Unparked: {ticket}")
        print(f"Fee: ${fee:.2f} ({lot.pricing.name})")
    
    # Change pricing strategy at runtime
    print("\n" + "=" * 60)
    print("CHANGE PRICING STRATEGY (Strategy Pattern)")
    print("=" * 60)
    lot.set_pricing_strategy(FlatRatePricing(20.0))
    print(f"New pricing: {lot.pricing.name}")
    
    ticket, fee = lot.unpark_vehicle("CAR-002")
    if ticket:
        print(f"Fee with flat rate: ${fee:.2f}")
    
    lot.display_status()


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

**SAY THIS:**
> "Let me discuss the edge cases I've handled."

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Park same vehicle twice** | Raise ValueError | `park_vehicle()` check |
| **Unpark non-existent vehicle** | Return (None, 0) | `unpark_vehicle()` |
| **Parking full** | Return None | `park_vehicle()` |
| **Bus in compact spot** | `can_fit()` returns False | `ParkingSpot.can_fit()` |
| **Invalid lot configuration** | Raise ValueError | `__init__()` validation |
| **Zero duration parking** | Minimum 1 hour fee | `HourlyPricing.calculate_fee()` |

**Spot Compatibility Explanation:**
> "A Bus can ONLY fit in LARGE spots.
> A Car can fit in COMPACT, LARGE, or HANDICAPPED.
> A Motorcycle can fit anywhere."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest
from datetime import datetime, timedelta

class TestParkingLot:
    
    def test_park_vehicle_success(self):
        """Vehicle parks and ticket is issued."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        car = Vehicle("ABC123", VehicleType.CAR)
        
        ticket = lot.park_vehicle(car)
        
        assert ticket is not None
        assert ticket.vehicle == car
        assert lot.get_available_count() == 4
    
    def test_park_vehicle_when_full(self):
        """Returns None when parking is full."""
        lot = ParkingLot(levels=1, spots_per_level=1)
        lot.park_vehicle(Vehicle("A", VehicleType.MOTORCYCLE))
        
        result = lot.park_vehicle(Vehicle("B", VehicleType.MOTORCYCLE))
        
        assert result is None
    
    def test_park_same_vehicle_twice_raises(self):
        """Cannot park same vehicle twice."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        car = Vehicle("ABC123", VehicleType.CAR)
        lot.park_vehicle(car)
        
        with pytest.raises(ValueError):
            lot.park_vehicle(car)
    
    def test_unpark_vehicle_returns_fee(self):
        """Unpark returns ticket and correct fee."""
        lot = ParkingLot(levels=1, spots_per_level=5, 
                        pricing_strategy=HourlyPricing(10.0))
        car = Vehicle("ABC123", VehicleType.CAR)
        lot.park_vehicle(car)
        
        ticket, fee = lot.unpark_vehicle("ABC123")
        
        assert ticket is not None
        assert fee >= 10.0  # At least 1 hour
        assert lot.get_available_count() == 5  # Spot freed
    
    def test_unpark_nonexistent_vehicle(self):
        """Returns (None, 0) for non-existent vehicle."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        
        ticket, fee = lot.unpark_vehicle("NOTFOUND")
        
        assert ticket is None
        assert fee == 0
    
    def test_spot_compatibility_bus_large_only(self):
        """Bus only fits in LARGE spots."""
        large_spot = ParkingSpot(1, SpotType.LARGE)
        compact_spot = ParkingSpot(2, SpotType.COMPACT)
        bus = Vehicle("BUS1", VehicleType.BUS)
        
        assert large_spot.can_fit(bus) == True
        assert compact_spot.can_fit(bus) == False
    
    def test_vehicle_lookup_O1(self):
        """Vehicle lookup is O(1) using dictionary."""
        lot = ParkingLot(levels=3, spots_per_level=100)
        
        # Park many vehicles
        for i in range(250):
            lot.park_vehicle(Vehicle(f"CAR-{i}", VehicleType.CAR))
        
        # Lookup should be O(1), not O(N)
        spot = lot.get_vehicle_location("CAR-100")
        assert spot is not None
    
    def test_pricing_strategy_change(self):
        """Pricing strategy can be changed at runtime."""
        lot = ParkingLot(levels=1, spots_per_level=5)
        
        hourly = HourlyPricing(5.0)
        flat = FlatRatePricing(20.0)
        
        assert hourly.calculate_fee(2.0) == 10.0
        assert flat.calculate_fee(2.0) == 20.0
        
        lot.set_pricing_strategy(flat)
        assert lot.pricing == flat
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Operation | Time | Space |
|-----------|------|-------|
| `park_vehicle` | O(L × S) | O(1) |
| `unpark_vehicle` | **O(1)** | O(1) |
| `get_vehicle_location` | **O(1)** | O(1) |
| `get_available_count` | O(L × S) | O(1) |
| `is_full` | O(L × S) | O(1) |

**Where:** L = levels, S = spots per level

**Why O(1) for unpark?**
> "Because I use `vehicle_tickets` dictionary:
> - Maps license_plate → Ticket
> - Ticket has reference to ParkingSpot
> - No searching through all spots needed!"

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add reservations?"**

```python
@dataclass
class ParkingSpot:
    reserved_for: Optional[str] = None  # license plate
    reservation_time: Optional[datetime] = None
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        # Check reservation
        if self.reserved_for and self.reserved_for != vehicle.license_plate:
            if self.reservation_time and datetime.now() < self.reservation_time:
                return False  # Reserved for someone else
        # ... rest of logic

class ParkingLot:
    def reserve_spot(self, license_plate: str, time: datetime) -> Optional[ParkingSpot]:
        """Reserve a spot for future arrival."""
        for level in self.levels:
            for spot in level.spots:
                if spot.is_available() and not spot.reserved_for:
                    spot.reserved_for = license_plate
                    spot.reservation_time = time
                    return spot
        return None
```

---

#### **Q2: "How would you add EV charging?"**

```python
class SpotType(Enum):
    COMPACT = auto()
    LARGE = auto()
    HANDICAPPED = auto()
    EV_CHARGING = auto()  # New type

@dataclass
class EVChargingSpot(ParkingSpot):
    charging_rate_kw: float = 7.2
    is_charging: bool = False
    
    def start_charging(self) -> None:
        self.is_charging = True
    
    def stop_charging(self) -> float:
        """Returns kWh consumed."""
        self.is_charging = False
        # Calculate based on duration
        return hours * self.charging_rate_kw
```

---

#### **Q3: "How would you add a display board?"**

```python
class DisplayBoard:
    """Real-time availability display (Observer Pattern)."""
    
    def __init__(self, parking_lot: ParkingLot):
        self.lot = parking_lot
    
    def show(self) -> str:
        lines = ["=== PARKING AVAILABILITY ==="]
        for level in self.lot.levels:
            avail = level.get_available_count()
            lines.append(f"Level {level.level_number}: {avail} spots")
        return "\n".join(lines)
    
    def update(self) -> None:
        """Called when parking state changes."""
        print(self.show())
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: O(N) Vehicle Lookup** ❌

```python
# WRONG - Search all spots to find vehicle!
def unpark_vehicle(self, license_plate):
    for level in self.levels:
        for spot in level.spots:
            if spot.vehicle and spot.vehicle.license_plate == license_plate:
                # Found it after O(L × S) search!
                ...

# CORRECT - O(1) dictionary lookup
def unpark_vehicle(self, license_plate):
    ticket = self.vehicle_tickets.get(license_plate)  # O(1)
    if ticket:
        ticket.spot.unpark()
        ...
```

---

### **MISTAKE 2: Hardcoded Pricing** ❌

```python
# WRONG - Can't change pricing without modifying class
class ParkingLot:
    def calculate_fee(self, hours):
        return hours * 5  # Hardcoded $5/hr

# CORRECT - Strategy Pattern
class ParkingLot:
    def __init__(self, pricing: PricingStrategy):
        self.pricing = pricing
    
    def calculate_fee(self, hours):
        return self.pricing.calculate_fee(hours)  # Delegated
```

---

### **MISTAKE 3: Not Validating Spot Compatibility** ❌

```python
# WRONG - Any vehicle in any spot
def park(self, vehicle):
    self.vehicle = vehicle  # Bus in Compact?!

# CORRECT - Check compatibility first
def park(self, vehicle):
    if not self.can_fit(vehicle):
        return False
    self.vehicle = vehicle
    return True
```

---

## 💯 Interview Checklist

- [ ] ✅ **Clarified requirements** (vehicle types, spot types, pricing)
- [ ] ✅ **Used Strategy Pattern** for pricing
- [ ] ✅ **Used Dictionary** for O(1) vehicle lookup
- [ ] ✅ **Implemented spot compatibility** rules
- [ ] ✅ **Created Ticket system** for tracking
- [ ] ✅ **Handled edge cases** (full lot, duplicate park)
- [ ] ✅ **Mentioned thread safety** (locks for concurrent access)
- [ ] ✅ **Discussed extensions** (reservations, EV, display)
- [ ] ✅ **Analyzed complexity** (O(1) for unpark)

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                  PARKING LOT CHEAT SHEET                   │
├────────────────────────────────────────────────────────────┤
│ KEY DESIGN PATTERN:                                        │
│   Strategy Pattern for pricing                             │
│   - HourlyPricing, FlatRatePricing, SurgePricing          │
│   - Change at runtime without modifying ParkingLot        │
│                                                            │
│ O(1) VEHICLE LOOKUP:                                      │
│   vehicle_tickets: Dict[license_plate, Ticket]            │
│   Ticket contains: vehicle, spot, entry_time              │
│                                                            │
│ SPOT COMPATIBILITY:                                       │
│   COMPACT: Motorcycle, Car                                │
│   LARGE: All vehicles (including Bus)                     │
│   HANDICAPPED: Motorcycle, Car (not Bus)                  │
│                                                            │
│ SPOT DISTRIBUTION:                                        │
│   60% Compact, 30% Large, 10% Handicapped                 │
│                                                            │
│ COMPLEXITY:                                               │
│   - park_vehicle: O(L × S) to find spot                   │
│   - unpark_vehicle: O(1) via dictionary                   │
│   - get_vehicle_location: O(1) via dictionary             │
│                                                            │
│ EXTENSIONS:                                               │
│   - Reservations (reserved_for field)                     │
│   - EV Charging (new spot type + charging logic)          │
│   - Display Board (Observer Pattern)                      │
└────────────────────────────────────────────────────────────┘
```

---

**Design Patterns Used:**
- Strategy Pattern (Pricing)
- Factory Pattern (Vehicle creation)
- Observer Pattern (Display Board extension)

**Related Problems:**
- Design Parking Garage
- Design Valet Parking System
- Design Bike Rental System

