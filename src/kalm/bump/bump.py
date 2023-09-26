import os
from pprint import pprint
import toml 

def major():  
    print("major")
    with open('pyproject.toml', 'r') as toml_file:
        data = toml.load(toml_file)
    # Bump the version numbers
    if 'project' in data and 'version' in data['project']:
        current_version = data['project']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            major += 1
            minor = 0
            patch = 0

            new_version = f'{major}.{minor}.{patch}'
            data['project']['version'] = new_version

    if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
        current_version = data['tool']['poetry']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            major += 1
            minor = 0
            patch = 0

            new_version = f'{major}.{minor}.{patch}'
            data['tool']['poetry']['version'] = new_version
    # Save the modified pyproject.toml file
    print(data['project']['version'])
    print(data['tool']['poetry']['version'])

    with open('pyproject.toml', 'w') as toml_file:
        toml.dump(data, toml_file)

def minor():
    print("minor")
    with open('pyproject.toml', 'r') as toml_file:
        data = toml.load(toml_file)
    # Bump the version numbers
    if 'project' in data and 'version' in data['project']:
        current_version = data['project']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            minor += 1
            patch = 0

            new_version = f'{major}.{minor}.{patch}'
            data['project']['version'] = new_version

    if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
        current_version = data['tool']['poetry']['version']
        parts = current_version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            minor += 1  
            patch = 0

            new_version = f'{major}.{minor}.{patch}'
            data['tool']['poetry']['version'] = new_version
    # Save the modified pyproject.toml file
    print(data['project']['version'])
    print(data['tool']['poetry']['version'])
    with open('pyproject.toml', 'w') as toml_file:
        toml.dump(data, toml_file)


def patch():
  with open('pyproject.toml', 'r') as toml_file:
    data = toml.load(toml_file)

  # Bump the version numbers
  if 'project' in data and 'version' in data['project']:
    current_version = data['project']['version']
    parts = current_version.split('.')
    if len(parts) == 3:
      major, minor, patch = map(int, parts)
      patch += 1
      new_version = f'{major}.{minor}.{patch}'
      data['project']['version'] = new_version

  if 'tool' in data and 'poetry' in data['tool'] and 'version' in data['tool']['poetry']:
    current_version = data['tool']['poetry']['version']
    parts = current_version.split('.')
    if len(parts) == 3:
        major, minor, patch = map(int, parts)
        patch += 1
        new_version = f'{major}.{minor}.{patch}'
        data['tool']['poetry']['version'] = new_version

  # Save the modified pyproject.toml file
  print(data['project']['version'])
  print(data['tool']['poetry']['version'])
  with open('pyproject.toml', 'w') as toml_file:
    toml.dump(data, toml_file)
