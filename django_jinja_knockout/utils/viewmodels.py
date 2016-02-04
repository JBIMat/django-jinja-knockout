from pudb import set_trace
import json

# dict manipulation functions are used on HttpRequest.client_data or HttpRequest.session.

def has_vm_list(dict):
    return 'onloadViewModels' in dict

def get_vm_list(dict):
    return dict['onloadViewModels']

def to_vm_list(dict, key='onloadViewModels'):
    dict[key] = vm_list(*dict.get(key, []))
    return dict[key]

# List of client-side viewmodels, which can be serialized to json
class vm_list(list):

    def __init__(self, *initial_vms):
        for vm in initial_vms:
            self.append(vm)

    def append_kw(self, **vm):
        self.append(vm)

    def append(self, p_object):
        if type(p_object) is not dict:
            raise ValueError('Only dict can be appended to vm_list')
        super().append(p_object)

    def insert(self, index, p_object):
        if type(p_object) is not dict:
            raise ValueError('Only dict can be appended to vm_list')
        super().insert(index, p_object)

    def extend(self, iterable):
        for vm in iterable:
            if type(vm) is not dict:
                raise ValueError('Only dict can be appended to vm_list')
        super().extend(iterable)

    def prepend(self, *vms):
        for vm in reversed(vms):
            self.insert(0, vm)

# Next functions may be used with ordinary lists or as methods of vm_list,
# because list of viewmodels might be instance of ordinary list or vm_list.

def find_by_keys(self, *match_vm_keys):
    if not isinstance(self, list):
        raise ValueError('Self is not the list of viewmodels')
    match_keys = set(match_vm_keys)
    for idx, vm in enumerate(self):
        if match_keys.issubset(set(vm.keys())):
            return (idx, vm)
    return (False, None)
vm_list.find_by_keys = find_by_keys

def find_by_kw(self, **partial_vm):
    if not isinstance(self, list):
        raise ValueError('Self is not the list of viewmodels')
    for idx, vm in enumerate(self):
        found = True
        for key in partial_vm:
            if not key in vm or vm[key] != partial_vm[key]:
                found = False
                break
        if found:
            return (idx, vm)
    return (False, None)
vm_list.find_by_kw = find_by_kw

def find_by_vm(self, partial_vm):
    if not isinstance(self, list):
        raise ValueError('Self is not the list of viewmodels')
    return self.find_by_kw(**partial_vm)
vm_list.find_by_vm = find_by_vm

def to_json(self):
    if not isinstance(self, list):
        raise ValueError('Self is not the list of viewmodels')
    return json.dumps(self)
vm_list.to_json = to_json
