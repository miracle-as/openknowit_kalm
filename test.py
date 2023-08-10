import os
import stat
from PIL import Image
import redis

def is_text_file(file_path):
    # Get the file extension
    _, ext = os.path.splitext(file_path)

    # Common text file extensions
    text_extensions = ['.txt', '.csv', '.json', '.xml', '.log', '.html', '.htm', '.md', 'cfg', 'conf', 'yml', 'yaml']

    # Check if the extension matches a text file extension
    return ext.lower() in text_extensions


def is_named_pipe(file_path):
    try:
        file_stat = os.stat(file_path)
        return stat.S_ISFIFO(file_stat.st_mode)
    except FileNotFoundError:
        return False

def is_photo(file_path):
    print(file_path)
    try:
        with Image.open(file_path) as img:
            try:
                img.verify()
                return True
            except:
                return False
            return img.format in ("JPEG", "PNG", "GIF", "BMP", "ICO", "WEBP", "TIFF")
    except (IOError, SyntaxError):
        return False

def is_proc_file(file_path):
    return file_path.startswith('/proc/')

def is_device_file(file_path):
    return file_path.startswith('/dev/')

def has_read_permission(file_path):
    return os.access(file_path, os.R_OK)

def is_symbolic_link(file_path):
    return os.path.islink(file_path)

def ignore_file(file_path):
  if is_symbolic_link(file_path):
    return True
  if not has_read_permission(file_path):
    return True
  if is_proc_file(file_path):
    return True
  if is_device_file(file_path):
    return True
  return False

   

def find_files_on_device(device_path, r):
    
    ignored_files= ['']
    for root, _, files in os.walk(device_path):
        totalfiles=(len(files))
        counter=0
        for file in files:
            print(f"{device_path} {root} {counter}/{totalfiles}                                                           ", end='\r')
            counter=counter+1
            if file not in ignored_files:
              file_path = os.path.join(root, file)
              if r.exists(file_path):
                fileinfo = r.get(file_path)    
              else:
                if ignore_file(file_path):
                    r.set(file_path, "ignore")
                else:
                  if is_named_pipe(file_path):
                    r.set(file_path, "pipe")
                  else:
                    if file_path not in ignored_files and not file_path.endswith('.xpm'):
                      print(file_path)
                      if(is_text_file(file_path)):
                        print("text")
                        r.set(file_path, "text")
                      else:
                        if(is_photo(file_path)):
                          r.set(file_path, "photo")
                        else:
                          r.set(file_path, "unknown")

                


def loop_over_devices(r):
    with open('/proc/mounts', 'r') as mounts_file:
        mounts = mounts_file.readlines()
    ignored_fs_types = ['devpts', 'rfkill']
    for mount_info in mounts:
        mount_info = mount_info.strip()
        mount_elements = mount_info.split(' ')

        # Check if there are at least four elements (device, mount point, filesystem type, options)
        if len(mount_elements) >= 4:
            device, mount_point, fs_type, _ = mount_elements[:4]
            if fs_type in ignored_fs_types:
                continue
            if fs_type not in ['proc', 'sysfs', 'tmpfs', 'devtmpfs']:
                find_files_on_device(mount_point,r )
                print()

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)

    loop_over_devices(r)

