"""
Complete Analysis Pipeline
Executes the full analysis workflow and launches the interactive dashboard
"""

import subprocess
import sys
import os

def run_analysis():
    """Execute the main analytical pipeline"""
    print("Initiating academic performance analysis...")
    try:
        from main import AcademicPerformanceAnalyzer
        
        analyzer = AcademicPerformanceAnalyzer()
        analyzer.run_full_analysis()
        
        print("\n--> Analysis pipeline completed successfully!")
        return True
        
    except Exception as e:
        print(f"--> Error during analysis execution: {e}")
        return False

def launch_dashboard():
    """Launch the Streamlit interactive dashboard"""
    print("\n--> Launching interactive dashboard...")
    print("--> The dashboard will open in your web browser.")
    print("--> Press Ctrl+C to stop the dashboard when finished.")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n--> Dashboard session ended.")
    except Exception as e:
        print(f"--> Error launching dashboard: {e}")
        print("--> Ensure streamlit is installed: pip install streamlit")

def main():
    """Main execution function for complete pipeline"""
    print("="*60)
    print("--> ACADEMIC PERFORMANCE ANALYTICS - COMPLETE PIPELINE")
    print("="*60)
    
    # Execute analysis pipeline
    if run_analysis():
        print("\n" + "="*60)
        print("--> ANALYSIS COMPLETE - LAUNCHING INTERACTIVE DASHBOARD")
        print("="*60)
        
        # Launch interactive dashboard
        launch_dashboard()
    else:
        print("\n--> Analysis failed. Please review error messages above.")

if __name__ == "__main__":
    main()