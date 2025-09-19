import sqlite3
from fastapi import Depends

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

db_path = './db.db'

def get_db_connection():
  conn = sqlite3.connect(db_path)
  conn.row_factory = sqlite3.Row
  try:
      yield conn
  finally:
      conn.close()

def create():
  print("Creating")
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  # c.execute('''
  #           DROP TABLE IF EXISTS users
  #           ''')
  c.execute('''
            CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE NOT NULL,
              full_name TEXT,
              picture TEXT,
              email TEXT NOT NULL UNIQUE,
              password TEXT
            )
            ''')
  
  # c.execute('''
  #             CREATE TABLE IF NOT EXISTS messages(
  #               user_id INTEGER REFERENCES users(id),
  #               message TEXT,
  #               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                
  #             )
  #           ''')
  
  conn.commit()
  
  conn.close()
  
def seed():
  print("Seeding")
  conn = sqlite3.connect(db_path)
  # products = [
  #   ('apples', 1.25, .99, 25),
  #   ('bananas', .75, .50, 12),
  #   ('burgers', 3.99, 2.99, 8),
  #   ('hamburger buns', 3.25, 2.99, 6),
  #   ('lettuce', .99, .79, 3),
  #   ('ketchup', 3.29, 2.99, 6),
  #   ('mustard', 2.99, 2.79, 4),
  #   ('hot dogs', 4.59, 3.99, 6),
  #   ('hot dog buns', 2.75, 1.99, 6),
  #   ('pickles', 1.25, .99, 3)
  # ]
  
  # movies = [
  #   ("A Bug's Life", "Denis Leary, Jonathan Harris, Kevin Spacey", "1998"),
  #   ("Aladdin", "Robin Williams, Jim Cummings, Linda Larkin", "1992"),
  #   ("Bambi", "Fred Shields, Peter Behn, Cammie King Conlon", "1942"),
  #   ("Brave", "Robbie Coltrane, Kevin McKidd, Kelly McDonald", "2012"),
  #   ("Cars", "Owen Wilson, Paul Newman, Bonnie Hunt", "2006"),
  #   ("Freaky Friday", "Lindsay Lohan, Jamie Lee Curtis, Chad Michael Murray", "2003"),
  #   ("Hercules", "Danny DeVito, James Woods, Barbara Barrie", "1997"),
  #   ("Moana", "Auli'i Cravalho, Dwayne Johnson, Alan Tudyk", "2016"),
  #   ("Monsters, Inc.", "John Goodman, Mary Gibbs, Billy Crystal", "2001")
  # ]
  
  c = conn.cursor()
  # c.executemany('insert into orders (name, price, cost, quantity) VALUES (?,?,?,?)', products)
  # c.executemany('INSERT INTO movies (movie, actors, year) VALUES (?,?,?)', movies)
  conn.commit()
  conn.close()

def run():
  print(f"{GREEN}Enter command:{RESET}")
  while True:
    user_input = input(">: ")
    if user_input.lower() == "bye":
      print(f"{GREEN}Have a nice day{RESET}")
      break
    elif user_input.lower() == "create":
      create()
    elif user_input.lower() == "seed":
      seed()
  
  
if __name__ == "__main__":
  run()