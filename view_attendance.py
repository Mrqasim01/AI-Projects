"""
View attendance records
"""

import pandas as pd
import os
from config import ATTENDANCE_FILE
from datetime import datetime

def view_all_attendance():
    """Display all attendance records"""
    if not os.path.exists(ATTENDANCE_FILE):
        print("No attendance records found!")
        return
    
    df = pd.read_csv(ATTENDANCE_FILE)
    print("\n" + "="*60)
    print("ATTENDANCE RECORDS")
    print("="*60)
    print(df.to_string(index=False))
    print("="*60)

def view_today_attendance():
    """Display today's attendance"""
    if not os.path.exists(ATTENDANCE_FILE):
        print("No attendance records found!")
        return
    
    df = pd.read_csv(ATTENDANCE_FILE)
    today = datetime.now().strftime('%Y-%m-%d')
    today_df = df[df['Date'] == today]
    
    print("\n" + "="*60)
    print(f"ATTENDANCE FOR {today}")
    print("="*60)
    
    if today_df.empty:
        print("No attendance recorded for today")
    else:
        print(today_df.to_string(index=False))
    
    print("="*60)
    print(f"Total present: {len(today_df)}")

def view_person_attendance(name):
    """Display attendance for a specific person"""
    if not os.path.exists(ATTENDANCE_FILE):
        print("No attendance records found!")
        return
    
    df = pd.read_csv(ATTENDANCE_FILE)
    person_df = df[df['Name'].str.lower() == name.lower()]
    
    print("\n" + "="*60)
    print(f"ATTENDANCE FOR {name}")
    print("="*60)
    
    if person_df.empty:
        print(f"No attendance records found for {name}")
    else:
        print(person_df.to_string(index=False))
    
    print("="*60)
    print(f"Total records: {len(person_df)}")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*60)
        print("ATTENDANCE VIEWER")
        print("="*60)
        print("1. View all attendance records")
        print("2. View today's attendance")
        print("3. View person's attendance")
        print("4. Export to CSV")
        print("5. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            view_all_attendance()
        elif choice == '2':
            view_today_attendance()
        elif choice == '3':
            name = input("Enter person's name: ").strip()
            if name:
                view_person_attendance(name)
        elif choice == '4':
            if os.path.exists(ATTENDANCE_FILE):
                df = pd.read_csv(ATTENDANCE_FILE)
                export_file = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(export_file, index=False)
                print(f"✓ Exported to {export_file}")
            else:
                print("No attendance records found!")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
