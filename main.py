"""
Simple Academic Performance Analytics
A professional data analysis project demonstrating:
- Data cleaning and transformation
- Statistical analysis and reporting
- Data visualization and dashboard creation
- Professional documentation and code structure
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Set up nice looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AcademicPerformanceAnalyzer:
    def __init__(self):
        """Initialize the analyzer"""
        self.raw_data = None
        self.cleaned_data = None
        self.results = {}
        
    def create_sample_data(self):
        """Create sample student grade data"""
        print("--> Creating sample student data...")
        
        # Create realistic student data
        np.random.seed(42)  # For reproducible results
        
        students = []
        subjects = ['Math', 'Science', 'English', 'History', 'Art']
        
        for i in range(100):
            student = {
                'student_id': f'STU{i+1:03d}',
                'name': f'Student {i+1}',
                'grade_level': np.random.choice(['9th', '10th', '11th', '12th']),
                'gender': np.random.choice(['Male', 'Female']),
            }
            
            # Add grades for each subject (some missing values to demonstrate cleaning)
            for subject in subjects:
                if np.random.random() > 0.05:  # 95% chance of having a grade
                    grade = np.random.normal(75, 15)  # Average 75, std dev 15
                    grade = max(0, min(100, grade))  # Keep between 0-100
                    student[subject] = round(grade, 1)
                else:
                    student[subject] = None  # Missing grade
            
            students.append(student)
        
        # Create DataFrame
        df = pd.DataFrame(students)
        
        # Add some data quality issues for cleaning demonstration
        # 1. Some names have extra spaces
        df.loc[0:5, 'name'] = df.loc[0:5, 'name'].apply(lambda x: f"  {x}  ")
        
        # 2. Some inconsistent grade level formatting
        df.loc[10:15, 'grade_level'] = df.loc[10:15, 'grade_level'].str.replace('th', 'TH')
        
        # Save to CSV
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/student_grades.csv', index=False)
        
        print(f"--> Sample data created: {len(df)} students")
        return df
    
    def load_data(self, file_path='data/student_grades.csv'):
        """Load student data from CSV file"""
        print(f"--> Loading data from {file_path}...")
        
        try:
            self.raw_data = pd.read_csv(file_path)
            print(f"--> Data loaded: {len(self.raw_data)} rows, {len(self.raw_data.columns)} columns")
            return self.raw_data
        except FileNotFoundError:
            print("--> File not found. Creating sample data...")
            self.raw_data = self.create_sample_data()
            return self.raw_data
    
    def clean_data(self):
        """Clean the raw data"""
        print("\n--> Cleaning data...")
        
        if self.raw_data is None:
            print("--> No data to clean. Load data first!")
            return None
        
        # Start with a copy
        self.cleaned_data = self.raw_data.copy()
        
        # Step 1: Clean text columns (remove extra spaces)
        print("  • Cleaning text columns...")
        text_columns = ['name', 'grade_level', 'gender']
        for col in text_columns:
            if col in self.cleaned_data.columns:
                self.cleaned_data[col] = self.cleaned_data[col].astype(str).str.strip()
        
        # Step 2: Standardize grade level formatting
        print("  • Standardizing grade levels...")
        if 'grade_level' in self.cleaned_data.columns:
            self.cleaned_data['grade_level'] = self.cleaned_data['grade_level'].str.lower().str.replace('TH', 'th')
        
        # Step 3: Handle missing grades (fill with subject average)
        print("  • Handling missing grades...")
        grade_columns = ['Math', 'Science', 'English', 'History', 'Art']
        
        # Check which grade columns actually exist
        existing_grade_columns = [col for col in grade_columns if col in self.cleaned_data.columns]
        
        if existing_grade_columns:
            missing_before = self.cleaned_data[existing_grade_columns].isnull().sum().sum()
            
            for col in existing_grade_columns:
                avg_grade = self.cleaned_data[col].mean()
                self.cleaned_data[col] = self.cleaned_data[col].fillna(avg_grade)
            
            missing_after = self.cleaned_data[existing_grade_columns].isnull().sum().sum()
            print(f"  • Fixed {missing_before} missing grades")
            
            # Step 4: Round grades to 1 decimal place
            for col in existing_grade_columns:
                self.cleaned_data[col] = self.cleaned_data[col].round(1)
        
        # Save cleaned data
        try:
            self.cleaned_data.to_csv('data/cleaned_grades.csv', index=False)
            print("--> Data cleaning complete!")
        except Exception as e:
            print(f"--> Warning: Could not save cleaned data: {e}")
        
        return self.cleaned_data
    
    def transform_data(self):
        """Transform data to create new features"""
        print("\n--> Transforming data...")
        
        if self.cleaned_data is None:
            print("--> No clean data available. Clean data first!")
            return None
        
        # Calculate overall average for each student
        grade_columns = ['Math', 'Science', 'English', 'History', 'Art']
        existing_grade_columns = [col for col in grade_columns if col in self.cleaned_data.columns]
        
        if existing_grade_columns:
            self.cleaned_data['overall_average'] = self.cleaned_data[existing_grade_columns].mean(axis=1).round(1)
        else:
            print("--> No grade columns found!")
            return None
        
        # Create letter grades
        def get_letter_grade(score):
            if score >= 90:
                return 'A'
            elif score >= 80:
                return 'B'
            elif score >= 70:
                return 'C'
            elif score >= 60:
                return 'D'
            else:
                return 'F'
        
        self.cleaned_data['letter_grade'] = self.cleaned_data['overall_average'].apply(get_letter_grade)
        
        # Create performance categories
        def get_performance_category(score):
            if score >= 85:
                return 'Excellent'
            elif score >= 75:
                return 'Good'
            elif score >= 65:
                return 'Average'
            else:
                return 'Needs Improvement'
        
        self.cleaned_data['performance'] = self.cleaned_data['overall_average'].apply(get_performance_category)
        
        # Find best and worst subject for each student
        if existing_grade_columns:
            self.cleaned_data['best_subject'] = self.cleaned_data[existing_grade_columns].idxmax(axis=1)
            self.cleaned_data['worst_subject'] = self.cleaned_data[existing_grade_columns].idxmin(axis=1)
        
        print("--> Data transformation complete!")
        return self.cleaned_data
    
    def analyze_data(self):
        """Perform basic statistical analysis"""
        print("\n--> Analyzing data...")
        
        if self.cleaned_data is None:
            print("--> No data to analyze!")
            return None
        
        grade_columns = ['Math', 'Science', 'English', 'History', 'Art']
        existing_grade_columns = [col for col in grade_columns if col in self.cleaned_data.columns]
        
        if not existing_grade_columns:
            print("--> No grade columns found for analysis!")
            return None
        
        # Basic statistics
        self.results['basic_stats'] = {
            'total_students': len(self.cleaned_data),
            'average_overall_grade': self.cleaned_data['overall_average'].mean().round(1),
            'highest_grade': self.cleaned_data['overall_average'].max(),
            'lowest_grade': self.cleaned_data['overall_average'].min(),
        }
        
        # Subject averages
        self.results['subject_averages'] = {}
        for subject in existing_grade_columns:
            self.results['subject_averages'][subject] = self.cleaned_data[subject].mean().round(1)
        
        # Grade distribution
        self.results['grade_distribution'] = self.cleaned_data['letter_grade'].value_counts().to_dict()
        
        # Performance by grade level
        self.results['performance_by_grade'] = self.cleaned_data.groupby('grade_level')['overall_average'].mean().round(1).to_dict()
        
        # Gender performance comparison
        if 'gender' in self.cleaned_data.columns:
            self.results['gender_performance'] = self.cleaned_data.groupby('gender')['overall_average'].mean().round(1).to_dict()
        else:
            self.results['gender_performance'] = {}
        
        print("--> Analysis complete!")
        
        # Print results
        print("\n--> ANALYSIS RESULTS:")
        print(f"  • Total Students: {self.results['basic_stats']['total_students']}")
        print(f"  • Average Grade: {self.results['basic_stats']['average_overall_grade']}")
        print(f"  • Highest Grade: {self.results['basic_stats']['highest_grade']}")
        print(f"  • Lowest Grade: {self.results['basic_stats']['lowest_grade']}")
        
        return self.results
    
    def create_visualizations(self):
        """Create data visualizations"""
        print("\n--> Creating visualizations...")
        
        if self.cleaned_data is None:
            print("--> No data to visualize!")
            return
        
        # Create output directory
        os.makedirs('visualizations', exist_ok=True)
        
        # Set up the plot style
        plt.style.use('default')
        
        # 1. Grade Distribution (Bar Chart)
        plt.figure(figsize=(10, 6))
        grade_counts = self.cleaned_data['letter_grade'].value_counts()
        colors = ['#2E8B57', '#4682B4', '#DAA520', '#CD853F', '#DC143C']
        
        plt.bar(grade_counts.index, grade_counts.values, color=colors[:len(grade_counts)])
        plt.title('Grade Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Letter Grade', fontsize=12)
        plt.ylabel('Number of Students', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, v in enumerate(grade_counts.values):
            plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('visualizations/grade_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Subject Performance (Horizontal Bar Chart)
        plt.figure(figsize=(10, 6))
        subject_avgs = self.results['subject_averages']
        subjects = list(subject_avgs.keys())
        averages = list(subject_avgs.values())
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(subjects)))
        bars = plt.barh(subjects, averages, color=colors)
        
        plt.title('Average Grade by Subject', fontsize=16, fontweight='bold')
        plt.xlabel('Average Grade', fontsize=12)
        plt.ylabel('Subject', fontsize=12)
        plt.xlim(0, 100)
        
        # Add value labels
        for i, (bar, avg) in enumerate(zip(bars, averages)):
            plt.text(avg + 1, i, f'{avg}', va='center', fontweight='bold')
        
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/subject_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 3. Performance by Grade Level (Line Chart)
        plt.figure(figsize=(10, 6))
        grade_level_perf = self.results['performance_by_grade']
        
        grade_levels = list(grade_level_perf.keys())
        performance = list(grade_level_perf.values())
        
        plt.plot(grade_levels, performance, marker='o', linewidth=3, markersize=8, color='#FF6B6B')
        plt.title('Performance by Grade Level', fontsize=16, fontweight='bold')
        plt.xlabel('Grade Level', fontsize=12)
        plt.ylabel('Average Grade', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        
        # Add value labels
        for i, (level, perf) in enumerate(zip(grade_levels, performance)):
            plt.text(i, perf + 2, f'{perf}', ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('visualizations/performance_by_grade_level.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 4. Gender Performance Comparison (Pie Chart)
        if self.results['gender_performance']:
            plt.figure(figsize=(8, 8))
            gender_perf = self.results['gender_performance']
            
            genders = list(gender_perf.keys())
            performances = list(gender_perf.values())
            colors = ['#FF9999', '#66B2FF']
            
            plt.pie(performances, labels=[f'{g}\n(Avg: {p})' for g, p in zip(genders, performances)], 
                    autopct='%1.1f%%', colors=colors, startangle=90)
            plt.title('Performance by Gender', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('visualizations/gender_performance.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        print("--> Visualizations saved to 'visualizations/' folder")
    
    def generate_report(self):
        """Generate a summary report"""
        print("\n--> Generating report...")
        
        report = f"""
