from typing import Dict, List

class EmployeeHierarchy:
    
    def __init__(self, data: Dict[str, List[str]], emp_to_group: Dict[str, str]):
        self.data = data
        self.emp_to_group = emp_to_group
        self.parent = {}  
        self.root = self._find_root()
        self._build_parents()

    def _find_root(self) -> str:
        children = set()
        for grp, subs in self.data.items():
            for s in subs:
                children.add(s)
        for grp in self.data:
            if grp not in children:
                return grp
        return None

    def _build_parents(self):
        for grp, subs in self.data.items():
            for s in subs:
                self.parent[s] = grp
        self.parent[self.root] = None

    def _get_path_to_root(self, group: str) -> List[str]:
        path = []
        while group is not None:
            path.append(group)
            group = self.parent[group]
        return path

    def closest_common_group(self, employees: List[str]) -> str:
        paths = []

        for emp in employees:
            group = self.emp_to_group[emp]
            paths.append(self._get_path_to_root(group))

        first_path = paths[0]
        common = set(first_path)

        for p in paths[1:]:
            common.intersection_update(p)

        for group in first_path:
            if group in common:
                return group

        return None
    
    
group_tree = {
    "Company": ["Engg", "HR", "Sales"],
    "Engg": ["Backend", "Frontend", "Mobile"],
    "Backend": [],
    "Frontend": [],
    "Mobile": [],
    "HR": [],
    "Sales": []
}

employee_to_group = {
    "Alice": "Backend",
    "Lisa": "Frontend",
    "Mike": "Mobile"
}


hier = EmployeeHierarchy(group_tree, employee_to_group)
print(hier.closest_common_group(["Alice", "Lisa"]))   # Engg
print(hier.closest_common_group(["Alice", "Mike"]))   # Engg
print(hier.closest_common_group(["Lisa"]))            # Frontend
