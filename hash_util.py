import hashlib as hl
import json

def hash_string_256(string) -> str:
    '''
    Args:
        :string: The current block to represent
    Return:
        string: Hash of the given input
    '''
    return hl.sha256(string).hexdigest()
    
def hash_block(block) -> str:
    '''
    Args:
        :block: The current block to represent
    '''
    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