STUDENT GRADE ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*50}
SUMMARY STATISTICS
{'='*50}
Total Students: {self.results['basic_stats']['total_students']}
Average Overall Grade: {self.results['basic_stats']['average_overall_grade']}
Highest Grade: {self.results['basic_stats']['highest_grade']}
Lowest Grade: {self.results['basic_stats']['lowest_grade']}

{'='*50}
SUBJECT PERFORMANCE
{'='*50}
"""
        
        for subject, avg in self.results['subject_averages'].items():
            report += f"{subject}: {avg}\n"
        
        report += f"""
{'='*50}
GRADE DISTRIBUTION
{'='*50}
"""
        
        for grade, count in self.results['grade_distribution'].items():
            percentage = (count / self.results['basic_stats']['total_students']) * 100
            report += f"{grade}: {count} students ({percentage:.1f}%)\n"
        
        report += f"""
{'='*50}
PERFORMANCE BY GRADE LEVEL
{'='*50}
"""
        
        for level, avg in self.results['performance_by_grade'].items():
            report += f"{level}: {avg}\n"
        
        # Save report
        with open('analysis_report.txt', 'w') as f:
            f.write(report)
        
        print("--> Report saved as 'analysis_report.txt'")
        print("\n" + report)
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("--> Starting Student Grade Analysis...")
        print("="*50)
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Clean data
        self.clean_data()
        
        # Step 3: Transform data
        self.transform_data()
        
        # Step 4: Analyze data
        self.analyze_data()
        
        # Step 5: Create visualizations
        self.create_visualizations()
        
        # Step 6: Generate report
        self.generate_report()
        
        print("\n--> Analysis complete! Check the following files:")
        print("  • data/cleaned_grades.csv - Cleaned data")
        print("  • visualizations/ - Charts and graphs")
        print("  • analysis_report.txt - Summary report")
        

# Run the analysis
if __name__ == "__main__":
    analyzer = StudentGradeAnalyzer()
    analyzer.run_full_analysis()
