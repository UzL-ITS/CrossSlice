#!/usr/bin/env python3
"""
Variable Mapping Creation During Statement Merging

This module creates comprehensive variable mappings between old and new statements
during the merge process, taking into account variable IDs, scopes, and statement
matching relationships.
"""

import json
from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict


class VariableMappingBuilder:
    """
    Builds comprehensive variable mappings during the merge process.
    """
    
    def __init__(self):
        # Main mapping: var_id -> generic_name
        self.var_id_to_generic: Dict[str, str] = {}
        
        # Tracking mappings
        self.old_var_id_to_new_var_id: Dict[str, str] = {}  # old var_id -> new var_id (for matched statements)
        self.var_name_to_var_ids: Dict[str, Set[str]] = defaultdict(set)  # name -> set of var_ids
        self.var_id_to_name: Dict[str, str] = {}  # var_id -> original name
        
        # Context tracking
        self.var_id_to_context: Dict[str, Dict[str, Any]] = {}  # var_id -> context info
        
        # Generic name counter
        self.generic_counter = 1
        
    def build_mapping_during_merge(self, old_stmts: List[Dict[str, Any]], 
                                 new_stmts: List[Dict[str, Any]], 
                                 match_pairs: List[Tuple[str, str]]) -> Dict[str, str]:
        """
        Build variable mapping during the merge process.
        
        Args:
            old_stmts: List of old statements
            new_stmts: List of new statements  
            match_pairs: List of (old_id, new_id) pairs for matched statements
            
        Returns:
            Dictionary mapping var_id -> generic_name
        """
        print("Building variable mapping during merge...")
        
        # Step 1: Collect all variables from new statements (these take priority)
        new_stmt_map = {stmt['id']: stmt for stmt in new_stmts}
        old_stmt_map = {stmt['id']: stmt for stmt in old_stmts}
        
        # Step 2: Process matched statements to build old->new var_id mappings
        self._build_old_to_new_mappings(match_pairs, old_stmt_map, new_stmt_map)
        
        # Step 3: Collect all variables from new statements first
        self._collect_variables_from_statements(new_stmts, context="new")
        
        # Step 4: Collect variables from old statements and map them
        self._collect_variables_from_statements(old_stmts, context="old")
        
        # Step 5: Create generic names based on collected variables
        self._create_generic_mappings()
        
        print(f"Created mappings for {len(self.var_id_to_generic)} variable IDs")
        return self.var_id_to_generic
    
    def _build_old_to_new_mappings(self, match_pairs: List[Tuple[str, str]], 
                                 old_stmt_map: Dict[str, Dict], 
                                 new_stmt_map: Dict[str, Dict]):
        """
        Build mappings between old and new var_ids for matched statements.
        """
        for old_stmt_id, new_stmt_id in match_pairs:
            old_stmt = old_stmt_map.get(old_stmt_id)
            new_stmt = new_stmt_map.get(new_stmt_id)
            
            if not old_stmt or not new_stmt:
                continue
                
            # Map variables by name within matched statements
            old_vars = self._extract_all_variables_from_statement(old_stmt)
            new_vars = self._extract_all_variables_from_statement(new_stmt)
            
            # Group by variable name
            old_vars_by_name = defaultdict(list)
            new_vars_by_name = defaultdict(list)
            
            for var in old_vars:
                old_vars_by_name[var['name']].append(var['var_id'])
            for var in new_vars:
                new_vars_by_name[var['name']].append(var['var_id'])
            
            # Map old var_ids to new var_ids for same names
            for name, old_var_ids in old_vars_by_name.items():
                if name in new_vars_by_name:
                    new_var_ids = new_vars_by_name[name]
                    # Simple 1:1 mapping (could be enhanced for complex cases)
                    for i, old_var_id in enumerate(old_var_ids):
                        if i < len(new_var_ids):
                            self.old_var_id_to_new_var_id[old_var_id] = new_var_ids[i]
    
    def _collect_variables_from_statements(self, statements: List[Dict[str, Any]], context: str):
        """
        Collect all variables from a list of statements.
        """
        for stmt in statements:
            variables = self._extract_all_variables_from_statement(stmt)
            
            for var in variables:
                var_id = var['var_id']
                var_name = var['name']
                
                # Store basic info
                self.var_id_to_name[var_id] = var_name
                self.var_name_to_var_ids[var_name].add(var_id)
                
                # Store context
                self.var_id_to_context[var_id] = {
                    'name': var_name,
                    'context': context,
                    'statement_id': stmt['id'],
                    'source': var.get('source', 'unknown')
                }
    
    def _extract_all_variables_from_statement(self, stmt: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract all variables from a statement and its parts.
        """
        variables = []
        
        # Extract from main statement
        variables.extend(self._extract_variables_from_container(stmt, "main"))
        
        # Extract from parts
        for part in stmt.get("parts", []):
            variables.extend(self._extract_variables_from_container(part, "part"))
            
        return variables
    
    def _extract_variables_from_container(self, container: Dict[str, Any], source: str) -> List[Dict[str, Any]]:
        """Extract variables from left_side, right_side, and parameters of a container."""
        variables = []
        
        # Extract from left_side and right_side
        for side in ["left_side", "right_side"]:
            for var in container.get(side, []):
                if var.get("var_id") and var.get("name") and var.get("id_type") == "variable":
                    variables.append({
                        "name": var["name"],
                        "var_id": var["var_id"],
                        "source": f"{source}_{side}"
                    })
        
        # Extract from parameters
        for param in container.get("parameters", []):
            if param.get("var_id") and param.get("name"):
                variables.append({
                    "name": param["name"],
                    "var_id": param["var_id"],
                    "source": f"{source}_parameter"
                })
        
        return variables
    
    def _create_generic_mappings(self):
        """
        Create generic variable names based on collected variable information.
        Priority: new statements > old statements, with proper var_id handling.
        """
        processed_var_ids = set()
        
        # Step 1: Process variables from new statements first (higher priority)
        new_var_ids = [var_id for var_id, context in self.var_id_to_context.items()
                       if context['context'] == 'new']  # statement order, so VAR_n numbering is stable
        
        # Group new variables by name to ensure same names get same generic name
        # unless they have different var_ids (different scope/instances)
        new_vars_by_name = defaultdict(list)
        for var_id in new_var_ids:
            name = self.var_id_to_name[var_id]
            new_vars_by_name[name].append(var_id)
        
        # Assign generic names to new variables
        for name, var_ids in new_vars_by_name.items():
            if len(var_ids) == 1:
                # Single variable with this name
                var_id = var_ids[0]
                generic_name = f"VAR_{self.generic_counter}"
                self.var_id_to_generic[var_id] = generic_name
                processed_var_ids.add(var_id)
                self.generic_counter += 1
            else:
                # Multiple variables with same name but different var_ids
                for var_id in var_ids:
                    generic_name = f"VAR_{self.generic_counter}"
                    self.var_id_to_generic[var_id] = generic_name
                    processed_var_ids.add(var_id)
                    self.generic_counter += 1
        
        # Step 2: Process old variables
        old_var_ids = [var_id for var_id, context in self.var_id_to_context.items()
                       if context['context'] == 'old' and var_id not in processed_var_ids]
        
        for var_id in old_var_ids:
            # Check if this old var_id maps to a new var_id
            if var_id in self.old_var_id_to_new_var_id:
                new_var_id = self.old_var_id_to_new_var_id[var_id]
                if new_var_id in self.var_id_to_generic:
                    # Use the same generic name as the corresponding new variable
                    self.var_id_to_generic[var_id] = self.var_id_to_generic[new_var_id]
                    continue
            
            # Check if there's a new variable with the same name (fallback)
            old_var_name = self.var_id_to_name[var_id]
            found_matching_new = False
            
            for new_var_id in new_var_ids:
                if (new_var_id in self.var_id_to_generic and 
                    self.var_id_to_name[new_var_id] == old_var_name):
                    # Use the same generic name as the new variable with same name
                    self.var_id_to_generic[var_id] = self.var_id_to_generic[new_var_id]
                    found_matching_new = True
                    break
            
            if not found_matching_new:
                # Old variable has no corresponding new variable (deleted)
                generic_name = f"VAR_{self.generic_counter}"
                self.var_id_to_generic[var_id] = generic_name
                self.generic_counter += 1
    
    def get_mapping_summary(self) -> Dict[str, Any]:
        """Get a summary of the variable mapping for debugging."""
        return {
            'total_variables': len(self.var_id_to_generic),
            'old_to_new_mappings': len(self.old_var_id_to_new_var_id),
            'unique_names': len(set(self.var_id_to_name.values())),
            'generic_names_used': self.generic_counter - 1,
            'name_to_generic_sample': {
                name: self.var_id_to_generic.get(min(var_ids), 'N/A')
                for name, var_ids in list(self.var_name_to_var_ids.items())[:5]
            }
        }


# Integration functions for merge_v4.py
def create_variable_mapping_during_merge(old_stmts: List[Dict[str, Any]], 
                                       new_stmts: List[Dict[str, Any]], 
                                       match_pairs: List[Tuple[str, str]]) -> Dict[str, str]:
    """
    Create variable mapping during the merge process.
    
    This function should be called from merge_v4.py during the merging process.
    
    Args:
        old_stmts: List of old statements
        new_stmts: List of new statements
        match_pairs: List of (old_id, new_id) tuples for matched statements
        
    Returns:
        Dictionary mapping var_id -> generic_name
    """
    builder = VariableMappingBuilder()
    mapping = builder.build_mapping_during_merge(old_stmts, new_stmts, match_pairs)
    
    # Print summary
    summary = builder.get_mapping_summary()
    print(f"Variable mapping summary: {summary}")
    
    return mapping


if __name__ == "__main__":
    # Test with sample data
    old_stmts = [
        {
            "id": "old1",
            "type": "declaration",
            "expression": "int x = 5;",
            "left_side": [{"name": "x", "var_id": "old_var_1", "id_type": "variable"}],
            "right_side": [],
            "parts": [],
            "match_id": "new1"
        }
    ]
    
    new_stmts = [
        {
            "id": "new1", 
            "type": "declaration",
            "expression": "int x = 10;",
            "left_side": [{"name": "x", "var_id": "new_var_1", "id_type": "variable"}],
            "right_side": [],
            "parts": [],
            "match_id": "old1"
        }
    ]
    
    match_pairs = [("old1", "new1")]
    
    mapping = create_variable_mapping_during_merge(old_stmts, new_stmts, match_pairs)
    print(f"Generated mapping: {mapping}")
