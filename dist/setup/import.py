#import statements
import csv, os
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import scoped_session as sqlalchemy_orm_scoped_session
from sqlalchemy.orm import sessionmaker as sqlalchemy_orm_sessionmaker

#create the database connection
databaseEngine = sqlalchemy_create_engine(os.getenv('DATABASE_URL'))
databaseDatabase = sqlalchemy_orm_scoped_session(sqlalchemy_orm_sessionmaker(bind = databaseEngine))

#read the books.csv file
booksCSVFile = csv.reader(open('books.csv'))

#set the counter for the next bit where you iterate through the entries
index = 0

#iterate through the files lines
for booksCSVFile_isbn, booksCSVFile_title, booksCSVFile_author, booksCSVFile_year in booksCSVFile:

    #make two more variables for the lowercase data
    booksCSVFile_titleLowercase = booksCSVFile_title.lower()
    booksCSVFile_authorLowercase = booksCSVFile_author.lower()

    #alert the user what the index is
    print('Adding entry #{}'.format(index + 1))

    #check that the line you are adding isnt the first line of the csv file
    if (index > 0):

        #add the data to the database
        databaseDatabase.execute(
            'INSERT INTO books (isbn, title, title_lowercase, author, author_lowercase, year) VALUES (:isbn, :title, :title_lowercase, :author, :author_lowercase, :year)',
            {'isbn':booksCSVFile_isbn, 'title':booksCSVFile_title, 'title_lowercase':booksCSVFile_titleLowercase, 'author':booksCSVFile_author, 'author_lowercase':booksCSVFile_authorLowercase, 'year':booksCSVFile_year}
        )

    #increase the counter
    index += 1

#commit the changes
databaseDatabase.commit()