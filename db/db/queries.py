class SelectQuery:
    sql = """
        select {columns}
        from {table}
    """

    def __init__(self, table, columns=None, predicts=None, values=None):
        """
        :type table: str
        :type columns: list[str]
        :type predicts: list[str]
        :type values: list[Any]
        """
        self.table = table
        self.columns = columns
        assert type(predicts) == type(values)
        if not predicts and not values:
            assert len(predicts) == len(values)
            self.conditions = ' and '.join(item for item in ["{predict}={value}".format(predict=predict, value=value)
                                                             for predict, value in zip(predicts, values)])

    def __str__(self):
        isql = self.sql.format(columns=','.join(c for c in self.columns) if self.columns else '*',
                               table=self.table)
        if hasattr(self, 'conditions'):
            return isql + ' where ' + self.conditions
        return isql


class InsertQuery:
    sql = """
        insert into {table}
        ({columns})
        values ({values})
    """
    
    def __init__(self, table, columns, values):
        """
        :type table: str
        :type columns: list[str]
        :type values: list[str]
        """
        self.table = table
        assert columns is not None
        assert values is not None
        assert len(columns) == len(values)
        self.columns = columns
        self.values = values

    def __str__(self):
        isql = self.sql.format(table=self.table,
                               columns=','.join(c for c in self.columns),
                               values=','.join("'" + v + "'" for v in self.values))
        return isql


class DeleteQuery:
    sql = """
        delete from
        {table}
    """

    def __init__(self, table):
        self.table = table

    def __str__(self):
        isql = self.sql.format(table=self.table)
        return isql