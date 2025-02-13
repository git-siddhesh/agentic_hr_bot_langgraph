from functools import wraps
import queue
import sqlite3
from typing import Any, List, Tuple, Union, Dict
from sqlite3 import Connection, Cursor


class DBPool:
    def __init__(self, minconn: int, maxconn: int, *args, **kwargs):
        self.minconn: int = minconn
        self.maxconn: int = maxconn
        self.args = args
        self.kwargs = kwargs
        self.pool: queue.Queue[Connection] = queue.Queue(maxsize=maxconn)
        for _ in range(minconn):
            self.pool.put(self.create_connection())

    def create_connection(self)-> Connection:
        # sqlite3 connection
        conn: Connection = sqlite3.connect('utils\\hr_bot.db')
        return conn

    def getconn(self) -> Connection:
        if self.pool.empty():
            if self.pool.qsize() < self.maxconn:
                self.pool.put(self.create_connection())
            else:
                raise Exception("Connection pool exhausted")
        return self.pool.get()

    def putconn(self, conn: Connection) -> None:
        self.pool.put(conn)


def db_connection(db_pool: DBPool | None):
    if db_pool is None:
        db_pool = DBPool(minconn=1, maxconn=5)

    def decorator(func: Any)-> Any:
        @wraps(wrapped=func)
        def wrapper(*args:Any, **kwargs:Any) -> Any:
            
            connection = None
            cursor = None
            try:
                connection: Connection = db_pool.getconn()
                print('Connected to PostgreSQL database successfully.')
                cursor: Cursor = connection.cursor()
                result: Any = func(*args, cursor=cursor, **kwargs)
                connection.commit()
                return result
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                if connection:
                    connection.rollback()
                raise e
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    db_pool.putconn(connection)

        return wrapper
    return decorator

print("intializing DBPool")
db_pool = DBPool(minconn=1, maxconn=5)
print("DBPool intialized")
@db_connection(db_pool)
def execute_query(query: str, args: Tuple[Any], cursor: Cursor) -> List[Union[Dict[Any, Any], Tuple[Any]]]:
    cursor.execute(query, args)
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# # get the schema of each table in the database
# query = "SELECT name FROM sqlite_master WHERE type='table';"
# tables = execute_query(query, {})
# # [{'name': 'paysheet'}, {'name': 'it_reco'}, {'name': 'ctc_reco'}, {'name': 'pf_reco'}, {'name': 'master_reco'}, {'name': 'other_deduction'}, {'name': 'reimbursements'}, {'name': 'july_reimbursements'}, {'name': 'aug_reimbursements'}]

# for table in tables:
#     table_name = table['name']
#     print("Table Name: ", table_name)
#     # get the columns of the table and their data types
#     query = f"PRAGMA table_info({table_name});"
#     columns = execute_query(query, {})
#     print(columns)



# # Table Name:  paysheet
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'DOJ', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'Relieved Date', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'Department', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Designation', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'Bank name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 8, 'name': 'Bank Ac No', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 9, 'name': 'IFSC Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 10, 'name': 'Resigned Date', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 11, 'name': 'Emp Worked days', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 12, 'name': 'LOP Days', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 13, 'name': 'RLOP', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 14, 'name': 'BASIC', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 15, 'name': 'House Rent Allowance', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 16, 'name': 'Conveyance Allowance', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 17, 'name': 'Special Allowance', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 18, 'name': 'Field Expenses', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 19, 'name': 'Total Earnings', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 20, 'name': 'Income Tax', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 21, 'name': 'Other Deductions', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 22, 'name': 'Provident Fund', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 23, 'name': 'Total Deductions', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 24, 'name': 'NETPAY', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 25, 'name': 'Remarks', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  it_reco
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'Total Earnings', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': '2024-07-01 00:00:00', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': '2024-08-01 00:00:00', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Diff', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'Remarks', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  ctc_reco
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Emp_Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'Working days', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'Annual CTC PA', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'VP', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'CTC PM', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'PF_Empr', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 8, 'name': 'ESIC_Empr', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 9, 'name': 'Monthly Fixed CTC', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 10, 'name': 'Proration Earnings', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 11, 'name': 'Total Earnings', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 12, 'name': 'Bonus', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 13, 'name': 'Difference', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 14, 'name': 'Field Expenses & Salary Advance Recovery', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 15, 'name': 'Final Difference', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  pf_reco
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'Basic Salary', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'BASIC Arrears', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'PF Wages', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'PF as per clacualtion', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'AS per salary Sheet', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 8, 'name': 'Diff', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 9, 'name': 'Remarks', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  master_reco
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Emp_Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'BASIC', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'House Rent Allowance', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'Conveyance Allowance', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Special Allowance', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'PF Employer', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 8, 'name': 'CTC PM', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 9, 'name': 'FIX CTC', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 10, 'name': 'VP', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 11, 'name': 'CTC PA', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  other_deduction
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'Deductions', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'Reason', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]        

# # Table Name:  reimbursements
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': 'Reimbursements', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': '2024-07-01 00:00:00', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': '2024-08-01 00:00:00', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Diff', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'Remarks', 'type': 'REAL', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  july_reimbursements
# # [{'cid': 0, 'name': 'Sl No.', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': '2024-07-01 00:00:00', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'Bill No', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'Reason', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Approval Status', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'Remark', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]

# # Table Name:  aug_reimbursements
# # [{'cid': 0, 'name': 'aug', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 1, 'name': 'Code', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 2, 'name': 'Name', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 3, 'name': '2024-08-01 00:00:00', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 4, 'name': 'Bill No', 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 5, 'name': 'Remarks', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 6, 'name': 'Approval Status', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}, {'cid': 7, 'name': 'Remark', 'type': 'TEXT', 'notnull': 0, 'dflt_value': None, 'pk': 0}]
