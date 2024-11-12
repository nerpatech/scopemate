#!/usr/bin/env python3
# scopemate test suggested by Claude 3.5 Sonnet
import itertools
import subprocess

def run_scopemate_test():
    # Base command
    base_cmd = "./scopemate.py"
    
    # Test parameters
    instrument = "TCPIP::192.168.4.120::INSTR"  # Replace with your scope's address
    masks = ["mask-default-blank.png"]
    output = "test-output"
    
    # Define all possible flags
    flags = {
        "-i": [instrument],
        "-m": masks,
        "-o": [output],
        "-s": [""],
        "-c": [""]
    }
    
    # First test the list command independently
    list_cmd = [base_cmd, "-l"]
    print(f"Testing: {' '.join(list_cmd)}")
    subprocess.run(list_cmd)
    
    # Generate all possible flag combinations
    for r in range(1, len(flags) + 1):
        for flag_combo in itertools.combinations(flags.keys(), r):
            cmd = [base_cmd]
            
            for flag in flag_combo:
                cmd.append(flag)
                if flags[flag][0]:  # If the flag takes a value
                    cmd.extend(flags[flag])
            
            print(f"\nTesting: {' '.join(cmd)}")
            subprocess.run(cmd)

if __name__ == "__main__":
    print("Starting scopemate.py test suite...")
    run_scopemate_test()
