import argparse

passcodes = [
    "780464", "290299", "918660", "520967", "028431", "524383", "189493", "499707",
    "074355", "300590", "291709", "958640", "448106", "210362", "098598", "000241",
    "683596", "284933", "119785", "543019", "728724", "987319", "293486", "088198",
    "250453", "426329", "660141", "769721", "691859", "280351", "138620", "879021",
    "614955"
]

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
    parser.add_argument('-l', '--level', action=LevelAction, help='Specify a single level (e.g., --level 3) or a range of levels (e.g., --level 3-5). The level must be between 1 and 33.')
    parser.add_argument('-s', '--search', choices=['DFS', 'BFS', 'A*', 'MCTS'], default='DFS', help='Type of searching algorithm. If this flag is not set, the default choice is DFS.')
    parser.add_argument('-v','--visualization' ,action='store_true' ,help ='Enable visualization of output')
    parser.add_argument('-r', '--realtime', action='store_true', help='Enable real-time computing. If this option is not selected, pre-computed results will be used.')
    parser.add_argument('-o','--store_output' ,action='store_true' ,help ='Store or update the outputs to files in specific folders')
    parser.add_argument('--output_folder' ,type=str ,default='./' ,help ='Specify the folder path to store the output file')
    
    args = parser.parse_args()

    if args.flag:
        print('Flag is set')
    else:
        print('Flag is not set')

if __name__ == "__main__":
    main()