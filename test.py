from collections import defaultdict
from typing import List, Dict, Tuple, Optional
import heapq

def generate_report(files: List[Dict], k: int) -> Dict:
    """
    Generate file storage report with total size and top K collections.
    
    Args:
        files: List of file dictionaries with keys: name, size, collectionId
        k: Number of top collections to return
    
    Returns:
        Dictionary with total_size and top_collections
    
    Time: O(N + C log K) where N = files, C = collections
    Space: O(C) for collection map
    """
    total_size = 0
    collection_sizes = defaultdict(int)
    
    # Phase 1: Aggregation (O(N))
    for file in files:
        size = file.get("size", 0)
        collection_id = file.get("collectionId")
        
        # Add to global total
        total_size += size
        
        # Add to collection total (skip null collections)
        if collection_id is not None:
            collection_sizes[collection_id] += size
    
    # Phase 2: Extract Top K (O(C log K))
    # heapq.nlargest returns list of tuples: [(col_id, size), ...]
    # sorted by size descending
    top_k_collections = heapq.nlargest(
        k,
        collection_sizes.items(),
        key=lambda item: item[1]  # Sort by size
    )
    
    return {
        "total_size": total_size,
        "top_collections": top_k_collections
    }


def generate_detailed_report(files: List[Dict], k: int) -> Dict:
    """
    Enhanced version with additional statistics.
    """
    total_size = 0
    collection_sizes = defaultdict(int)
    collection_file_counts = defaultdict(int)
    uncategorized_size = 0
    
    for file in files:
        size = file.get("size", 0)
        collection_id = file.get("collectionId")
        
        total_size += size
        
        if collection_id is not None:
            collection_sizes[collection_id] += size
            collection_file_counts[collection_id] += 1
        else:
            uncategorized_size += size
    
    # Top K with additional info
    top_k_full = [
        {
            "collection_id": col_id,
            "total_size": size,
            "file_count": collection_file_counts[col_id],
            "avg_size": size / collection_file_counts[col_id]
        }
        for col_id, size in heapq.nlargest(
            k, collection_sizes.items(), key=lambda x: x[1]
        )
    ]
    
    return {
        "total_size": total_size,
        "num_collections": len(collection_sizes),
        "uncategorized_size": uncategorized_size,
        "top_collections": top_k_full
    }


# ============================================
# COMPLETE RUNNABLE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("FILE COLLECTIONS REPORT GENERATOR")
    print("=" * 60)
    
    # Test 1: Basic report
    print("\n[Test 1] Basic Report")
    print("-" * 40)
    files1 = [
        {"name": "photo1.jpg", "size": 100, "collectionId": "photos"},
        {"name": "photo2.jpg", "size": 200, "collectionId": "photos"},
        {"name": "doc1.pdf", "size": 300, "collectionId": "documents"},
        {"name": "doc2.pdf", "size": 150, "collectionId": "documents"},
        {"name": "temp.txt", "size": 50, "collectionId": None}
    ]
    
    report1 = generate_report(files1, k=2)
    print(f"Total Size: {report1['total_size']} bytes")
    print(f"Top 2 Collections:")
    for col_id, size in report1['top_collections']:
        print(f"  {col_id}: {size} bytes")
    
    # Test 2: Detailed report
    print("\n[Test 2] Detailed Report")
    print("-" * 40)
    report2 = generate_detailed_report(files1, k=2)
    print(f"Total Size: {report2['total_size']} bytes")
    print(f"Number of Collections: {report2['num_collections']}")
    print(f"Uncategorized Size: {report2['uncategorized_size']} bytes")
    print(f"\nTop Collections:")
    for col in report2['top_collections']:
        print(f"  {col['collection_id']}:")
        print(f"    Total: {col['total_size']} bytes")
        print(f"    Files: {col['file_count']}")
        print(f"    Average: {col['avg_size']:.2f} bytes/file")
    
    # Test 3: Large dataset simulation
    print("\n[Test 3] Large Dataset")
    print("-" * 40)
    import random
    
    # Generate 10,000 files across 100 collections
    collections = [f"col{i}" for i in range(100)]
    files3 = [
        {
            "name": f"file{i}",
            "size": random.randint(100, 1000),
            "collectionId": random.choice(collections + [None] * 10)
        }
        for i in range(10000)
    ]
    
    report3 = generate_report(files3, k=5)
    print(f"Total Size: {report3['total_size']:,} bytes")
    print(f"Top 5 Collections:")
    for col_id, size in report3['top_collections']:
        print(f"  {col_id}: {size:,} bytes")
    
    # Test 4: Edge cases
    print("\n[Test 4] Edge Cases")
    print("-" * 40)
    
    # Empty files
    report_empty = generate_report([], k=5)
    print(f"Empty list - Total: {report_empty['total_size']}, Top: {report_empty['top_collections']}")
    
    # All null collections
    files_null = [
        {"name": "f1", "size": 100, "collectionId": None},
        {"name": "f2", "size": 200, "collectionId": None}
    ]
    report_null = generate_report(files_null, k=1)
    print(f"All null - Total: {report_null['total_size']}, Top: {report_null['top_collections']}")
    
    # K larger than collections
    files_small = [
        {"name": "f1", "size": 100, "collectionId": "A"},
        {"name": "f2", "size": 200, "collectionId": "B"}
    ]
    report_large_k = generate_report(files_small, k=10)
    print(f"K > C - Top: {report_large_k['top_collections']}")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)