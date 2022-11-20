import os
import tabula
from sqlalchemy import create_engine
import pymysql

# 1 - first download original monthly hdfc bank statement from email
# 2 - then run qpdf command in CLI (as shown below) in the same directory (use standard input and output file nomenclatures as in earlier files)
# command: qpdf --decrypt --password=<your password> encrypted_file.pdf decrypted_file.pdf

file_names = os.listdir(r'D:\python\Personal Finance Analysis\HDFC bank statements')
for filename in file_names:
    if 'output' in filename:
        filename = f'D:\python\Personal Finance Analysis\HDFC bank statements\{filename}'
        # Returns a list of dataframes
        df_list = tabula.read_pdf(filename, lattice = True, area = (25,0,90,100), relative_area = True, pages = 'all')
        
        # Adding '_' in column names if it contains space(s)
        col_list = list(df_list[0].columns)

        for i in range(len(col_list)):
            if ' ' in col_list[i]:
                col_list[i] = col_list[i].replace(' ', '_')

        # Making same column names for all different dataframes
        for dataframe in df_list:
            dataframe.columns = col_list

        # Appending all dataframes in one dataframe to pass into mysql
        for i in range(len(df_list)-1):
            if i == 0:
                df = df_list[0].append(df_list[1])
            else:
                df = df.append(df_list[i+1])

        df['key'] = df[col_list[0]].astype(str) + df[col_list[1]].astype(str) + df[col_list[2]].astype(str) + df[col_list[3]].astype(str) + df[col_list[4]].astype(str) + df[col_list[5]].astype(str) + df[col_list[6]].astype(str) 

        # Create sqlalchemy engine, Connect to the database
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="11121992", db="testdb"))

        # Insert whole DataFrame into MySQL
        df.to_sql('hdfc_new', con = engine, if_exists = 'append', chunksize = 1000, index=False)

        # Reading Records from a Database
        # create connection
        connection = pymysql.connect(host='localhost', user='root', password='11121992', db='testdb')

        # # Create cursor
        my_cursor = connection.cursor()

        # Execute Query
        # add id column
        # id_col = 'ALTER TABLE hdfc_new ADD COLUMN id int auto_increment primary key first'
        # my_cursor.execute(id_col)

        # try:
        #    # Execute the SQL command
        #    my_cursor.execute(id_col)
        
        #    # Commit your changes in the database
        #    connection.commit()
        # except:
        #    # Roll back in case there is any error
        #    connection.rollback()

        # delete duplicates based on 'key' column
        del_col = 'delete t1 from hdfc_new t1 inner join hdfc_new t2 where t2.id < t1.id and t1.key = t2.key;'

        try:
        #     # Execute the SQL command
            my_cursor.execute(del_col)
            
        #     # Commit your changes in the database
            connection.commit()
        except:
        #     # Roll back in case there is any error
            connection.rollback()

        # # Fetch the records
        # result = my_cursor.fetchall()

        # for i in result:
        #     print(i)

        # Close the connection
        connection.close()
