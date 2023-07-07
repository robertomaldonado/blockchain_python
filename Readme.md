BLOCKCHAIN IMPLEMENTATION
=========================
This is a test exercise to develop the implementation of a blockchain such as bitcoin

For what we need to implement is: 

Transactions, Blocks, Participants

- Participants => set()
  Ideally IDs

- Trasactions => dict()
  Sender
  Receipient
  Amount

- Block  => list()
  Previuous-Hash 
  Index
  Transactions  => list()

- Block Chain 
  Linkage between blocks => list()

Rewards: 
  User will be rewarded with 10 coins each time they successfully mine a block.

Note:
  This is based on Academind's python blockchain course