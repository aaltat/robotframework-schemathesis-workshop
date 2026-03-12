import random

import schemathesis


@schemathesis.hook
def map_path_parameters(ctx, path_parameters):
    if ctx and path_parameters:
        if "user" in ctx.operation.path and "user_id" in path_parameters:
            user = random.choice([1, 2, 3])
            path_parameters["user_id"] = user
        elif "item" in ctx.operation.path and "item_id" in path_parameters:
            item = random.choice([10, 20, 30])
            path_parameters["item_id"] = item
    return path_parameters
