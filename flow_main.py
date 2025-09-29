from prefect import flow, task
import subprocess, sys
from reset_db import reset_database   #  importera reset

@task
def reset_db_task():
    reset_database()  #  kör reset

@task
def run_validation():
    subprocess.run([sys.executable, "validation.py"], check=True)

@task
def import_customers():
    subprocess.run([sys.executable, "import_customers.py"], check=True)

@task
def import_transactions():
    subprocess.run([sys.executable, "import_transactions.py"], check=True)

@task
def import_flagged():
    subprocess.run([sys.executable, "import_flagged_transactions.py"], check=True)

@flow(name="ETL-bank-flow")
def full_pipeline():
    reset_db_task()        #  körs alltid först
    run_validation()
    import_customers()
    import_transactions()
    import_flagged()
    print(" Klart! Databasen är nollställd och all data är importerad.")

if __name__ == "__main__":
    full_pipeline()


