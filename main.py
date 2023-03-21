import os
import argparse
import time
from Util.output import get_output , write_output
from Util.visual import visual_output

passcodes = [
    "780464", "290299", "918660", "520967", "028431", "524383", "189493", "499707",
    "074355", "300590", "291709", "958640", "448106", "210362", "098598", "000241",
    "683596", "284933", "119785", "543019", "728724", "987319", "293486", "088198",
    "250453", "426329", "660141", "769721", "691859", "280351", "138620", "879021",
    "614955"
]

def open_game():
    url = 'https://www.coolmathgames.com/0-bloxorz'
    if os.name == 'nt': # Windows
        os.startfile(url)
    elif os.name == 'posix': # macOS or Linux
        opener = 'open' if os.uname().sysname == 'Darwin' else 'xdg-open'
        subprocess.Popen([opener, url])
        


class LevelAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if '-' in values:
            start, end = map(int, values.split('-'))
            if start > end :
                parser.error(f'The start level must be less than the end level.')
            if start < 1 or end > 33:
                parser.error(f'Level must be between 1 and 33')
            setattr(namespace, self.dest, list(range(start, end + 1)))
        else:
            level = int(values)
            if level < 1 or level > 33:
                parser.error(f'Level must be between 1 and 33')
            setattr(namespace, self.dest, [level])

def main():
    parser = argparse.ArgumentParser(description='AI BLOXORZ USAGE')
    parser.add_argument('-l', '--level', action=LevelAction, required=True, help='Specify a single level (e.g., --level 3) or a range of levels (e.g., --level 3-5). The level must be between 1 and 33.')
    parser.add_argument('-s', '--search', choices=['DFS', 'BFS', 'AStar', 'MCTS'], default='DFS', help='Type of searching algorithm. If this flag is not set, the default choice is DFS.')
    parser.add_argument('-v','--visualization' ,action='store_true' ,help ='Enable visualization of output')
    parser.add_argument('-r', '--realtime', action='store_true', help='Enable real-time computing. If this option is not selected, pre-computed results will be used.')
    parser.add_argument('-o','--store_output' ,action='store_true' ,help ='Store or update the outputs to files in specific folders')
    parser.add_argument('--output_folder' ,type=str ,default='./Output' ,help ='Specify the folder path to store the output file')
    
    args = parser.parse_args()
    
    
    if args.visualization:
        answer = input("Would you like to launch the game? Please enter 'y' for yes or 'n' for no: ")
        if answer.lower() == "y":
            open_game()
            
    first_level = True
    for i in args.level :
        actions = get_output( i, args.search, args.realtime )
        print('------------------------------------MY ACTIONS------------------------------------')
        print(actions)
        if args.visualization :
            if first_level:
                print("Initiating visualization. Please ensure that your screen is currently displaying the game's menu.")
                visual_output(actions ,False , passcodes[i-1])
                first_level = False
                time.sleep(6)
            else:
                print("Initiating visualization. Please ensure that your screen is currently displaying the game.")
                visual_output(actions , True)
                time.sleep(6)
            
            
        if args.store_output :
            if not os.path.exists(os.path.join(args.output_folder, args.search)):
                os.makedirs(os.path.join(args.output_folder, args.search))
            with open(os.path.join(args.output_folder, args.search, str(i) + '.txt'), 'w') as f:
                f.write(' '.join(actions))
            print('File write operation successful.')  
    print("Task completed successfully.")
    

if __name__ == "__main__":
    main()