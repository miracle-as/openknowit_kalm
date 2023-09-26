import os
from pprint import pprint
import toml 

def major():  
    print("major")
    with open('pyproject.toml', 'r') as toml_file:
        data = toml.load(toml_file)
    # Bump the version numbers
    if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
        current_version = data['tool']['poetry']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            major += 1
            new_version = f'{major}.{minor}.{patch}'
            data['tool']['poetry']['version'] = new_version
    # Save the modified pyproject.toml file
    with open('pyproject.toml', 'w') as toml_file:
        toml.dump(data, toml_file)

def minor():
    print("minor")
    with open('pyproject.toml', 'r') as toml_file:
        data = toml.load(toml_file)
    # Bump the version numbers
    if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
        current_version = data['tool']['poetry']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            minor += 1
            new_version = f'{major}.{minor}.{patch}'
            data['tool']['poetry']['version'] = new_version
    # Save the modified pyproject.toml file
    with open('pyproject.toml', 'w') as toml_file:
        toml.dump(data, toml_file)

def patch():
  with open('pyproject.toml', 'r') as toml_file:
    data = toml.load(toml_file)

  # Bump the version numbers
  if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
    current_version = data['tool']['poetry']['version']
    parts = current_version.split('.')
    if len(parts) == 3:
        major, minor, patch = map(int, parts)
        patch += 1
        new_version = f'{major}.{minor}.{patch}'
        data['tool']['poetry']['version'] = new_version

  # Save the modified pyproject.toml file
  with open('pyproject.toml', 'w') as toml_file:
    toml.dump(data, toml_file)
