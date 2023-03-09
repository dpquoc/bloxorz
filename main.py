import argparse

passcodes = [
    780464,290299,918660,520967,028431,524383,189493,499707,074355,300590,291709,
    958640,448106,210362,098598,000241,683596,284933,119785,543019,728724,987319,
    293486,088198,250453,426329,660141,769721,691859,280351,138620,879021,614955
]

def main():
    parser = argparse.ArgumentParser(description='BLOXORZ')
    parser.add_argument('-f', '--flag', action='store_true', help='A flag')

    args = parser.parse_args()

    if args.flag:
        print('Flag is set')
    else:
        print('Flag is not set')

if __name__ == "__main__":
    main()