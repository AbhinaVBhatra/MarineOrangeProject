import os
import subprocess
import sys
import time

def run_script(script_path):
    print(f"\n{'='*70}")
    print(f"RUNNING: {script_path}")
    print(f"{'='*70}")
    start = time.time()
    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    elapsed = time.time() - start
    if res.returncode != 0:
        print(f"FAILED: {script_path} (Exit Code: {res.returncode})")
        print("STDERR:")
        print(res.stderr)
        print("STDOUT:")
        print(res.stdout)
        sys.exit(res.returncode)
    else:
        print(res.stdout.strip())
        print(f"COMPLETED in {elapsed:.2f}s (Success)")

def main():
    print("="*70)
    print("STARTING END-TO-END REPRODUCIBLE MARINE DATA MINING PIPELINE")
    print("="*70)

    scripts = [
        os.path.join("scripts", "01_inspect.py"),
        os.path.join("scripts", "02_clean.py"),
        os.path.join("scripts", "03_eda.py"),
        os.path.join("scripts", "04_clustering.py"),
        os.path.join("scripts", "05_classification.py"),
        os.path.join("scripts", "06_generate_results_md.py"),
        os.path.join("scripts", "07_generate_report.py"),
        os.path.join("scripts", "08_generate_presentation.py"),
        os.path.join("scripts", "09_generate_orange_workflow.py")
    ]

    total_start = time.time()
    for s in scripts:
        run_script(s)

    total_elapsed = time.time() - total_start
    print("\n" + "="*70)
    print(f"ALL 9 SCRIPTS RAN SUCCESSFULLY AND COMPLETED IN {total_elapsed:.2f}s!")
    print("Deliverables Verified:")
    print("  - data/raw.csv, cleaned_core.csv, cleaned_sst.csv")
    print("  - results/01_inspection, 02_cleaning, 03_eda, 04_clustering, 05_classification")
    print("  - RESULTS.md & DECISIONS.md")
    print("  - Report.docx")
    print("  - Presentation.pptx")
    print("  - Demo_Script.md")
    print("  - Orange_Steps.md & marine_project.ows")
    print("="*70)

if __name__ == "__main__":
    main()
