nohup python3 main.py > logs/nohup.log 2>&1 & echo $! > bot.pid --9946

Survives SSH disconnects
View logs: tail -f logs/nohup.log
Stop it: kill $(cat bot.pid)


# RUN in Tmux
command > tmux
command > source .venv/bin/activate
command > python3 main.py
command > ctrl + b >> d

# Check 
command > tmux ls

# Kill
command > tmux kill-server

git reset --hard origin/main
