class Bucket:
    def __init__(self, count):
        self.count = count
        self.items = set()
        self.prev = None
        self.next = None

class PopularityTracker:
    def __init__(self):
        # Dummy nodes
        self.head = Bucket(float('-inf'))
        self.tail = Bucket(float('inf'))
        self.head.next = self.tail
        self.tail.prev = self.head

        # Maps item -> bucket
        self.item_bucket = {}

    # Insert new bucket after a given node
    def _insert_after(self, prevBucket, newBucket):
        nxt = prevBucket.next
        prevBucket.next = newBucket
        newBucket.prev = prevBucket
        newBucket.next = nxt
        nxt.prev = newBucket

    # Remove bucket if empty
    def _remove_if_empty(self, bucket):
        if len(bucket.items) == 0 and bucket != self.head and bucket != self.tail:
            bucket.prev.next = bucket.next
            bucket.next.prev = bucket.prev

    def increase(self, item):
        # Item first time → goes to bucket 1
        if item not in self.item_bucket:
            first = self.head.next
            if first == self.tail or first.count != 1:
                newBucket = Bucket(1)
                self._insert_after(self.head, newBucket)
                first = newBucket
            first.items.add(item)
            self.item_bucket[item] = first
            return

        # Item already has some count
        currBucket = self.item_bucket[item]
        nextBucket = currBucket.next

        # Need a new bucket?
        if nextBucket == self.tail or nextBucket.count != currBucket.count + 1:
            newBucket = Bucket(currBucket.count + 1)
            self._insert_after(currBucket, newBucket)
            nextBucket = newBucket

        # Move item
        currBucket.items.remove(item)
        nextBucket.items.add(item)
        self.item_bucket[item] = nextBucket

        # Cleanup
        self._remove_if_empty(currBucket)

    def decrease(self, item):
        if item not in self.item_bucket:
            return

        currBucket = self.item_bucket[item]

        # If count falls to zero → remove completely
        if currBucket.count == 1:
            currBucket.items.remove(item)
            del self.item_bucket[item]
            self._remove_if_empty(currBucket)
            return

        # Move to previous bucket
        prevBucket = currBucket.prev
        if prevBucket == self.head or prevBucket.count != currBucket.count - 1:
            newBucket = Bucket(currBucket.count - 1)
            self._insert_after(currBucket.prev, newBucket)
            prevBucket = newBucket

        currBucket.items.remove(item)
        prevBucket.items.add(item)
        self.item_bucket[item] = prevBucket

        self._remove_if_empty(currBucket)

    def mostPopular(self):
        maxBucket = self.tail.prev
        if maxBucket == self.head:
            return None
        return next(iter(maxBucket.items))


