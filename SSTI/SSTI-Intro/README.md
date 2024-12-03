# SSTI-Intro

### Difficulty: Beginner

## Setting Up

Ensures that `Docker` is installed into your machine as this challenge requires Docker. If you're unsure how to do it, you can refer [here](https://www.kali.org/docs/containers/installing-docker-on-kali/) to install it into your Kali machine. Then, install the files `app.py` , `Dockerfile` and `flag-6fbbff92650117ea3994ead7b72dbda7.txt` into the same directory.

### Commands (Kali)
[1] `sudo docker build -t sstichall .`

[2] `sudo docker run -d sstichall`

[3] `sudo docker logs <The container id>`

Use the first IP provided by the command [3] to access the challenge as highlighted below.

![image](https://github.com/user-attachments/assets/a2dc8099-2cb9-42d9-a8d2-c34d04b245e8)

Challenge should look like this and you are ready to go!

![image](https://github.com/user-attachments/assets/71d4d057-c35f-4c21-b28f-efaa2f35bff9)
