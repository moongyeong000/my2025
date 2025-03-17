#!/usr/bin/env python3

import argparse
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List
import json

class RepoAnalyzer:
    """Class to analyze GitHub repository participation"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.participants: Dict = {}
        self.score_weights = {
            'commits': 0.4,
            'issues_created': 0.3,
            'issue_comments': 0.3
        }

    def collect_commits(self) -> None:
        """Collect commit data from repository"""
        # Placeholder for Git commit collection
        # Will need gitpython or similar library
        pass

    def collect_issues(self) -> None:
        """Collect issues and comments data"""
        # Placeholder for GitHub API integration
        pass

    def calculate_scores(self) -> Dict:
        """Calculate participation scores for each contributor"""
        scores = {}
        for participant, activities in self.participants.items():
            total_score = (
                activities.get('commits', 0) * self.score_weights['commits'] +
                activities.get('issues_created', 0) * self.score_weights['issues_created'] +
                activities.get('issue_comments', 0) * self.score_weights['issue_comments']
            )
            scores[participant] = total_score
        return scores

    def generate_table(self, scores: Dict) -> pd.DataFrame:
        """Generate a table of participation scores"""
        df = pd.DataFrame.from_dict(scores, orient='index', columns=['Score'])
        return df

    def generate_chart(self, scores: Dict) -> None:
        """Generate a visualization of participation scores"""
        plt.figure(figsize=(10, 6))
        plt.bar(scores.keys(), scores.values())
        plt.xticks(rotation=45)
        plt.ylabel('Participation Score')
        plt.title('Repository Participation Scores')
        plt.tight_layout()
        plt.savefig('participation_chart.png')

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Analyze GitHub repository participation for class grading'
    )
    parser.add_argument(
        '--repo',
        type=str,
        required=True,
        help='Path to the git repository'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='Output directory for results'
    )
    parser.add_argument(
        '--format',
        choices=['table', 'chart', 'both'],
        default='both',
        help='Output format'
    )
    return parser.parse_args()

def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Initialize analyzer
    analyzer = RepoAnalyzer(args.repo)
    
    try:
        # Collect participation data
        print("Collecting commit data...")
        analyzer.collect_commits()
        
        print("Collecting issues data...")
        analyzer.collect_issues()
        
        # Calculate scores
        scores = analyzer.calculate_scores()
        
        # Generate outputs based on format
        if args.format in ['table', 'both']:
            table = analyzer.generate_table(scores)
            table.to_csv(f"{args.output}_scores.csv")
            print("\nParticipation Scores Table:")
            print(table)
            
        if args.format in ['chart', 'both']:
            analyzer.generate_chart(scores)
            print(f"Chart saved as participation_chart.png")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()