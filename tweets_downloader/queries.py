def get_max_value(table, column, conditions=[], values=[]):
    """
    :type table: str
    :type column: str
    :type conditions: list[str]
    :type values: list[str]
    :rtype: str
    """
    assert type(table) is str
    assert type(column) is str
    assert type(conditions) is list
    assert type(values) is list
    assert len(conditions) == len(values)

    predicts = ["{c} = '{v}'".format(c=c, v=v) for c, v in zip(conditions, values)]
    predicts = ' and '.join(p for p in predicts)
    if predicts:
        query = """
            SELECT max({column}) FROM {table} WHERE {predicts};
                    """.format(column=column, table=table, predicts=predicts)
    else:
        query = """
            SELECT max({column}) from {table};
                    """.format(column=column, table=table)
    return query
