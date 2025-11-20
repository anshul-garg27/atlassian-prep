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

---

## 🎨 Visual Example

```text
Level 1:
[C1: Car] [C2: ___] [L1: Bus] [H1: ___]

Level 2:
[C3: Motorcycle] [C4: ___] [L2: ___] [H2: Car]

C = Compact, L = Large, H = Handicapped
___ = Empty
```

---

## 💻 Implementation

```java
enum VehicleSize {
    MOTORCYCLE, COMPACT, LARGE
}

enum SpotType {
    COMPACT, LARGE, HANDICAPPED
}

class Vehicle {
    String licensePlate;
    VehicleSize size;
}

class ParkingSpot {
    int spotNumber;
    SpotType type;
    Vehicle vehicle;
    
    boolean canFit(Vehicle v) {
        if (vehicle != null) return false;
        return (type == SpotType.LARGE) ||
               (type == SpotType.COMPACT && v.size != VehicleSize.LARGE) ||
               (type == SpotType.HANDICAPPED);
    }
    
    void park(Vehicle v) {
        this.vehicle = v;
    }
    
    void unpark() {
        this.vehicle = null;
    }
}

class ParkingLevel {
    int levelNumber;
    List<ParkingSpot> spots;
    
    Optional<ParkingSpot> findAvailableSpot(Vehicle v) {
        return spots.stream()
                .filter(spot -> spot.canFit(v))
                .findFirst();
    }
    
    int getAvailableCount() {
        return (int) spots.stream()
                .filter(spot -> spot.vehicle == null)
                .count();
    }
}

class ParkingLot {
    List<ParkingLevel> levels;
    Map<String, ParkingSpot> vehicleLocations; // licensePlate -> spot
    
    boolean parkVehicle(Vehicle v) {
        for (ParkingLevel level : levels) {
            Optional<ParkingSpot> spot = level.findAvailableSpot(v);
            if (spot.isPresent()) {
                spot.get().park(v);
                vehicleLocations.put(v.licensePlate, spot.get());
                return true;
            }
        }
        return false; // Parking full
    }
    
    boolean unparkVehicle(String licensePlate) {
        ParkingSpot spot = vehicleLocations.get(licensePlate);
        if (spot != null) {
            spot.unpark();
            vehicleLocations.remove(licensePlate);
            return true;
        }
        return false;
    }
    
    int getTotalAvailableSpots() {
        return levels.stream()
                .mapToInt(ParkingLevel::getAvailableCount)
                .sum();
    }
}
```

---

## 🚀 Extensions

### **1. Pricing Strategy**
```java
interface PricingStrategy {
    double calculateFee(long parkingDurationMs);
}

class HourlyPricing implements PricingStrategy {
    public double calculateFee(long durationMs) {
        long hours = durationMs / (1000 * 60 * 60);
        return hours * 5.0; // $5 per hour
    }
}
```

### **2. Display Board**
```java
class DisplayBoard {
    void showAvailability(ParkingLot lot) {
        for (ParkingLevel level : lot.levels) {
            System.out.println("Level " + level.levelNumber + 
                             ": " + level.getAvailableCount() + " spots");
        }
    }
}
```

### **3. Payment System**
```java
class Ticket {
    String ticketId;
    Vehicle vehicle;
    LocalDateTime entryTime;
    LocalDateTime exitTime;
    
    double calculateFee(PricingStrategy strategy) {
        long duration = Duration.between(entryTime, exitTime).toMillis();
        return strategy.calculateFee(duration);
    }
}
```

---

## 🧪 Testing

```java
@Test
public void testParkVehicle() {
    ParkingLot lot = new ParkingLot(3, 10); // 3 levels, 10 spots each
    Vehicle car = new Vehicle("ABC123", VehicleSize.COMPACT);
    
    assertTrue(lot.parkVehicle(car));
    assertEquals(29, lot.getTotalAvailableSpots());
}

@Test
public void testFullParking() {
    ParkingLot lot = new ParkingLot(1, 2);
    assertTrue(lot.parkVehicle(new Vehicle("A", VehicleSize.COMPACT)));
    assertTrue(lot.parkVehicle(new Vehicle("B", VehicleSize.COMPACT)));
    assertFalse(lot.parkVehicle(new Vehicle("C", VehicleSize.COMPACT)));
}
```

---

## 💡 Interview Tips

✅ Use **Strategy Pattern** for pricing
✅ **Enum** for vehicle/spot types
✅ **Map** for quick vehicle lookup
✅ Discuss **thread safety** (concurrent parking)
✅ Ask about peak hour multipliers, reserved spots

**Design Patterns:** Strategy, Factory, Singleton
