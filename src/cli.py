import argparse
import sys
from analyzer import analyze
from storage import append_entry, get_last_entries


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Journal Analyzer - Track your mood and energy"
    )
    subparsers = parser.add_subparsers(dest="cmd", help="Commands")
    
    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new journal entry")
    add_parser.add_argument("text", type=str, help="Journal entry text")
    
    # Command: last
    last_parser = subparsers.add_parser("last", help="View last N entries")
    last_parser.add_argument("--n", type=int, default=3, help="Number of entries (default: 3)")
    
    # Command: stats
    stats_parser = subparsers.add_parser("stats", help="Show mood statistics")
    stats_parser.add_argument("--n", type=int, default=10, help="Analyze last N entries (default: 10)")
    
    args = parser.parse_args()
    
    if args.cmd == "add":
        handle_add(args.text)
    elif args.cmd == "last":
        handle_last(args.n)
    elif args.cmd == "stats":
        handle_stats(args.n)
    else:
        parser.print_help()


def handle_add(text: str):
    """Handle 'add' command."""
    if not text.strip():
        print("Error: Entry text cannot be empty")
        sys.exit(1)
    
    result = analyze(text)
    entry = append_entry(text, result)
    
    print(f"\n✓ Entry saved!")
    print(f"  Text: {entry['text']}")
    print(f"  Mood: {entry['mood']}")
    print(f"  Energy: {entry['energy']}")
    print(f"  Time: {entry['timestamp']}")


def handle_last(n: int):
    """Handle 'last' command."""
    entries = get_last_entries(n)
    
    if not entries:
        print("No entries found.")
        return
    
    print(f"\n📖 Last {min(n, len(entries))} entries:\n")
    for i, entry in enumerate(entries, 1):
        print(f"{i}. [{entry['timestamp']}]")
        print(f"   Text: {entry['text']}")
        print(f"   Mood: {entry['mood']} | Energy: {entry['energy']}\n")


def handle_stats(n: int):
    """Handle 'stats' command - show mood breakdown."""
    entries = get_last_entries(n)
    
    if not entries:
        print("No entries found.")
        return
    
    moods = {}
    energies = {}
    
    for entry in entries:
        mood = entry["mood"]
        energy = entry["energy"]
        
        moods[mood] = moods.get(mood, 0) + 1
        energies[energy] = energies.get(energy, 0) + 1
    
    print(f"\n📊 Mood Statistics (last {len(entries)} entries):\n")
    
    print("Moods:")
    for mood, count in sorted(moods.items()):
        pct = (count / len(entries)) * 100
        print(f"  {mood}: {count} ({pct:.1f}%)")
    
    print("\nEnergy Levels:")
    for energy, count in sorted(energies.items()):
        pct = (count / len(entries)) * 100
        print(f"  {energy}: {count} ({pct:.1f}%)")
    
    print()


if __name__ == "__main__":
    main()