"""
Crawler script to fetch student data from local WEBSITE with pagination,
clean missing scores, export to CSV, and generate visualizations.
Uses Selenium to crawl from frontend UI.
"""

import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class StudentDataCrawler:
    def __init__(self, frontend_url: str = "http://localhost:5173"):
        self.frontend_url = frontend_url
        self.all_students: List[Dict] = []
        self.driver = None
        
    def _setup_driver(self):
        """Setup Chrome driver with visible browser."""
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        driver_path = os.path.join(os.path.dirname(__file__), '../../drivers/chromedriver.exe')
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    
    def fetch_all_students(self, page_size: int = 10) -> bool:
        """
        Returns:
            True if successful, False otherwise
        """
        print(f"Crawling from {self.frontend_url}...")
        
        try:
            self._setup_driver()
            self.driver.get(self.frontend_url)
            
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
            time.sleep(2)
            
            page = 1
            total_fetched = 0
            
            while True:
                try:
                    print(f"Page {page}...", end=" ")
                    time.sleep(1.5)
                    
                    students_on_page = self._extract_table_data()
                    
                    if not students_on_page:
                        break
                    
                    self.all_students.extend(students_on_page)
                    total_fetched += len(students_on_page)
                    print(f"✓ {len(students_on_page)} students (Total: {total_fetched})")
                    
                    if not self._go_to_next_page():
                        break
                    
                    page += 1
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break
            
            print(f"\nCompleted! Total: {total_fetched} students")
            return True
            
        except Exception as e:
            print(f"Error during crawl: {str(e)}")
            return False
        finally:
            if self.driver:
                time.sleep(3)
                self.driver.quit()
    
    def _extract_table_data(self) -> List[Dict]:
        """Extract student data from HTML table."""
        students = []
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                get_value = lambda cell: cell.text.strip() or None
                
                if len(cells) >= 9:
                    student = {k: get_value(cells[i]) for i, k in enumerate(['student_id', 'first_name', 'last_name', 'email', 'dob', 'hometown', 'math_score', 'english_score', 'literature_score'])}
                elif len(cells) >= 5:
                    name_parts = (get_value(cells[0]) or "").split(maxsplit=1)
                    student = {'student_id': None, 'first_name': name_parts[0] if name_parts else None, 'last_name': name_parts[1] if len(name_parts) > 1 else None, 'email': get_value(cells[1]), 'dob': None, 'hometown': get_value(cells[2]), 'math_score': get_value(cells[3]), 'english_score': get_value(cells[4]), 'literature_score': get_value(cells[5]) if len(cells) > 5 else None}
                else:
                    continue
                students.append(student)
        except:
            pass
        return students
    
    def _go_to_next_page(self) -> bool:
        """Click next page button."""
        try:
            next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
            if next_button.get_attribute('disabled'):
                return False
            next_button.click()
            time.sleep(1)
            return True
        except:
            return False
    
    def clean_data(self) -> pd.DataFrame:
        """Clean missing scores using hometown averages."""
        print("\nCleaning data...")
        df = pd.DataFrame(self.all_students)
        
        for col in ['math_score', 'english_score', 'literature_score']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            hometown_avg = df.groupby('hometown')[col].transform('mean')
            df[col] = df[col].fillna(hometown_avg).fillna(df[col].mean())
        
        print(f"Cleaned {len(df)} records")
        return df
    
    def export_to_csv(self, df: pd.DataFrame, output_dir: str = "../output") -> str:
        """Export cleaned data to CSV."""
        print("Exporting to CSV...")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = os.path.join(output_dir, "students_cleaned.csv")
        
        available_cols = [col for col in ['student_id', 'first_name', 'last_name', 'email', 'dob', 'hometown', 'math_score', 'english_score', 'literature_score'] if col in df.columns and not df[col].isna().all()]
        export_df = df[available_cols].copy()
        
        for col in ['math_score', 'english_score', 'literature_score']:
            if col in export_df.columns:
                export_df[col] = export_df[col].round(1)
        
        export_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Exported: {output_path}")
        return output_path
    
    def generate_visualizations(self, df: pd.DataFrame, output_dir: str = "../output"):
        """Generate 4 visualizations: histogram, boxplot, scatter plot, bar chart."""
        print("\nGenerating visualizations...")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        fig = plt.figure(figsize=(16, 12))
        
        # DIAGRAM 1: Histogram - Score Distribution
        ax1 = plt.subplot(2, 2, 1)
        ax1.hist(df['math_score'], bins=15, alpha=0.6, label='Math', edgecolor='black')
        ax1.hist(df['english_score'], bins=15, alpha=0.6, label='English', edgecolor='black')
        ax1.hist(df['literature_score'], bins=15, alpha=0.6, label='Literature', edgecolor='black')
        ax1.set_xlabel('Score', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.set_title('Score Distribution Histogram', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # DIAGRAM 2: Boxplot - Score by Hometown
        ax2 = plt.subplot(2, 2, 2)
        df_melted = df.melt(id_vars=['hometown'], 
                            value_vars=['math_score', 'english_score', 'literature_score'],
                            var_name='Subject', value_name='Score')
        sns.boxplot(data=df_melted, x='hometown', y='Score', hue='Subject', ax=ax2)
        ax2.set_xlabel('Hometown', fontsize=11)
        ax2.set_ylabel('Score', fontsize=11)
        ax2.set_title('Score Distribution by Hometown (Boxplot)', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # DIAGRAM 3: Scatter Plot - Math vs English Score
        ax3 = plt.subplot(2, 2, 3)
        scatter = ax3.scatter(df['math_score'], df['english_score'], 
                             c=df['literature_score'], cmap='viridis', 
                             s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
        
        min_score = min(df['math_score'].min(), df['english_score'].min())
        max_score = max(df['math_score'].max(), df['english_score'].max())
        ax3.plot([min_score, max_score], [min_score, max_score], 'r--', alpha=0.5, label='Perfect Correlation')
        
        ax3.set_xlabel('Math Score', fontsize=11)
        ax3.set_ylabel('English Score', fontsize=11)
        ax3.set_title('Scatter Plot: Math vs English Score\n(Color = Literature Score)', 
                     fontsize=12, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label('Literature Score', fontsize=10)
        
        # DIAGRAM 4: Bar Chart - Students with Score >= 7
        ax4 = plt.subplot(2, 2, 4)
        def count_above_threshold(series, threshold=7):
            return (series >= threshold).sum()
        
        math_above = count_above_threshold(df['math_score'])
        english_above = count_above_threshold(df['english_score'])
        literature_above = count_above_threshold(df['literature_score'])
        
        total_students = len(df)
        
        subjects = ['Math', 'English', 'Literature']
        counts = [math_above, english_above, literature_above]
        percentages = [(count / total_students) * 100 for count in counts]
        
        bars = ax4.bar(subjects, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
                       edgecolor='black', linewidth=1.5)
        
        for i, (bar, percentage) in enumerate(zip(bars, percentages)):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}\n({percentage:.1f}%)',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax4.set_ylabel('Number of Students', fontsize=11)
        ax4.set_title('Students with Score >= 7 (Pass Threshold)', fontsize=12, fontweight='bold')
        ax4.set_ylim(0, total_students * 1.15)
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_path = os.path.join(output_dir, "student_visualizations.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {output_path}")


def main():
    """Main execution flow."""
    
    print("Student Data Crawler & Visualizer")
    print("="*60)
    
    crawler = StudentDataCrawler(frontend_url="http://localhost:5173")
    
    # Step 1: Fetch data from WEBSITE
    success = crawler.fetch_all_students(page_size=10)
    if not success or len(crawler.all_students) == 0:
        print("Failed to fetch students. Exiting.")
        return
    
    # Step 2: Clean data
    df_cleaned = crawler.clean_data()
    
    # Step 3: Export to CSV
    csv_path = crawler.export_to_csv(df_cleaned, output_dir="../output")
    
    # Step 4: Generate visualizations
    crawler.generate_visualizations(df_cleaned, output_dir="../output")
    
    print("\nAll tasks completed successfully!")
    print(f"Check 'crawler/output' for results:")
    print(f"   - students_cleaned.csv")
    print(f"   - student_visualizations.png")


if __name__ == "__main__":
    main()
