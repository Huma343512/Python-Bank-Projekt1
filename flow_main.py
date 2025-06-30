from prefect import flow, task
import subprocess
import sys

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
    run_validation()
    import_customers()
    import_transactions()
    import_flagged()
    print(" Klart! Allt är importerat.")

if __name__ == "__main__":
    full_pipeline()

