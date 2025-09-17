#!/usr/bin/env python3
"""
Test script for SPDX taxonomy synchronization
This script simulates the workflow locally for testing
"""

import yaml
import os
import glob
import shutil
import tempfile
from pathlib import Path

class TaxonomySyncTester:
    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix='taxonomy_test_')
        self.taxonomy_dir = os.path.join(self.test_dir, 'taxonomy')
        self.detection_dir = os.path.join(self.test_dir, 'detection')
        os.makedirs(self.taxonomy_dir)
        os.makedirs(self.detection_dir)
        print(f"Test directory created: {self.test_dir}")

    def cleanup(self):
        """Remove test directory"""
        shutil.rmtree(self.test_dir)
        print("Test directory cleaned up")

    def create_taxonomy_file(self, algo_id, name=None, category=None):
        """Create a taxonomy YAML file"""
        data = {'id': algo_id}
        if name:
            data['name'] = name
        if category:
            data['category'] = category

        file_path = os.path.join(self.taxonomy_dir, f'{algo_id}.yaml')
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        return file_path

    def create_detection_file(self, algo_id, keywords=None):
        """Create a detection YAML file"""
        if keywords is None:
            keywords = [algo_id]

        data = {
            'id': algo_id,
            'keywords': keywords
        }

        file_path = os.path.join(self.detection_dir, f'{algo_id}.yaml')
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        return file_path

    def run_sync(self):
        """Run the synchronization logic"""
        def load_yaml(file_path):
            try:
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            except:
                return None

        def save_yaml(file_path, data):
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        # Get all algorithm IDs from taxonomy
        taxonomy_algorithms = {}
        for yaml_file in glob.glob(f'{self.taxonomy_dir}/**/*.yaml', recursive=True):
            data = load_yaml(yaml_file)
            if data and 'id' in data:
                taxonomy_algorithms[data['id']] = {
                    'name': data.get('name', ''),
                    'category': data.get('category', ''),
                    'file': yaml_file
                }

        # Get all existing detection files
        existing_detections = {}
        for yaml_file in glob.glob(f'{self.detection_dir}/*.yaml'):
            data = load_yaml(yaml_file)
            if data and 'id' in data:
                existing_detections[data['id']] = yaml_file

        changes = []

        # Find new algorithms to add
        for algo_id, algo_info in taxonomy_algorithms.items():
            if algo_id not in existing_detections:
                detection_file = f'{self.detection_dir}/{algo_id}.yaml'
                detection_data = {
                    'id': algo_id,
                    'keywords': [algo_id]
                }
                save_yaml(detection_file, detection_data)
                changes.append(f'Added: {algo_id}')

        # Find algorithms to remove
        for algo_id, detection_file in existing_detections.items():
            if algo_id not in taxonomy_algorithms:
                os.remove(detection_file)
                changes.append(f'Removed: {algo_id}')

        return changes

    def test_add_new_algorithm(self):
        """Test adding a new algorithm"""
        print("\n=== Test: Add New Algorithm ===")

        # Setup: Create taxonomy entry but no detection
        self.create_taxonomy_file('new-algo-1', 'New Algorithm 1', 'Hash')

        # Run sync
        changes = self.run_sync()

        # Verify
        detection_file = os.path.join(self.detection_dir, 'new-algo-1.yaml')
        assert os.path.exists(detection_file), "Detection file should be created"
        assert 'Added: new-algo-1' in changes, "Change should be recorded"
        print("✅ New algorithm detection file created successfully")

    def test_remove_deleted_algorithm(self):
        """Test removing a deleted algorithm"""
        print("\n=== Test: Remove Deleted Algorithm ===")

        # Setup: Create detection but no taxonomy
        self.create_detection_file('old-algo-1', ['old-algo-1', 'legacy'])

        # Run sync
        changes = self.run_sync()

        # Verify
        detection_file = os.path.join(self.detection_dir, 'old-algo-1.yaml')
        assert not os.path.exists(detection_file), "Detection file should be removed"
        assert 'Removed: old-algo-1' in changes, "Change should be recorded"
        print("✅ Obsolete detection file removed successfully")

    def test_sync_multiple_algorithms(self):
        """Test syncing multiple algorithms at once"""
        print("\n=== Test: Sync Multiple Algorithms ===")

        # Setup: Mix of new, existing, and obsolete
        self.create_taxonomy_file('algo-1', 'Algorithm 1')
        self.create_taxonomy_file('algo-2', 'Algorithm 2')
        self.create_detection_file('algo-2', ['algo-2'])  # Existing
        self.create_detection_file('algo-3', ['algo-3'])  # To be removed

        # Run sync
        changes = self.run_sync()

        # Verify
        assert os.path.exists(os.path.join(self.detection_dir, 'algo-1.yaml'))
        assert os.path.exists(os.path.join(self.detection_dir, 'algo-2.yaml'))
        assert not os.path.exists(os.path.join(self.detection_dir, 'algo-3.yaml'))
        assert len(changes) == 2  # 1 added, 1 removed
        print(f"✅ Multiple algorithms synced: {len(changes)} changes")

    def test_no_changes(self):
        """Test when everything is already in sync"""
        print("\n=== Test: No Changes Needed ===")

        # Setup: Everything in sync
        self.create_taxonomy_file('algo-1', 'Algorithm 1')
        self.create_detection_file('algo-1', ['algo-1'])

        # Run sync
        changes = self.run_sync()

        # Verify
        assert len(changes) == 0, "No changes should be detected"
        print("✅ Correctly detected no changes needed")

def main():
    """Run all tests"""
    print("Starting SPDX Taxonomy Sync Tests")
    print("=" * 50)

    tester = TaxonomySyncTester()

    try:
        # Run all test cases
        tester.test_add_new_algorithm()
        tester.test_remove_deleted_algorithm()
        tester.test_sync_multiple_algorithms()
        tester.test_no_changes()

        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        print("\nYou can now test the actual workflow with:")
        print("  1. Push changes to trigger the workflow")
        print("  2. Or run manually: gh workflow run sync-spdx-taxonomy.yml")
        print("  3. Or test locally: act -W .github/workflows/sync-spdx-taxonomy.yml")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    finally:
        tester.cleanup()

    return 0

if __name__ == '__main__':
    exit(main())