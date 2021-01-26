#!/usr/bin/env python3

import sys
try:
    import apps.interface.app as app
    import apps.database.database as db
except ImportError as e:
    print(e)
    sys.exit(1)

def main():
    datab = db.Database()
    datab.init_db()
    application = app.App()
    application.mainloop()
    sys.exit(1)

if __name__  == "__main__":
    main()


    # FFz3z0731h
