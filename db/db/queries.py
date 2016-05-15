class SelectQuery:
    sql = """
        select {columns}
        from {table}
    """

    def __init__(self, table, columns=None, predicts=None, values=None):
        """
        :param table: str
        :param columns: list[str]
        :param predicts: list[str]
        :param values: list[Any]
        """
        self.table = table
        self.columns = columns
        assert type(predicts) == type(values)
        if predicts and values:
            assert len(predicts) == len(values)
            self.conditions = ' and '.join(item for item in ["{predict}={value}".format(predict=predict, value=value)
                                                             for predict, value in zip(predicts, values)])

    def __str__(self):
        """
        :return: str
        """
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
        :param table: str
        :param columns: list[str]
        :param values: list[str]
        """
        self.table = table
        assert columns is not None
        assert values is not None
        assert len(columns) == len(values)
        self.columns = columns
        self.values = values

    def __str__(self):
        """
        :return: str
        """
        isql = self.sql.format(table=self.table,
                               columns=','.join(c for c in self.columns),
                               values=','.join("'" + str(v) + "'" for v in self.values))
        return isql


class DeleteQuery:
    sql = """
        delete from
        {table}
    """

    def __init__(self, table):
        """
        :param table: str
        """
        self.table = table

    def __str__(self):
        """
        :return: str
        """
        isql = self.sql.format(table=self.table)
        return isql


class UpdateQuery:
    sql = """
        update {table}
        set {updates}
        where {predicts}
    """

    def __init__(self, table, columns, values, pred_columns, pred_values):
        """
        :param table: str
        :param columns: list[str]
        :param values: list[str]
        :param pred_columns: list[str]
        :param pred_values: list[str]
        """
        self.table = table
        self.updates = ','.join(item for item in ['{column}={value}'.format(column=column, value=value) for
                                                  column, value in zip(columns, values)])
        self.predicts = ','.join(item for item in ['{column}={value}'.format(column=column, value=value) for
                                                   column, value in zip(pred_columns, pred_values)])

    def __str__(self):
        """
        :return: sql
        """
        isql = self.sql.format(table=self.table,
                               updates=self.updates,
                               predicts=self.predicts)
        return isql

