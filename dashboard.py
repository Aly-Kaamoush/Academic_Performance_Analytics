"""
Academic Performance Analytics Dashboard
Interactive web dashboard for educational performance insights
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="Academic Performance Analytics Dashboard",
    page_icon="-->",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DashboardApp:
    def __init__(self):
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load and validate dataset"""
        try:
            if os.path.exists('data/cleaned_grades.csv'):
                self.data = pd.read_csv('data/cleaned_grades.csv')
                # Check if processed columns exist, if not, create them
                self.ensure_processed_columns()
            elif os.path.exists('data/student_grades.csv'):
                st.warning("Found raw data but no cleaned data. Processing now...")
                self.data = pd.read_csv('data/student_grades.csv')
                self.process_raw_data()
            else:
                st.error("No data found. Please run main.py first!")
                return None
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    
    def process_raw_data(self):
        """Process raw data to create necessary analytical columns"""
        if self.data is not None:
            # Calculate overall average for each student
            grade_columns = ['Math', 'Science', 'English', 'History', 'Art']
            existing_grade_columns = [col for col in grade_columns if col in self.data.columns]
            
            if existing_grade_columns:
                self.data['overall_average'] = self.data[existing_grade_columns].mean(axis=1).round(1)
            else:
                st.error("No grade columns found in the data!")
                return
            
            # Create letter grades
            def get_letter_grade(score):
                if score >= 90: return 'A'
                elif score >= 80: return 'B'
                elif score >= 70: return 'C'
                elif score >= 60: return 'D'
                else: return 'F'
            
            self.data['letter_grade'] = self.data['overall_average'].apply(get_letter_grade)
            
            # Create performance categories
            def get_performance_category(score):
                if score >= 85: return 'Excellent'
                elif score >= 75: return 'Good'
                elif score >= 65: return 'Average'
                else: return 'Needs Improvement'
            
            self.data['performance'] = self.data['overall_average'].apply(get_performance_category)
            
            st.success("Data processed successfully!")
    
    def ensure_processed_columns(self):
        """Ensure all necessary columns exist in the data"""
        if self.data is not None:
            # Check if overall_average exists
            if 'overall_average' not in self.data.columns:
                grade_columns = ['Math', 'Science', 'English', 'History', 'Art']
                existing_grade_columns = [col for col in grade_columns if col in self.data.columns]
                
                if existing_grade_columns:
                    self.data['overall_average'] = self.data[existing_grade_columns].mean(axis=1).round(1)
            
            # Check if letter_grade exists
            if 'letter_grade' not in self.data.columns and 'overall_average' in self.data.columns:
                def get_letter_grade(score):
                    if score >= 90: return 'A'
                    elif score >= 80: return 'B'
                    elif score >= 70: return 'C'
                    elif score >= 60: return 'D'
                    else: return 'F'
                
                self.data['letter_grade'] = self.data['overall_average'].apply(get_letter_grade)
            
            # Check if performance exists
            if 'performance' not in self.data.columns and 'overall_average' in self.data.columns:
                def get_performance_category(score):
                    if score >= 85: return 'Excellent'
                    elif score >= 75: return 'Good'
                    elif score >= 65: return 'Average'
                    else: return 'Needs Improvement'
                
                self.data['performance'] = self.data['overall_average'].apply(get_performance_category)
    
    def create_header(self):
        """Create professional dashboard header with key metrics"""
        st.title("--> Academic Performance Analytics Dashboard")
        st.markdown("---")
        
        # Display summary statistics
        if self.data is not None and 'overall_average' in self.data.columns:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Total Students",
                    value=len(self.data)
                )
            
            with col2:
                avg_grade = self.data['overall_average'].mean()
                st.metric(
                    label="Average Grade",
                    value=f"{avg_grade:.1f}",
                    delta=f"{avg_grade - 75:.1f}" if avg_grade > 75 else f"{avg_grade - 75:.1f}"
                )
            
            with col3:
                st.metric(
                    label="Highest Grade",
                    value=f"{self.data['overall_average'].max():.1f}"
                )
            
            with col4:
                st.metric(
                    label="Lowest Grade",
                    value=f"{self.data['overall_average'].min():.1f}"
                )
        elif self.data is not None:
            st.metric(
                label="Total Students",
                value=len(self.data)
            )
            st.warning("Overall average not calculated. Some features may be limited.")
        
        st.markdown("---")
    
    def create_sidebar(self):
        """Create interactive filtering sidebar"""
        st.sidebar.header("--> Filters")
        
        if self.data is not None:
            # Grade level filter
            if 'grade_level' in self.data.columns:
                grade_levels = ['All'] + sorted(self.data['grade_level'].unique().tolist())
                selected_grade = st.sidebar.selectbox("Select Grade Level", grade_levels)
            else:
                selected_grade = 'All'
            
            # Letter grade filter
            if 'letter_grade' in self.data.columns:
                letter_grades = ['All'] + sorted(self.data['letter_grade'].unique().tolist())
                selected_letter = st.sidebar.selectbox("Select Letter Grade", letter_grades)
            else:
                selected_letter = 'All'
            
            # Performance filter
            if 'performance' in self.data.columns:
                performance_levels = ['All'] + sorted(self.data['performance'].unique().tolist())
                selected_performance = st.sidebar.selectbox("Select Performance Level", performance_levels)
            else:
                selected_performance = 'All'
            
            # Apply filters
            filtered_data = self.data.copy()
            
            if selected_grade != 'All' and 'grade_level' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['grade_level'] == selected_grade]
            
            if selected_letter != 'All' and 'letter_grade' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['letter_grade'] == selected_letter]
            
            if selected_performance != 'All' and 'performance' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['performance'] == selected_performance]
            
            # Show filter results
            st.sidebar.metric("Filtered Students", len(filtered_data))
            
            return filtered_data
        
        return None
    
    def create_grade_distribution_chart(self, data):
        """Create interactive grade distribution chart"""
        st.subheader("--> Grade Distribution")
        
        if 'letter_grade' not in data.columns:
            st.warning("Letter grades not available. Please run the full analysis first.")
            return
        
        # Get grade counts
        grade_counts = data['letter_grade'].value_counts().sort_index()
        
        # Create interactive plotly chart
        fig = px.bar(
            x=grade_counts.index,
            y=grade_counts.values,
            labels={'x': 'Letter Grade', 'y': 'Number of Students'},
            title="Distribution of Letter Grades",
            color=grade_counts.values,
            color_continuous_scale="viridis"
        )
        
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Letter Grade",
            yaxis_title="Number of Students"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show percentage breakdown
        total_students = len(data)
        grade_percentages = (grade_counts / total_students * 100).round(1)
        
        st.write("**Grade Breakdown:**")
        cols = st.columns(len(grade_counts))
        for i, (grade, count) in enumerate(grade_counts.items()):
            with cols[i]:
                st.metric(
                    label=f"Grade {grade}",
                    value=f"{count} students",
                    delta=f"{grade_percentages[grade]}%"
                )
    
    def create_subject_performance_chart(self, data):
        """Create subject performance chart"""
        st.subheader("--> Subject Performance")
        
        # Get subject columns
        subject_columns = ['Math', 'Science', 'English', 'History', 'Art']
        existing_subjects = [col for col in subject_columns if col in data.columns]
        
        if existing_subjects:
            # Calculate subject averages
            subject_avgs = data[existing_subjects].mean().round(1)
            
            # Create horizontal bar chart
            fig = px.bar(
                x=subject_avgs.values,
                y=subject_avgs.index,
                orientation='h',
                labels={'x': 'Average Grade', 'y': 'Subject'},
                title="Average Performance by Subject",
                color=subject_avgs.values,
                color_continuous_scale="RdYlGn"
            )
            
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="Average Grade",
                yaxis_title="Subject"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed stats
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Subject Rankings:**")
                ranked_subjects = subject_avgs.sort_values(ascending=False)
                for i, (subject, avg) in enumerate(ranked_subjects.items(), 1):
                    st.write(f"{i}. {subject}: {avg}")
            
            with col2:
                st.write("**Subject Statistics:**")
                best_subject = subject_avgs.idxmax()
                worst_subject = subject_avgs.idxmin()
                st.write(f"**Best Subject:** {best_subject} ({subject_avgs[best_subject]})")
                st.write(f"**Worst Subject:** {worst_subject} ({subject_avgs[worst_subject]})")
                st.write(f"**Grade Range:** {subject_avgs.max() - subject_avgs.min():.1f} points")
    
    def create_performance_analysis(self, data):
        """Generate performance analysis visualizations"""
        st.subheader("--> Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance by grade level
            if 'grade_level' in data.columns:
                grade_performance = data.groupby('grade_level')['overall_average'].mean().round(1)
                
                fig = px.line(
                    x=grade_performance.index,
                    y=grade_performance.values,
                    markers=True,
                    title="Performance by Grade Level",
                    labels={'x': 'Grade Level', 'y': 'Average Grade'}
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance categories
            if 'performance' in data.columns:
                performance_counts = data['performance'].value_counts()
                
                fig = px.pie(
                    values=performance_counts.values,
                    names=performance_counts.index,
                    title="Performance Categories"
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_detailed_tables(self, data):
        """Generate detailed data tables with multiple views"""
        st.subheader("--> Detailed Data")
        
        # Tab layout for different views
        tab1, tab2, tab3 = st.tabs(["Student Data", "Top Performers", "Subject Analysis"])
        
        with tab1:
            st.write("**All Student Data:**")
            # Display columns selection
            if data is not None:
                all_columns = data.columns.tolist()
                selected_columns = st.multiselect(
                    "Select columns to display:",
                    all_columns,
                    default=['student_id', 'name', 'grade_level', 'overall_average', 'letter_grade']
                )
                
                if selected_columns:
                    display_data = data[selected_columns].copy()
                    st.dataframe(display_data, use_container_width=True)
                    
                    # Download button
                    csv = display_data.to_csv(index=False)
                    st.download_button(
                        label="Download filtered data as CSV",
                        data=csv,
                        file_name=f"filtered_student_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
        
        with tab2:
            st.write("**Top 10 Performers:**")
            top_students = data.nlargest(10, 'overall_average')[
                ['student_id', 'name', 'grade_level', 'overall_average', 'letter_grade']
            ]
            st.dataframe(top_students, use_container_width=True)
            
            st.write("**Bottom 10 Performers:**")
            bottom_students = data.nsmallest(10, 'overall_average')[
                ['student_id', 'name', 'grade_level', 'overall_average', 'letter_grade']
            ]
            st.dataframe(bottom_students, use_container_width=True)
        
        with tab3:
            st.write("**Subject Analysis:**")
            subject_columns = ['Math', 'Science', 'English', 'History', 'Art']
            existing_subjects = [col for col in subject_columns if col in data.columns]
            
            if existing_subjects:
                # Subject statistics
                subject_stats = data[existing_subjects].describe().round(1)
                st.dataframe(subject_stats, use_container_width=True)
                
                # Subject correlation
                if len(existing_subjects) > 1:
                    st.write("**Subject Correlation Matrix:**")
                    corr_matrix = data[existing_subjects].corr()
                    
                    fig = px.imshow(
                        corr_matrix,
                        aspect="auto",
                        color_continuous_scale="RdBu",
                        title="Subject Correlation Matrix"
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    def create_insights_section(self, data):
        """Create insights and recommendations section"""
        st.subheader("--> Key Insights & Recommendations")
        
        if data is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**--> Key Findings:**")
                
                # Calculate insights
                avg_grade = data['overall_average'].mean()
                subject_columns = ['Math', 'Science', 'English', 'History', 'Art']
                existing_subjects = [col for col in subject_columns if col in data.columns]
                
                if existing_subjects:
                    subject_avgs = data[existing_subjects].mean()
                    best_subject = subject_avgs.idxmax()
                    worst_subject = subject_avgs.idxmin()
                    
                    insights = [
                        f"• Average grade across all students: {avg_grade:.1f}",
                        f"• Best performing subject: {best_subject} ({subject_avgs[best_subject]:.1f})",
                        f"• Weakest subject: {worst_subject} ({subject_avgs[worst_subject]:.1f})",
                        f"• Grade distribution: {(data['letter_grade'].value_counts().sort_index() / len(data) * 100).round(1).to_dict()}",
                    ]
                    
                    if 'grade_level' in data.columns:
                        best_grade_level = data.groupby('grade_level')['overall_average'].mean().idxmax()
                        insights.append(f"• Best performing grade level: {best_grade_level}")
                    
                    for insight in insights:
                        st.write(insight)
            
            with col2:
                st.write("**--> Recommendations:**")
                
                recommendations = [
                    f"• Focus additional support on {worst_subject} subject",
                    "• Implement peer tutoring programs for struggling students",
                    "• Celebrate high performers to maintain motivation",
                    "• Consider subject-specific intervention programs",
                    "• Regular progress monitoring and feedback sessions"
                ]
                
                for rec in recommendations:
                    st.write(rec)
    
    def run_dashboard(self):
        """Run the complete dashboard"""
        # Create header
        self.create_header()
        
        # Create sidebar and get filtered data
        filtered_data = self.create_sidebar()
        
        if filtered_data is not None and len(filtered_data) > 0:
            # Main dashboard content
            self.create_grade_distribution_chart(filtered_data)
            st.markdown("---")
            
            self.create_subject_performance_chart(filtered_data)
            st.markdown("---")
            
            self.create_performance_analysis(filtered_data)
            st.markdown("---")
            
            self.create_detailed_tables(filtered_data)
            st.markdown("---")
            
            self.create_insights_section(filtered_data)
            
        elif filtered_data is not None and len(filtered_data) == 0:
            st.warning("No data matches the selected filters. Please adjust your filters.")
        else:
            st.error("No data available. Please run main.py first to generate the data.")
        
        # Footer
        st.markdown("---")
        st.markdown("*Dashboard created with Streamlit • Data analyzed with Python*")

# Run the dashboard
if __name__ == "__main__":
    app = DashboardApp()
    app.run_dashboard()