#!/usr/bin/env python3
"""
GitHub Contribution Graph Generator - Spell 'SANDiP' for 2022
With 1 week spacing between letters and brightest dot on 'i'
"""

import os
import subprocess
from datetime import datetime, timedelta

# Define the letters in a 7-row grid (7 days of the week)
# 1 = contribution, 0 = no contribution
# Each letter is 5 columns wide

PATTERNS = {
    'S': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    'A': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]
    ],
    'N': [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1]
    ],
    'D': [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0]
    ],
    'i': [
        [0, 0, 2, 0, 0],  # 2 = brightest (the dot)
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0]
    ],
    'P': [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ]
}

def create_commit(date, repo_path, count=1):
    """Create commit(s) with a specific date."""
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')
    
    for i in range(count):
        # Create or modify a file
        with open(os.path.join(repo_path, 'contributions.txt'), 'a') as f:
            f.write(f'Contribution #{i+1} on {date_str}\n')
        
        # Stage the file
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        
        # Create commit with custom date
        env = os.environ.copy()
        # Add slight time variation for multiple commits on same day
        commit_time = date + timedelta(hours=i)
        env['GIT_AUTHOR_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
        env['GIT_COMMITTER_DATE'] = commit_time.strftime('%Y-%m-%d %H:%M:%S')
        
        subprocess.run(
            ['git', 'commit', '-m', f'Contribution on {date_str}'],
            cwd=repo_path,
            env=env,
            check=True,
            capture_output=True
        )

def generate_pattern(text, start_date, repo_path, commits_per_day=15, brightest_commits=30):
    """Generate commits to create a pattern on GitHub."""
    
    # Calculate starting Sunday (GitHub weeks start on Sunday)
    if start_date.weekday() == 6:  # Already Sunday
        start_sunday = start_date
    else:
        days_since_sunday = (start_date.weekday() + 1) % 7
        start_sunday = start_date - timedelta(days=days_since_sunday)
    
    print(f"Pattern will start on: {start_sunday.strftime('%Y-%m-%d (%A)')}")
    
    col_offset = 0
    total_commits = 0
    
    for char_index, char in enumerate(text):
        if char == ' ':
            col_offset += 2
            continue
            
        if char not in PATTERNS:
            print(f"Warning: Character '{char}' not defined, skipping...")
            col_offset += 6
            continue
        
        pattern = PATTERNS[char]
        letter_start = col_offset
        
        # For each column in the letter pattern
        for col in range(len(pattern[0])):
            # For each row (day of week)
            for row in range(7):
                cell_value = pattern[row][col]
                
                if cell_value > 0:
                    # Calculate the date for this contribution
                    commit_date = start_sunday + timedelta(weeks=col_offset, days=row)
                    
                    # Determine number of commits based on cell value
                    if cell_value == 2:  # Brightest (dot of 'i')
                        num_commits = brightest_commits
                    else:  # Normal contribution
                        num_commits = commits_per_day
                    
                    # Create commits
                    create_commit(commit_date, repo_path, num_commits)
                    total_commits += num_commits
            
            col_offset += 1
        
        # Add 1 week spacing between letters
        col_offset += 1
        
        letter_end = col_offset - 1
        print(f"  '{char}' placed at weeks {letter_start}-{letter_end}")
    
    end_date = start_sunday + timedelta(weeks=col_offset)
    print(f"\n✓ Generated pattern for: {text}")
    print(f"✓ Total weeks used: {col_offset}")
    print(f"✓ Total commits created: {total_commits}")
    print(f"✓ Pattern ends on: {end_date.strftime('%Y-%m-%d')}")

def main():
    """Main function to set up and generate the pattern."""
    
    # Configuration for 2022
    REPO_PATH = '.'
    TEXT = 'SANDiP'
    
    # With 1 week spacing: S(5+1) + A(5+1) + N(5+1) + D(5+1) + i(5+1) + P(5+1) = 42 weeks
    # Starting in January 2022 to fit the whole year
    START_DATE = datetime(2022, 4, 15)  # Adjust if needed
    COMMITS_PER_DAY = 10  # Normal contributions
    BRIGHTEST_COMMITS = 30  # Double commits for the dot of 'i'
    
    print("=" * 70)
    print("GitHub Contribution Art Generator - 2022 'SANDiP'")
    print("=" * 70)
    print(f"Text: {TEXT}")
    print(f"Start Date: {START_DATE.strftime('%Y-%m-%d')}")
    print(f"Repository: {REPO_PATH}")
    print(f"Normal commits per day: {COMMITS_PER_DAY}")
    print(f"Brightest (dot of 'i') commits: {BRIGHTEST_COMMITS}")
    print(f"Letter spacing: 1 week between each letter")
    print()
    
    # Create repository if it doesn't exist
    if not os.path.exists(REPO_PATH):
        print("Creating new repository...")
        os.makedirs(REPO_PATH)
        subprocess.run(['git', 'init'], cwd=REPO_PATH, check=True, capture_output=True)
        print("✓ Repository initialized")
    else:
        print(f"⚠️  Repository already exists at {REPO_PATH}")
        response = input("Do you want to continue? This will add more commits. (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
    
    # Check git config
    print("\nChecking git configuration...")
    result = subprocess.run(
        ['git', 'config', 'user.name'],
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("\n⚠️  Git user not configured!")
        name = input("Enter your git user name: ")
        email = input("Enter your git email: ")
        subprocess.run(['git', 'config', 'user.name', name], cwd=REPO_PATH, check=True)
        subprocess.run(['git', 'config', 'user.email', email], cwd=REPO_PATH, check=True)
        print("✓ Git config set")
    else:
        print(f"✓ Git user: {result.stdout.strip()}")
    
    # Generate the pattern
    print("\n" + "=" * 70)
    print("Generating commits for 2022...")
    print("This may take a few minutes...")
    print("=" * 70)
    print()
    
    generate_pattern(TEXT, START_DATE, REPO_PATH, COMMITS_PER_DAY, BRIGHTEST_COMMITS)
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Commits generated for 2022")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Create a new PUBLIC repository on GitHub")
    print("2. Copy and run these commands:")
    print()
    print(f"   cd {REPO_PATH}")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
    print("   git branch -M main")
    print("   git push -u origin main --force")
    print()
    print("⚠️  IMPORTANT REMINDERS:")
    print("   • Repository MUST be PUBLIC for contributions to show on your profile")
    print("   • The dot on 'i' will be the brightest square")
    print("   • There's 1 week spacing between each letter")
    print("   • Changes may take a few minutes to appear on GitHub")
    print()

if __name__ == '__main__':
    main()