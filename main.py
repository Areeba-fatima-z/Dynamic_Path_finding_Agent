from gui import PathfindingGUI
import argparse

def main():
    parser = argparse.ArgumentParser(description='Dynamic Pathfinding Agent')
    parser.add_argument('--rows', type=int, default=20, help='Number of rows')
    parser.add_argument('--cols', type=int, default=20, help='Number of columns')
    parser.add_argument('--cell-size', type=int, default=30, help='Cell size in pixels')
    
    args = parser.parse_args()
    
    print("Starting Dynamic Pathfinding Agent...")
    print(f"Grid Size: {args.rows}x{args.cols}")
    print("Controls:")
    print("  - Click cells to toggle obstacles")
    print("  - Use buttons to change algorithms")
    print("  - Press SPACE to run search")
    print("  - Press D to toggle dynamic mode")
    
    gui = PathfindingGUI(rows=args.rows, cols=args.cols, cell_size=args.cell_size)
    gui.run()

if __name__ == '__main__':
    main()