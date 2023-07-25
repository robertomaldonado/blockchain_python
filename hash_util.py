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
    Return: 
        :string: A string representation of the block
    '''
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
