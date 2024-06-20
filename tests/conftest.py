
def _construct_config_branch(node: list) -> dict:
    if not node:
        return {}
    return {
        leaf['name']: _construct_config_branch(
            leaf.get('properties', [])
        )
        for leaf in node
    }
