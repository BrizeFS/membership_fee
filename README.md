# Calculate membership fee

Run tests with pytest, see test file for usage

## Test files
### Adjacency list

To describe the tree structure, follow the ADJLIST format: https://networkx.org/documentation/stable/reference/readwrite/adjlist.html

    parent child1 child2

### JSON config data

Config objects are stored as a JSON file with the structure:
    {"organisation_unit": {"has_fixed_membership_fee": bool, "fixed_membership_fee_amount": int}}