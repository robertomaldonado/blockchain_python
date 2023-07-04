from typing import List

blockchain = list()
blockchain = [[1]]

def get_last_blockchain_value () -> List[int]:
    return blockchain[-1]

def add_value(transaction_amout: int) -> None:
    blockchain.append([get_last_blockchain_value(),transaction_amout])

add_value(0)
add_value(1)
add_value(2)

print(blockchain)